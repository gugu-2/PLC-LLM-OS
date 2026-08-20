# Fine-Tuning Cost and Time Analysis: Qwen2.5-Coder 7B on Google Cloud

This document breaks down the mathematical estimates for fine-tuning a 7B to 8B parameter model (e.g., Qwen 2.5 Coder 7B) on a massive 100,000-record dataset using Google Cloud Platform (GCP).

## 1. Dataset & Token Mathematics
*   **Dataset Size:** 100,000 records
*   **Average Tokens per Record:** ~800 tokens (Standard for IEC 61131-3 code blocks + instructions)
*   **Total Tokens per Epoch:** 80,000,000 tokens (80 Million)
*   **Recommended Epochs:** 3 (Standard for code-specific fine-tuning)
*   **Total Training Tokens:** **240,000,000 tokens**

## 2. Hardware Selection on Google Cloud
To fine-tune a 7B parameter model using LoRA (Low-Rank Adaptation) efficiently, you need a GPU with at least 24GB to 40GB of VRAM.

**Option A: NVIDIA L4 (24GB VRAM)**
*   **Pros:** Very cheap, readily available on GCP.
*   **Cons:** Slower.
*   **GCP Cost (On-Demand):** ~.50 per hour
*   **GCP Cost (Spot/Preemptible):** ~.70 per hour

**Option B: NVIDIA A100 (40GB VRAM) — Recommended**
*   **Pros:** Massive throughput, perfect for 7B full or LoRA fine-tuning.
*   **Cons:** Slightly more expensive per hour, sometimes hard to get allocation.
*   **GCP Cost (On-Demand):** ~.93 per hour
*   **GCP Cost (Spot/Preemptible):** ~.20 per hour

## 3. Time and Cost Estimates

Assuming you use a single **NVIDIA A100** GPU on Google Cloud using the Unsloth library (which is highly optimized for fast fine-tuning):

*   **Training Throughput:** ~4,000 to 5,000 tokens per second.
*   **Total Time Calculation:** 240,000,000 tokens / 5,000 tokens per second = 48,000 seconds.
*   **Hours Required:** ~13.3 hours. (Adding overhead for checkpoint saving and setup, expect **15 to 20 hours**).

### Final Cost Calculation:
*   **Using Standard On-Demand A100:** 20 hours * .93 = **~.60**
*   **Using Spot/Preemptible A100:** 20 hours * .20 = **~.00**

## Conclusion
You have  to ,200 in Google Cloud credits. Fine-tuning 100,000 records on a 7B model will only cost between ** and **. 

You have more than enough credits to run this fine-tune dozens of times to experiment with different hyperparameters!
