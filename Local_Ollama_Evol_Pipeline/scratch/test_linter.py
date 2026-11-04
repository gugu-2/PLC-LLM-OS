import os, sys, json, uuid, re

# Setup paths
workspace = r"c:\Users\majip\Downloads\LLM REASEARCH"
sys.path.append(os.path.join(workspace, "Local_Ollama_Evol_Pipeline", "scripts"))
from linter import ST_Linter

print("Linter loaded successfully.")
