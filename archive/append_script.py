import json

def append_synthetic_data():
    prompt = "You are acting as a Lead Particle Physics Engineer (e.g., CERN). Evolve a basic cooling block into a Large Hadron Collider (LHC) Superfluid Helium Cryogenics Controller. Technical Specs: 1. 1.9 Kelvin superfluid helium cold-compressor cascade. 2. Beam-loss monitor (BLM) quench protection heater triggering. 3. Magnet current lead boil-off regulation."
    
    assistant_response = """(*
=============================================================================
LHC SUPERFLUID HELIUM CRYOGENICS CONTROLLER (1.9K CASCADE)
IEC 61131-3 Implementation
=============================================================================
Engineer: Lead Particle Physics Engineer (CERN)
System: Main Ring Superconducting Magnet Cryo-System

Core Subsystems:
1. 1.9K Superfluid Helium Cold-Compressor Cascade
2. Beam-Loss Monitor (BLM) Quench Protection & Heater Triggering
3. Magnet Current Lead Boil-Off Regulation
=============================================================================
*)

TYPE E_CryoState :
(
    CRYO_WARM_STANDBY := 0,
    CRYO_COOLDOWN_4_5K := 1,
    CRYO_PUMPDOWN_1_9K := 2,
    CRYO_NOMINAL_SUPERFLUID := 3,
    CRYO_QUENCH_RECOVERY := 4,
    CRYO_FAULT := 99
);
END_TYPE

TYPE ST_ColdCompressor :
STRUCT
    SpeedSetPoint   : REAL; (* RPM *)
    ActualSpeed     : REAL; (* RPM *)
    InletPressure   : REAL; (* mbar *)
    OutletPressure  : REAL; (* mbar *)
    BearingTemp     : REAL; (* K *)
    Vibration       : REAL; (* mm/s *)
    TripInterlock   : BOOL;
END_STRUCT
END_TYPE

TYPE ST_BLM_Sensor :
STRUCT
    LossRate        : REAL; (* Gy/s *)
    IntegratedLoss  : REAL; (* Gy *)
    ThresholdQuench : REAL; (* Gy/s *)
    ThresholdWarn   : REAL; (* Gy/s *)
    QuenchDetected  : BOOL;
END_STRUCT
END_TYPE

TYPE ST_CurrentLead :
STRUCT
    CurrentLevel    : REAL; (* kA *)
    VoltageDrop     : REAL; (* mV *)
    MassFlowActual  : REAL; (* g/s *)
    TempTop         : REAL; (* K *)
    TempBottom      : REAL; (* K *)
    ValvePosition   : REAL; (* % *)
END_STRUCT
END_TYPE

(* ========================================================================= *)
(* FUNCTION BLOCK: Cold Compressor Cascade Controller                        *)
(* ========================================================================= *)
FUNCTION_BLOCK FB_ColdCompressorCascade
VAR_INPUT
    Enable          : BOOL;
    TargetTemp      : REAL := 1.9; (* Target temperature in Kelvin *)
    HeliumBathTemp  : REAL;
    BathPressure    : REAL; (* mbar, nominal 16 mbar for 1.9K *)
END_VAR
VAR_OUTPUT
    CascadeActive   : BOOL;
    Stable1_9K      : BOOL;
    TotalPower      : REAL;
    FaultDetected   : BOOL;
END_VAR
VAR
    CC1, CC2, CC3, CC4 : ST_ColdCompressor;
    PID_Pressure    : FB_PID; (* Assuming external standard PID *)
    PressureError   : REAL;
    CascadeSeqStep  : INT := 0;
    SpeedRamp       : REAL := 0.0;
END_VAR

    (* Cascade regulation based on saturation pressure (16 mbar = ~1.9K) *)
    PID_Pressure(
        xSet := 16.0,
        xAct := BathPressure,
        Kp := 5.5,
        Ti := 120.0,
        Td := 5.0,
        LimLow := 0.0,
        LimHigh := 100.0,
        bReverseActing := TRUE
    );

    IF Enable THEN
        CASE CascadeSeqStep OF
            0: (* Standby / Spin-up check *)
                CC1.SpeedSetPoint := 0;
                IF BathPressure < 1000.0 THEN CascadeSeqStep := 1; END_IF;
            1: (* CC1 Start *)
                CC1.SpeedSetPoint := 20000.0; (* Base RPM *)
                IF CC1.ActualSpeed > 18000.0 THEN CascadeSeqStep := 2; END_IF;
            2: (* Sequence CC2 to CC4 *)
                CC2.SpeedSetPoint := 35000.0;
                CC3.SpeedSetPoint := 45000.0;
                CC4.SpeedSetPoint := 60000.0;
                IF CC4.ActualSpeed > 55000.0 THEN CascadeSeqStep := 3; END_IF;
            3: (* Active Regulation *)
                SpeedRamp := PID_Pressure.Y;
                (* Distribute load across stages proportionally *)
                CC1.SpeedSetPoint := 20000.0 + (SpeedRamp * 100.0);
                CC2.SpeedSetPoint := 35000.0 + (SpeedRamp * 150.0);
                CC3.SpeedSetPoint := 45000.0 + (SpeedRamp * 200.0);
                CC4.SpeedSetPoint := 60000.0 + (SpeedRamp * 300.0);
                
                CascadeActive := TRUE;
                IF (HeliumBathTemp <= 1.92 AND HeliumBathTemp >= 1.88) THEN
                    Stable1_9K := TRUE;
                ELSE
                    Stable1_9K := FALSE;
                END_IF;
        END_CASE;
    ELSE
        CascadeSeqStep := 0;
        CascadeActive := FALSE;
        Stable1_9K := FALSE;
        CC1.SpeedSetPoint := 0;
        CC2.SpeedSetPoint := 0;
        CC3.SpeedSetPoint := 0;
        CC4.SpeedSetPoint := 0;
    END_IF;

    (* Bearing Temp Interlocks *)
    IF CC1.BearingTemp > 80.0 OR CC4.Vibration > 2.5 THEN
        FaultDetected := TRUE;
        CascadeActive := FALSE;
    END_IF;
END_FUNCTION_BLOCK

(* ========================================================================= *)
(* FUNCTION BLOCK: Quench Protection & BLM Trigger                           *)
(* ========================================================================= *)
FUNCTION_BLOCK FB_QuenchProtectionSystem
VAR_INPUT
    BLM_Sensors     : ARRAY[1..16] OF ST_BLM_Sensor;
    MagnetVoltage   : REAL; (* mV *)
    MagnetCurrent   : REAL; (* kA, nominal 13 kA *)
    Reset           : BOOL;
END_VAR
VAR_OUTPUT
    QuenchFired     : BOOL;
    HeaterTrigger1  : BOOL;
    HeaterTrigger2  : BOOL;
    DumpResistorCmd : BOOL;
    EmergencyStop   : BOOL;
END_VAR
VAR
    i : INT;
    DerivativeV     : REAL;
    LastV           : REAL;
    ResistiveZone   : BOOL;
END_VAR
    
    IF Reset THEN
        QuenchFired := FALSE;
        HeaterTrigger1 := FALSE; HeaterTrigger2 := FALSE;
        DumpResistorCmd := FALSE;
        EmergencyStop := FALSE;
    END_IF;

    (* 1. Beam Loss Monitor Polling *)
    FOR i := 1 TO 16 DO
        IF BLM_Sensors[i].LossRate > BLM_Sensors[i].ThresholdQuench THEN
            BLM_Sensors[i].QuenchDetected := TRUE;
            EmergencyStop := TRUE;
        END_IF;
    END_FOR;

    (* 2. Magnet Voltage Differential dV/dt (Resistive Zone Detection) *)
    DerivativeV := (MagnetVoltage - LastV) / 0.01; (* Assume 10ms task *)
    LastV := MagnetVoltage;
    
    (* If unexplained resistive voltage appears, super-conductor quenched *)
    IF (MagnetVoltage > 100.0) AND (DerivativeV > 50.0) AND (MagnetCurrent > 1.0) THEN
        ResistiveZone := TRUE;
    END_IF;

    (* 3. Trigger Quench Heaters to spread quench volume & prevent localized melting *)
    IF EmergencyStop OR ResistiveZone THEN
        QuenchFired := TRUE;
        HeaterTrigger1 := TRUE; (* Primary capacitor bank *)
        HeaterTrigger2 := TRUE; (* Redundant capacitor bank *)
        DumpResistorCmd := TRUE; (* Route 13kA to external dump resistors *)
    END_IF;
END_FUNCTION_BLOCK

(* ========================================================================= *)
(* FUNCTION BLOCK: Current Lead Boil-off Regulator                           *)
(* ========================================================================= *)
FUNCTION_BLOCK FB_CurrentLeadRegulator
VAR_INPUT
    LeadState       : ST_CurrentLead;
END_VAR
VAR_OUTPUT
    UpdatedLead     : ST_CurrentLead;
END_VAR
VAR
    PID_Boiloff     : FB_PID;
    TargetMassFlow  : REAL;
END_VAR

    (* Calculate required cooling based on electrical heating (I^2 * R effective) *)
    (* Rule of thumb: ~0.05 g/s per kA for optimized HTS leads *)
    TargetMassFlow := LeadState.CurrentLevel * 0.052; 
    
    (* Override mass flow if warm end gets too hot (> 293K) *)
    IF LeadState.TempTop > 295.0 THEN
        TargetMassFlow := TargetMassFlow * 1.5;
    END_IF;

    PID_Boiloff(
        xSet := TargetMassFlow,
        xAct := LeadState.MassFlowActual,
        Kp := 2.5,
        Ti := 30.0,
        LimLow := 5.0,  (* Minimum flow to prevent frost *)
        LimHigh := 100.0
    );

    UpdatedLead := LeadState;
    UpdatedLead.ValvePosition := PID_Boiloff.Y;
END_FUNCTION_BLOCK

(* ========================================================================= *)
(* MAIN PROGRAM: LHC Cryogenics Supervisor                                   *)
(* ========================================================================= *)
PROGRAM MAIN_LHC_CRYO
VAR
    SysState        : E_CryoState := CRYO_WARM_STANDBY;
    
    ColdCascade     : FB_ColdCompressorCascade;
    QuenchProtect   : FB_QuenchProtectionSystem;
    LeadRegulator   : FB_CurrentLeadRegulator;
    
    GlobalBathTemp  : REAL := 1.9;
    GlobalBathPres  : REAL := 16.0;
    
    BLM_Array       : ARRAY[1..16] OF ST_BLM_Sensor;
    DipoleLead      : ST_CurrentLead;
    
    MasterStart     : BOOL := FALSE;
    MasterReset     : BOOL := FALSE;
END_VAR

    (* Execute Cascade *)
    ColdCascade(
        Enable := (SysState = CRYO_PUMPDOWN_1_9K OR SysState = CRYO_NOMINAL_SUPERFLUID),
        HeliumBathTemp := GlobalBathTemp,
        BathPressure := GlobalBathPres
    );
    
    IF ColdCascade.Stable1_9K THEN
        SysState := CRYO_NOMINAL_SUPERFLUID;
    END_IF;
    
    (* Execute Quench Protection *)
    QuenchProtect(
        BLM_Sensors := BLM_Array,
        MagnetVoltage := DipoleLead.VoltageDrop,
        MagnetCurrent := DipoleLead.CurrentLevel,
        Reset := MasterReset
    );
    
    IF QuenchProtect.QuenchFired THEN
        SysState := CRYO_QUENCH_RECOVERY;
        ColdCascade.Enable := FALSE; (* Stop compressors on massive heat load *)
    END_IF;
    
    (* Execute Boil-Off Regulation for 13kA Leads *)
    DipoleLead.CurrentLevel := 11.8; (* Simulated operating current *)
    LeadRegulator(LeadState := DipoleLead);
    DipoleLead := LeadRegulator.UpdatedLead;

END_PROGRAM
"""
    
    data = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_response}
        ]
    }
    
    file_path = "c:/Users/majip/Downloads/LLM REASEARCH/data/synthetic_generation_v3_enterprise.jsonl"
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\\n")
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    append_synthetic_data()
