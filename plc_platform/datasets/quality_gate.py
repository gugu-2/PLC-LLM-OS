"""
quality_gate.py
===============
Dataset Admission Quality Gate for the Industrial PLC LLM Platform.

Every generated DatasetRecordV2 (or raw record) MUST pass this gate
before entering the training pipeline. Records scoring below 85% are
REJECTED and logged. Records scoring ≥85% are ADMITTED.

The gate evaluates 6 dimensions:
  1. Structural Completeness (25%)  — FUNCTION_BLOCK / END_FUNCTION_BLOCK,
                                       VAR sections, parity checks
  2. Safety Coverage       (20%)  — E-Stop cutoff, 2oo3 TMR, ISA-18.2 alarms
  3. Variable Declaration  (20%)  — declared vs used variable match rate
  4. Physical Units        (10%)  — engineering unit comments [bar], [ms], etc.
  5. Sector Relevance      (15%)  — manufacturing keywords density
  6. Complexity Tier       (10%)  — state machine, MPC terms, matrix notation

A combined weighted score 0–100 is computed. Threshold is configurable
(default 85).

Usage:
    gate = DatasetQualityGate(threshold=85.0)
    result = gate.evaluate(code_text)
    if result.admitted:
        # save record
    else:
        logger.warning("REJECTED: %s", result.rejection_reasons)

CLI:
    python -m plc_platform.datasets.quality_gate --file mycode.st
    python -m plc_platform.datasets.quality_gate --dir data/swarm_raw --sample 50
"""

from __future__ import annotations

import argparse
import json
import logging
import pathlib
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants & regex patterns
# ---------------------------------------------------------------------------

DEFAULT_THRESHOLD = 85.0

# Structural
_FB_OPEN_RE     = re.compile(r"^\s*FUNCTION_BLOCK\s+\w+", re.MULTILINE | re.IGNORECASE)
_FB_CLOSE_RE    = re.compile(r"^\s*END_FUNCTION_BLOCK\s*$", re.MULTILINE | re.IGNORECASE)
_VAR_SECTION_RE = re.compile(r"\bVAR(?:_INPUT|_OUTPUT|_IN_OUT|_STAT|_GLOBAL|_EXTERNAL)?\b", re.IGNORECASE)
_END_VAR_RE     = re.compile(r"\bEND_VAR\b", re.IGNORECASE)
_IF_RE          = re.compile(r"\bIF\b", re.IGNORECASE)
_END_IF_RE      = re.compile(r"\bEND_IF\b", re.IGNORECASE)
_CASE_RE        = re.compile(r"\bCASE\b", re.IGNORECASE)
_END_CASE_RE    = re.compile(r"\bEND_CASE\b", re.IGNORECASE)
_FOR_RE         = re.compile(r"\bFOR\b", re.IGNORECASE)
_END_FOR_RE     = re.compile(r"\bEND_FOR\b", re.IGNORECASE)

# Safety
_ESTOP_RE       = re.compile(r"\bEStop\b|\bE_Stop\b|\bEmergency\b", re.IGNORECASE)
_ESTOP_RETURN_RE= re.compile(r"(?:bEStop|E_Stop|Emergency).{0,100}RETURN", re.DOTALL | re.IGNORECASE)
_TMR_RE         = re.compile(r"2oo3|bVoted|bTrip_[ABC]|Triple.*Modular|TMR", re.IGNORECASE)
_ALARM_HH_RE    = re.compile(r"bAlarm_HH|Alarm.*HH|HiHi|Hi_Hi", re.IGNORECASE)
_ALARM_LL_RE    = re.compile(r"bAlarm_LL|Alarm.*LL|LoLo|Lo_Lo", re.IGNORECASE)

# Variable declaration pattern: "   varname : TYPE"
_DECL_VAR_RE    = re.compile(r"^\s+(\w{2,})\s*:\s*(\w+)", re.MULTILINE)
# Variable usage: word appears in body (excluding declaration contexts)
_IEC_FORMAL_PARAMS = frozenset(["IN", "PT", "ET", "Q", "CV", "PV"])
_IEC_TYPES         = frozenset([
    "BOOL","INT","UINT","DINT","UDINT","LINT","ULINT","REAL","LREAL",
    "STRING","TIME","DATE","TOD","DT","BYTE","WORD","DWORD","LWORD",
    "SINT","USINT","TON","TOF","TP","CTU","CTD","CTUD","RS","SR",
    "R_TRIG","F_TRIG","ARRAY","STRUCT","ANY","WSTRING","CHAR",
])

# Physical units
_UNIT_RE        = re.compile(r"\[\s*(?:bar|mbar|Pa|kPa|MPa|°C|degC|°F|K|rpm|Hz|kHz|mm|cm|m|km|s|ms|us|μs|ns|%|A|mA|kA|V|mV|kV|W|kW|MW|N|kN|MN|Nm|kg|t|l|L|ml|mL|m3|°|deg|rad|ppm|pH)\s*\]", re.IGNORECASE)

# Sector relevance keywords per sector
_SECTOR_KEYWORDS = {
    "AUTOMOTIVE":     ["biw", "paint", "ev", "battery", "stator", "diecast", "robotic", "weld", "torque", "hemming", "busbar"],
    "ELECTRONICS":    ["smt", "pcb", "reflow", "pick_and_place", "soldering", "aoi", "semiconductor", "wafer", "wire_bond", "nozzle"],
    "HEAVY_MACHINERY":["press", "forge", "cnc", "mill", "grinding", "hydraulic", "servo", "spindle", "gantry", "stamp"],
    "PLASTICS":       ["inject", "mold", "extrusion", "blow", "parison", "polymer", "pellet", "screw", "barrel", "clamp"],
    "FOOD_BEVERAGE":  ["aseptic", "bottling", "cip", "sip", "retort", "delta", "filler", "bph", "pasteur", "sterilise"],
    "STEEL":          ["blast", "bof", "caster", "continuous_cast", "rolling", "ladle", "tundish", "slag"],
    "GENERAL_MANUFACTURING": ["conveyor", "assembly", "packaging", "material", "handling", "batch", "sequence"],
}

# Complexity indicators
_STATESPACE_RE  = re.compile(r"\bA\s*\*\s*x|\bx_\{k\+1\}|x\[k\+1\]|state.?space|State.*Matrix|A\s*:=\s*\[", re.IGNORECASE)
_MPC_RE         = re.compile(r"\bMPC\b|quadratic.*cost|rMPC_Cost|LQR|Riccati", re.IGNORECASE)
_FSM_RE         = re.compile(r"CASE\s+e?State", re.IGNORECASE)
_PACKML_RE      = re.compile(r"PackML|ISA.88|IDLE|EXECUTE|STOPPING|ABORTING|CLEARING", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Score components
# ---------------------------------------------------------------------------

@dataclass
class QualityDimension:
    name:    str
    score:   float          # 0.0 – 1.0
    weight:  float          # fraction of total score
    details: List[str] = field(default_factory=list)

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight * 100.0


@dataclass
class QualityGateResult:
    code_chars:        int
    total_score:       float          # 0 – 100
    admitted:          bool
    threshold:         float
    dimensions:        List[QualityDimension] = field(default_factory=list)
    rejection_reasons: List[str]              = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code_chars":    self.code_chars,
            "total_score":   round(self.total_score, 2),
            "admitted":      self.admitted,
            "threshold":     self.threshold,
            "dimensions":    [
                {
                    "name":           d.name,
                    "score":          round(d.score, 3),
                    "weight":         d.weight,
                    "weighted_score": round(d.weighted_score, 2),
                    "details":        d.details,
                }
                for d in self.dimensions
            ],
            "rejection_reasons": self.rejection_reasons,
        }


# ---------------------------------------------------------------------------
# Main Gate
# ---------------------------------------------------------------------------

class DatasetQualityGate:
    """
    Evaluates IEC 61131-3 Structured Text code snippets for dataset admission.

    Parameters
    ----------
    threshold    : minimum score (0–100) for admission (default 85.0)
    sector_hint  : optional manufacturing sector for relevance scoring
    """

    DIMENSION_WEIGHTS = {
        "structural":  0.25,
        "safety":      0.20,
        "variables":   0.20,
        "units":       0.10,
        "sector":      0.15,
        "complexity":  0.10,
    }

    def __init__(
        self,
        threshold:   float = DEFAULT_THRESHOLD,
        sector_hint: Optional[str] = None,
    ):
        self.threshold   = threshold
        self.sector_hint = sector_hint

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(self, code_text: str, sector_hint: Optional[str] = None) -> QualityGateResult:
        """
        Evaluate a code string and return a QualityGateResult.

        Parameters
        ----------
        code_text   : raw IEC-ST source code
        sector_hint : overrides instance-level sector_hint for this call
        """
        sector = sector_hint or self.sector_hint

        dims = [
            self._structural(code_text),
            self._safety(code_text),
            self._variables(code_text),
            self._units(code_text),
            self._sector_relevance(code_text, sector),
            self._complexity(code_text),
        ]

        total = sum(d.weighted_score for d in dims)
        admitted = total >= self.threshold
        rejections = [
            f"{d.name}: {d.score:.0%} ({', '.join(d.details[:2])})"
            for d in dims
            if d.score < 0.70
        ]

        return QualityGateResult(
            code_chars        = len(code_text),
            total_score       = round(total, 2),
            admitted          = admitted,
            threshold         = self.threshold,
            dimensions        = dims,
            rejection_reasons = rejections if not admitted else [],
        )

    def evaluate_messages_record(
        self, record: Dict[str, Any], sector_hint: Optional[str] = None
    ) -> QualityGateResult:
        """
        Evaluate a raw swarm_raw record in messages[] format.
        Extracts code from assistant turn markdown code blocks.
        """
        code = self._extract_code(record)
        if not code:
            return QualityGateResult(
                code_chars=0, total_score=0.0, admitted=False,
                threshold=self.threshold,
                rejection_reasons=["No IEC-ST code block found in record"],
            )
        return self.evaluate(code, sector_hint=sector_hint)

    # ------------------------------------------------------------------
    # Dimension evaluators
    # ------------------------------------------------------------------

    def _structural(self, code: str) -> QualityDimension:
        details = []
        score   = 0.0

        has_open  = bool(_FB_OPEN_RE.search(code))
        has_close = bool(_FB_CLOSE_RE.search(code))
        if has_open:  score += 0.20; details.append("FUNCTION_BLOCK ✓")
        else:         details.append("FUNCTION_BLOCK missing")
        if has_close: score += 0.20; details.append("END_FUNCTION_BLOCK ✓")
        else:         details.append("END_FUNCTION_BLOCK missing")

        # VAR sections match END_VAR count
        n_var     = len(_VAR_SECTION_RE.findall(code))
        n_end_var = len(_END_VAR_RE.findall(code))
        if n_var > 0 and n_var == n_end_var:
            score += 0.20; details.append(f"VAR parity ✓ ({n_var} sections)")
        elif n_var > 0:
            details.append(f"VAR/END_VAR mismatch: {n_var}/{n_end_var}")

        # IF/END_IF parity
        n_if    = len(_IF_RE.findall(code))
        n_endif = len(_END_IF_RE.findall(code))
        if n_if == n_endif:
            score += 0.15; details.append(f"IF parity ✓ ({n_if})")
        elif n_if > 0:
            details.append(f"IF/END_IF mismatch: {n_if}/{n_endif}")

        # CASE/END_CASE parity
        n_case    = len(_CASE_RE.findall(code))
        n_endcase = len(_END_CASE_RE.findall(code))
        if n_case > 0 and n_case == n_endcase:
            score += 0.15; details.append(f"CASE parity ✓ ({n_case})")
        elif n_case == 0:
            score += 0.10; details.append("No CASE blocks (acceptable)")

        # FOR/END_FOR parity
        n_for    = len(_FOR_RE.findall(code))
        n_endfor = len(_END_FOR_RE.findall(code))
        if n_for == 0 or n_for == n_endfor:
            score += 0.10

        return QualityDimension(
            name="structural", score=min(1.0, score),
            weight=self.DIMENSION_WEIGHTS["structural"], details=details
        )

    def _safety(self, code: str) -> QualityDimension:
        details = []
        score   = 0.0

        if _ESTOP_RE.search(code):
            score += 0.30; details.append("E-Stop variable ✓")
        else:
            details.append("No E-Stop variable found")

        if _ESTOP_RETURN_RE.search(code):
            score += 0.30; details.append("E-Stop → RETURN cutoff ✓")
        else:
            details.append("E-Stop does not trigger RETURN")

        if _TMR_RE.search(code):
            score += 0.25; details.append("2oo3 TMR voting ✓")
        else:
            details.append("2oo3 TMR voting missing")

        if _ALARM_HH_RE.search(code) and _ALARM_LL_RE.search(code):
            score += 0.15; details.append("ISA-18.2 HH/LL alarms ✓")
        elif _ALARM_HH_RE.search(code):
            score += 0.08; details.append("HH alarm ✓ (LL missing)")

        return QualityDimension(
            name="safety", score=min(1.0, score),
            weight=self.DIMENSION_WEIGHTS["safety"], details=details
        )

    def _variables(self, code: str) -> QualityDimension:
        details = []

        # Extract declared variables from VAR sections
        declared = set()
        for m in _DECL_VAR_RE.finditer(code):
            name, dtype = m.group(1), m.group(2)
            if dtype.upper() in _IEC_TYPES or dtype.upper() in _IEC_FORMAL_PARAMS:
                continue
            if len(name) >= 2 and name.upper() not in _IEC_TYPES:
                declared.add(name)

        if not declared:
            return QualityDimension(
                name="variables", score=0.5,
                weight=self.DIMENSION_WEIGHTS["variables"],
                details=["No variable declarations found — cannot evaluate"],
            )

        # Find used variable names in body (heuristic: word tokens that match declared)
        body = code
        used = {name for name in declared if body.count(name) >= 2}  # used at least twice

        ratio = len(used) / len(declared) if declared else 0.0
        details.append(f"Declared: {len(declared)}, Used: {len(used)}, Ratio: {ratio:.0%}")

        return QualityDimension(
            name="variables", score=min(1.0, ratio),
            weight=self.DIMENSION_WEIGHTS["variables"], details=details
        )

    def _units(self, code: str) -> QualityDimension:
        units_found = _UNIT_RE.findall(code)
        n = len(units_found)
        # 5+ units → full score (as per platform requirement)
        score = min(1.0, n / 5.0)
        return QualityDimension(
            name="units", score=score,
            weight=self.DIMENSION_WEIGHTS["units"],
            details=[f"Physical unit comments found: {n} (need ≥5 for full score)"],
        )

    def _sector_relevance(self, code: str, sector: Optional[str]) -> QualityDimension:
        lower = code.lower()
        best_sector = sector or "GENERAL_MANUFACTURING"
        best_score  = 0.0

        for sec, keywords in _SECTOR_KEYWORDS.items():
            hits = sum(1 for kw in keywords if kw.lower() in lower)
            kw_score = min(1.0, hits / max(1, len(keywords) // 3))
            if kw_score > best_score:
                best_score  = kw_score
                best_sector = sec

        return QualityDimension(
            name="sector", score=best_score,
            weight=self.DIMENSION_WEIGHTS["sector"],
            details=[f"Best sector match: {best_sector} ({best_score:.0%})"],
        )

    def _complexity(self, code: str) -> QualityDimension:
        details = []
        score   = 0.0

        if _FSM_RE.search(code):
            score += 0.35; details.append("FSM (CASE eState) ✓")
        if _MPC_RE.search(code):
            score += 0.30; details.append("MPC cost approximation ✓")
        if _STATESPACE_RE.search(code):
            score += 0.25; details.append("Discrete state-space ✓")
        if _PACKML_RE.search(code):
            score += 0.10; details.append("PackML/ISA-88 state names ✓")

        if not details:
            details.append("No complexity markers found")

        return QualityDimension(
            name="complexity", score=min(1.0, score),
            weight=self.DIMENSION_WEIGHTS["complexity"], details=details,
        )

    # ------------------------------------------------------------------
    # Code extraction
    # ------------------------------------------------------------------

    _CODE_RE = re.compile(
        r"```(?:iec-st|st|iec61131|structured.text|iecst)\s*(.*?)```",
        re.DOTALL | re.IGNORECASE,
    )

    def _extract_code(self, record: Dict[str, Any]) -> str:
        """Extract IEC-ST code from a raw messages[] record."""
        messages = record.get("messages", [])
        for msg in messages:
            if msg.get("role") in ("assistant", "gpt"):
                content = msg.get("content", "")
                m = self._CODE_RE.search(content)
                if m:
                    return m.group(1).strip()
        # Fallback: look for FUNCTION_BLOCK directly
        for msg in messages:
            content = msg.get("content", "")
            if "FUNCTION_BLOCK" in content and "END_FUNCTION_BLOCK" in content:
                return content
        return ""


# ---------------------------------------------------------------------------
# Batch evaluator
# ---------------------------------------------------------------------------

class BatchQualityEvaluator:
    """
    Evaluate a directory of raw *.json records and produce a summary report.
    """

    def __init__(self, threshold: float = DEFAULT_THRESHOLD):
        self.gate = DatasetQualityGate(threshold=threshold)

    def evaluate_directory(
        self,
        directory: str | pathlib.Path,
        sample_limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        directory = pathlib.Path(directory)
        files = sorted(directory.glob("*.json"))
        if sample_limit:
            files = files[:sample_limit]

        admitted  = 0
        rejected  = 0
        total_score = 0.0
        dim_totals: Dict[str, float] = {}

        for fpath in files:
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    record = json.load(fh)
                result = self.gate.evaluate_messages_record(record)
                if result.admitted:
                    admitted += 1
                else:
                    rejected += 1
                total_score += result.total_score
                for d in result.dimensions:
                    dim_totals[d.name] = dim_totals.get(d.name, 0.0) + d.score
            except Exception as exc:
                logger.warning("Error evaluating %s: %s", fpath.name, exc)
                rejected += 1

        n = admitted + rejected
        return {
            "total_evaluated": n,
            "admitted":        admitted,
            "rejected":        rejected,
            "admission_rate":  round(admitted / n * 100, 1) if n else 0.0,
            "mean_score":      round(total_score / n, 2) if n else 0.0,
            "mean_dim_scores": {
                k: round(v / n, 3) for k, v in dim_totals.items()
            } if n else {},
            "threshold":       self.gate.threshold,
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
    parser = argparse.ArgumentParser(description="Dataset Quality Gate for IEC-ST code")
    parser.add_argument("--file",      help="Evaluate a single .st or .json file")
    parser.add_argument("--dir",       help="Evaluate all *.json files in directory")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--sample",    type=int,   default=None)
    args = parser.parse_args()

    gate = DatasetQualityGate(threshold=args.threshold)

    if args.file:
        fpath = pathlib.Path(args.file)
        content = fpath.read_text(encoding="utf-8")
        if fpath.suffix == ".json":
            record = json.loads(content)
            result = gate.evaluate_messages_record(record)
        else:
            result = gate.evaluate(content)
        print(json.dumps(result.to_dict(), indent=2))

    elif args.dir:
        evaluator = BatchQualityEvaluator(threshold=args.threshold)
        summary = evaluator.evaluate_directory(args.dir, sample_limit=args.sample)
        print(json.dumps(summary, indent=2))

    else:
        parser.print_help()
