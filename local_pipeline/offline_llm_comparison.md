# Local Offline PLC Dataset Generator - Model Comparison
## NVIDIA RTX 5050 Laptop (8GB GDDR7 VRAM)

### What is Quantization?
Think of it like this:
The model has **14 billion numbers** (weights) stored inside it.
**Quantization = how precisely each number is stored.**

| Version | Bits per number | Like saving a photo at... | Precision lost |
|---------|----------------|--------------------------|---------------|
| Q4_K_M | 4 bits | Medium JPG quality | ~3–4% |
| Q3_K_M | 3 bits | Low JPG quality | ~5–6% |

Same 14 billion parameters. Same brain. Just different compression.
Q3_K_M fits in less VRAM because each weight takes 25% less space.

---

### 3-Model Comparison (RTX 5050 - 8GB VRAM)

| | \qwen2.5-coder:7b\ | \qwen2.5-coder:14b\ Q4_K_M | \qwen2.5-coder:14b\ Q3_K_M |
|---|---|---|---|
| **Parameters** | 7 Billion | 14 Billion | 14 Billion |
| **Quantization** | Q4_K_M | Q4_K_M (4-bit) | Q3_K_M (3-bit) |
| **VRAM needed** | ~4.5 GB ✅ | ~8.3 GB ❌ Overflow | ~6.8 GB ✅ |
| **VRAM left for context** | ~3.5 GB 🟢 | ~0 MB 🔴 CRASH RISK | ~1.2 GB 🟡 |
| **Speed on RTX 5050** | ~85–115 tok/s | ~20–30 tok/s ⚠️ (RAM overflow) | ~42–58 tok/s |
| **Seconds per record** | **7–10 sec** | **30–50 sec** ⚠️ | **13–18 sec** |
| **Records per hour** | **~400–500** | **~72–120** ⚠️ | **~200–270** |
| **Records per 24 hours** | **~10,000** | **~1,700–2,800** ⚠️ | **~5,000** |
| **Code quality vs Gemini Pro** | 65–70% | 76–80% | 72–76% |
| **IEC syntax correctness** | ~90% | ~96% | ~93% |
| **Thermal throttle risk** | 🟢 Low | 🔴 Very High | 🟡 Medium |
| **Laptop fan noise** | 🟢 Quiet | 🔴 Very loud | 🟡 Loud |
| **Crash/OOM risk** | 🟢 None | 🔴 High (no VRAM left) | 🟢 Low |

### The Sweet Spot Strategy:
`powershell
# Daytime → fast, quantity
python local_pipeline\local_swarm_generator.py --model qwen2.5-coder:7b

# Overnight → quality, safe fit in 8GB
python local_pipeline\local_swarm_generator.py --model qwen2.5-coder:14b-instruct-q3_K_M
`
