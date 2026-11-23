"""
Extended edge cases test suite for validate_iec.py
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import validate_iec

class TestValidateIECExtendedEdgeCases(unittest.TestCase):

    def test_variable_names_with_keyword_substrings(self):
        """Ensure variable names like nDiff, rPlatform, sForecast, rBriefcase don't trip keyword counters."""
        code = """FUNCTION_BLOCK FB_SubstringTest
VAR_INPUT
    rBriefcasePressure : REAL; (* [bar] *)
    nDiffTemp : REAL; (* [deg C] *)
    sForecastTorque : REAL; (* [kN] *)
    rPlatformVelocity : REAL; (* [m/s] *)
    bStiffnessActive : BOOL; (* [%] *)
END_VAR
VAR_OUTPUT
    bStatusOk : BOOL; (* [-] *)
END_VAR
VAR
    nShiftRegister : DINT; (* [counts] *)
    rBrief : REAL;
    sForecast : STRING;
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

IF rBriefcasePressure > 10.0 THEN
    nShiftRegister := 1;
ELSIF rPlatformVelocity > 5.0 THEN
    nShiftRegister := 2;
ELSE
    nShiftRegister := 0;
END_IF;

FOR nShiftRegister := 1 TO 5 DO
    rBrief := rBrief + 1.0;
END_FOR;

CASE nShiftRegister OF
    1: bStatusOk := TRUE;
    ELSE bStatusOk := FALSE;
END_CASE;

END_FUNCTION_BLOCK
"""
        res = validate_iec.check_parity(code, min_chars=1000)
        self.assertEqual(res["verdict"], "PASS", f"Errors: {res['errors']}")
        self.assertEqual(res["counts"]["IF"], 1)
        self.assertEqual(res["counts"]["END_IF"], 1)
        self.assertEqual(res["counts"]["CASE"], 1)
        self.assertEqual(res["counts"]["END_CASE"], 1)
        self.assertEqual(res["counts"]["FOR"], 1)
        self.assertEqual(res["counts"]["END_FOR"], 1)

    def test_deeply_nested_structures(self):
        """Test deeply nested IF inside CASE inside FOR."""
        code = """FUNCTION_BLOCK FB_DeeplyNested
VAR_INPUT
    rPressure : REAL; (* [bar] *)
    rTemp : REAL; (* [deg C] *)
    rForce : REAL; (* [kN] *)
    rSpeed : REAL; (* [rpm] *)
    rFlow : REAL; (* [l/min] *)
END_VAR
VAR_OUTPUT
    bDone : BOOL; (* [-] *)
END_VAR
VAR
    i, j, k : INT;
    nMode : INT;
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

FOR i := 1 TO 3 DO
    CASE nMode OF
        1:
            IF rPressure > 5.0 THEN
                IF rTemp > 100.0 THEN
                    bDone := TRUE;
                ELSE
                    bDone := FALSE;
                END_IF;
            END_IF;
        2:
            WHILE rSpeed < 1000.0 DO
                rSpeed := rSpeed + 10.0;
            END_WHILE;
    END_CASE;
END_FOR;

END_FUNCTION_BLOCK;
"""
        res = validate_iec.check_parity(code, min_chars=1000)
        self.assertEqual(res["verdict"], "PASS")
        self.assertEqual(res["counts"]["FOR"], 1)
        self.assertEqual(res["counts"]["END_FOR"], 1)
        self.assertEqual(res["counts"]["CASE"], 1)
        self.assertEqual(res["counts"]["END_CASE"], 1)
        self.assertEqual(res["counts"]["IF"], 2)
        self.assertEqual(res["counts"]["END_IF"], 2)
        self.assertEqual(res["counts"]["WHILE"], 1)
        self.assertEqual(res["counts"]["END_WHILE"], 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
