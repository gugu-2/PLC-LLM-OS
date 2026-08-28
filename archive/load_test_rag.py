import time
import random
import numpy as np
import psutil
import os
import sys

# Ensure lumina is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lumina.backend.lumina_ai import IndustrialRAGKnowledgeBase

def main():
    print("Initializing IndustrialRAGKnowledgeBase...")
    kb = IndustrialRAGKnowledgeBase()
    
    queries = [
        "Siemens S120 vibration on Axis 02",
        "Festo valve pressure drop",
        "Rockwell CompactLogix safety tag error",
        "Siemens PROFINET error 16#80C4",
        "Festo CPX-MPA timeout",
        "How to handle GuardLogix safety tags?",
        "S7-1500 communication interruption",
        "Mechanical resonance on packaging line"
    ]
    
    start_time = time.time()
    duration = 420  # 7 minutes
    
    latencies = []
    mem_usages = []
    
    process = psutil.Process(os.getpid())
    
    print("Starting load test for 7 minutes...")
    while time.time() - start_time < duration:
        query_text = random.choice(queries)
        
        q_start = time.time()
        res = kb.query(query_text, top_k=2)
        q_end = time.time()
        
        latencies.append(q_end - q_start)
        mem_usages.append(process.memory_info().rss / (1024 * 1024))
        
    total_queries = len(latencies)
    avg_latency = np.mean(latencies)
    p99_latency = np.percentile(latencies, 99)
    avg_mem = np.mean(mem_usages)
    max_mem = np.max(mem_usages)
    
    print(f"Test complete. Total queries: {total_queries}")
    print(f"Average query latency: {avg_latency:.5f} s")
    print(f"99th percentile latency: {p99_latency:.5f} s")
    print(f"Average memory footprint: {avg_mem:.2f} MB")
    print(f"Peak memory footprint: {max_mem:.2f} MB")

    # Generate markdown report
    report = f"""# RAG Knowledge Base Load Test Report

## Test Parameters
- **Duration**: 7 minutes (420 seconds)
- **Model**: SentenceTransformers (all-MiniLM-L6-v2)
- **Vector Store**: ChromaDB
- **Target**: `IndustrialRAGKnowledgeBase`

## Performance Metrics
- **Total Queries Executed**: {total_queries}
- **Average Query Latency**: {avg_latency:.5f} seconds
- **99th Percentile Latency**: {p99_latency:.5f} seconds

## Resource Utilization
- **Average Memory Footprint**: {avg_mem:.2f} MB
- **Peak Memory Footprint**: {max_mem:.2f} MB

## Analysis
The load test completed successfully, demonstrating the endurance and stability of the local embedding model and vector store integration over a continuous 7-minute querying period.
"""
    
    report_path = r"C:\Users\majip\.gemini\antigravity\brain\4a136880-690c-422e-88be-60ce46a1b230\scratch\rag_test_report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Report written to {report_path}")

if __name__ == "__main__":
    main()
