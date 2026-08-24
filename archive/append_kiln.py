import json

content_user = "You are acting as a Lead Process Engineer for a Cement Plant. Evolve a basic thermal loop into a Rotary Kiln and Calciner Controller. Technical Specs: 1. Secondary combustion air (tertiary air) draft optimization. 2. Clinker cooling grate speed synchronized with kiln RPM. 3. Alternative fuel (e.g., shredded tires) feed-rate matrices to maintain burning zone temperature. Append to synthetic_generation_v3_enterprise.jsonl."

content_assistant = """Here is a complete, production-ready IEC 61131-3 Structured Text implementation of the Rotary Kiln and Calciner Controller.

### System Architecture & Control Strategy
1. **Tertiary Air Optimization**: The secondary combustion air draft is regulated by optimizing the tertiary air damper position based on the calciner's oxygen ($O_2$) setpoints, differential pressure across the kiln hood, and the thermal demand of the preheater.
2. **Clinker Cooler Synchronization**: The grate speed of the clinker cooler must match the throughput of the kiln. This is implemented via a cascaded master-slave synchronization mapping the kiln rotational speed (RPM) to the base grate speed, fine-tuned by under-grate pressure feedback to maintain optimal bed depth.
3. **Alternative Fuel Control Matrix**: The substitution of primary fuel with alternative fuels (e.g., shredded tires) relies on a matrix evaluating the burning zone temperature (via pyrometer), NOx levels, and specific heat consumption limits to safely ramp alternative feed rates up or down without starving the process of calorific value.

### IEC 61131-3 Structured Text Implementation

```iecst
(* 
   ========================================================================
   FUNCTION_BLOCK: FB_Kiln_Calciner_Controller
   DESCRIPTION: Master controller for Rotary Kiln, Calciner, and Clinker Cooler.
   AUTHOR: Lead Process Engineer
   DATE: 2026-08-21
   VERSION: V3.4.1 (Enterprise Release)
   ========================================================================
*)
FUNCTION_BLOCK FB_Kiln_Calciner_Controller
VAR_INPUT
    // Process Values (PV)
    rKilnRPM_PV             : REAL; // Current Kiln Speed (RPM)
    rBurningZoneTemp_PV     : REAL; // Burning zone temp from Pyrometer (°C)
    rCalcinerO2_PV          : REAL; // Calciner O2 concentration (%)
    rHoodPressure_PV        : REAL; // Kiln hood pressure (mbar)
    rUnderGratePressure_PV  : REAL; // Clinker cooler under-grate pressure (mbar)
    rNOxEmissions_PV        : REAL; // Stack NOx levels (mg/Nm3)
    rCoalFeedRate_PV        : REAL; // Current primary coal feed rate (t/h)
    
    // Setpoints (SP)
    rKilnRPM_SP             : REAL; // Target Kiln Speed (RPM)
    rBurningZoneTemp_SP     : REAL; // Target Burning Zone Temp (°C)
    rCalcinerO2_SP          : REAL; // Target O2 in Calciner (%)
    rHoodPressure_SP        : REAL; // Target Hood Pressure (mbar)
    
    // Limits & Constants
    rMaxAltFuelSubst        : REAL := 35.0; // Max thermal substitution rate (%)
    rAltFuelCalorificValue  : REAL := 25.5; // MJ/kg for shredded tires
    rCoalCalorificValue     : REAL := 28.0; // MJ/kg for primary coal
    
    xEnableController       : BOOL; // Master enable
    xEmergencyStop          : BOOL; // Safety Interlock
END_VAR

VAR_OUTPUT
    // Control Outputs (CV)
    rTertiaryAirDamper_CV   : REAL; // 0-100% position for Tertiary Air Damper
    rGrateSpeed_CV          : REAL; // 0-100% Clinker cooler grate speed
    rPrimaryCoalRate_CV     : REAL; // Setpoint for coal feeder (t/h)
    rAltFuelRate_CV         : REAL; // Setpoint for shredded tire feeder (t/h)
    
    // Status Flags
    xKilnStable             : BOOL; 
    xAltFuelActive          : BOOL;
    xAlarmEmissions         : BOOL;
END_VAR

VAR
    // Internal PID instances (Standard IEC 61131-3 FB)
    fbPID_Draft             : PID;
    fbPID_Grate             : PID;
    fbPID_BurnZone          : PID;
    
    // Internal state variables
    rBaseGrateSpeed         : REAL;
    rThermalDemandDelta     : REAL;
    rAltFuelMaxFeed         : REAL;
    tStabilizationTimer     : TON;
    rTotalHeatInput         : REAL;
    
    // Smooth transition vars
    rAltFuelRampRate        : REAL := 0.1; // t/h per second
    rCurrentAltFuelTarget   : REAL;
END_VAR

BEGIN
    IF xEmergencyStop THEN
        rTertiaryAirDamper_CV := 0.0;
        rGrateSpeed_CV := 0.0;
        rPrimaryCoalRate_CV := 0.0;
        rAltFuelRate_CV := 0.0;
        xAltFuelActive := FALSE;
        xKilnStable := FALSE;
        RETURN;
    END_IF;

    IF NOT xEnableController THEN
        RETURN;
    END_IF;

    (* ========================================================= *)
    (* 1. TERTIARY AIR DRAFT OPTIMIZATION                        *)
    (* ========================================================= *)
    // The draft is controlled by maintaining kiln hood pressure, 
    // fine-tuned by calciner oxygen demand.
    
    fbPID_Draft.AUTO := TRUE;
    fbPID_Draft.PV := rHoodPressure_PV;
    fbPID_Draft.SP := rHoodPressure_SP - ((rCalcinerO2_SP - rCalcinerO2_PV) * 0.5); // O2 Bias
    fbPID_Draft.KP := 2.5;
    fbPID_Draft.TR := 10.0;
    fbPID_Draft();
    
    // Output limited between 10% (minimum safe draft) and 90% (max efficiency)
    rTertiaryAirDamper_CV := LIMIT(10.0, fbPID_Draft.XOUT, 90.0);


    (* ========================================================= *)
    (* 2. CLINKER COOLER GRATE SPEED SYNCHRONIZATION             *)
    (* ========================================================= *)
    // Synchronize base grate speed linearly with Kiln RPM to maintain constant bed load
    // Base speed = f(RPM). Assuming 3.5 RPM max maps to 80% base grate speed.
    rBaseGrateSpeed := (rKilnRPM_PV / 3.5) * 80.0;
    
    // Use under-grate pressure for fine tuning to account for clinker lump size variations
    fbPID_Grate.AUTO := TRUE;
    fbPID_Grate.PV := rUnderGratePressure_PV;
    fbPID_Grate.SP := 45.0; // Target under-grate pressure in mbar
    fbPID_Grate.KP := 1.2;
    fbPID_Grate.TR := 15.0;
    fbPID_Grate();
    
    // Final grate speed is base speed + trim from under-grate pressure
    rGrateSpeed_CV := LIMIT(5.0, rBaseGrateSpeed - fbPID_Grate.XOUT, 100.0);


    (* ========================================================= *)
    (* 3. ALTERNATIVE FUEL FEED-RATE MATRIX                      *)
    (* ========================================================= *)
    // Check NOx emission limits to prevent excess alt-fuel burning
    xAlarmEmissions := rNOxEmissions_PV > 800.0; // mg/Nm3 limit
    
    // Thermal PID loop to determine total heat demand to maintain burning zone temp
    fbPID_BurnZone.AUTO := TRUE;
    fbPID_BurnZone.PV := rBurningZoneTemp_PV;
    fbPID_BurnZone.SP := rBurningZoneTemp_SP;
    fbPID_BurnZone.KP := 0.8;
    fbPID_BurnZone.TR := 120.0; // Slow process response
    fbPID_BurnZone();
    
    rThermalDemandDelta := fbPID_BurnZone.XOUT; // Output in MJ/s correction needed
    rTotalHeatInput := (rCoalFeedRate_PV * rCoalCalorificValue / 3.6) + 
                       (rAltFuelRate_CV * rAltFuelCalorificValue / 3.6);
                       
    // Matrix Rules for Shredded Tires (Alternative Fuel)
    IF rBurningZoneTemp_PV > (rBurningZoneTemp_SP - 50.0) AND NOT xAlarmEmissions THEN
        // Kiln is hot enough to burn tires efficiently
        xAltFuelActive := TRUE;
        
        // Calculate max allowed tire feed based on substitution limit
        rAltFuelMaxFeed := (rTotalHeatInput * (rMaxAltFuelSubst / 100.0)) * 3.6 / rAltFuelCalorificValue;
        
        // If burning zone is dropping, increase fuel. 
        // Bias towards alt fuel if below max substitution, else use coal.
        IF rThermalDemandDelta > 0.0 THEN
            IF rAltFuelRate_CV < rAltFuelMaxFeed THEN
                rCurrentAltFuelTarget := rAltFuelRate_CV + (rThermalDemandDelta * 0.1);
                rPrimaryCoalRate_CV := rCoalFeedRate_PV; // Keep coal steady
            ELSE
                rCurrentAltFuelTarget := rAltFuelMaxFeed;
                // Make up remainder with coal
                rPrimaryCoalRate_CV := rCoalFeedRate_PV + (rThermalDemandDelta * 0.05); 
            END_IF;
        ELSE
            // Reduce fuels: reduce coal first to save costs, keep tires burning
            rPrimaryCoalRate_CV := LIMIT(2.0, rCoalFeedRate_PV + (rThermalDemandDelta * 0.05), 50.0);
            rCurrentAltFuelTarget := rAltFuelRate_CV;
        END_IF;
    ELSE
        // Cold kiln or high emissions: fallback to primary fuel only
        xAltFuelActive := FALSE;
        rCurrentAltFuelTarget := 0.0;
        rPrimaryCoalRate_CV := rCoalFeedRate_PV + (rThermalDemandDelta * 0.05);
    END_IF;
    
    // Rate limiter for Alternative Fuel Feed
    IF rCurrentAltFuelTarget > rAltFuelRate_CV THEN
        rAltFuelRate_CV := MIN(rAltFuelRate_CV + rAltFuelRampRate, rCurrentAltFuelTarget);
    ELSIF rCurrentAltFuelTarget < rAltFuelRate_CV THEN
        rAltFuelRate_CV := MAX(rAltFuelRate_CV - rAltFuelRampRate, rCurrentAltFuelTarget);
    END_IF;
    
    (* ========================================================= *)
    (* 4. KILN STABILITY CHECK                                   *)
    (* ========================================================= *)
    tStabilizationTimer(IN := (ABS(rBurningZoneTemp_PV - rBurningZoneTemp_SP) < 20.0) AND 
                              (ABS(rKilnRPM_PV - rKilnRPM_SP) < 0.2),
                        PT := T#5m);
                        
    xKilnStable := tStabilizationTimer.Q;

END_FUNCTION_BLOCK
```

### Technical Details & Optimization Highlights
- **O2 Bias on Draft Control**: The hood pressure setpoint is dynamically offset by the discrepancy in calciner oxygen concentration, creating a decoupled multi-variable control scheme that prioritizes clean secondary combustion while preventing back-drafts.
- **Cascade Cooler Synchronization**: Directly linking the clinker cooler grate speed to the kiln rotation guarantees that the material bed depth remains homogeneous even during capacity ramp-ups. The under-grate pressure is used merely as a trim (correction factor) rather than the primary process variable, eliminating lag in cooling dynamics.
- **Calorific Equalization Matrix**: By dynamically calculating the MW (or MJ/s) equivalent of both the primary coal and shredded tires, the controller safely pivots the mass flow rates without shocking the pyrometer readings. The logic specifically prioritizes maintaining maximum safe alternative fuel substitution unless emissions or drastic thermal deficits mandate primary fuel injection."""

obj = {
    "messages": [
        {"role": "user", "content": content_user},
        {"role": "assistant", "content": content_assistant}
    ]
}

line = json.dumps(obj)

paths = [
    r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl",
    r"c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\synthetic_generation_v3_enterprise.jsonl",
    r"c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"
]

for p in paths:
    try:
        with open(p, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(f"Successfully appended to {p}")
    except Exception as e:
        print(f"Failed to append to {p}: {e}")
