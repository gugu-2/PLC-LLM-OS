# build_full_dataset.py
import os
import sys
import uuid
import json

# Add scripts directory to path
sys.path.insert(0, os.path.abspath("Local_Ollama_Evol_Pipeline/scripts"))
from linter import ST_Linter

print("Starting generation of FB_FoodBev_AsepticCanning_DoubleSeamer_LeakInspect dataset...")
