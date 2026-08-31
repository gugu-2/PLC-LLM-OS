# SWARM AGENT PROMPT TEMPLATE v2.0
# ===================================
# Use this template when invoking SyntheticDataEvolverV3 agents.
# Replace DOMAIN_NAME and DOMAIN_DETAIL only. Keep everything else identical.

You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.

**Your assigned domain is: DOMAIN_NAME**

Task: Invent a highly complex control scenario for this domain (e.g., DOMAIN_DETAIL).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.

CRITICAL RULES - READ EVERY LINE:

1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   `iec-st
   (your code here)
   `
   NEVER use a single backtick iec-st. ALWAYS use triple backticks.

2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 4 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 3 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always

3. LENGTH: The assistant content MUST be >= 1500 characters total.

4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = '''(paste your full user prompt here)'''
   code = '''`iec-st
FUNCTION_BLOCK FB_YourName
(full code body)
END_FUNCTION_BLOCK
`'''
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)

5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is `iec-st (TRIPLE backtick, NOT single)
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT section
   [ ] Has VAR_OUTPUT section
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ` (triple)
   [ ] Total chars >= 1500

6. REPLY with: EVOLUTION COMPLETE: DOMAIN_NAME

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
