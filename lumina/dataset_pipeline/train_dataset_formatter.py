"""
Lumina Dataset Formatter
========================
Parses proprietary XML and text files from Open-Source PLC Repositories
(like Beckhoff TcOpen and Siemens LGF) and extracts pure Structured Text (ST).
Formats the extracted logic into HuggingFace ChatML JSONL pairs for LLM QLoRA Training.
"""

import os
import json
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DatasetFormatter")

# Define repository paths relative to this script
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
TCOPEN_DIR = os.path.join(BASE_DIR, "repos/tcopen")
OUTPUT_FILE = os.path.join(BASE_DIR, "tcopen_raw.jsonl")

def parse_tcopen_xml(filepath: str) -> dict:
    """
    Parses a Beckhoff TwinCAT XML file (.TcPOU, .TcDUT, .TcGVL).
    Extracts the Declaration and Implementation blocks.
    """
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        name = os.path.basename(filepath).replace(".TcPOU", "").replace(".TcDUT", "").replace(".TcGVL", "")
        extracted_code = ""

        # TwinCAT XML structure: <TcPlcObject> -> <POU> / <DUT> / <GVL>
        for block in root.findall(".//*"):
            if block.tag in ["POU", "DUT", "GVL"]:
                name = block.get("Name", name)
                
                # Extract Declaration
                decl_node = block.find("Declaration")
                if decl_node is not None and decl_node.text:
                    extracted_code += decl_node.text.strip() + "\n"
                
                # Extract Implementation (ST)
                impl_node = block.find("Implementation/ST")
                if impl_node is not None and impl_node.text:
                    extracted_code += "\n" + impl_node.text.strip() + "\n"

                # Extract nested Methods/Actions
                for method in block.findall("Method"):
                    method_name = method.get("Name", "Method")
                    extracted_code += f"\n// Method: {method_name}\n"
                    m_decl = method.find("Declaration")
                    if m_decl is not None and m_decl.text:
                        extracted_code += m_decl.text.strip() + "\n"
                    m_impl = method.find("Implementation/ST")
                    if m_impl is not None and m_impl.text:
                        extracted_code += m_impl.text.strip() + "\n"

        if extracted_code.strip():
            return {
                "name": name,
                "code": extracted_code.strip(),
                "type": "Beckhoff TwinCAT"
            }
    except Exception as e:
        logger.debug(f"Failed to parse {filepath}: {e}")
    
    return None

def format_to_chatml(name: str, code: str, language_type: str) -> dict:
    """Formats the raw code into a ChatML instruction pair."""
    prompt = f"Implement the {language_type} module or function block for '{name}'."
    return {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code}
        ]
    }

def main():
    logger.info("Starting Open-Source Dataset Formatting Pipeline...")
    
    if not os.path.exists(TCOPEN_DIR):
        logger.error(f"Target directory not found: {TCOPEN_DIR}")
        return

    processed_count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for root_dir, _, files in os.walk(TCOPEN_DIR):
            for file in files:
                if file.endswith((".TcPOU", ".TcDUT", ".TcGVL")):
                    filepath = os.path.join(root_dir, file)
                    
                    data = parse_tcopen_xml(filepath)
                    if data and len(data["code"]) > 50: # Skip empty or tiny files
                        chatml_obj = format_to_chatml(data["name"], data["code"], data["type"])
                        out_f.write(json.dumps(chatml_obj) + "\n")
                        processed_count += 1
                        
                        if processed_count % 100 == 0:
                            logger.info(f"Processed {processed_count} files...")

    logger.info(f"Pipeline Complete! Successfully formatted {processed_count} files into tcopen_raw.jsonl")

if __name__ == "__main__":
    main()
