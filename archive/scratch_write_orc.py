import json
import os

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

prompt = """You are acting as a Lead Geophysics Engineer. Evolve a basic fluid loop into a Massive Geothermal ORC (Organic Rankine Cycle) Controller. Technical Specs: 1. Isopentane working fluid vaporization pressure optimization based on brine temperature. 2. Radial inflow turbine speed and grid synchronization. 3. Air-cooled condenser fan speed arrays to maximize heat rejection in a desert climate. Append to synthetic_generation_v3_enterprise.jsonl."""

st_code = """
// ===================================================================================================
// MASSIVE GEOTHERMAL ORC (ORGANIC RANKINE CYCLE) CONTROLLER
// WORKING FLUID: ISOPENTANE
// IMPLEMENTATION: IEC 61131-3 STRUCTURED TEXT (ST)
// ===================================================================================================

TYPE 
    ORC_STATE : (
        SYS_STANDBY,
        SYS_WARMUP,
        SYS_START_FEEDPUMP,
        SYS_VAPORIZE,
        SYS_TURBINE_SPIN,
        SYS_GRID_SYNC,
        SYS_POWER_GEN,
        SYS_NORMAL_STOP,
        SYS_TRIP,
        SYS_EMERGENCY_SHUTDOWN
    );

    GRID_SYNC_STATUS : (
        SYNC_IDLE,
        SYNC_DETECTING,
        SYNC_ADJUSTING,
        SYNC_MATCHED,
        SYNC_CLOSED,
        SYNC_FAILED
    );
END_TYPE

// ===================================================================================================
// MAIN FUNCTION BLOCK: ORC_MASTER_CONTROLLER
// ===================================================================================================
FUNCTION_BLOCK FB_Geothermal_ORC_Controller
VAR_INPUT
    // Brine Inputs (Heat Source)
    rBrineInletTemp       : REAL; // [°C] Geothermal brine temperature
    rBrineFlowRate        : REAL; // [kg/s] Geothermal brine mass flow
    rBrinePressure        : REAL; // [bar] Brine wellhead pressure

    // Isopentane (Working Fluid) Inputs
    rIsopentaneVaporPress : REAL; // [bar] Current vaporization pressure
    rIsopentaneVaporTemp  : REAL; // [°C] Current vaporization temperature
    rIsopentaneCondTemp   : REAL; // [°C] Condensation temperature
    rIsopentaneFlow       : REAL; // [kg/s] Isopentane flow rate

    // Radial Turbine Inputs
    rTurbineSpeed         : REAL; // [RPM] Current turbine speed
    rTurbineVibration     : REAL; // [mm/s] Turbine casing vibration
    rTurbineBearingTemp   : REAL; // [°C] Turbine bearing temperature

    // Grid Inputs
    rGridFreq             : REAL; // [Hz] Grid frequency
    rGridVoltage          : REAL; // [kV] Grid voltage
    rGenVoltage           : REAL; // [kV] Generator terminal voltage
    rGenPhase             : REAL; // [rad] Phase angle difference

    // Desert Ambient Inputs
    rAmbientTemp          : REAL; // [°C] Desert air temperature
    rAmbientHumidity      : REAL; // [%] Relative humidity (usually low)

    // Control Signals
    bStartCommand         : BOOL; // Master start command
    bStopCommand          : BOOL; // Master normal stop command
    bEmergencyStop        : BOOL; // ESD Command
    bReset                : BOOL; // Alarm/Trip reset
END_VAR

VAR_OUTPUT
    // System Status
    eSystemState          : ORC_STATE := SYS_STANDBY;
    bSystemRunning        : BOOL;
    bTripAlarm            : BOOL;
    sStatusMessage        : STRING[80];

    // Valve Controls
    rBrineControlValvePos : REAL; // [%] 0-100 Control brine flow to heat exchanger
    rTurbineGovValvePos   : REAL; // [%] 0-100 Turbine governing/throttle valve
    rTurbineBypassValvePos: REAL; // [%] 0-100 Bypass valve to condenser

    // Pump Controls
    rFeedPumpSpeedRef     : REAL; // [%] 0-100 Isopentane feed pump VFD
    bFeedPumpRun          : BOOL;

    // Condenser Fan Arrays (Desert Climate Heat Rejection)
    rFanArray1_Speed      : REAL; // [%] VFD Fan Array 1
    rFanArray2_Speed      : REAL; // [%] VFD Fan Array 2
    rFanArray3_Speed      : REAL; // [%] VFD Fan Array 3
    rFanArray4_Speed      : REAL; // [%] VFD Fan Array 4

    // Grid Synchronization
    bBreakerClose         : BOOL; // Command to close main generator breaker
END_VAR

VAR
    // Internal States
    eSyncState            : GRID_SYNC_STATUS := SYNC_IDLE;
    
    // Process Targets
    rTargetVapPressure    : REAL; // Calculated optimum vaporization pressure
    rTargetTurbineSpeed   : REAL := 3000.0; // Nominal RPM for 50Hz (2-pole)
    
    // PID Controllers
    PID_VapPressure       : FB_PID; // Controls Feed Pump Speed
    PID_TurbineSpeed      : FB_PID; // Controls Turbine Governor Valve
    PID_CondenserPress    : FB_PID; // Controls Fan Array Speed

    // Timers
    TMR_Warmup            : TON;
    TMR_SyncTimeout       : TON;
    TMR_Purge             : TON;

    // Isopentane Optimization Constants
    // Target Pressure = A * T_brine^2 + B * T_brine + C (Empirical curve for Isopentane)
    c_Opt_A               : REAL := 0.0015;
    c_Opt_B               : REAL := 0.12;
    c_Opt_C               : REAL := -4.5;
    c_MaxVapPressure      : REAL := 35.0; // [bar] Isopentane critical pressure approx 33.7 bar, keep below subcritical
    
    // Desert Air Cooled Condenser (ACC) Management
    rFanStagingThresh     : REAL; // Dynamic threshold based on ambient
END_VAR

// ===================================================================================================
// 1. SAFETY & ESD MONITORING
// ===================================================================================================
IF bEmergencyStop OR (rTurbineVibration > 8.0) OR (rTurbineBearingTemp > 95.0) THEN
    eSystemState := SYS_EMERGENCY_SHUTDOWN;
END_IF;

IF eSystemState = SYS_EMERGENCY_SHUTDOWN THEN
    bSystemRunning         := FALSE;
    bTripAlarm             := TRUE;
    sStatusMessage         := 'ESD TRIGGERED: TURBINE/VIB/TEMP/MANUAL';
    
    rBrineControlValvePos  := 0.0;
    rTurbineGovValvePos    := 0.0;
    rTurbineBypassValvePos := 100.0; // Full bypass
    rFeedPumpSpeedRef      := 0.0;
    bFeedPumpRun           := FALSE;
    bBreakerClose          := FALSE;
    eSyncState             := SYNC_IDLE;
    
    // Run fans at 100% to rapidly cool down the inventory
    rFanArray1_Speed       := 100.0;
    rFanArray2_Speed       := 100.0;
    rFanArray3_Speed       := 100.0;
    rFanArray4_Speed       := 100.0;
    
    IF bReset AND NOT bEmergencyStop AND (rTurbineVibration < 4.0) THEN
        eSystemState := SYS_STANDBY;
        bTripAlarm   := FALSE;
    END_IF;
    RETURN;
END_IF;

// ===================================================================================================
// 2. ISOPENTANE VAPORIZATION PRESSURE OPTIMIZATION
// ===================================================================================================
// Sliding pressure control based on incoming Brine Temperature to maximize exergy efficiency
rTargetVapPressure := (c_Opt_A * rBrineInletTemp * rBrineInletTemp) + (c_Opt_B * rBrineInletTemp) + c_Opt_C;

// Saturate to safe operating boundaries
IF rTargetVapPressure > c_MaxVapPressure THEN
    rTargetVapPressure := c_MaxVapPressure;
ELSIF rTargetVapPressure < 5.0 THEN
    rTargetVapPressure := 5.0;
END_IF;

// Feed Pump PID - Maintains target vaporization pressure
PID_VapPressure(
    SetPoint := rTargetVapPressure,
    ProcessVariable := rIsopentaneVaporPress,
    Kp := 2.5,
    Ki := 0.4,
    Kd := 0.1,
    OutputMax := 100.0,
    OutputMin := 20.0 // Min safe VFD speed
);

// ===================================================================================================
// 3. AIR-COOLED CONDENSER (ACC) OPTIMIZATION FOR DESERT CLIMATE
// ===================================================================================================
// In desert climates, daytime T_amb can exceed 45°C. Fan energy consumption is parasitic.
// Objective: Minimize fan speed while keeping condensing pressure low enough for turbine delta-P.
// We modulate fans in staggered arrays to prevent acoustic resonance and reduce inrush.

// Determine Base Fan Demand from Ambient
rFanStagingThresh := rAmbientTemp * 1.5 + (rIsopentaneCondTemp - 35.0) * 2.0;

IF rFanStagingThresh > 100.0 THEN rFanStagingThresh := 100.0; END_IF;
IF rFanStagingThresh < 0.0 THEN rFanStagingThresh := 0.0; END_IF;

// Staggered Fan Array logic
IF rFanStagingThresh < 25.0 THEN
    rFanArray1_Speed := rFanStagingThresh * 4.0;
    rFanArray2_Speed := 0.0; rFanArray3_Speed := 0.0; rFanArray4_Speed := 0.0;
ELSIF rFanStagingThresh < 50.0 THEN
    rFanArray1_Speed := 100.0;
    rFanArray2_Speed := (rFanStagingThresh - 25.0) * 4.0;
    rFanArray3_Speed := 0.0; rFanArray4_Speed := 0.0;
ELSIF rFanStagingThresh < 75.0 THEN
    rFanArray1_Speed := 100.0; rFanArray2_Speed := 100.0;
    rFanArray3_Speed := (rFanStagingThresh - 50.0) * 4.0;
    rFanArray4_Speed := 0.0;
ELSE
    rFanArray1_Speed := 100.0; rFanArray2_Speed := 100.0; rFanArray3_Speed := 100.0;
    rFanArray4_Speed := (rFanStagingThresh - 75.0) * 4.0;
END_IF;

// ===================================================================================================
// 4. RADIAL INFLOW TURBINE & SYNCHRONIZATION
// ===================================================================================================
// Turbine speed PID controls governor valve to match grid frequency initially
PID_TurbineSpeed(
    SetPoint := rTargetTurbineSpeed,
    ProcessVariable := rTurbineSpeed,
    Kp := 1.2,
    Ki := 0.5,
    Kd := 0.05,
    OutputMax := 100.0,
    OutputMin := 0.0
);

// Synchronization Logic
CASE eSyncState OF
    SYNC_IDLE:
        bBreakerClose := FALSE;
        IF eSystemState = SYS_GRID_SYNC THEN
            eSyncState := SYNC_DETECTING;
        END_IF;
        
    SYNC_DETECTING:
        // Adjust target speed slightly to create slip frequency
        rTargetTurbineSpeed := (rGridFreq * 60.0) + 2.0; // +2 RPM slip
        eSyncState := SYNC_ADJUSTING;
        TMR_SyncTimeout(IN:=TRUE, PT:=T#120s);
        
    SYNC_ADJUSTING:
        // Wait for voltage matching and phase angle < 5 degrees (0.087 rad)
        IF ABS(rGenVoltage - rGridVoltage) < 0.5 AND ABS(rGenPhase) < 0.087 THEN
            eSyncState := SYNC_MATCHED;
        END_IF;
        
        IF TMR_SyncTimeout.Q THEN
            eSyncState := SYNC_FAILED;
        END_IF;
        
    SYNC_MATCHED:
        bBreakerClose := TRUE; // Boom, we are on the grid
        eSyncState := SYNC_CLOSED;
        
    SYNC_CLOSED:
        // Breaker is closed. Turbine speed is now locked to grid frequency.
        // Switch control mode from Speed Control to Power/Load Control (Droop)
        // (Handled in STATE MACHINE)
        
    SYNC_FAILED:
        // Sync took too long, trip turbine to avoid islanding issues
        eSystemState := SYS_TRIP;
END_CASE;

// ===================================================================================================
// 5. MASTER STATE MACHINE
// ===================================================================================================
CASE eSystemState OF
    SYS_STANDBY:
        sStatusMessage := 'STANDBY: Ready to Start';
        rBrineControlValvePos  := 0.0;
        rTurbineGovValvePos    := 0.0;
        rTurbineBypassValvePos := 100.0;
        bFeedPumpRun           := FALSE;
        IF bStartCommand THEN
            eSystemState := SYS_WARMUP;
        END_IF;

    SYS_WARMUP:
        sStatusMessage := 'WARMUP: Preheating Vaporizer';
        rBrineControlValvePos := 20.0; // Crack open brine
        TMR_Warmup(IN:=TRUE, PT:=T#300s);
        IF TMR_Warmup.Q THEN
            eSystemState := SYS_START_FEEDPUMP;
            TMR_Warmup(IN:=FALSE);
        END_IF;

    SYS_START_FEEDPUMP:
        sStatusMessage := 'PUMPING: Establishing Isopentane Circulation';
        bFeedPumpRun := TRUE;
        rFeedPumpSpeedRef := PID_VapPressure.Output;
        IF rIsopentaneFlow > 5.0 THEN
            eSystemState := SYS_VAPORIZE;
        END_IF;

    SYS_VAPORIZE:
        sStatusMessage := 'VAPORIZING: Pressurizing System';
        rBrineControlValvePos := 80.0;
        rFeedPumpSpeedRef := PID_VapPressure.Output;
        // Wait for optimized target pressure
        IF rIsopentaneVaporPress >= (rTargetVapPressure * 0.95) THEN
            eSystemState := SYS_TURBINE_SPIN;
        END_IF;

    SYS_TURBINE_SPIN:
        sStatusMessage := 'TURBINE SPIN: Accelerating to Rated Speed';
        rTurbineBypassValvePos := 100.0 - PID_TurbineSpeed.Output; 
        rTurbineGovValvePos    := PID_TurbineSpeed.Output;
        rFeedPumpSpeedRef      := PID_VapPressure.Output;
        IF ABS(rTurbineSpeed - rTargetTurbineSpeed) < 10.0 THEN
            eSystemState := SYS_GRID_SYNC;
        END_IF;

    SYS_GRID_SYNC:
        sStatusMessage := 'SYNCHRONIZING: Matching Grid Parameters';
        rTurbineGovValvePos := PID_TurbineSpeed.Output; // Governor controls sync speed
        IF eSyncState = SYNC_CLOSED THEN
            eSystemState := SYS_POWER_GEN;
        END_IF;

    SYS_POWER_GEN:
        sStatusMessage := 'POWER GEN: Synchronized & Exporting Power';
        bSystemRunning := TRUE;
        // In grid-tied mode, governor valve modulates based on MW setpoint/sliding pressure
        // For ORC, we often run base-load (Valve 100% open, driven by Vaporizer production)
        rTurbineGovValvePos    := 100.0;
        rTurbineBypassValvePos := 0.0;
        rBrineControlValvePos  := 100.0; // Maximize exergy extraction
        rFeedPumpSpeedRef      := PID_VapPressure.Output; // Maintain optimized pressure

        IF bStopCommand THEN
            eSystemState := SYS_NORMAL_STOP;
        END_IF;

    SYS_NORMAL_STOP:
        sStatusMessage := 'STOPPING: Unloading Turbine';
        rBrineControlValvePos := 0.0;
        rTurbineGovValvePos   := 0.0;
        bBreakerClose         := FALSE; // Open breaker
        IF rTurbineSpeed < 100.0 THEN
            bFeedPumpRun := FALSE;
            rFeedPumpSpeedRef := 0.0;
            eSystemState := SYS_STANDBY;
        END_IF;

    SYS_TRIP:
        sStatusMessage := 'SYSTEM TRIP: Abnormal Condition';
        bSystemRunning := FALSE;
        rTurbineGovValvePos := 0.0;
        rTurbineBypassValvePos := 100.0;
        bBreakerClose := FALSE;
        IF bReset THEN
            eSystemState := SYS_STANDBY;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
"""

response = f"""**Massive Geothermal ORC (Organic Rankine Cycle) Controller**

### **Design Architecture**
This controller manages an ORC system utilizing **Isopentane** as the working fluid, extracting heat from geothermal brine. Key optimization routines include:
1.  **Sliding Pressure Vaporization**: Dynamically calculates the optimum Isopentane vaporization pressure based on incoming brine temperature. This maximizes exergy efficiency across fluctuating wellhead temperatures.
2.  **Grid Synchronization**: Employs slip-frequency adjustments to align the generator's phase angle and voltage with the electrical grid before engaging the breaker.
3.  **Desert Air-Cooled Condenser (ACC) Management**: Staggers VFD fan arrays based on extreme ambient temperatures, balancing parasitic power draw against necessary heat rejection to maintain the turbine's expansion delta-P.

### **IEC 61131-3 ST Implementation**
```iecst
{st_code}
```

### **Critical Control Methodologies**
*   **VFD Array Staging (Desert Logic)**: Parasitic losses in an ACC can destroy the net power output of an ORC plant, especially at 45°C+ ambient. The `rFanStagingThresh` calculates a unified demand, which is split linearly across four independent fan arrays to prevent inrush transients and acoustic resonance, maintaining the lowest possible condensing temperature.
*   **Governor and Bypass Coordination**: During startup and synchronizing (`SYS_TURBINE_SPIN`), the governor and bypass valves operate in a complementary split-range to smoothly inject vapor into the radial turbine without dropping header pressure.
*   **Target Pressure Mapping**: The polynomial equation `(A * T^2 + B * T + C)` acts as the empirical baseline for Isopentane's optimal saturation dome tracking. The feed pump PID directly follows this setpoint to maintain a stable, saturated vapor phase just below critical pressure limits (35 bar max)."""

json_obj = {
    "messages": [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "assistant",
            "content": response
        }
    ]
}

with open(target_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(json_obj) + "\\n")

print("Successfully appended to JSONL.")
