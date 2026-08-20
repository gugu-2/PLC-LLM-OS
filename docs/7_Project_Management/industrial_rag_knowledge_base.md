# Lumina AI: Industrial RAG Knowledge Base

## 1. The Context Problem
Industrial controllers rely on thousands of pages of deeply proprietary documentation (e.g., the Siemens S7-1500 memory mapping manual or the Rockwell CIP protocol specs). General LLMs hallucinate these specifics because they lack context.

## 2. RAG Architecture (`lumina_ai.py`)
To solve this, Lumina employs **Retrieval-Augmented Generation (RAG)** specifically tailored for industrial documents.
- **Vector Database:** We use `chromadb`. It is fully local, meaning it runs on the air-gapped Edge device without requiring outbound internet access (a strict requirement for industrial cybersecurity).
- **Embedding Model:** `SentenceTransformers` (`all-MiniLM-L6-v2`) is used to convert PDF manuals into semantic vectors. It has a tiny ~500MB footprint and executes semantic search in ~10ms.

## 3. Dynamic Injection
When a user asks Lumina to "Configure a PID block for a Festo proportional valve", the system:
1. Queries ChromaDB for the vector mathematically closest to "Festo proportional valve PID".
2. Retrieves the exact paragraph from the official Festo PDF.
3. Injects this context into the Qwen2.5-Coder system prompt.
4. The LLM generates the Structured Text leveraging the exact memory addresses required by the manual.
