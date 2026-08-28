import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Synthetic Diamond CVD Reactor.
Task: Invent a highly complex control scenario for this domain (e.g., microwave plasma density stability, multi-gas MFC recipe blending, and active substrate cooling cascade).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

response = """```iec-st
FUNCTION_BLOCK FB_DiamondCVD_ReactorCtrl
VAR_INPUT
    bEnable                 : BOOL;   (* Enable reactor control *)
    bEmergencyStop          : BOOL;   (* E-Stop condition *)
    rTargetPlasmaDensity    : REAL;   (* Target plasma density in cm^-3 *)
    rActualPlasmaDensity    : REAL;   (* Measured plasma density from Langmuir probe *)
    rTargetSubstrateTemp    : REAL;   (* Target substrate temp in Celsius *)
    rActualSubstrateTemp    : REAL;   (* Pyrometer temp feedback in Celsius *)
    rRecipeCH4Flow          : REAL;   (* Methane flow setpoint sccm *)
    rRecipeH2Flow           : REAL;   (* Hydrogen flow setpoint sccm *)
    rRecipeArFlow           : REAL;   (* Argon flow setpoint sccm *)
    rCoolantInletTemp       : REAL;   (* Cooling water inlet temp *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;   (* Reactor ready for ignition *)
    rMicrowavePowerSetp     : REAL;   (* Output to 2.45 GHz magnetron generator kW *)
    rCH4_MFC_ValvePos       : REAL;   (* 0-100% position for CH4 MFC *)
    rH2_MFC_ValvePos        : REAL;   (* 0-100% position for H2 MFC *)
    rAr_MFC_ValvePos        : REAL;   (* 0-100% position for Argon MFC *)
    rCoolingPumpSpeed       : REAL;   (* 0-100% VFD speed for cooling pump *)
    rChamberPressureSetp    : REAL;   (* Vacuum throttle valve setpoint Torr *)
    bPlasmaIgnited          : BOOL;   (* Status of plasma ignition *)
    bAlarmActive            : BOOL;   (* General alarm *)
    iAlarmCode              : INT;    (* Diagnostic alarm code *)
END_VAR

VAR
    fbPlasmaPID             : PID;    (* PID for microwave power control *)
    fbTempCascadePID        : PID;    (* Master PID for substrate temp *)
    fbCoolingPID            : PID;    (* Slave PID for coolant flow *)
    
    rTempPIDOutput          : REAL;   (* Output from master temp PID *)
    tIgnitionTimer          : TON;    (* Timer for plasma ignition sequence *)
    iState                  : INT := 0; (* State machine state *)
    
    (* Internal tuning parameters *)
    Kp_Plasma               : REAL := 1.5;
    Ki_Plasma               : REAL := 0.2;
    Kd_Plasma               : REAL := 0.05;
    
    Kp_TempMaster           : REAL := 2.0;
    Ki_TempMaster           : REAL := 0.1;
    
    Kp_CoolMaster           : REAL := 5.0;
    Ki_CoolMaster           : REAL := 1.0;
    
    rChamberBasePressure    : REAL := 10.0; (* Torr *)
END_VAR

(* E-Stop Handling *)
IF bEmergencyStop THEN
    iState := 999;
END_IF;

CASE iState OF
    0: (* Standby and Initialization *)
        bSystemReady := FALSE;
        rMicrowavePowerSetp := 0.0;
        rCH4_MFC_ValvePos := 0.0;
        rH2_MFC_ValvePos := 0.0;
        rAr_MFC_ValvePos := 0.0;
        rCoolingPumpSpeed := 0.0;
        rChamberPressureSetp := rChamberBasePressure;
        bPlasmaIgnited := FALSE;
        bAlarmActive := FALSE;
        iAlarmCode := 0;
        
        IF bEnable AND NOT bEmergencyStop THEN
            iState := 10;
        END_IF;
        
    10: (* Purge and Gas Mix Stabilization *)
        bSystemReady := TRUE;
        rChamberPressureSetp := 50.0; (* Operating pressure for ignition *)
        
        (* Open Ar and H2 for initial plasma *)
        rAr_MFC_ValvePos := 100.0; (* Max flow for flush *)
        rH2_MFC_ValvePos := 50.0;
        rCH4_MFC_ValvePos := 0.0; (* No carbon source yet *)
        
        tIgnitionTimer(IN:=TRUE, PT:=T#10S);
        IF tIgnitionTimer.Q THEN
            tIgnitionTimer(IN:=FALSE);
            iState := 20;
        END_IF;
        
    20: (* Plasma Ignition Phase *)
        rMicrowavePowerSetp := 1.5; (* 1.5 kW initial strike power *)
        tIgnitionTimer(IN:=TRUE, PT:=T#5S);
        
        IF rActualPlasmaDensity > 1.0E10 THEN (* Threshold for ignition *)
            bPlasmaIgnited := TRUE;
            tIgnitionTimer(IN:=FALSE);
            iState := 30;
        ELSIF tIgnitionTimer.Q THEN
            (* Ignition failed *)
            bAlarmActive := TRUE;
            iAlarmCode := 101; (* Failed to ignite *)
            iState := 999;
        END_IF;
        
    30: (* Growth Phase - Plasma Density and Temp Control *)
        (* Introduce Carbon source slowly *)
        rCH4_MFC_ValvePos := rRecipeCH4Flow;
        rH2_MFC_ValvePos := rRecipeH2Flow;
        rAr_MFC_ValvePos := rRecipeArFlow;
        
        (* Microwave Power PID for Plasma Density *)
        fbPlasmaPID(
            ENABLE := TRUE,
            SP := rTargetPlasmaDensity,
            PV := rActualPlasmaDensity,
            KP := Kp_Plasma,
            KI := Ki_Plasma,
            KD := Kd_Plasma,
            OUT => rMicrowavePowerSetp
        );
        
        (* Cascade Temperature Control for Substrate *)
        (* Master PID: Target Temp vs Actual Temp -> Required Cooling Capacity *)
        fbTempCascadePID(
            ENABLE := TRUE,
            SP := rTargetSubstrateTemp,
            PV := rActualSubstrateTemp,
            KP := Kp_TempMaster,
            KI := Ki_TempMaster,
            OUT => rTempPIDOutput
        );
        
        (* Slave PID: Required Cooling Capacity vs Coolant Inlet Temp -> Pump Speed *)
        fbCoolingPID(
            ENABLE := TRUE,
            SP := rTempPIDOutput,
            PV := rCoolantInletTemp,
            KP := Kp_CoolMaster,
            KI := Ki_CoolMaster,
            OUT => rCoolingPumpSpeed
        );
        
        (* Safety check during growth *)
        IF rActualSubstrateTemp > 1200.0 THEN
            bAlarmActive := TRUE;
            iAlarmCode := 202; (* Overtemp *)
            iState := 999;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 40;
        END_IF;
        
    40: (* Shutdown Sequence *)
        rCH4_MFC_ValvePos := 0.0;
        rMicrowavePowerSetp := rMicrowavePowerSetp * 0.9; (* Ramp down *)
        IF rMicrowavePowerSetp < 0.1 THEN
            rMicrowavePowerSetp := 0.0;
            bPlasmaIgnited := FALSE;
            iState := 0;
        END_IF;
        
    999: (* Fault State *)
        rMicrowavePowerSetp := 0.0;
        rCH4_MFC_ValvePos := 0.0;
        rH2_MFC_ValvePos := 100.0; (* Flush with H2 *)
        rAr_MFC_ValvePos := 100.0; (* Flush with Ar *)
        rCoolingPumpSpeed := 100.0; (* Max cooling *)
        bPlasmaIgnited := FALSE;
        
        IF NOT bEmergencyStop AND NOT bAlarmActive THEN
            iState := 0;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
print("done")
