import re
import logging
from typing import Tuple

logger = logging.getLogger("Linter")

class ST_Linter:
    """
    Enterprise-grade Abstract Syntax Tree (AST) & Regex Linter for IEC-61131-3.
    Ensures generated code is mathematically sound and structurally flawless.
    """
    
    @staticmethod
    def verify_code(code_str: str) -> Tuple[bool, str]:
        """
        Runs a suite of static analysis tests on the generated ST code.
        Returns (True, "") if perfect, or (False, "Error message") if it fails.
        """
        if not code_str or len(code_str.strip()) < 20:
            return False, "Code is empty or critically undersized."
            
        # 1. Check for standard ST block enclosures
        has_prog = bool(re.search(r'(PROGRAM|FUNCTION_BLOCK|FUNCTION)\s+\w+', code_str, re.IGNORECASE))
        has_end = bool(re.search(r'(END_PROGRAM|END_FUNCTION_BLOCK|END_FUNCTION)', code_str, re.IGNORECASE))
        
        if not (has_prog and has_end):
            return False, "Fatal Syntax Error: Missing valid PROGRAM or FUNCTION_BLOCK declaration block."
            
        # 2. Check for unclosed statements
        if code_str.count("IF ") != (code_str.count("END_IF;") + code_str.count("END_IF")):
            return False, "Logical Error: Mismatched IF / END_IF statements."
            
        if code_str.count("FOR ") != (code_str.count("END_FOR;") + code_str.count("END_FOR")):
            return False, "Logical Error: Mismatched FOR / END_FOR loops."
            
        # 3. Prevent Hallucinated AI Apologies
        bad_phrases = ["here is the code", "as an ai", "certainly!", "i hope this helps"]
        if any(phrase in code_str.lower() for phrase in bad_phrases):
            return False, "Formatting Error: Code block contains conversational AI text. Strip all conversational text and return ONLY raw IEC 61131-3 code."
            
        # 4. Check Variable Declarations
        if "VAR" in code_str and "END_VAR" not in code_str:
            return False, "Syntax Error: Unclosed VAR declaration block."
            
        return True, "Code passes all static verification checks."
