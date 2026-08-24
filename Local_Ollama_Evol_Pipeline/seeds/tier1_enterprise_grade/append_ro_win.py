import json

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"

user_prompt = """Evolve a basic fluid block into an Ultra-Pure Water (UPW) Reverse Osmosis Controller. Technical Specs: 1. 18.2 Megaohm-cm resistivity tracking and fail-to-drain interlocks. 2. Total Organic Carbon (TOC) continuous UV oxidation looping. 3. Final sub-micron ultrafiltration (UF) cross-flow matrix."""

assistant_response = """\
FUNCTION_BLOCK "UPW_RO_Controller"
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : 'Lumina Elite Architect'
FAMILY : 'SemiFabUPW'
VERSION : 1.0
//=============================================================================
// Ultra-Pure Water (UPW) Reverse Osmosis Advanced Controller
// Technical Specs:
// 1. 18.2 Megaohm-cm resistivity tracking and fail-to-drain interlocks.
// 2. Total Organic Carbon (TOC) continuous UV oxidation looping.
// 3. Final sub-micron ultrafiltration (UF) cross-flow matrix.
//=============================================================================
   VAR_INPUT 
      ib_SystemEnable : Bool;   // Master enable for the UPW RO system
      ir_FeedPressure_bar : Real;   // Feed pressure from main supply
      ir_RO_PermeateResistivity_MOhm : Real;   // RO Permeate Resistivity (Target: > 18.2 MOhm-cm)
      ir_TOC_Level_ppb : Real;   // Total Organic Carbon level in ppb (Target: < 1.0 ppb)
      ir_UF_TransMembranePressure_bar : Real; // TMP across Ultrafiltration matrix
      ib_DrainValve_ClosedFB : Bool; // Feedback from fail-to-drain valve
   END_VAR

   VAR_OUTPUT 
      ob_HighPressurePumpCmd : Bool; // Command for main RO HP pump
      or_HighPressurePumpSpeed_pct : Real; // VFD Speed for HP pump
      ob_FailToDrainValveCmd : Bool; // Command to open fail-to-drain valve
      ob_UV_OxidationLampCmd : Bool; // Command to power on UV 185nm/254nm oxidation lamps
      ob_UF_RecirculationPumpCmd : Bool; // Ultrafiltration cross-flow matrix pump
      ob_SystemFault : Bool; // Master fault indicator
      ob_WaterQualityOK : Bool; // True if UPW is 18.2 MOhm-cm and TOC < 1 ppb
   END_VAR

   VAR 
      stat_State_Machine : Int; // 0: OFF, 1: FLUSH, 2: PRODUCTION, 3: FAIL_TO_DRAIN
      inst_TimerFlush {InstructionName := 'TON_TIME'; LibVersion := '1.0'} : TON_TIME;
      inst_TimerResistivityDelay {InstructionName := 'TON_TIME'; LibVersion := '1.0'} : TON_TIME;
      stat_ResistivityFault : Bool;
      stat_TOCFault : Bool;
      stat_UFFault : Bool;
   END_VAR

   VAR CONSTANT 
      RESISTIVITY_LIMIT_MOHM : Real := 18.15; // Setpoint below 18.2 to allow hysteresis
      TOC_LIMIT_PPB : Real := 1.5; // Max allowable TOC in ppb
      UF_TMP_MAX_BAR : Real := 2.5; // Max trans-membrane pressure
      STATE_OFF : Int := 0;
      STATE_FLUSH : Int := 1;
      STATE_PRODUCTION : Int := 2;
      STATE_FAIL_TO_DRAIN : Int := 3;
   END_VAR

BEGIN
    // ------------------------------------------------------------------------
    // Fault Evaluation
    // ------------------------------------------------------------------------
    // 1. Resistivity tracking (18.2 Megaohm-cm)
    // Delay fault slightly to allow transient stabilization
    #inst_TimerResistivityDelay(IN := (#ir_RO_PermeateResistivity_MOhm < #RESISTIVITY_LIMIT_MOHM) AND (#stat_State_Machine = #STATE_PRODUCTION),
                                PT := T#5s);
    #stat_ResistivityFault := #inst_TimerResistivityDelay.Q;

    // 2. Total Organic Carbon (TOC) evaluation
    #stat_TOCFault := (#ir_TOC_Level_ppb > #TOC_LIMIT_PPB);

    // 3. Ultrafiltration (UF) cross-flow matrix TMP evaluation
    #stat_UFFault := (#ir_UF_TransMembranePressure_bar > #UF_TMP_MAX_BAR);

    #ob_SystemFault := #stat_ResistivityFault OR #stat_TOCFault OR #stat_UFFault;

    // ------------------------------------------------------------------------
    // State Machine
    // ------------------------------------------------------------------------
    IF NOT #ib_SystemEnable THEN
        #stat_State_Machine := #STATE_OFF;
    ELSIF #ob_SystemFault THEN
        #stat_State_Machine := #STATE_FAIL_TO_DRAIN;
    END_IF;

    CASE #stat_State_Machine OF
        #STATE_OFF:
            #ob_HighPressurePumpCmd := FALSE;
            #or_HighPressurePumpSpeed_pct := 0.0;
            #ob_FailToDrainValveCmd := FALSE;
            #ob_UV_OxidationLampCmd := FALSE;
            #ob_UF_RecirculationPumpCmd := FALSE;
            #ob_WaterQualityOK := FALSE;
            
            IF #ib_SystemEnable AND NOT #ob_SystemFault THEN
                #stat_State_Machine := #STATE_FLUSH;
            END_IF;

        #STATE_FLUSH:
            // Flush sequence to purge initial lines
            #ob_HighPressurePumpCmd := TRUE;
            #or_HighPressurePumpSpeed_pct := 40.0; // Low speed flush
            #ob_FailToDrainValveCmd := TRUE; // Flush goes to drain
            #ob_UV_OxidationLampCmd := TRUE; // Warm up UV
            #ob_UF_RecirculationPumpCmd := TRUE; // Run cross-flow matrix

            #inst_TimerFlush(IN := TRUE, PT := T#30s);
            IF #inst_TimerFlush.Q AND (#ir_RO_PermeateResistivity_MOhm >= #RESISTIVITY_LIMIT_MOHM) THEN
                #stat_State_Machine := #STATE_PRODUCTION;
            END_IF;

        #STATE_PRODUCTION:
            #inst_TimerFlush(IN := FALSE, PT := T#30s); // Reset flush timer
            #ob_HighPressurePumpCmd := TRUE;
            #or_HighPressurePumpSpeed_pct := 100.0; // Full production
            #ob_FailToDrainValveCmd := FALSE; // Send UPW to fab
            #ob_UV_OxidationLampCmd := TRUE; // Continuous TOC UV oxidation
            #ob_UF_RecirculationPumpCmd := TRUE; // Continuous sub-micron UF
            #ob_WaterQualityOK := TRUE;

        #STATE_FAIL_TO_DRAIN:
            // Fail-to-drain interlocks
            #ob_HighPressurePumpCmd := TRUE; // Keep running to maintain pressure, but dump
            #or_HighPressurePumpSpeed_pct := 50.0; 
            #ob_FailToDrainValveCmd := TRUE; // Divert to drain to protect fab
            #ob_UV_OxidationLampCmd := TRUE; // Keep UV on to attempt recovery
            #ob_UF_RecirculationPumpCmd := TRUE;
            #ob_WaterQualityOK := FALSE;
            
            IF NOT #ob_SystemFault AND #ib_SystemEnable THEN
                #stat_State_Machine := #STATE_FLUSH; // Re-attempt flush if faults clear
            END_IF;

    END_CASE;
END_FUNCTION_BLOCK
"""

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open(target_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(record) + '\n')

print("Append successful.")
