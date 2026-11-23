#!/usr/bin/env python3
"""
plc_platform/dialects/ladder_diagram.py — Relay Ladder Logic (RLL / LD) Engine
Reference: PLC_DOMAIN_INTELLIGENCE.md, PROJECT_ARCHITECTURE.md

Bi-directional compiler, AST representation, and ASCII art renderer for
Relay Ladder Logic (IEC 61131-3 LD and Rockwell RLL dialects).

Capabilities:
1. AST model: Instructions (XIC, XIO, OTE, OTL, OTU, TON, CTU), Branches (BST/NXB/BND), and Rungs.
2. Rockwell RLL Text Serializer and Parser:
   e.g. "XIC(b_EStop_OK)BST XIC(b_Start) NXB XIC(b_Running) BND XIO(b_Fault) OTE(b_MotorRun);"
3. High-Fidelity ASCII Art Generator for visual terminal rendering.
4. Bi-directional Transpiler:
   - Compiles RLL Rungs to IEC 61131-3 Structured Text.
   - Transpiles Structured Text Boolean logic expressions into RLL Rungs with parallel branching.
"""

from dataclasses import dataclass, field
from typing import List, Union, Optional, Dict, Any
import re


@dataclass
class LadderInstruction:
    op: str  # XIC, XIO, OTE, OTL, OTU, TON, CTU, CMP
    tag: str
    operands: List[str] = field(default_factory=list)

    def to_rockwell_text(self) -> str:
        if self.operands:
            args = ",".join([self.tag] + self.operands)
            return f"{self.op}({args})"
        return f"{self.op}({self.tag})"


@dataclass
class LadderBranch:
    branches: List[List[Union[LadderInstruction, "LadderBranch"]]] = field(default_factory=list)

    def to_rockwell_text(self) -> str:
        branch_texts = []
        for branch_elements in self.branches:
            b_str = "".join([elem.to_rockwell_text() for elem in branch_elements])
            branch_texts.append(b_str)
        return "BST " + " NXB ".join(branch_texts) + " BND "


@dataclass
class LadderRung:
    number: int
    comment: str
    elements: List[Union[LadderInstruction, LadderBranch]] = field(default_factory=list)

    def to_rockwell_text(self) -> str:
        core = "".join([e.to_rockwell_text() for e in self.elements])
        if not core.endswith(";"):
            core += ";"
        return core

    def to_ascii_art(self) -> str:
        """Renders the rung as classic ASCII schematic with power rails."""
        header = f"Rung {self.number:03d}: // {self.comment}\n"
        rail_left = "|---"
        rail_right = "---|"

        parts = []
        for elem in self.elements:
            if isinstance(elem, LadderInstruction):
                if elem.op == "XIC":
                    parts.append(f"-[ ]-{elem.tag}-")
                elif elem.op == "XIO":
                    parts.append(f"-[/]-{elem.tag}-")
                elif elem.op == "OTE":
                    parts.append(f"-( )-{elem.tag}-")
                elif elem.op == "OTL":
                    parts.append(f"-(L)-{elem.tag}-")
                elif elem.op == "OTU":
                    parts.append(f"-(U)-{elem.tag}-")
                elif elem.op == "TON":
                    pt = elem.operands[0] if elem.operands else "1000ms"
                    parts.append(f"-{{TON:{elem.tag} PT={pt}}}-")
                else:
                    parts.append(f"-{{{elem.op}:{elem.tag}}}-")
            elif isinstance(elem, LadderBranch):
                sub_branches = []
                for b in elem.branches:
                    sub_str = "".join([f"-[ ]-{inst.tag}-" if isinstance(inst, LadderInstruction) else "..." for inst in b])
                    sub_branches.append(sub_str)
                branch_rendered = " +-[ " + " ]-+--+-[ ".join(sub_branches) + " ]-+ "
                parts.append(branch_rendered)

        body = "".join(parts)
        return f"{header}{rail_left}{body}{rail_right}\n"


@dataclass
class LadderProgram:
    name: str
    rungs: List[LadderRung] = field(default_factory=list)

    def to_rockwell_text(self) -> str:
        return "\n".join([f"// {r.comment}\n{r.to_rockwell_text()}" for r in self.rungs])

    def to_ascii_view(self) -> str:
        return "\n".join([r.to_ascii_art() for r in self.rungs])


class LadderDiagramEngine:
    """Relay Ladder Logic Engine with bi-directional transpilation and ASCII rendering."""

    def parse_rockwell_rung(self, text: str, rung_num: int = 0, comment: str = "") -> LadderRung:
        """Parses Rockwell RLL string into structured LadderRung AST."""
        clean_text = text.strip()
        if clean_text.endswith(";"):
            clean_text = clean_text[:-1]

        tokens = self._tokenize_rll(clean_text)
        elements = self._parse_tokens(tokens)
        return LadderRung(number=rung_num, comment=comment, elements=elements)

    def _tokenize_rll(self, text: str) -> List[str]:
        """Tokenizes an RLL string into atomic instruction strings and branch markers."""
        # Tokens: BST, NXB, BND, or INSTR(TAG,...)
        token_pattern = re.compile(r"\b(BST|NXB|BND)\b|([A-Za-z0-9_]+)\(([^)]*)\)")
        tokens = []
        for m in token_pattern.finditer(text):
            if m.group(1):
                tokens.append(m.group(1))
            else:
                tokens.append(f"{m.group(2)}({m.group(3)})")
        return tokens

    def _parse_tokens(self, tokens: List[str]) -> List[Union[LadderInstruction, LadderBranch]]:
        """Parses token list into instructions and nested branch ASTs."""
        elements: List[Union[LadderInstruction, LadderBranch]] = []
        i = 0
        n = len(tokens)

        while i < n:
            token = tokens[i]
            if token == "BST":
                # Parse branch until matching BND
                branch_obj, next_i = self._parse_branch(tokens, i + 1)
                elements.append(branch_obj)
                i = next_i
            elif token in ("NXB", "BND"):
                # Should be consumed within _parse_branch
                i += 1
            else:
                # Instruction: OP(tag, operands...)
                inst_m = re.match(r"([A-Za-z0-9_]+)\(([^)]*)\)", token)
                if inst_m:
                    op = inst_m.group(1).upper()
                    raw_args = [a.strip() for a in inst_m.group(2).split(",") if a.strip()]
                    tag = raw_args[0] if raw_args else ""
                    operands = raw_args[1:] if len(raw_args) > 1 else []
                    elements.append(LadderInstruction(op=op, tag=tag, operands=operands))
                i += 1
        return elements

    def _parse_branch(self, tokens: List[str], start_idx: int) -> tuple[LadderBranch, int]:
        """Parses branch contents with nested levels until BND."""
        branch = LadderBranch()
        current_sub: List[Union[LadderInstruction, LadderBranch]] = []
        i = start_idx
        n = len(tokens)

        while i < n:
            token = tokens[i]
            if token == "BST":
                sub_branch, next_i = self._parse_branch(tokens, i + 1)
                current_sub.append(sub_branch)
                i = next_i
            elif token == "NXB":
                branch.branches.append(current_sub)
                current_sub = []
                i += 1
            elif token == "BND":
                branch.branches.append(current_sub)
                return branch, i + 1
            else:
                inst_m = re.match(r"([A-Za-z0-9_]+)\(([^)]*)\)", token)
                if inst_m:
                    op = inst_m.group(1).upper()
                    raw_args = [a.strip() for a in inst_m.group(2).split(",") if a.strip()]
                    tag = raw_args[0] if raw_args else ""
                    operands = raw_args[1:] if len(raw_args) > 1 else []
                    current_sub.append(LadderInstruction(op=op, tag=tag, operands=operands))
                i += 1
        branch.branches.append(current_sub)
        return branch, i

    def rung_to_structured_text(self, rung: LadderRung) -> str:
        """
        Compiles an RLL rung AST into equivalent IEC 61131-3 Structured Text.
        Evaluates input condition chain and assigns output coils.
        """
        conditions = []
        outputs = []

        def eval_element(elem):
            if isinstance(elem, LadderInstruction):
                if elem.op == "XIC":
                    conditions.append(elem.tag)
                elif elem.op == "XIO":
                    conditions.append(f"NOT {elem.tag}")
                elif elem.op in ("OTE", "OTL", "OTU"):
                    outputs.append(elem)
                elif elem.op == "TON":
                    outputs.append(elem)
            elif isinstance(elem, LadderBranch):
                sub_exprs = []
                for sub in elem.branches:
                    sub_conds = []
                    for sub_elem in sub:
                        if isinstance(sub_elem, LadderInstruction):
                            if sub_elem.op == "XIC":
                                sub_conds.append(sub_elem.tag)
                            elif sub_elem.op == "XIO":
                                sub_conds.append(f"NOT {sub_elem.tag}")
                    if sub_conds:
                        sub_exprs.append(" AND ".join(sub_conds))
                if sub_exprs:
                    conditions.append(f"({' OR '.join(sub_exprs)})")

        for elem in rung.elements:
            eval_element(elem)

        cond_str = " AND ".join(conditions) if conditions else "TRUE"
        st_lines = [f"// Rung {rung.number}: {rung.comment}"]

        for out in outputs:
            if out.op == "OTE":
                st_lines.append(f"{out.tag} := {cond_str};")
            elif out.op == "OTL":
                st_lines.append(f"IF {cond_str} THEN\n    {out.tag} := TRUE;\nEND_IF;")
            elif out.op == "OTU":
                st_lines.append(f"IF {cond_str} THEN\n    {out.tag} := FALSE;\nEND_IF;")
            elif out.op == "TON":
                pt = out.operands[0] if out.operands else "T#1s"
                st_lines.append(f"{out.tag}(IN := {cond_str}, PT := {pt});")

        return "\n".join(st_lines)

    def boolean_st_to_rung(self, target_coil: str, bool_expr: str, rung_num: int = 0, comment: str = "") -> LadderRung:
        """
        Transpiles simple Boolean expressions (AND / OR) into an RLL LadderRung.
        Example: "b_Permissive AND (b_Start OR b_Running) AND NOT b_Fault"
        """
        elements: List[Union[LadderInstruction, LadderBranch]] = []

        # Find any parenthesized OR expressions: (A OR B)
        or_match = re.search(r"\(([^)]+OR[^)]+)\)", bool_expr)
        branch_obj = None
        cleaned_expr = bool_expr

        if or_match:
            or_inner = or_match.group(1)
            or_parts = [p.strip() for p in or_inner.split("OR")]
            branch_list = []
            for part in or_parts:
                inst_list = []
                for sub in part.split("AND"):
                    sub = sub.strip()
                    if sub.startswith("NOT "):
                        inst_list.append(LadderInstruction(op="XIO", tag=sub[4:].strip()))
                    else:
                        inst_list.append(LadderInstruction(op="XIC", tag=sub))
                branch_list.append(inst_list)
            branch_obj = LadderBranch(branches=branch_list)
            cleaned_expr = bool_expr.replace(or_match.group(0), "___BRANCH_PLACEHOLDER___")

        # Now parse remaining top-level AND tokens
        tokens = [t.strip() for t in cleaned_expr.split("AND") if t.strip()]
        for t in tokens:
            if t == "___BRANCH_PLACEHOLDER___":
                if branch_obj:
                    elements.append(branch_obj)
            elif t.startswith("NOT "):
                elements.append(LadderInstruction(op="XIO", tag=t[4:].strip()))
            else:
                elements.append(LadderInstruction(op="XIC", tag=t))

        # Add output coil
        elements.append(LadderInstruction(op="OTE", tag=target_coil))

        return LadderRung(number=rung_num, comment=comment or f"Energize {target_coil}", elements=elements)
