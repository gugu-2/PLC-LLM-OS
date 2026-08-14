import os
import json
import glob
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

def format_as_chatml(instruction, response):
    return {
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": response}
        ]
    }

def extract_pdf_errors(pdf_dir="manuals", output_file="data/pdf_errors.jsonl"):
    if fitz is None:
        print("PyMuPDF (fitz) is not installed. Run 'pip install PyMuPDF'")
        return
        
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    pdf_files = glob.glob(f"{pdf_dir}/*.pdf")
    
    if not pdf_files:
        print(f"No PDF files found in '{pdf_dir}'. Please add Siemens/Fanuc manuals there.")
        # Create a mock entry to show how it works
        with open(output_file, 'w', encoding='utf-8') as f:
            record = format_as_chatml(
                "What does Error 16#80C4 mean in Siemens TIA Portal?", 
                "Error 16#80C4 indicates a temporary communication error. The connection could not be established because the remote partner is not responding or the maximum number of connections has been exceeded. To fix this, verify your connection parameters and ensure the remote device is powered on and accessible."
            )
            f.write(json.dumps(record) + "\n")
        print(f"Created mock output at {output_file} since no PDFs were found.")
        return

    print(f"Found {len(pdf_files)} PDF manuals. Extracting tables...")
    
    total_records = 0
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for pdf_path in pdf_files:
            try:
                doc = fitz.open(pdf_path)
                print(f"Processing {pdf_path} ({len(doc)} pages)...")
                # This is a simplified extraction:
                # In a real scenario, you'd look for tables containing "Error Code" and "Description" headers.
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    tables = page.find_tables()
                    for table in tables:
                        rows = table.extract()
                        if rows and len(rows) > 1:
                            # Let's assume col 0 is Error Code and col 1 is Description
                            header = [str(x).lower() for x in rows[0] if x]
                            if any("error" in h or "code" in h for h in header):
                                for row in rows[1:]:
                                    if len(row) >= 2 and row[0] and row[1]:
                                        err_code = str(row[0]).strip()
                                        err_desc = str(row[1]).strip()
                                        if err_code:
                                            instruction = f"What does error {err_code} mean and how do I fix it?"
                                            record = format_as_chatml(instruction, err_desc)
                                            out_f.write(json.dumps(record) + "\n")
                                            total_records += 1
            except Exception as e:
                print(f"Failed to process {pdf_path}: {e}")
                
    print(f"Saved {total_records} error code pairs to {output_file}.")

if __name__ == "__main__":
    extract_pdf_errors()
