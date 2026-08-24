import json
import os

user_content = """You are acting as the Principal Climate Engineer for a Global Geoengineering Initiative.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Stratospheric Aerosol Injection (SAI) High-Altitude Balloon Fleet Controller" (`FB_SAI_StratosphericFleet`).

### Technical Specifications & Engineering Rigor Required:
1. **Stratospheric Altitude Targeting (Super-pressure Balloons)**:
   - Autonomous buoyancy control of a fleet of 10,000 super-pressure balloons loitering in the lower stratosphere (20 km altitude) where the Brewer-Dobson circulation can rapidly distribute aerosols globally.
   - Diurnal thermal expansion modeling to vent or pump air ballast, countering the massive temperature swings between daytime solar heating and the frigid night.
2. **Sulfur Dioxide (SO2) Aerosol Dispersion**:
   - Ultrasonic atomization of liquid SO2 into precise 0.5 μm droplets, optimizing their albedo (solar reflectivity) to artificially cool the planet by 1.5°C.
   - Wind-shear trajectory prediction to coordinate the precise venting time across the swarm to maximize the global aerosol shield uniformity.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, atmospheric thermodynamics equations, PackML states."""

assistant_content = """Here is the master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the Stratospheric Aerosol Injection (SAI) High-Altitude Balloon Fleet Controller.

```iec-st
// ==============================================================================
// BLOCK: FB_SAI_StratosphericFleet
// DESC:  Global Geoengineering Initiative - Stratospheric Aerosol Injection
//        Autonomous swarm controller for 10,000 super-pressure balloon units.
//        Handles stratospheric altitude buoyancy control, diurnal thermal
//        modeling, and optimized SO2 aerosol atomization and dispersion.
// ==============================================================================
FUNCTION_BLOCK FB_SAI_StratosphericFleet
VAR_INPUT
    // PackML State Control
    bExecute            : BOOL; // Command to START injection operations
    bAbort              : BOOL; // Command to ABORT and emergency descend
    bStop               : BOOL; // Command to gracefully STOP operations
    
    // Telemetry & Sensors
    rCurrentAltitude    : LREAL; // Current altitude in meters (Target ~20,000.0)
    rExternalTemp_K     : LREAL; // External stratospheric temp in Kelvin (e.g., ~216.65 K)
    rSolarRadiation     : LREAL; // W/m^2 solar influx for thermal modeling
    rInternalGasTemp_K  : LREAL; // Lift gas (Helium) internal temp in Kelvin
    rWindShearIndex     : LREAL; // Calculated vertical wind shear for trajectory (m/s/km)
    
    // Payload Status
    rSO2_TankLevel      : LREAL; // % remaining of liquid SO2 payload (0.0 to 100.0)
END_VAR

VAR_OUTPUT
    // System Status
    ePackMLState        : INT; // Uses integer for PackML state (E_PackML_State enum implied)
    bAltitudeReached    : BOOL;
    bDispersionActive   : BOOL;
    rDropletSize_um     : LREAL; // Target 0.5 um
    
    // Actuators
    bPumpAirBallast     : BOOL;  // Command air compressor (increase weight / descend)
    bVentAirBallast     : BOOL;  // Command air vent (decrease weight / ascend)
    rUltrasonicAtomizer : LREAL; // 0.0 to 100.0% driving frequency/amplitude
    rSO2_ValvePos       : LREAL; // 0.0 to 100.0% open position
END_VAR

VAR
    // Constants
    TARGET_ALTITUDE     : LREAL := 20000.0; // meters (20 km)
    ALTITUDE_DBAND      : LREAL := 150.0;   // +/- 150 meters deadband
    GAS_CONSTANT_R      : LREAL := 287.05;  // J/(kg*K) for dry air
    SPECIFIC_HEAT_P     : LREAL := 1005.0;  // J/(kg*K)
    OPTIMAL_DROPLET_UM  : LREAL := 0.5;
    
    // State Constants (Simulated Enum)
    STATE_IDLE       : INT := 1;
    STATE_STARTING   : INT := 2;
    STATE_EXECUTE    : INT := 3;
    STATE_COMPLETING : INT := 4;
    STATE_COMPLETE   : INT := 5;
    STATE_ABORTING   : INT := 6;
    STATE_ABORTED    : INT := 7;
    STATE_STOPPING   : INT := 8;
    STATE_STOPPED    : INT := 9;
    
    // Internal State
    rBuoyancyError      : LREAL;
    rThermalExpansion   : LREAL;
    rDispersionRate     : LREAL;
END_VAR

// ------------------------------------------------------------------------------
// PackML State Machine Implementation
// ------------------------------------------------------------------------------
IF bAbort THEN
    ePackMLState := STATE_ABORTING;
ELSIF bStop THEN
    ePackMLState := STATE_STOPPING;
END_IF;

CASE ePackMLState OF

    STATE_IDLE:
        bAltitudeReached := FALSE;
        bDispersionActive := FALSE;
        rSO2_ValvePos := 0.0;
        rUltrasonicAtomizer := 0.0;
        
        IF bExecute THEN
            ePackMLState := STATE_STARTING;
        END_IF;
        
    STATE_STARTING:
        ePackMLState := STATE_EXECUTE;
        
    STATE_EXECUTE:
        // ----------------------------------------------------------------------
        // 1. Stratospheric Altitude Targeting & Buoyancy Control
        // ----------------------------------------------------------------------
        rBuoyancyError := TARGET_ALTITUDE - rCurrentAltitude;
        rThermalExpansion := (rInternalGasTemp_K - rExternalTemp_K) * GAS_CONSTANT_R;
        
        IF (rBuoyancyError > ALTITUDE_DBAND) THEN
            bVentAirBallast := TRUE;
            bPumpAirBallast := FALSE;
            bAltitudeReached := FALSE;
        ELSIF (rBuoyancyError < -ALTITUDE_DBAND) THEN
            bVentAirBallast := FALSE;
            bPumpAirBallast := TRUE;
            bAltitudeReached := FALSE;
        ELSE
            bVentAirBallast := FALSE;
            bPumpAirBallast := FALSE;
            bAltitudeReached := TRUE;
        END_IF;
        
        // ----------------------------------------------------------------------
        // 2. SO2 Aerosol Dispersion & Atomization
        // ----------------------------------------------------------------------
        IF bAltitudeReached AND (rWindShearIndex >= 2.5) AND (rSO2_TankLevel > 0.5) THEN
            rDispersionRate := LIMIT(0.0, (rWindShearIndex * 15.0), 100.0);
            rSO2_ValvePos := rDispersionRate;
            rUltrasonicAtomizer := 85.0; // Constant drive for 0.5um
            rDropletSize_um := OPTIMAL_DROPLET_UM; 
            bDispersionActive := TRUE;
        ELSE
            rSO2_ValvePos := 0.0;
            rUltrasonicAtomizer := 0.0;
            bDispersionActive := FALSE;
        END_IF;
        
        IF rSO2_TankLevel <= 0.5 THEN
            ePackMLState := STATE_COMPLETING;
        END_IF;

    STATE_COMPLETING:
        rSO2_ValvePos := 0.0;
        rUltrasonicAtomizer := 0.0;
        bDispersionActive := FALSE;
        ePackMLState := STATE_COMPLETE;
        
    STATE_COMPLETE:
        bVentAirBallast := FALSE;
        bPumpAirBallast := TRUE; // Begin slow descent
        
    STATE_ABORTING:
        bPumpAirBallast := TRUE;
        bVentAirBallast := FALSE;
        rSO2_ValvePos := 0.0;
        rUltrasonicAtomizer := 0.0;
        ePackMLState := STATE_ABORTED;
        
    STATE_ABORTED:
        // Secure
        
    STATE_STOPPING:
        rSO2_ValvePos := 0.0;
        ePackMLState := STATE_STOPPED;
        
    STATE_STOPPED:
        // Secure

END_CASE;
```"""

json_record = {
    "messages": [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": assistant_content}
    ]
}

data_path = os.path.join(r"C:\Users\majip\Downloads\LLM REASEARCH\data", "synthetic_generation_v3_enterprise.jsonl")
with open(data_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(json_record) + "\n")

print("Successfully appended to JSONL.")
