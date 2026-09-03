"""
few_shot_picker.py
==================
Selects the best 3 few-shot examples from train.jsonl for a given domain.
Uses keyword overlap scoring to find the most relevant examples.
Falls back to random high-quality examples if no domain match is found.
"""
import json
import random
import re
from pathlib import Path


class FewShotPicker:
    """Loads the master training dataset and serves relevant few-shot examples."""

    def __init__(self, train_jsonl_path: str | Path, n_shots: int = 3):
        self.n_shots = n_shots
        self._records: list[dict] = []
        self._load(Path(train_jsonl_path))

    def _load(self, path: Path):
        if not path.exists():
            print(f"  [WARN] few_shot_picker: {path} not found — no few-shot examples")
            return
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    msgs = obj.get("messages", [])
                    if len(msgs) >= 2:
                        asst = msgs[-1].get("content", "")
                        # Only keep high-quality long examples
                        if len(asst) >= 2000:
                            self._records.append(obj)
                except json.JSONDecodeError:
                    continue
        print(f"  [INFO] FewShotPicker loaded {len(self._records)} examples from {path.name}")

    def _score(self, record: dict, domain_keywords: list[str]) -> int:
        """Score a record by how many domain keywords appear in it."""
        text = " ".join(
            m.get("content", "") for m in record.get("messages", [])
        ).lower()
        return sum(1 for kw in domain_keywords if kw.lower() in text)

    def get(self, domain: str) -> list[dict]:
        """
        Return n_shots example records most relevant to the given domain.

        Args:
            domain: The industrial domain string e.g. "Cement Rotary Kiln"

        Returns:
            List of message dicts (each a full {"messages": [...]} record)
        """
        if not self._records:
            return []

        # Tokenise domain into keywords
        keywords = re.findall(r"\b[a-zA-Z]{3,}\b", domain)

        # Score all records
        scored = [(self._score(r, keywords), r) for r in self._records]
        scored.sort(key=lambda x: x[0], reverse=True)

        # Take top matches; if score is 0 for all, use random selection
        top = scored[:self.n_shots]
        if all(s == 0 for s, _ in top):
            return [r for _, r in random.sample(scored, min(self.n_shots, len(scored)))]

        return [r for _, r in top]

    def format_few_shot_block(self, domain: str) -> str:
        """
        Returns a formatted string of few-shot examples to inject into a prompt.
        """
        examples = self.get(domain)
        if not examples:
            return ""

        parts = ["### FEW-SHOT EXAMPLES (study these and follow the exact same format)\n"]
        for i, record in enumerate(examples, 1):
            msgs = record.get("messages", [])
            # Find user and assistant messages
            user_msg = next((m["content"] for m in msgs if m.get("role") == "user"), "")
            asst_msg = next((m["content"] for m in msgs if m.get("role") == "assistant"), "")
            parts.append(f"--- EXAMPLE {i} ---")
            parts.append(f"USER: {user_msg[:300]}...")
            parts.append(f"ASSISTANT:\n{asst_msg}")
            parts.append("")

        parts.append("--- END OF EXAMPLES ---\n")
        return "\n".join(parts)
