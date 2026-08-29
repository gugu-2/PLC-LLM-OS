import json
import uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Deep-Sea ROV Tether Management System (TMS).
Task: Invent a highly complex control scenario for this domain (e.g., umbilical tension slip-ring payout synchronization, thruster vectoring compensation, and hydrostatic pressure monitoring).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

response = """```iec-st
FUNCTION_BLOCK FB_DeepSea_TMS_Advanced_Control
(* =========================================================================
   FB_DeepSea_TMS_Advanced_Control
   Description: Highly complex Tether Management System (TMS) controller.
   Synchronizes umbilical tension with slip-ring payout, compensates for
   ROV thruster vectoring, and continuously monitors hydrostatic pressure.
   ========================================================================= *)

VAR_INPUT
    xSystemEnable          : BOOL;  (* Master enable signal for TMS *)
    xEmergencyStop         : BOOL;  (* Hard E-Stop signal *)
    rHydrostaticPressure_Bar: REAL; (* Environmental depth pressure *)
    rUmbilicalTension_N    : REAL;  (* Direct strain gauge tension measurement *)
    rSlipRingPayout_m      : REAL;  (* Current umbilical payout from encoder *)
    rROV_HeaveVelocity_mps : REAL;  (* ROV Z-axis velocity (heave) *)
    rROV_SurgeVelocity_mps : REAL;  (* ROV X-axis velocity (surge) *)
    rROV_PitchAngle_deg    : REAL;  (* ROV pitch angle *)
    rWinchMotorFeedback_rpm: REAL;  (* Winch drum rotational speed *)
    rSlipRingTemp_C        : REAL;  (* Temperature monitoring of the slip ring *)
END_VAR

VAR_OUTPUT
    xSystemReady           : BOOL;  (* TMS is active and ready *)
    xFaultActive           : BOOL;  (* General fault indicator *)
    wFaultCode             : WORD;  (* Bitmask for fault codes *)
    rWinchMotorCommand_rpm : REAL;  (* Output speed command to winch VFD *)
    rSlipRingBrakeCommand  : REAL;  (* 0.0 to 100.0% brake pressure command *)
    rThrusterCompensation  : REAL;  (* Pitch/heave compensation command to ROV *)
    xCoolingPumpEnable     : BOOL;  (* Active cooling for slip ring *)
END_VAR

VAR
    (* --- Control Parameters --- *)
    rTargetTension_N       : REAL := 1500.0; (* Optimal tether tension *)
    rMaxSafeTension_N      : REAL := 5500.0; (* Ultimate safety threshold *)
    rMinSafeTension_N      : REAL := 300.0;  (* Slack threshold *)
    rMaxPayout_m           : REAL := 3500.0; (* Maximum length of umbilical *)
    
    (* --- PID Variables for Tension Control --- *)
    rKp_Tension            : REAL := 0.35;
    rKi_Tension            : REAL := 0.12;
    rKd_Tension            : REAL := 0.05;
    rTensionError          : REAL;
    rTensionIntegral       : REAL;
    rTensionDerivative     : REAL;
    rLastTensionError      : REAL;
    rPIDOutput_rpm         : REAL;
    
    (* --- Feedforward & Kinematic Compensation --- *)
    rHeaveCompensation     : REAL;
    rSurgeCompensation     : REAL;
    rDepthScalingFactor    : REAL;
    
    (* --- State Machine --- *)
    eState                 : INT := 0; (* 0: INIT, 1: STANDBY, 2: ACTIVE, 3: FAULT *)
    
    (* --- Internal Timers & Counters --- *)
    rFaultTimer_ms         : REAL := 0.0;
    rDeltaTime_s           : REAL := 0.01; (* Assumed 10ms cycle time *)
END_VAR

(* =========================================================================
   IMPLEMENTATION BEGINS
   ========================================================================= *)

(* Hard E-Stop Overrides Everything *)
IF xEmergencyStop THEN
    eState := 3;
    wFaultCode := wFaultCode OR 16#8000; (* Critical E-Stop *)
END_IF;

CASE eState OF
    0: (* INIT STATE: Reset everything and verify sensors *)
        xSystemReady := FALSE;
        xFaultActive := FALSE;
        wFaultCode := 16#0000;
        rWinchMotorCommand_rpm := 0.0;
        rSlipRingBrakeCommand := 100.0; (* Full brake *)
        rThrusterCompensation := 0.0;
        xCoolingPumpEnable := FALSE;
        
        rTensionIntegral := 0.0;
        rLastTensionError := 0.0;
        
        IF xSystemEnable AND NOT xEmergencyStop THEN
            eState := 1; (* Move to STANDBY *)
        END_IF;

    1: (* STANDBY STATE: Waiting for launch depth *)
        xSystemReady := TRUE;
        rSlipRingBrakeCommand := 100.0; (* Brakes locked *)
        rWinchMotorCommand_rpm := 0.0;
        
        (* Slip ring thermal management in standby *)
        IF rSlipRingTemp_C > 50.0 THEN
            xCoolingPumpEnable := TRUE;
        ELSIF rSlipRingTemp_C < 40.0 THEN
            xCoolingPumpEnable := FALSE;
        END_IF;

        IF NOT xSystemEnable THEN
            eState := 0;
        ELSIF rHydrostaticPressure_Bar > 2.0 THEN (* approx 20 meters depth *)
            eState := 2; (* Move to ACTIVE *)
            rSlipRingBrakeCommand := 0.0; (* Release brakes *)
        END_IF;

    2: (* ACTIVE STATE: Dynamic Payout and Tension Control *)
        IF NOT xSystemEnable THEN
            eState := 1;
            rSlipRingBrakeCommand := 100.0;
        ELSIF rUmbilicalTension_N > rMaxSafeTension_N THEN
            eState := 3;
            wFaultCode := wFaultCode OR 16#0001; (* Snag or over-tension *)
        ELSIF rUmbilicalTension_N < rMinSafeTension_N THEN
            eState := 3;
            wFaultCode := wFaultCode OR 16#0002; (* Slack tether *)
        ELSIF rSlipRingPayout_m >= rMaxPayout_m THEN
            eState := 3;
            wFaultCode := wFaultCode OR 16#0004; (* Out of tether *)
        ELSE
            (* 1. Tension PID Calculation *)
            rTensionError := rTargetTension_N - rUmbilicalTension_N;
            rTensionIntegral := rTensionIntegral + (rTensionError * rDeltaTime_s);
            
            (* Integral Anti-Windup *)
            IF rTensionIntegral > 500.0 THEN rTensionIntegral := 500.0; END_IF;
            IF rTensionIntegral < -500.0 THEN rTensionIntegral := -500.0; END_IF;
            
            rTensionDerivative := (rTensionError - rLastTensionError) / rDeltaTime_s;
            rLastTensionError := rTensionError;
            
            rPIDOutput_rpm := (rKp_Tension * rTensionError) + 
                              (rKi_Tension * rTensionIntegral) + 
                              (rKd_Tension * rTensionDerivative);
            
            (* 2. Feedforward Kinematic Compensation *)
            (* High pressure alters cable buoyancy and drag *)
            rDepthScalingFactor := 1.0 + (rHydrostaticPressure_Bar * 0.005); 
            
            rHeaveCompensation := rROV_HeaveVelocity_mps * 12.5 * rDepthScalingFactor;
            rSurgeCompensation := rROV_SurgeVelocity_mps * 8.2 * rDepthScalingFactor;
            
            (* Final Winch Command incorporates PID + Feedforward *)
            rWinchMotorCommand_rpm := rPIDOutput_rpm + rHeaveCompensation + rSurgeCompensation;
            
            (* 3. Thruster Vectoring Compensation *)
            (* If payout is lagging behind heave/surge, tell ROV to adjust pitch to minimize drag *)
            IF rTensionError < -800.0 THEN
                rThrusterCompensation := -15.0; (* Dive pitch command *)
            ELSIF rTensionError > 800.0 THEN
                rThrusterCompensation := 10.0;  (* Climb pitch command *)
            ELSE
                rThrusterCompensation := 0.0;
            END_IF;
            
            (* Thermal Management *)
            xCoolingPumpEnable := (rSlipRingTemp_C > 45.0);
        END_IF;

    3: (* FAULT STATE: Safe Shutdown *)
        xFaultActive := TRUE;
        xSystemReady := FALSE;
        rWinchMotorCommand_rpm := 0.0;
        
        (* Modulate brake application to prevent shock loads *)
        IF rSlipRingBrakeCommand < 100.0 THEN
            rSlipRingBrakeCommand := rSlipRingBrakeCommand + 5.0;
            IF rSlipRingBrakeCommand > 100.0 THEN
                rSlipRingBrakeCommand := 100.0;
            END_IF;
        END_IF;
        
        (* Require reset sequence *)
        IF NOT xSystemEnable AND NOT xEmergencyStop THEN
            eState := 0;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
