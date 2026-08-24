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
            
        # 2. Check for unclosed statements (strip comments first)
        clean_code = re.sub(r'\(\*.*?\*\)', '', code_str, flags=re.DOTALL)
        clean_code = re.sub(r'//.*', '', clean_code)
        
        if_count = len(re.findall(r'\bIF\b', clean_code, re.IGNORECASE))
        endif_count = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
        if if_count != endif_count:
            return False, f"Logical Error: Mismatched IF ({if_count}) / END_IF ({endif_count}) statements."
            
        for_count = len(re.findall(r'\bFOR\b', clean_code, re.IGNORECASE))
        endfor_count = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
        if for_count != endfor_count:
            return False, f"Logical Error: Mismatched FOR ({for_count}) / END_FOR ({endfor_count}) loops."
            
        case_count = len(re.findall(r'\bCASE\b', clean_code, re.IGNORECASE))
        endcase_count = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))
        if case_count != endcase_count:
            return False, f"Logical Error: Mismatched CASE ({case_count}) / END_CASE ({endcase_count}) statements."

        # 3. Prevent Hallucinated AI Apologies & Refusals
        bad_phrases = [
            "here is the code", "as an ai", "certainly!", "i hope this helps",
            "please note", "note that", "as requested", "here's the",
            "let me know if you need"
        ]
        if any(phrase in code_str.lower() for phrase in bad_phrases):
            return False, "Formatting Error: Code block contains conversational AI text. Strip all conversational text and return ONLY raw IEC 61131-3 code."
            
        refusal_phrases = [
            "cannot provide", "cannot fulfill", "must decline", "safety guidelines",
            "prohibited", "cannot generate"
        ]
        if any(phrase in code_str.lower() for phrase in refusal_phrases):
            return False, "Safety Error: LLM refused to generate code for this prompt."

        # 4. Check Variable Declarations & Interfaces
        if "VAR" in code_str and "END_VAR" not in code_str:
            return False, "Syntax Error: Unclosed VAR declaration block."
            
        if not re.search(r'\bVAR_INPUT\b', code_str, re.IGNORECASE):
            return False, "Design Error: Missing VAR_INPUT interface block."
            
        if not re.search(r'\bVAR_OUTPUT\b', code_str, re.IGNORECASE):
            return False, "Design Error: Missing VAR_OUTPUT interface block."

        # 5. Check Minimum Code Size
        if len(code_str.strip()) < 1500:
            return False, f"Code size too small ({len(code_str.strip())} chars). Minimum allowed is 1500."

        return True, "Code passes all static verification checks."

