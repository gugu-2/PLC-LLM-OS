import json, uuid, os

prompt = "Invent a highly complex control scenario for this domain (e.g., cocoa butter beta-crystal structure staging, scraped-surface heat exchanger shear stress, and thermal cascade loops). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."

st_code = """```iec-st
FUNCTION_BLOCK FB_AdvancedChocolateTempering
TITLE = 'Advanced Commercial Chocolate Tempering Control'
VERSION : '2.1'

VAR_INPUT
    Enable : BOOL; // System enable
    MassFlowRate : REAL; // kg/h of chocolate mass
    InletTemp : REAL; // Incoming chocolate temperature (deg C)
    TargetViscosity : REAL; // Target viscosity (Pa.s)
    AgitatorSpeed_SP : REAL; // Setpoint for scraped-surface agitator (RPM)
    CoolingWaterTemp_In : REAL; // Chilled water temperature
    HeatingWaterTemp_In : REAL; // Hot water temperature
    EmergencyStop : BOOL; // E-Stop condition
END_VAR

VAR_OUTPUT
    AgitatorSpeed_CV : REAL; // Command to agitator VFD (RPM)
    CoolingValve_CV : REAL; // 0-100% cooling valve position
    HeatingValve_CV : REAL; // 0-100% heating valve position
    Zone1_Temp : REAL; // Decrystallization zone actual temp
    Zone2_Temp : REAL; // Nucleation zone actual temp
    Zone3_Temp : REAL; // Crystal growth zone actual temp
    ShearStressLevel : REAL; // Calculated shear stress on chocolate mass
    BetaCrystalIndex : REAL; // Estimated Form V beta crystal concentration
    SystemState : INT; // 0=Off, 1=Melt, 2=Cool, 3=Temper, 4=Fault
    ReadyForExtrusion : BOOL; // True when perfectly tempered
    Alarms : DWORD; // Bitfield of active alarms
END_VAR

VAR
    // Internal State
    StateTimer : TIME;
    LastUpdateTime : TIME;
    
    // PID Controllers (Simulated structure)
    PID_Zone1_Melt_SP : REAL := 45.0;
    PID_Zone2_Nucl_SP : REAL := 28.5;
    PID_Zone3_Tcmp_SP : REAL := 31.0;

    PID_Zone1_Error : REAL;
    PID_Zone2_Error : REAL;
    PID_Zone3_Error : REAL;
    
    PID_Zone1_Integral : REAL;
    PID_Zone2_Integral : REAL;
    PID_Zone3_Integral : REAL;

    PID_Kp : REAL := 2.5;
    PID_Ki : REAL := 0.1;
    PID_Kd : REAL := 0.5;

    // Physical parameters
    SpecificHeatChoc : REAL := 1.6; // kJ/kg.K
    DensityChoc : REAL := 1300.0; // kg/m3

    // Shear calculation constants
    RotorRadius : REAL := 0.15; // meters
    GapSize : REAL := 0.005; // meters
END_VAR

// Safety and Enable Interlocks
IF EmergencyStop THEN
    SystemState := 4;
    AgitatorSpeed_CV := 0.0;
    CoolingValve_CV := 100.0; 
    HeatingValve_CV := 0.0;
    ReadyForExtrusion := FALSE;
    Alarms := Alarms OR 16#0001; 
    RETURN;
END_IF;

IF NOT Enable THEN
    SystemState := 0;
    AgitatorSpeed_CV := 0.0;
    CoolingValve_CV := 0.0;
    HeatingValve_CV := 0.0;
    ReadyForExtrusion := FALSE;
    RETURN;
END_IF;

// Shear Stress Calculation Model
// tau = viscosity * shear rate
// shear rate = velocity / gap size
IF TargetViscosity > 0.0 THEN
    ShearStressLevel := TargetViscosity * ((AgitatorSpeed_SP * 6.28318 * RotorRadius / 60.0) / GapSize);
ELSE
    ShearStressLevel := 0.0;
END_IF;

// Shear limit alarm condition
IF ShearStressLevel > 1500.0 THEN
    Alarms := Alarms OR 16#0002;
ELSE
    Alarms := Alarms AND (NOT 16#0002);
END_IF;

// Cascade State Machine for Multi-Zone Tempering
CASE SystemState OF
    0: // Off
        IF Enable THEN
            SystemState := 1;
        END_IF;

    1: // Zone 1: Decrystallization (Melting Form I-VI)
        PID_Zone1_Error := PID_Zone1_Melt_SP - InletTemp;
        PID_Zone1_Integral := PID_Zone1_Integral + (PID_Zone1_Error * 0.1); // Assuming 100ms cycle
        HeatingValve_CV := (PID_Kp * PID_Zone1_Error) + (PID_Ki * PID_Zone1_Integral);
        
        // Limit CV
        IF HeatingValve_CV > 100.0 THEN HeatingValve_CV := 100.0; END_IF;
        IF HeatingValve_CV < 0.0 THEN HeatingValve_CV := 0.0; END_IF;
        
        AgitatorSpeed_CV := AgitatorSpeed_SP * 0.4; // Low shear for initial melt

        // Transition to Nucleation when fully melted
        IF InletTemp >= 44.0 THEN
            SystemState := 2;
        END_IF;

    2: // Zone 2: Nucleation (Chilling to form beta and unstable crystals)
        PID_Zone2_Error := Zone2_Temp - PID_Zone2_Nucl_SP; // Reverse acting for cooling
        PID_Zone2_Integral := PID_Zone2_Integral + (PID_Zone2_Error * 0.1);
        CoolingValve_CV := (PID_Kp * PID_Zone2_Error) + (PID_Ki * PID_Zone2_Integral);
        
        // Limit CV
        IF CoolingValve_CV > 100.0 THEN CoolingValve_CV := 100.0; END_IF;
        IF CoolingValve_CV < 0.0 THEN CoolingValve_CV := 0.0; END_IF;
        
        AgitatorSpeed_CV := AgitatorSpeed_SP; // High shear to promote crystallization

        // Empirical crystallization estimation based on sustained shear & temp
        BetaCrystalIndex := BetaCrystalIndex + (ShearStressLevel * 0.00005);
        IF BetaCrystalIndex > 1.0 THEN BetaCrystalIndex := 1.0; END_IF;

        IF Zone2_Temp <= (PID_Zone2_Nucl_SP + 0.5) AND BetaCrystalIndex > 0.5 THEN
            SystemState := 3;
        END_IF;

    3: // Zone 3: Tempering / Crystal Growth (Melt out unstable forms)
        PID_Zone3_Error := PID_Zone3_Tcmp_SP - Zone3_Temp;
        PID_Zone3_Integral := PID_Zone3_Integral + (PID_Zone3_Error * 0.1);
        HeatingValve_CV := (PID_Kp * PID_Zone3_Error) + (PID_Ki * PID_Zone3_Integral);
        
        IF HeatingValve_CV > 100.0 THEN HeatingValve_CV := 100.0; END_IF;
        IF HeatingValve_CV < 0.0 THEN HeatingValve_CV := 0.0; END_IF;
        CoolingValve_CV := 0.0; 
        
        AgitatorSpeed_CV := AgitatorSpeed_SP * 0.8;

        IF BetaCrystalIndex > 0.85 AND Zone3_Temp >= (PID_Zone3_Tcmp_SP - 0.2) THEN
            ReadyForExtrusion := TRUE;
        ELSE
            ReadyForExtrusion := FALSE;
        END_IF;

    4: // Fault / E-Stop
        ReadyForExtrusion := FALSE;
        AgitatorSpeed_CV := 0.0;
        HeatingValve_CV := 0.0;
        CoolingValve_CV := 100.0;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)
