import json
data = {
    'messages': [
        {
            'role': 'user',
            'content': 'You are acting as a Lead Geophysics Engineer. Evolve a basic fluid loop into a Massive Hydraulic Fracturing (Fracking) Blender and Pump Controller. Technical Specs: 1. Proppant (sand) and fracturing fluid mixing ratio cross-control. 2. High-pressure (15,000 PSI) quintuplex pump synchronization. 3. Cavitation detection and automatic flow bypass.'
        },
        {
            'role': 'assistant',
            'content': """FUNCTION_BLOCK "fb_FrackingController_V2.1.0"
TITLE = Massive Hydraulic Fracturing Blender and Pump Controller
{ S7_Optimized_Access := 'TRUE' }
AUTHOR : 'Lumina Elite Architect'
FAMILY : 'Geophysics'
VERSION : 2.1

VAR_INPUT
    ir_ProppantFeedRate : Real;   // Current proppant feed rate (kg/s)
    ir_FluidFeedRate : Real;      // Current fluid flow rate (L/s)
    ir_TargetMixingRatio : Real;  // Target mixing ratio (kg/L)
    ir_SuctionPressure : Real;    // Suction manifold pressure (PSI)
    ir_DischargePressure : Real;  // High-pressure manifold (PSI)
    ir_PumpRPM : Real;            // Quintuplex pump RPM
    ib_EmergencyStop : Bool;      // Emergency stop signal
    ib_AutoMode : Bool;           // Auto control enabled
END_VAR

VAR_OUTPUT
    or_ProppantCommand : Real;    // Proppant screw command 0-100%
    or_FluidCommand : Real;       // Fluid supply pump command 0-100%
    or_BypassValveCommand : Real; // Bypass valve position 0-100%
    ob_CavitationWarning : Bool;  // Cavitation detected warning
    ob_HighPressureTrip : Bool;   // Overpressure trip
    ob_SystemHealthy : Bool;      // Overall system health
END_VAR

VAR
    inst_MixingPID {InstructionName := 'PID_Compact'; LibVersion := '2.2'} : PID_Compact;
    inst_CavitationTimer {InstructionName := 'TON_TIME'; LibVersion := '1.0'} : TON_TIME;
    inst_OverpressureTimer {InstructionName := 'TON_TIME'; LibVersion := '1.0'} : TON_TIME;
    
    stat_CurrentMixingRatio : Real;
    stat_CavitationDetected : Bool;
    stat_OverpressureDetected : Bool;
    
    stat_TimeCavitation : Time := T#2S;
    stat_TimeOverpressure : Time := T#500MS;
END_VAR

VAR CONSTANT
    CONST_MAX_PRESSURE : Real := 15000.0;    // Maximum operating pressure
    CONST_TRIP_PRESSURE : Real := 15500.0;   // Hard trip pressure limit
    CONST_CAVITATION_P_MIN : Real := 35.0;   // Minimum suction pressure
    CONST_MIN_RPM_CAVITATION : Real := 15.0; // Minimum RPM to care about cavitation
END_VAR

BEGIN
    // ==========================================
    // 1. Proppant and Fluid Mixing Ratio Cross-Control
    // ==========================================
    IF #ir_FluidFeedRate > 0.0 THEN
        #stat_CurrentMixingRatio := #ir_ProppantFeedRate / #ir_FluidFeedRate;
    ELSE
        #stat_CurrentMixingRatio := 0.0;
    END_IF;

    // Cross-control PID execution
    // Assuming PID_Compact handles the underlying integration and derivative action
    #inst_MixingPID(Setpoint := #ir_TargetMixingRatio,
                    Input := #stat_CurrentMixingRatio,
                    Reset := #ib_EmergencyStop);
                    
    IF #ib_AutoMode AND NOT #ib_EmergencyStop THEN
        // Base feedforward calculation + PID output trim
        #or_ProppantCommand := (#ir_FluidFeedRate * #ir_TargetMixingRatio * 0.1) + #inst_MixingPID.Output;
        #or_FluidCommand := 75.0; // Nominal steady-state fluid delivery command for fracking
    ELSE
        #or_ProppantCommand := 0.0;
        #or_FluidCommand := 0.0;
    END_IF;
    
    // Saturation limits
    #or_ProppantCommand := LIMIT(MN:=0.0, IN:=#or_ProppantCommand, MX:=100.0);

    // ==========================================
    // 2. High-Pressure (15,000 PSI) Quintuplex Pump Synchronization
    // ==========================================
    // Dynamic throttling based on discharge manifold pressure feedback
    IF #ir_DischargePressure > #CONST_MAX_PRESSURE THEN
        #or_FluidCommand := #or_FluidCommand * (#CONST_MAX_PRESSURE / #ir_DischargePressure);
    END_IF;

    #stat_OverpressureDetected := (#ir_DischargePressure > #CONST_TRIP_PRESSURE);
    #inst_OverpressureTimer(IN := #stat_OverpressureDetected, PT := #stat_TimeOverpressure);
    
    IF #inst_OverpressureTimer.Q THEN
        #ob_HighPressureTrip := TRUE;
    END_IF;

    // ==========================================
    // 3. Cavitation Detection and Automatic Flow Bypass
    // ==========================================
    // Quintuplex pumps suffer catastrophic failure during cavitation
    #stat_CavitationDetected := (#ir_SuctionPressure < #CONST_CAVITATION_P_MIN) AND (#ir_PumpRPM > #CONST_MIN_RPM_CAVITATION);
    #inst_CavitationTimer(IN := #stat_CavitationDetected, PT := #stat_TimeCavitation);
    #ob_CavitationWarning := #inst_CavitationTimer.Q;

    // Automatic Flow Bypass Logic
    IF #ib_EmergencyStop OR #ob_HighPressureTrip THEN
        #or_BypassValveCommand := 100.0; // 100% Open to relieve system pressure instantly
        #or_FluidCommand := 0.0;
        #or_ProppantCommand := 0.0;
    ELSIF #ob_CavitationWarning THEN
        #or_BypassValveCommand := 45.0; // Modulate bypass to 45% to stabilize suction flow
        #or_FluidCommand := #or_FluidCommand * 0.4; // Throttle down supply pumps
    ELSE
        #or_BypassValveCommand := 0.0; // Normal operation, bypass securely closed
    END_IF;
    
    // Health status
    #ob_SystemHealthy := NOT #ib_EmergencyStop AND NOT #ob_HighPressureTrip AND NOT #ob_CavitationWarning;

END_FUNCTION_BLOCK"""
        }
    ]
}

with open(r'c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl', 'a') as f:
    f.write(json.dumps(data) + '\n')
