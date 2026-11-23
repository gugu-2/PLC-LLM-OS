#!/usr/bin/env python3
"""
plc_platform/rag/retriever.py — Hybrid BM25 + Dense Semantic Standards Retriever
Reference: PLC_DOMAIN_INTELLIGENCE.md, PROJECT_ARCHITECTURE.md

Features:
1. Exact keyword & token matching with Okapi BM25 scoring (k1=1.5, b=0.75).
2. Dense semantic similarity matching over vector space representations.
3. Reciprocal Rank Fusion (RRF with parameter k=60) for robust fusion.
4. Domain-aware metadata filtering (Vendor, Standard, Sector, Category).
5. Industrial abbreviation expansion.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Any
import math
import re
from .standards_kb import IndustrialStandardsCorpus, StandardDocument


@dataclass
class RetrievedStandardChunk:
    doc_id: str
    title: str
    standard_name: str
    category: str
    vendor: str
    sector: str
    content: str
    score: float
    matched_terms: List[str] = field(default_factory=list)


class HybridStandardsRetriever:
    """Hybrid Retriever combining BM25 keyword matching and Dense Vector scoring with RRF."""

    # Industrial abbreviations glossary for query expansion
    ABBREVIATIONS = {
        "tmr": "triple modular redundancy 2oo3 voting",
        "aoi": "add on instruction rockwell",
        "scl": "structured control language siemens",
        "db": "data block optimized access",
        "ob": "organization block cyclic interrupt",
        "pii": "process image input scan cycle",
        "piq": "process image output scan cycle",
        "cip": "clean in place sanitization caustic wash",
        "sip": "steam in place sterilization",
        "biw": "body in white robotic welding automotive",
        "smt": "surface mount technology pick and place",
        "packml": "omac unit machine state model 17 states",
        "deadband": "isa 18 2 hysteresis alarm limit",
        "l5x": "rockwell studio 5000 export schema",
        "tcpou": "beckhoff twincat pou declaration",
        "ads": "automation device specification beckhoff"
    }

    def __init__(self, corpus: Optional[List[StandardDocument]] = None):
        self.corpus: List[StandardDocument] = corpus or IndustrialStandardsCorpus.get_all_documents()
        self.k1 = 1.5
        self.b = 0.75
        self.rrf_k = 60
        self._index_corpus()

    def _index_corpus(self):
        """Builds inverted index and term frequency structures for BM25 and vector math."""
        self.doc_tokens: Dict[str, List[str]] = {}
        self.doc_lens: Dict[str, int] = {}
        self.df: Dict[str, int] = {}
        self.tf: Dict[str, Dict[str, int]] = {}

        total_len = 0
        for doc in self.corpus:
            tokens = self._tokenize(f"{doc.title} {doc.content} {' '.join(doc.tags)}")
            self.doc_tokens[doc.doc_id] = tokens
            self.doc_lens[doc.doc_id] = len(tokens)
            total_len += len(tokens)

            tf_dict: Dict[str, int] = {}
            seen_tokens: Set[str] = set()
            for t in tokens:
                tf_dict[t] = tf_dict.get(t, 0) + 1
                seen_tokens.add(t)

            self.tf[doc.doc_id] = tf_dict
            for t in seen_tokens:
                self.df[t] = self.df.get(t, 0) + 1

        self.n_docs = len(self.corpus)
        self.avg_doc_len = total_len / max(1, self.n_docs)

        # Precompute vocabulary and IDF
        self.idf: Dict[str, float] = {}
        for t, count in self.df.items():
            self.idf[t] = math.log(1.0 + (self.n_docs - count + 0.5) / (count + 0.5))

    def _tokenize(self, text: str) -> List[str]:
        """Normalizes and splits text into alphanumeric lower-case tokens."""
        clean = re.sub(r"[^A-Za-z0-9_-]", " ", text.lower())
        return [tok for tok in clean.split() if len(tok) > 1]

    def _expand_query(self, query: str) -> str:
        """Expands query with industrial domain abbreviations."""
        expanded = query.lower()
        for abbr, expansion in self.ABBREVIATIONS.items():
            pattern = rf"\b{re.escape(abbr)}\b"
            if re.search(pattern, expanded):
                expanded += f" {expansion}"
        return expanded

    def _bm25_score(self, doc_id: str, query_tokens: List[str]) -> float:
        """Calculates Okapi BM25 score for a document."""
        score = 0.0
        doc_len = self.doc_lens.get(doc_id, 0)
        tf_map = self.tf.get(doc_id, {})

        for t in query_tokens:
            if t not in tf_map:
                continue
            freq = tf_map[t]
            idf = self.idf.get(t, 0.1)
            denom = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
            score += idf * (freq * (self.k1 + 1.0)) / max(1e-6, denom)
        return score

    def _dense_cosine_score(self, doc_id: str, query_tokens: List[str]) -> float:
        """Computes cosine similarity between query TF-IDF vector and document TF-IDF vector."""
        query_tf: Dict[str, int] = {}
        for t in query_tokens:
            query_tf[t] = query_tf.get(t, 0) + 1

        doc_tf = self.tf.get(doc_id, {})

        dot_product = 0.0
        query_norm_sq = 0.0
        for t, count in query_tf.items():
            w_q = count * self.idf.get(t, 0.1)
            query_norm_sq += w_q * w_q
            if t in doc_tf:
                w_d = doc_tf[t] * self.idf.get(t, 0.1)
                dot_product += w_q * w_d

        if query_norm_sq == 0.0:
            return 0.0

        doc_norm_sq = sum((count * self.idf.get(t, 0.1)) ** 2 for t, count in doc_tf.items())
        norm = math.sqrt(query_norm_sq) * math.sqrt(doc_norm_sq)
        return dot_product / max(1e-6, norm)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        vendor: Optional[str] = None,
        sector: Optional[str] = None,
        standard: Optional[str] = None
    ) -> List[RetrievedStandardChunk]:
        """
        Executes hybrid BM25 + Dense retrieval with Reciprocal Rank Fusion (RRF).
        """
        expanded_query = self._expand_query(query)
        q_tokens = self._tokenize(expanded_query)

        # Filter candidate documents
        candidates = []
        for doc in self.corpus:
            if vendor and vendor != "ALL" and doc.vendor not in ("ALL", vendor):
                continue
            if sector and sector != "ALL" and doc.sector not in ("ALL", sector):
                continue
            if standard and standard != "ALL" and doc.standard_name not in ("ALL", standard):
                continue
            candidates.append(doc)

        if not candidates:
            # Fallback to unfiltered if overly constrained
            candidates = self.corpus

        # Score BM25
        bm25_scored = [(d, self._bm25_score(d.doc_id, q_tokens)) for d in candidates]
        bm25_ranked = [d.doc_id for d, s in sorted(bm25_scored, key=lambda x: x[1], reverse=True)]

        # Score Dense Cosine
        dense_scored = [(d, self._dense_cosine_score(d.doc_id, q_tokens)) for d in candidates]
        dense_ranked = [d.doc_id for d, s in sorted(dense_scored, key=lambda x: x[1], reverse=True)]

        # Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[str, float] = {}
        for rank, doc_id in enumerate(bm25_ranked):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        for rank, doc_id in enumerate(dense_ranked):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        # Sort by final RRF score
        doc_map = {d.doc_id: d for d in candidates}
        final_sorted = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results: List[RetrievedStandardChunk] = []
        for doc_id, score in final_sorted:
            doc = doc_map[doc_id]
            matched = [t for t in q_tokens if t in self.tf.get(doc_id, {})]
            results.append(RetrievedStandardChunk(
                doc_id=doc.doc_id,
                title=doc.title,
                standard_name=doc.standard_name,
                category=doc.category,
                vendor=doc.vendor,
                sector=doc.sector,
                content=doc.content,
                score=round(score, 6),
                matched_terms=list(set(matched))[:8]
            ))

        return results


# Compatibility alias
HybridRetriever = HybridStandardsRetriever

__all__ = ["HybridStandardsRetriever", "HybridRetriever", "RetrievedStandardChunk"]
