import json
import os

message_obj = {
    'messages': [
        {
            'role': 'user',
            'content': 'Act as a Lead Defense Engineer. Evolve a basic motion control block into a Nuclear Aircraft Carrier Arresting Gear Controller (IEC 61131-3 implementation). Technical Specs: 1. Water twister hydraulic dampening matrix based on incoming aircraft weight and engagement speed. 2. Cross-deck pendant tension equalization. 3. Constant run-out deceleration profiling to prevent tailhook failure.'
        },
        {
            'role': 'assistant',
            'content': '''Here is the evolved IEC 61131-3 Structured Text implementation for the Advanced Arresting Gear Controller (AAG-C), satisfying your constraints for water twister dampening, cross-deck equalization, and constant run-out deceleration profiling.

```pascal
FUNCTION_BLOCK "fb_AdvancedArrestingGear_Controller"
TITLE = Nuclear Aircraft Carrier Arresting Gear Controller (AAG-C)
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : Lumina_Defense
FAMILY : AVS
VERSION : 3.2

   VAR_INPUT 
      ir_AircraftWeight_kg { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;   // Incoming aircraft gross weight (kg)
      ir_EngagementSpeed_mps { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;   // Radar-measured engagement velocity (m/s)
      ir_PendantTensionPort_kN { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;   // Port side cable tension (kN)
      ir_PendantTensionStbd_kN { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;   // Starboard side cable tension (kN)
      ir_PayoutDistance_m { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;   // Current cable payout distance (m)
      ib_HookEngaged { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Bool;   // Triggered by load cell threshold
      ib_SystemReset { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Bool;   // Reset system for next arrestment
      ir_CycleTime_s { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real := 0.005;   // Scan cycle time (5ms)
   END_VAR

   VAR_OUTPUT 
      or_WaterTwisterValvePort_Pct { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;   // Port water twister restriction valve command (0-100%)
      or_WaterTwisterValveStbd_Pct { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;   // Stbd water twister restriction valve command (0-100%)
      or_DecelProfileTarget_g { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;   // Telemetry output: Target deceleration (g-force)
      ob_SystemFault { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Bool;   // Critical system fault indicator
      ob_ArrestmentComplete { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Bool;   // Arrestment sequence successfully completed
   END_VAR

   VAR 
      stat_KineticEnergy_MJ { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;
      stat_TargetRunoutDistance_m { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real := 105.0; // Nominal run-out (approx 344 ft)
      stat_RequiredTension_kN { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;
      stat_TensionDiff_kN { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;
      stat_EqualizationCorrection { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real;
      
      // PID control variables for deceleration profiling
      stat_PID_Integral { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real := 0.0;
      stat_PID_Error { ExternalAccessible := 'False'; ExternalVisible := 'False'; ExternalWritable := 'False'} : Real := 0.0;
   END_VAR

   VAR CONSTANT 
      c_MaxTensionDiff_kN : Real := 75.0; // Maximum allowable asymmetrical tension before fault
      c_MaxDecel_g : Real := 4.5; // Prevent structural/tailhook failure
      c_Gravity_mps2 : Real := 9.80665;
      c_BaseValveGain : Real := 0.045; // Empirical matrix gain for valve % per kN
      c_Kp : Real := 0.15; // Proportional gain for constant run-out profiling
      c_Ki : Real := 0.02; // Integral gain
   END_VAR

BEGIN
    // ---------------------------------------------------------
    // System Reset Sequence
    // ---------------------------------------------------------
    IF #ib_SystemReset THEN
        #or_WaterTwisterValvePort_Pct := 0.0;
        #or_WaterTwisterValveStbd_Pct := 0.0;
        #or_DecelProfileTarget_g := 0.0;
        #ob_SystemFault := FALSE;
        #ob_ArrestmentComplete := FALSE;
        #stat_PID_Integral := 0.0;
        RETURN;
    END_IF;

    // ---------------------------------------------------------
    // Standby Mode: Pre-charge Dampening Matrix
    // ---------------------------------------------------------
    IF NOT #ib_HookEngaged THEN
        // Calculate incoming kinetic energy (MJ)
        #stat_KineticEnergy_MJ := (0.5 * #ir_AircraftWeight_kg * (#ir_EngagementSpeed_mps ** 2.0)) / 1000000.0;
        
        // Matrix look-up equivalent: Set pre-tension valve state based on predicted energy
        // Higher energy requires initial higher valve restriction to prevent initial payout shock
        #or_WaterTwisterValvePort_Pct := LIMIT(MN:=5.0, IN:=(#stat_KineticEnergy_MJ * 1.2), MX:=85.0);
        #or_WaterTwisterValveStbd_Pct := #or_WaterTwisterValvePort_Pct;
        RETURN;
    END_IF;

    // =========================================================
    // ACTIVE ARRESTMENT SEQUENCE
    // =========================================================
    
    // 1. Constant Run-Out Deceleration Profiling
    // Calculate necessary constant tension (Work = Force * Distance => Force = KE / remaining_distance)
    IF (#stat_TargetRunoutDistance_m - #ir_PayoutDistance_m) > 2.0 THEN
        #stat_RequiredTension_kN := ((0.5 * #ir_AircraftWeight_kg * (#ir_EngagementSpeed_mps ** 2.0)) / (#stat_TargetRunoutDistance_m - #ir_PayoutDistance_m)) / 1000.0;
    ELSE
        #stat_RequiredTension_kN := 0.0; // Arrestment near completion
        #ob_ArrestmentComplete := TRUE;
    END_IF;

    // Safety Override: Limit deceleration to prevent tailhook yielding (c_MaxDecel_g)
    #or_DecelProfileTarget_g := (#stat_RequiredTension_kN * 1000.0) / (#ir_AircraftWeight_kg * #c_Gravity_mps2);
    IF #or_DecelProfileTarget_g > #c_MaxDecel_g THEN
        #stat_RequiredTension_kN := (#c_MaxDecel_g * #ir_AircraftWeight_kg * #c_Gravity_mps2) / 1000.0;
        #or_DecelProfileTarget_g := #c_MaxDecel_g;
    END_IF;

    // 2. Closed-Loop Tension Control (PID)
    // Error = Target Total Tension - Actual Total Tension
    #stat_PID_Error := #stat_RequiredTension_kN - (#ir_PendantTensionPort_kN + #ir_PendantTensionStbd_kN);
    #stat_PID_Integral := #stat_PID_Integral + (#stat_PID_Error * #ir_CycleTime_s);
    
    // Anti-windup for integral component
    #stat_PID_Integral := LIMIT(MN:=-50.0, IN:=#stat_PID_Integral, MX:=50.0);

    // 3. Cross-Deck Pendant Tension Equalization
    // Calculate imbalance between port and starboard sheaves
    #stat_TensionDiff_kN := #ir_PendantTensionPort_kN - #ir_PendantTensionStbd_kN;
    
    IF ABS(#stat_TensionDiff_kN) > #c_MaxTensionDiff_kN THEN
        #ob_SystemFault := TRUE; // Asymmetric loading beyond structural limits
    END_IF;
    
    // Equalization adjustment (reduce restriction on the side with higher tension to balance)
    #stat_EqualizationCorrection := #stat_TensionDiff_kN * 0.25; 

    // 4. Water Twister Hydraulic Dampening Matrix Application
    // Apply base valve command + PID correction -/+ Equalization adjustment
    #or_WaterTwisterValvePort_Pct := LIMIT(
        MN:=0.0, 
        IN:=(#stat_RequiredTension_kN * #c_BaseValveGain) + (#stat_PID_Error * #c_Kp) + (#stat_PID_Integral * #c_Ki) - #stat_EqualizationCorrection, 
        MX:=100.0);
        
    #or_WaterTwisterValveStbd_Pct := LIMIT(
        MN:=0.0, 
        IN:=(#stat_RequiredTension_kN * #c_BaseValveGain) + (#stat_PID_Error * #c_Kp) + (#stat_PID_Integral * #c_Ki) + #stat_EqualizationCorrection, 
        MX:=100.0);

END_FUNCTION_BLOCK
```'''
        }
    ]
}

target_file = r'C:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl'
with open(target_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(message_obj) + '\n')

print('Success')
