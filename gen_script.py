import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Utility-Scale BESS (Battery Energy Storage System).
Task: Invent a highly complex control scenario for this domain (e.g., multi-rack State of Charge (SOC) active balancing, thermal liquid cooling zone profiling, and bi-directional inverter micro-grid islanding).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.

CRITICAL RULES:
1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.
2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT.
3. You MUST save your JSON payload to a uniquely named file in the swarm directory using python."""

code = """```iec-st
FUNCTION_BLOCK FB_BESS_MasterController
    VAR_INPUT
        Enable : BOOL; // Global Enable
        GridVoltage_L1 : REAL; // Grid Voltage L1 (V)
        GridVoltage_L2 : REAL; // Grid Voltage L2 (V)
        GridVoltage_L3 : REAL; // Grid Voltage L3 (V)
        GridFreq : REAL; // Grid Frequency (Hz)
        IslandingRequest : BOOL; // Request to decouple from grid
        
        Rack1_SOC : REAL; // Rack 1 State of Charge (%)
        Rack1_Temp : REAL; // Rack 1 Average Temperature (C)
        Rack2_SOC : REAL; // Rack 2 State of Charge (%)
        Rack2_Temp : REAL; // Rack 2 Average Temperature (C)
        Rack3_SOC : REAL; // Rack 3 State of Charge (%)
        Rack3_Temp : REAL; // Rack 3 Average Temperature (C)
        Rack4_SOC : REAL; // Rack 4 State of Charge (%)
        Rack4_Temp : REAL; // Rack 4 Average Temperature (C)
        
        CoolantInletTemp : REAL; // Liquid coolant inlet temperature
        CoolantFlowRate : REAL; // L/min
    END_VAR
    
    VAR_OUTPUT
        SystemReady : BOOL;
        InverterMode : INT; // 0=Off, 1=Grid-Following, 2=Grid-Forming (Islanding)
        ActivePowerCmd : REAL; // kW commanded
        ReactivePowerCmd : REAL; // kVAR commanded
        
        Rack1_CurrentCmd : REAL; // A
        Rack2_CurrentCmd : REAL; // A
        Rack3_CurrentCmd : REAL; // A
        Rack4_CurrentCmd : REAL; // A
        
        CoolingPumpSpeed : REAL; // % 0-100
        ChillerEnable : BOOL;
        
        GridBreakerOpen : BOOL; // Open main breaker
    END_VAR
    
    VAR
        AvgSOC : REAL;
        MaxTemp : REAL;
        BalancingFactor : REAL := 0.05; // 5% correction per % deviation
        TotalTargetPower : REAL; 
        
        State : INT := 0; // 0=Init, 1=Grid-Connected, 2=Transition, 3=Islanding
        Timer_Transition : TON;
        
        TempSetpoint : REAL := 25.0;
        TempHysteresis : REAL := 2.0;
        
        // Internal variables for PI control
        P_Gain_Cooling : REAL := 5.0;
        I_Gain_Cooling : REAL := 0.1;
        TempError : REAL;
        CoolingIntegral : REAL := 0.0;
        
        // Phase-Locked Loop pseudo-vars
        PLL_LossOfSync : BOOL;
    END_VAR
    
    // Safety and Enable Check
    IF NOT Enable THEN
        SystemReady := FALSE;
        InverterMode := 0;
        ActivePowerCmd := 0.0;
        ReactivePowerCmd := 0.0;
        Rack1_CurrentCmd := 0.0;
        Rack2_CurrentCmd := 0.0;
        Rack3_CurrentCmd := 0.0;
        Rack4_CurrentCmd := 0.0;
        CoolingPumpSpeed := 0.0;
        ChillerEnable := FALSE;
        GridBreakerOpen := TRUE; // Safe state
        RETURN;
    END_IF;
    
    SystemReady := TRUE;
    
    // --- 1. Thermal Management (Liquid Cooling Zone Profiling) ---
    MaxTemp := Rack1_Temp;
    IF Rack2_Temp > MaxTemp THEN MaxTemp := Rack2_Temp; END_IF;
    IF Rack3_Temp > MaxTemp THEN MaxTemp := Rack3_Temp; END_IF;
    IF Rack4_Temp > MaxTemp THEN MaxTemp := Rack4_Temp; END_IF;
    
    IF MaxTemp > (TempSetpoint + TempHysteresis) THEN
        ChillerEnable := TRUE;
    ELSIF MaxTemp < (TempSetpoint - TempHysteresis) THEN
        ChillerEnable := FALSE;
    END_IF;
    
    // PI Control for Pump Speed based on MaxTemp
    TempError := MaxTemp - TempSetpoint;
    IF TempError > 0.0 THEN
        CoolingIntegral := CoolingIntegral + (TempError * 0.1); // Assuming 100ms task
        IF CoolingIntegral > 50.0 THEN CoolingIntegral := 50.0; END_IF; // Anti-windup
        CoolingPumpSpeed := (P_Gain_Cooling * TempError) + (I_Gain_Cooling * CoolingIntegral);
    ELSE
        CoolingIntegral := 0.0;
        CoolingPumpSpeed := 20.0; // Minimum circulation
    END_IF;
    
    IF CoolingPumpSpeed > 100.0 THEN
        CoolingPumpSpeed := 100.0;
    END_IF;
    
    // --- 2. Multi-rack SOC Active Balancing ---
    AvgSOC := (Rack1_SOC + Rack2_SOC + Rack3_SOC + Rack4_SOC) / 4.0;
    
    // Base current calculated from total active power demand (simplified logic for demonstration)
    TotalTargetPower := ActivePowerCmd; 
    
    // Let's assume nominal base current per rack is BaseI
    VAR
        BaseI : REAL;
    END_VAR
    BaseI := (TotalTargetPower * 1000.0) / (4.0 * 1000.0); // Simple assumption
    
    Rack1_CurrentCmd := BaseI * (1.0 + (Rack1_SOC - AvgSOC) * BalancingFactor * SIGN(BaseI));
    Rack2_CurrentCmd := BaseI * (1.0 + (Rack2_SOC - AvgSOC) * BalancingFactor * SIGN(BaseI));
    Rack3_CurrentCmd := BaseI * (1.0 + (Rack3_SOC - AvgSOC) * BalancingFactor * SIGN(BaseI));
    Rack4_CurrentCmd := BaseI * (1.0 + (Rack4_SOC - AvgSOC) * BalancingFactor * SIGN(BaseI));
    
    // Limiters
    IF Rack1_CurrentCmd > 200.0 THEN Rack1_CurrentCmd := 200.0; ELSIF Rack1_CurrentCmd < -200.0 THEN Rack1_CurrentCmd := -200.0; END_IF;
    IF Rack2_CurrentCmd > 200.0 THEN Rack2_CurrentCmd := 200.0; ELSIF Rack2_CurrentCmd < -200.0 THEN Rack2_CurrentCmd := -200.0; END_IF;
    IF Rack3_CurrentCmd > 200.0 THEN Rack3_CurrentCmd := 200.0; ELSIF Rack3_CurrentCmd < -200.0 THEN Rack3_CurrentCmd := -200.0; END_IF;
    IF Rack4_CurrentCmd > 200.0 THEN Rack4_CurrentCmd := 200.0; ELSIF Rack4_CurrentCmd < -200.0 THEN Rack4_CurrentCmd := -200.0; END_IF;

    // --- 3. Bi-directional Inverter Micro-grid Islanding ---
    // Grid monitoring
    PLL_LossOfSync := (GridFreq < 49.5) OR (GridFreq > 50.5) OR (GridVoltage_L1 < 380.0);
    
    CASE State OF
        0: // Init
            GridBreakerOpen := TRUE;
            InverterMode := 0; // Off
            IF GridVoltage_L1 > 390.0 AND GridFreq > 49.8 AND NOT IslandingRequest THEN
                State := 1;
            END_IF;
            
        1: // Grid-Connected
            GridBreakerOpen := FALSE;
            InverterMode := 1; // Grid-Following
            
            IF IslandingRequest OR PLL_LossOfSync THEN
                State := 2; 
                Timer_Transition(IN:=FALSE);
            END_IF;
            
        2: // Transition
            GridBreakerOpen := TRUE;
            InverterMode := 0; // Temporary float
            Timer_Transition(IN:=TRUE, PT:=T#100ms);
            
            IF Timer_Transition.Q THEN
                State := 3;
            END_IF;
            
        3: // Islanding (Grid-Forming)
            GridBreakerOpen := TRUE;
            InverterMode := 2; // Grid-Forming
            
            IF NOT IslandingRequest AND NOT PLL_LossOfSync THEN
                State := 1;
            END_IF;
    END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2)

os.makedirs("data", exist_ok=True)
with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"Success, saved to {filepath} and appended to JSONL")
