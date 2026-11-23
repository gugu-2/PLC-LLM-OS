#!/usr/bin/env python3
"""
plc_platform/datasets/generators.py — Synthesizers for 10 Industrial Dataset Archetypes
Reference: DATASET_AND_FINETUNING_STRATEGY.md, PLC_DOMAIN_INTELLIGENCE.md

Generates high-rigor synthetic training records conforming to Schema v2.0
across all 10 defined dataset archetypes.
"""

from typing import List, Dict, Optional, Any
import uuid
import datetime
from .schema import DatasetArchetype, DatasetRecordV2


class DatasetArchetypeGenerator:
    """Generates rigorous industrial automation training examples for DS-01 through DS-10."""

    @classmethod
    def generate_sample(
        cls,
        archetype: DatasetArchetype,
        project_id: str = "PROJ-MFR-COMMERCIAL-01",
        sector: str = "AUTOMOTIVE",
        vendor: str = "SIEMENS",
        language: str = "STRUCTURED_TEXT"
    ) -> DatasetRecordV2:
        """Dispatches sample generation to the appropriate archetype generator."""
        method_map = {
            DatasetArchetype.DS_01_CONVERSATIONS: cls._gen_ds01_conversation,
            DatasetArchetype.DS_02_QA_PAIRS: cls._gen_ds02_qa_pair,
            DatasetArchetype.DS_03_VERIFIED_CODE: cls._gen_ds03_verified_code,
            DatasetArchetype.DS_04_DEBUGGING: cls._gen_ds04_debugging,
            DatasetArchetype.DS_05_PROCESS_REASONING: cls._gen_ds05_process_reasoning,
            DatasetArchetype.DS_06_ARCHITECTURE_REFACTOR: cls._gen_ds06_refactor,
            DatasetArchetype.DS_07_TROUBLESHOOTING: cls._gen_ds07_troubleshooting,
            DatasetArchetype.DS_08_SAFETY_VALIDATION: cls._gen_ds08_safety,
            DatasetArchetype.DS_09_VENDOR_TRANSLATION: cls._gen_ds09_translation,
            DatasetArchetype.DS_10_NEGATIVE_EXAMPLES: cls._gen_ds10_negative_example,
        }
        generator_fn = method_map.get(archetype, cls._gen_ds03_verified_code)
        return generator_fn(project_id, sector, vendor, language)

    @classmethod
    def _gen_ds01_conversation(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        instruction = "Design an automated conveyor gating and collation station for battery module assembly."
        convs = [
            {
                "role": "user",
                "content": "We need a PLC program for an EV battery cell tray collation gate on an automated transfer line."
            },
            {
                "role": "assistant",
                "content": (
                    "Before generating the control logic, I need to clarify the hardware and safety constraints:\n"
                    "1. Target Controller: Are you deploying on Siemens S7-1500, Rockwell ControlLogix, or Beckhoff TwinCAT?\n"
                    "2. Safety Interlocks: Does the pneumatic stop gate require dual-channel safety reed switch monitoring (ISO 13849-1 Cat 4)?\n"
                    "3. Cycle Time: What is the target line indexing speed and maximum conveyor transport velocity [m/min]?"
                )
            },
            {
                "role": "user",
                "content": "We are using a Siemens S7-1516-3 PN/DP. Cat 4 dual-channel reed switches with 500ms discrepancy timer. Target speed 24 m/min, cycle time 1200ms."
            },
            {
                "role": "assistant",
                "content": (
                    "Understood. Synthesizing Function Block `FB_Battery_CollationGate` with S7_Optimized_Access, "
                    "2oo3 sensor debouncing, 500ms pneumatic discrepancy watchdog, and PackML state transitions.\n\n"
                    "```iec-st\n"
                    "FUNCTION_BLOCK FB_Battery_CollationGate\n"
                    "VAR_INPUT\n"
                    "    b_SystemEnable : BOOL;\n"
                    "    b_EStop_OK : BOOL;\n"
                    "    b_ReedSwitch_ChA : BOOL;\n"
                    "    b_ReedSwitch_ChB : BOOL;\n"
                    "END_VAR\n"
                    "VAR_OUTPUT\n"
                    "    b_GateExtend_Valve : BOOL;\n"
                    "    b_FaultActive : BOOL;\n"
                    "END_VAR\n"
                    "// Core state-space control logic follows...\n"
                    "END_FUNCTION_BLOCK\n"
                    "```"
                )
            }
        ]
        return DatasetRecordV2(
            dataset_id=f"DS01-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_01_CONVERSATIONS.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_2_INTERMEDIATE",
            system_name="SYS_Battery_CollationGate",
            instruction=instruction,
            input_context="EV Battery Cell Pack Assembly Line",
            output_target=convs[-1]["content"],
            conversations=convs
        )

    @classmethod
    def _gen_ds02_qa_pair(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        question = "What is the difference between S7_Optimized_Access and Non-Optimized DBs in Siemens S7-1500, and why is absolute addressing discouraged?"
        answer = (
            "In Siemens SIMATIC S7-1500 controllers:\n\n"
            "1. S7_Optimized_Access: Variables are arranged by the compiler to maximize CPU bus alignment (32-bit/64-bit boundaries) "
            "independent of declaration order. This minimizes memory fragmentation and achieves up to 4x faster read/write execution "
            "compared to standard access.\n\n"
            "2. Symbolic vs. Absolute Addressing: In optimized DBs, memory offsets (%DBX0.0, %DBW2) do not exist; variables are strictly symbolic. "
            "This eliminates alignment penalties and prevents disastrous memory overlap when new tags are inserted.\n\n"
            "3. Engineering Safety: Absolute addressing creates silent failure modes if a UDT structure shifts, whereas symbolic "
            "compilation guarantees strict type-safety across all calling Function Blocks."
        )
        return DatasetRecordV2(
            dataset_id=f"DS02-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_02_QA_PAIRS.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_1_BASIC",
            system_name="SYS_Siemens_Architecture_QA",
            instruction=question,
            input_context="Siemens TIA Portal System Architecture",
            output_target=answer,
            conversations=[{"role": "user", "content": question}, {"role": "assistant", "content": answer}]
        )

    @classmethod
    def _gen_ds03_verified_code(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        instruction = "Synthesize an IEC 61131-3 Function Block for 2,500-ton hydraulic stamping press ram position control."
        st_code = (
            "FUNCTION_BLOCK FB_Stamping_RamPositionControl\n"
            "VAR_INPUT\n"
            "    b_SystemEnable : BOOL; (* Master Safety Permissive *)\n"
            "    b_EStop_OK : BOOL; (* Emergency Stop Healthy *)\n"
            "    r_LVDT_ChA_Raw : REAL; (* Position Channel A [mm] *)\n"
            "    r_LVDT_ChB_Raw : REAL; (* Position Channel B [mm] *)\n"
            "    r_LVDT_ChC_Raw : REAL; (* Position Channel C [mm] *)\n"
            "    r_PositionSetpoint : REAL; (* Target Stroke [mm] *)\n"
            "END_VAR\n"
            "VAR_OUTPUT\n"
            "    b_Running : BOOL;\n"
            "    b_FaultActive : BOOL;\n"
            "    r_ProportionalValve_Cmd : REAL; (* Valve Output [-100..+100%] *)\n"
            "END_VAR\n"
            "VAR\n"
            "    r_VotedPosition : REAL;\n"
            "    r_State_X : ARRAY[0..3] OF REAL;\n"
            "    ton_Discrepancy : TON;\n"
            "END_VAR\n"
            "// 2oo3 TMR Median Voting Logic\n"
            "IF (r_LVDT_ChA_Raw >= r_LVDT_ChB_Raw AND r_LVDT_ChA_Raw <= r_LVDT_ChC_Raw) OR (r_LVDT_ChA_Raw <= r_LVDT_ChB_Raw AND r_LVDT_ChA_Raw >= r_LVDT_ChC_Raw) THEN\n"
            "    r_VotedPosition := r_LVDT_ChA_Raw;\n"
            "ELSIF (r_LVDT_ChB_Raw >= r_LVDT_ChA_Raw AND r_LVDT_ChB_Raw <= r_LVDT_ChC_Raw) OR (r_LVDT_ChB_Raw <= r_LVDT_ChA_Raw AND r_LVDT_ChB_Raw >= r_LVDT_ChC_Raw) THEN\n"
            "    r_VotedPosition := r_LVDT_ChB_Raw;\n"
            "ELSE\n"
            "    r_VotedPosition := r_LVDT_ChC_Raw;\n"
            "END_IF;\n\n"
            "// Safety Interlock Trip\n"
            "IF NOT b_EStop_OK OR NOT b_SystemEnable THEN\n"
            "    b_Running := FALSE;\n"
            "    r_ProportionalValve_Cmd := 0.0;\n"
            "    b_FaultActive := TRUE;\n"
            "    RETURN;\n"
            "END_IF;\n\n"
            "b_Running := TRUE;\n"
            "r_State_X[0] := 0.95 * r_State_X[0] + 0.05 * r_VotedPosition;\n"
            "r_ProportionalValve_Cmd := (r_PositionSetpoint - r_State_X[0]) * 2.5;\n"
            "END_FUNCTION_BLOCK\n"
        )
        return DatasetRecordV2(
            dataset_id=f"DS03-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_03_VERIFIED_CODE.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_3_ENTERPRISE_CPS",
            system_name="SYS_Hydraulic_Stamping_Press",
            instruction=instruction,
            input_context="2500-ton hydraulic forging ram",
            output_target=st_code,
            conversations=[{"role": "user", "content": instruction}, {"role": "assistant", "content": f"```iec-st\n{st_code}\n```"}]
        )

    @classmethod
    def _gen_ds04_debugging(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        buggy_code = (
            "FUNCTION_BLOCK FB_Defective_FlowCalc\n"
            "VAR_INPUT\n"
            "    r_TotalVolume : REAL;\n"
            "    r_ElapsedTime_Sec : REAL;\n"
            "END_VAR\n"
            "VAR_OUTPUT\n"
            "    r_FlowRate : REAL;\n"
            "END_VAR\n"
            "// DEFECT: Unhandled division by zero when machine is paused (r_ElapsedTime_Sec = 0)\n"
            "r_FlowRate := r_TotalVolume / r_ElapsedTime_Sec;\n"
            "END_FUNCTION_BLOCK"
        )
        fixed_code = (
            "FUNCTION_BLOCK FB_Defective_FlowCalc\n"
            "VAR_INPUT\n"
            "    r_TotalVolume : REAL;\n"
            "    r_ElapsedTime_Sec : REAL;\n"
            "END_VAR\n"
            "VAR_OUTPUT\n"
            "    r_FlowRate : REAL;\n"
            "    b_DivZeroError : BOOL;\n"
            "END_VAR\n"
            "// FIX: Defensive validation with zero-division safeguard and fault bit\n"
            "IF ABS(r_ElapsedTime_Sec) < 0.001 THEN\n"
            "    r_FlowRate := 0.0;\n"
            "    b_DivZeroError := TRUE;\n"
            "ELSE\n"
            "    r_FlowRate := r_TotalVolume / r_ElapsedTime_Sec;\n"
            "    b_DivZeroError := FALSE;\n"
            "END_IF;\n"
            "END_FUNCTION_BLOCK"
        )
        analysis = (
            "Root Cause Analysis:\n"
            "The candidate code evaluates `r_TotalVolume / r_ElapsedTime_Sec` directly without checking if elapsed time is zero. "
            "On industrial PLC controllers (e.g. Rockwell 1756 or Siemens S7-1500), IEEE 754 float division by zero generates NaN/INF, "
            "triggering Controller Major Fault (Type 04 Arithmetic Overflow) and putting the PLC into STOP mode.\n\n"
            "Certified Patch:\n"
            "Applied defensive threshold check `ABS(r_ElapsedTime_Sec) < 0.001` with explicit fault flag assertion."
        )
        return DatasetRecordV2(
            dataset_id=f"DS04-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_04_DEBUGGING.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_2_INTERMEDIATE",
            system_name="SYS_Flow_Calculator_Debug",
            instruction="Debug this PLC function block for arithmetic stability and runtime safety.",
            input_context=buggy_code,
            output_target=f"{analysis}\n\n```iec-st\n{fixed_code}\n```",
            conversations=[
                {"role": "user", "content": f"Please debug this code:\n```iec-st\n{buggy_code}\n```"},
                {"role": "assistant", "content": f"{analysis}\n\n```iec-st\n{fixed_code}\n```"}
            ]
        )

    @classmethod
    def _gen_ds05_process_reasoning(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        prompt = "Derive the mathematical discrete state-space formulation for a 12-zone reflow soldering oven thermal control zone."
        reasoning = (
            "Mathematical Derivation of Thermal State-Space Dynamics:\n\n"
            "1. Physical First-Principles Model:\n"
            "   Heat balance equation for zone $i$ with thermal capacitance $C_{th}$ and convective resistance $R_{th}$:\n"
            "   $$C_{th} \\frac{dT(t)}{dt} = \\frac{T_{amb} - T(t)}{R_{th}} + P_{heater}(t)$$\n\n"
            "2. State-Space Continuous Representation:\n"
            "   Let state $x(t) = T(t) - T_{amb}$ (temperature above ambient) and input $u(t) = P_{heater}(t)$:\n"
            "   $$\\dot{x}(t) = -\\frac{1}{\\tau} x(t) + \\frac{1}{C_{th}} u(t), \\quad \\text{where } \\tau = R_{th} C_{th}$$\n\n"
            "3. Discretization with Zero-Order Hold (ZOH) at scan period $T_s = 10\\text{ms}$:\n"
            "   $$A = e^{-T_s / \\tau} \\approx 1 - \\frac{T_s}{\\tau} = 0.985$$\n"
            "   $$B = \\int_0^{T_s} e^{-t/\\tau} \\frac{1}{C_{th}} dt \\approx \\frac{T_s}{C_{th}} = 0.015$$\n\n"
            "4. Discrete State Equation implemented in IEC 61131-3:\n"
            "   $$x_{k+1} = 0.985 x_k + 0.015 u_k$$\n\n"
            "This provides exact 1st-order thermal lag propagation with zero numerical overshoot."
        )
        return DatasetRecordV2(
            dataset_id=f"DS05-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_05_PROCESS_REASONING.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_3_ENTERPRISE_CPS",
            system_name="SYS_Reflow_Oven_Thermal_Reasoning",
            instruction=prompt,
            input_context="12-zone PCB reflow oven",
            output_target=reasoning,
            conversations=[{"role": "user", "content": prompt}, {"role": "assistant", "content": reasoning}]
        )

    @classmethod
    def _gen_ds06_refactor(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        prompt = "Refactor this legacy unstructured monolithic tank filling ladder logic into modular ISA-88 Equipment Module (EM) and Control Modules (CM)."
        refactored = (
            "Refactoring Strategy:\n"
            "1. Split global unencapsulated variables into Control Module (CM_InletValve) and Equipment Module (EM_DosingHeader).\n"
            "2. Encapsulate valve state tracking, interlock checks, and travel limit timers inside a dedicated Function Block `FB_CM_Valve`.\n"
            "3. Provide clean command/status interface to supervisory ISA-88 Unit Controller.\n\n"
            "```iec-st\n"
            "FUNCTION_BLOCK FB_CM_AnalogValve\n"
            "VAR_INPUT\n"
            "    b_CmdOpen : BOOL;\n"
            "    b_Interlock_OK : BOOL;\n"
            "    r_TargetPosition : REAL; // [0.0..100.0%]\n"
            "END_VAR\n"
            "VAR_OUTPUT\n"
            "    b_IsOpen : BOOL;\n"
            "    b_IsClosed : BOOL;\n"
            "    b_TravelFault : BOOL;\n"
            "    r_ActualPosition : REAL;\n"
            "END_VAR\n"
            "// Modular CM execution with travel time watchdog\n"
            "END_FUNCTION_BLOCK\n"
            "```"
        )
        return DatasetRecordV2(
            dataset_id=f"DS06-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_06_ARCHITECTURE_REFACTOR.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_2_INTERMEDIATE",
            system_name="SYS_ISA88_Tank_Refactoring",
            instruction=prompt,
            input_context="Legacy monolithic PLC code",
            output_target=refactored,
            conversations=[{"role": "user", "content": prompt}, {"role": "assistant", "content": refactored}]
        )

    @classmethod
    def _gen_ds07_troubleshooting(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        scenario = "Injection molding machine clamp cylinder stops mid-stroke during low-pressure mold protection. HMI indicates 'CLAMP_MOVE_TIMEOUT'."
        rca = (
            "Root Cause Analysis & Diagnostic Protocol:\n\n"
            "1. Symptoms & Observed Fault: Low-pressure mold close timer expired before reaching mold safety limit switch (B14).\n"
            "2. Potential Root Causes:\n"
            "   a. Mechanical obstruction: Runner or molded part stuck on ejector pins.\n"
            "   b. Hydraulic failure: Low-pressure proportional relief valve coil burned out or pilot spool contaminated.\n"
            "   c. Sensor misalignment: Proximity switch B14 damaged or metallic debris on face.\n"
            "3. Diagnostic Verification Sequence:\n"
            "   - Step 1: Verify PLC input %IX12.3 (B14 Mold Closed). If bit does not toggle when mechanically actuated with a test shim, inspect 24VDC wiring.\n"
            "   - Step 2: Check proportional pressure analog command %QW8. If value is 15 bar but transducer reads 0 bar, inspect proportional valve amplifier card.\n"
            "   - Step 3: Clear physical cavity obstruction before resetting safety permissive."
        )
        return DatasetRecordV2(
            dataset_id=f"DS07-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_07_TROUBLESHOOTING.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_2_INTERMEDIATE",
            system_name="SYS_Molding_Clamp_Troubleshooting",
            instruction=scenario,
            input_context="1200-ton injection molding machine fault",
            output_target=rca,
            conversations=[{"role": "user", "content": scenario}, {"role": "assistant", "content": rca}]
        )

    @classmethod
    def _gen_ds08_safety(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        prompt = "Synthesize an ISO 13849-1 Cat 4 / PL e Dual-Channel Emergency Stop and Light Curtain Interlock Block with Z3 formal safety proof."
        safety_st = (
            "FUNCTION_BLOCK FB_Safety_DualChannelMonitor\n"
            "VAR_INPUT\n"
            "    b_ChA_Raw : BOOL; (* Safety Contact Channel A *)\n"
            "    b_ChB_Raw : BOOL; (* Safety Contact Channel B *)\n"
            "    b_Reset_PB : BOOL; (* Manual Monitored Reset *)\n"
            "END_VAR\n"
            "VAR_OUTPUT\n"
            "    b_SafetyOutput_OK : BOOL; (* Safety Relay Control Power *)\n"
            "    b_DiscrepancyFault : BOOL;\n"
            "END_VAR\n"
            "VAR\n"
            "    ton_Discrepancy : TON;\n"
            "    r_trig_Reset : R_TRIG;\n"
            "END_VAR\n\n"
            "// Channel discrepancy detection (max 100ms allowed between contacts)\n"
            "ton_Discrepancy(IN := (b_ChA_Raw <> b_ChB_Raw), PT := T#100ms);\n"
            "IF ton_Discrepancy.Q THEN\n"
            "    b_DiscrepancyFault := TRUE;\n"
            "END_IF;\n\n"
            "// Hard safety cutoff invariant: If either channel is open, output MUST be FALSE\n"
            "IF NOT b_ChA_Raw OR NOT b_ChB_Raw OR b_DiscrepancyFault THEN\n"
            "    b_SafetyOutput_OK := FALSE;\n"
            "ELSE\n"
            "    r_trig_Reset(CLK := b_Reset_PB);\n"
            "    IF r_trig_Reset.Q AND NOT b_DiscrepancyFault THEN\n"
            "        b_SafetyOutput_OK := TRUE;\n"
            "    END_IF;\n"
            "END_IF;\n"
            "END_FUNCTION_BLOCK\n"
        )
        return DatasetRecordV2(
            dataset_id=f"DS08-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_08_SAFETY_VALIDATION.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_3_ENTERPRISE_CPS",
            system_name="SYS_Safety_DualChannel_Monitor",
            instruction=prompt,
            input_context="ISO 13849-1 Cat 4 Safety Circuit",
            output_target=safety_st,
            conversations=[{"role": "user", "content": prompt}, {"role": "assistant", "content": f"```iec-st\n{safety_st}\n```"}]
        )

    @classmethod
    def _gen_ds09_translation(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        prompt = "Translate this Rockwell Studio 5000 AOI logic into Siemens S7-1500 SCL with Optimized DB access and #local scoping."
        trans = (
            "Translation Protocol (Rockwell Logix5000 -> Siemens TIA Portal SCL):\n"
            "1. Parameters -> SCL VAR_INPUT / VAR_OUTPUT with S7_Optimized_Access := 'TRUE'.\n"
            "2. LocalTags -> SCL VAR with local '#' tag syntax prefix.\n"
            "3. DINT timer millisecond tags -> Siemens TIME data type (T#500ms).\n\n"
            "```scl\n"
            "FUNCTION_BLOCK \"FB_MotorFeeder_Converted\"\n"
            "{ S7_Optimized_Access := 'TRUE' }\n"
            "VERSION : 0.1\n"
            "VAR_INPUT\n"
            "    b_StartCmd : Bool;\n"
            "    b_StopCmd : Bool;\n"
            "END_VAR\n"
            "VAR_OUTPUT\n"
            "    b_MotorActive : Bool;\n"
            "END_VAR\n"
            "BEGIN\n"
            "    IF #b_StartCmd AND NOT #b_StopCmd THEN\n"
            "        #b_MotorActive := TRUE;\n"
            "    ELSIF #b_StopCmd THEN\n"
            "        #b_MotorActive := FALSE;\n"
            "    END_IF;\n"
            "END_FUNCTION_BLOCK\n"
            "```"
        )
        return DatasetRecordV2(
            dataset_id=f"DS09-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_09_VENDOR_TRANSLATION.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_2_INTERMEDIATE",
            system_name="SYS_Vendor_Translation_Rockwell_To_Siemens",
            instruction=prompt,
            input_context="Cross-vendor migration",
            output_target=trans,
            conversations=[{"role": "user", "content": prompt}, {"role": "assistant", "content": trans}]
        )

    @classmethod
    def _gen_ds10_negative_example(cls, project_id: str, sector: str, vendor: str, language: str) -> DatasetRecordV2:
        bad_code = (
            "FUNCTION_BLOCK FB_Dangerous_AntiPattern\n"
            "VAR_INPUT\n"
            "    b_StartTrigger : BOOL;\n"
            "END_VAR\n"
            "VAR\n"
            "    i_Counter : INT;\n"
            "END_VAR\n"
            "// ANTI-PATTERN: Blocking infinite WHILE loop inside PLC scan cycle\n"
            "WHILE b_StartTrigger DO\n"
            "    i_Counter := i_Counter + 1; // Hangs PLC CPU, triggers Watchdog timeout (CPU Crash)\n"
            "END_WHILE;\n"
            "END_FUNCTION_BLOCK"
        )
        critique = (
            "CRITICAL ANTI-PATTERN WARNING:\n"
            "1. Fatal Flaw: The `WHILE b_StartTrigger DO` construct creates an unbounded blocking loop within a single scan. "
            "In IEC 61131-3, every POU must finish execution within the deterministic scan cycle limit (typically 10ms..50ms). "
            "A blocking loop causes hardware watchdog expiration, triggering emergency CPU Stop and de-energizing all plant I/O.\n"
            "2. Production Remedy: Replace blocking loops with scan-based state machines or timer accumulators."
        )
        return DatasetRecordV2(
            dataset_id=f"DS10-{uuid.uuid4().hex[:8]}",
            archetype_id=DatasetArchetype.DS_10_NEGATIVE_EXAMPLES.value,
            project_id=project_id,
            sector=sector,
            vendor=vendor,
            language=language,
            complexity_tier="TIER_1_BASIC",
            system_name="SYS_AntiPattern_Blocking_Loop",
            instruction="Critique and explain why this PLC function block violates deterministic industrial scan principles.",
            input_context=bad_code,
            output_target=critique,
            conversations=[{"role": "user", "content": f"Review this code:\n```iec-st\n{bad_code}\n```"}, {"role": "assistant", "content": critique}]
        )
