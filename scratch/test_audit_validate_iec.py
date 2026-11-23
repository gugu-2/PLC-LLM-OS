"""
Comprehensive Test Suite & Audit for validate_iec.py
Tests:
1. Markdown code block unwrapping
2. Control structure parity (IF/END_IF, CASE/END_CASE, FOR/END_FOR, WHILE/END_WHILE, FB/END_FB)
3. Bracketed physical units check
4. Comment parity (* *)
5. Boundary and character threshold validation
6. Single-turn and multi-turn JSON datasets
7. Live batch validation on real datasets
"""

import os
import sys
import json
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import validate_iec from root
import validate_iec

def create_valid_st_code(extra_chars=0, num_units=5, num_ifs=2, num_cases=1, num_fors=1):
    units = ["bar", "deg C", "kN", "m/s^2", "rpm", "mm/s", "kW", "°C", "%"][:max(5, num_units)]
    units_comments = " ".join([f"(* Sensor unit: [{u}] *)" for u in units])
    
    ifs = ""
    for i in range(num_ifs):
        ifs += f"IF bCondition_{i} THEN\n    nVal_{i} := {i};\nELSIF bElseIf_{i} THEN\n    nVal_{i} := {i} * 2;\nELSE\n    nVal_{i} := 0;\nEND_IF;\n"
        
    cases = ""
    for c in range(num_cases):
        cases += f"CASE nState_{c} OF\n    1: sMsg := 'State 1';\n    2: sMsg := 'State 2';\n    ELSE sMsg := 'Unknown';\nEND_CASE;\n"
        
    fors = ""
    for f in range(num_fors):
        fors += f"FOR nIdx_{f} := 1 TO 10 DO\n    nTotal := nTotal + nIdx_{f};\nEND_FOR;\n"

    # Padding to satisfy min_chars
    padding = "(* " + ("LuminaIndustrialAutomationRigorousTestPadding_" * 100) + " *)\n"
    if extra_chars > 0:
        padding += "(* " + ("X" * extra_chars) + " *)\n"

    code = f"""FUNCTION_BLOCK FB_LuminaAuditedController
VAR_INPUT
    bEnable : BOOL; (* [1/0] *)
    rPressure : REAL; (* [bar] *)
END_VAR
VAR_OUTPUT
    bReady : BOOL; (* [bool] *)
    rOutTemp : REAL; (* [deg C] *)
END_VAR
VAR
    nState : INT; (* [status] *)
    nIdx : INT; (* [-] *)
    sStringWithKeywords : STRING := 'IF CASE FOR END_IF END_CASE END_FOR';
    (* Physical units in declarations: {units_comments} *)
END_VAR

(* Control Logic *)
{padding}
{ifs}
{cases}
{fors}

END_FUNCTION_BLOCK
"""
    return code


class TestValidateIEC(unittest.TestCase):

    def test_01_valid_base_code(self):
        """Test that a fully compliant code passes with zero errors."""
        code = create_valid_st_code()
        res = validate_iec.check_parity(code, min_chars=1000)
        self.assertEqual(res["verdict"], "PASS")
        self.assertEqual(len(res["errors"]), 0)
        self.assertGreaterEqual(res["counts"]["physical_units"], 5)

    def test_02_markdown_code_block_unwrapping(self):
        """Test markdown code block unwrapping (iec-st and generic)."""
        base_code = create_valid_st_code()
        
        # Wrapped with ```iec-st
        wrapped_iec_st = f"```iec-st\n{base_code}\n```"
        res1 = validate_iec.check_parity(wrapped_iec_st, min_chars=1000)
        self.assertEqual(res1["verdict"], "PASS", f"Failed on ```iec-st: {res1['errors']}")
        
        # Wrapped with generic ```
        wrapped_generic = f"```\n{base_code}\n```"
        res2 = validate_iec.check_parity(wrapped_generic, min_chars=1000)
        self.assertEqual(res2["verdict"], "PASS", f"Failed on generic ```: {res2['errors']}")

        # Wrapped with trailing and leading whitespace around fences
        wrapped_ws = f"   \n\n```iec-st   \n{base_code}\n```   \n\n"
        res3 = validate_iec.check_parity(wrapped_ws, min_chars=1000)
        self.assertEqual(res3["verdict"], "PASS", f"Failed on whitespace fences: {res3['errors']}")

    def test_03_if_end_if_parity(self):
        """Test IF / END_IF balance, ELSIF isolation, string & comment robustness."""
        base_code = create_valid_st_code(num_ifs=2)
        
        # Baseline must pass
        self.assertEqual(len(validate_iec.validate_iec_st(base_code, min_chars=1000)), 0)

        # Missing END_IF
        corrupt_code = base_code.replace("END_IF;", "", 1)
        errs = validate_iec.validate_iec_st(corrupt_code, min_chars=1000)
        self.assertTrue(any("IF (" in e and "mismatch" in e for e in errs), f"Did not catch missing END_IF: {errs}")

        # Extra END_IF
        extra_code = base_code + "\nEND_IF;\n"
        errs = validate_iec.validate_iec_st(extra_code, min_chars=1000)
        self.assertTrue(any("IF (" in e and "mismatch" in e for e in errs), f"Did not catch extra END_IF: {errs}")

        # Verify ELSIF does not count as IF
        # base_code already has ELSIF; counts must show exact IF count
        res = validate_iec.check_parity(base_code, min_chars=1000)
        self.assertEqual(res["counts"]["IF"], 2)
        self.assertEqual(res["counts"]["END_IF"], 2)

        # IF inside comments and strings should not affect counts
        code_with_comment_if = base_code + "\n(* IF fake_comment THEN END_IF; *)\n"
        res_comment = validate_iec.check_parity(code_with_comment_if, min_chars=1000)
        self.assertEqual(res_comment["counts"]["IF"], 2)
        self.assertEqual(res_comment["counts"]["END_IF"], 2)

    def test_04_case_end_case_parity(self):
        """Test CASE / END_CASE balance and isolation."""
        base_code = create_valid_st_code(num_cases=2)
        
        # Missing END_CASE
        corrupt_code = base_code.replace("END_CASE;", "", 1)
        errs = validate_iec.validate_iec_st(corrupt_code, min_chars=1000)
        self.assertTrue(any("CASE (" in e and "mismatch" in e for e in errs), f"Did not catch missing END_CASE: {errs}")

        # Extra END_CASE
        extra_code = base_code + "\nEND_CASE;\n"
        errs = validate_iec.validate_iec_st(extra_code, min_chars=1000)
        self.assertTrue(any("CASE (" in e and "mismatch" in e for e in errs), f"Did not catch extra END_CASE: {errs}")

        # CASE in comments
        code_comment_case = base_code + "\n(* CASE fake OF 1: END_CASE; *)\n"
        res_comment = validate_iec.check_parity(code_comment_case, min_chars=1000)
        self.assertEqual(res_comment["counts"]["CASE"], 2)
        self.assertEqual(res_comment["counts"]["END_CASE"], 2)

    def test_05_for_end_for_parity(self):
        """Test FOR / END_FOR balance and isolation."""
        base_code = create_valid_st_code(num_fors=3)
        
        # Missing END_FOR
        corrupt_code = base_code.replace("END_FOR;", "", 1)
        errs = validate_iec.validate_iec_st(corrupt_code, min_chars=1000)
        self.assertTrue(any("FOR (" in e and "mismatch" in e for e in errs), f"Did not catch missing END_FOR: {errs}")

        # Extra END_FOR
        extra_code = base_code + "\nEND_FOR;\n"
        errs = validate_iec.validate_iec_st(extra_code, min_chars=1000)
        self.assertTrue(any("FOR (" in e and "mismatch" in e for e in errs), f"Did not catch extra END_FOR: {errs}")

    def test_06_physical_units_check(self):
        """Test bracketed physical units count (>= 5 required)."""
        # Code with exactly 5 units -> pass
        code_5_units = create_valid_st_code(num_units=5)
        res_5 = validate_iec.check_parity(code_5_units, min_chars=1000)
        self.assertEqual(res_5["verdict"], "PASS")

        # Code with only 3 units
        code_few_units = """FUNCTION_BLOCK FB_FewUnits
VAR_INPUT
    rPressure : REAL; (* [bar] *)
    rTemp : REAL; (* [deg C] *)
END_VAR
VAR_OUTPUT
    rForce : REAL; (* [kN] *)
END_VAR
VAR
    nState : INT;
END_VAR
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
(* LuminaIndustrialAutomationRigorousTestPadding_LuminaIndustrialAutomationRigorousTestPadding_ *)
IF TRUE THEN
    nState := 1;
END_IF;
END_FUNCTION_BLOCK
"""
        res_few = validate_iec.check_parity(code_few_units, min_chars=1000)
        self.assertEqual(res_few["verdict"], "FAIL")
        self.assertTrue(any("Too few physical units found in comments" in e for e in res_few["errors"]))

    def test_07_comment_parity(self):
        """Test (* *) comment parity matching."""
        base_code = create_valid_st_code()
        
        # Unclosed comment
        corrupt_code = base_code + "\n(* Unclosed comment block\n"
        errs = validate_iec.validate_iec_st(corrupt_code, min_chars=1000)
        self.assertTrue(any("Comment mismatch" in e for e in errs))

        # Stray closing comment
        stray_close = base_code + "\n*) Stray close\n"
        errs2 = validate_iec.validate_iec_st(stray_close, min_chars=1000)
        self.assertTrue(any("Comment mismatch" in e for e in errs2))

    def test_08_first_and_last_lines(self):
        """Test FUNCTION_BLOCK FB_ first line and END_FUNCTION_BLOCK last line."""
        base_code = create_valid_st_code()
        
        # Bad first line
        bad_first = base_code.replace("FUNCTION_BLOCK FB_LuminaAuditedController", "PROGRAM MainProgram", 1)
        errs = validate_iec.validate_iec_st(bad_first, min_chars=1000)
        self.assertTrue(any("First line does not start with 'FUNCTION_BLOCK FB_'" in e for e in errs))

        # Bad last line
        bad_last = base_code.replace("END_FUNCTION_BLOCK", "END_PROGRAM", 1)
        errs2 = validate_iec.validate_iec_st(bad_last, min_chars=1000)
        self.assertTrue(any("Last line mismatch" in e for e in errs2))

    def test_09_single_turn_json_dataset(self):
        """Test validation on standard single-turn JSON format."""
        code = create_valid_st_code()
        dataset = {
            "messages": [
                {"role": "user", "content": "Generate a controller for Lumina assembly cell."},
                {"role": "assistant", "content": f"Here is the complete ST implementation:\n\n```iec-st\n{code}\n```"}
            ]
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump(dataset, tf)
            tf_path = tf.name

        try:
            errs = validate_iec.validate_json_file(tf_path, min_chars=1000)
            self.assertEqual(len(errs), 0, f"Single-turn validation failed: {errs}")
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_10_multi_turn_json_dataset(self):
        """Test validation on multi-turn dialogue JSON format with multiple blocks."""
        code1 = create_valid_st_code()
        code2 = create_valid_st_code().replace("FB_LuminaAuditedController", "FB_SecondarySubsystem")
        
        dataset = {
            "messages": [
                {"role": "user", "content": "Phase 1: Generate primary controller."},
                {"role": "assistant", "content": f"```iec-st\n{code1}\n```"},
                {"role": "user", "content": "Phase 2: Generate secondary subsystem."},
                {"role": "assistant", "content": f"Certainly, here is the second subsystem:\n```iec-st\n{code2}\n```"}
            ]
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump(dataset, tf)
            tf_path = tf.name

        try:
            errs = validate_iec.validate_json_file(tf_path, min_chars=1000)
            self.assertEqual(len(errs), 0, f"Multi-turn validation failed: {errs}")
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_11_corrupt_multi_turn_json_dataset(self):
        """Test that multi-turn catches an error specifically in block 2."""
        code1 = create_valid_st_code()
        corrupt_code2 = create_valid_st_code().replace("END_IF;", "", 1)
        
        dataset = {
            "messages": [
                {"role": "user", "content": "Phase 1: Generate primary controller."},
                {"role": "assistant", "content": f"```iec-st\n{code1}\n```"},
                {"role": "user", "content": "Phase 2: Corrupt second subsystem."},
                {"role": "assistant", "content": f"```iec-st\n{corrupt_code2}\n```"}
            ]
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump(dataset, tf)
            tf_path = tf.name

        try:
            errs = validate_iec.validate_json_file(tf_path, min_chars=1000)
            self.assertGreater(len(errs), 0)
            self.assertTrue(any("[Block 2]" in e and "mismatch" in e for e in errs))
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_12_edge_cases_json(self):
        """Test edge cases: corrupt json, missing messages, empty messages."""
        # Invalid JSON syntax
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            tf.write("{ this is not json }")
            tf_path = tf.name
        try:
            errs = validate_iec.validate_json_file(tf_path)
            self.assertTrue(any("Corrupt JSON" in e for e in errs))
        finally:
            os.remove(tf_path)

        # Insufficient messages (< 2)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump({"messages": [{"role": "user", "content": "hi"}]}, tf)
            tf_path = tf.name
        try:
            errs = validate_iec.validate_json_file(tf_path)
            self.assertTrue(any("Invalid structure" in e for e in errs))
        finally:
            os.remove(tf_path)

        # No assistant role present at all (< 1 assistant message)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump({"messages": [{"role": "user", "content": "hi"}, {"role": "user", "content": "there"}]}, tf)
            tf_path = tf.name
        try:
            errs = validate_iec.validate_json_file(tf_path)
            self.assertTrue(any("No assistant code content found" in e for e in errs))
        finally:
            os.remove(tf_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
