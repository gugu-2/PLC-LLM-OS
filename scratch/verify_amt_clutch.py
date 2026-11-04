import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_amt_clutch import build_code

code = build_code()
clean = re.sub(r'\(\*[\s\S]*?\*\)', '', code)

tokens = {
    'IF': len(re.findall(r'\bIF\b', clean)),
    'END_IF;': len(re.findall(r'\bEND_IF;', clean)),
    'CASE': len(re.findall(r'\bCASE\b', clean)),
    'END_CASE;': len(re.findall(r'\bEND_CASE;', clean)),
    'FOR': len(re.findall(r'\bFOR\b', clean)),
    'END_FOR;': len(re.findall(r'\bEND_FOR;', clean)),
    'FUNCTION_BLOCK': len(re.findall(r'\bFUNCTION_BLOCK\b', clean)),
    'END_FUNCTION_BLOCK': len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean)),
}

for k, v in tokens.items():
    print(f"{k}: {v}")

assert tokens['IF'] == tokens['END_IF;'], f"IF mismatch: {tokens['IF']} vs {tokens['END_IF;']}"
assert tokens['CASE'] == tokens['END_CASE;'], f"CASE mismatch: {tokens['CASE']} vs {tokens['END_CASE;']}"
assert tokens['FOR'] == tokens['END_FOR;'], f"FOR mismatch: {tokens['FOR']} vs {tokens['END_FOR;']}"
assert tokens['FUNCTION_BLOCK'] == tokens['END_FUNCTION_BLOCK'], "FUNCTION_BLOCK mismatch"

print("SUCCESS: ALL DELIMITER PARITIES PERFECT!")
