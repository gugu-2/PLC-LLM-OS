import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)
record = {
    "messages": [
        {"role": "user", "content": "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data. Your specific domain is: District Heating Heat Pump Array. Task: Invent a highly complex control scenario for this domain (e.g., Ammonia (R717) dual-stage compression curves, evaporator source cascading, and district network flow balancing). Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."},
        {"role": "assistant", "content": """```iec-st
FUNCTION_BLOCK FB_DH_HeatPump_Array_Control
    VAR_INPUT
        Enable : BOOL; // System enable
        NetworkTempSP : REAL; // Target district heating supply temperature (C)
        NetworkFlowSP : REAL; // Target network flow rate (m3/h)
        ReturnTemp : REAL; // Actual network return temperature (C)
        SupplyTemp : REAL; // Actual network supply temperature (C)
        FlowRate : REAL; // Actual network flow rate (m3/h)
        SourceWaterTemp1 : REAL; // Evaporator source 1 inlet temperature (C)
        SourceWaterTemp2 : REAL; // Evaporator source 2 inlet temperature (C)
        PowerTariff : REAL; // Current electrical power tariff
        MaxPowerCap : REAL; // Maximum electrical power capacity (kW)
    END_VAR
    VAR_OUTPUT
        HP1_Comp1_Speed : REAL; // Stage 1 compressor speed HP1 (%)
        HP1_Comp2_Speed : REAL; // Stage 2 compressor speed HP1 (%)
        HP2_Comp1_Speed : REAL; // Stage 1 compressor speed HP2 (%)
        HP2_Comp2_Speed : REAL; // Stage 2 compressor speed HP2 (%)
        Source1_ValvePos : REAL; // Source 1 cascade valve position (%)
        Source2_ValvePos : REAL; // Source 2 cascade valve position (%)
        NetworkPump_Speed : REAL; // District network circulation pump speed (%)
        TotalPower : REAL; // Estimated total power consumption (kW)
        COP : REAL; // Estimated Coefficient of Performance
        SystemFault : BOOL; // Global fault indicator
    END_VAR
    VAR
        HP1_CapacityReq : REAL;
        HP2_CapacityReq : REAL;
        PID_Temp : FB_PID;
        PID_Flow : FB_PID;
        HeatLoad : REAL;
        TempError : REAL;
        FlowError : REAL;
        HP1_MaxEff_Curve : ARRAY[0..10] OF REAL := [0.0, 10.0, 25.0, 40.0, 55.0, 70.0, 80.0, 88.0, 95.0, 98.0, 100.0];
        HP2_MaxEff_Curve : ARRAY[0..10] OF REAL := [0.0, 12.0, 27.0, 42.0, 57.0, 72.0, 82.0, 90.0, 96.0, 99.0, 100.0];
        OptIndex : INT;
        TotalDemandCap : REAL;
    END_VAR
    
    // System Safety and Enable Logic
    IF NOT Enable THEN
        HP1_Comp1_Speed := 0.0; HP1_Comp2_Speed := 0.0;
        HP2_Comp1_Speed := 0.0; HP2_Comp2_Speed := 0.0;
        Source1_ValvePos := 0.0; Source2_ValvePos := 0.0;
        NetworkPump_Speed := 0.0;
        SystemFault := FALSE;
        RETURN;
    END_IF;

    // District Network Flow Balancing
    FlowError := NetworkFlowSP - FlowRate;
    PID_Flow(
        Enable := TRUE,
        Setpoint := NetworkFlowSP,
        ProcessVariable := FlowRate,
        Kp := 1.5, Ki := 0.5, Kd := 0.1,
        Output => NetworkPump_Speed
    );
    
    // Thermal Demand Assessment
    TempError := NetworkTempSP - SupplyTemp;
    PID_Temp(
        Enable := TRUE,
        Setpoint := NetworkTempSP,
        ProcessVariable := SupplyTemp,
        Kp := 2.5, Ki := 0.8, Kd := 0.2,
        Output => HeatLoad
    );
    
    // Evaporator Source Cascading (Sensible Heat Maximization)
    IF SourceWaterTemp1 >= SourceWaterTemp2 THEN
        Source1_ValvePos := 100.0;
        Source2_ValvePos := 0.0;
        IF HeatLoad > 50.0 THEN // Cascading active if load exceeds single source capability
            Source2_ValvePos := (HeatLoad - 50.0) * 2.0;
        END_IF;
    ELSE
        Source2_ValvePos := 100.0;
        Source1_ValvePos := 0.0;
        IF HeatLoad > 50.0 THEN
            Source1_ValvePos := (HeatLoad - 50.0) * 2.0;
        END_IF;
    END_IF;
    
    // R717 Dual-Stage Compression Load Distribution
    HP1_CapacityReq := HeatLoad * 0.5; // Symetrical load sharing logic
    HP2_CapacityReq := HeatLoad * 0.5;
    
    // Non-linear Interpolation for HP1 Ammonia Compression Curve
    OptIndex := REAL_TO_INT(HP1_CapacityReq / 10.0);
    IF OptIndex > 10 THEN OptIndex := 10; END_IF;
    IF OptIndex < 0 THEN OptIndex := 0; END_IF;
    HP1_Comp1_Speed := HP1_MaxEff_Curve[OptIndex] * 0.92; // LP Stage optimal displacement ratio
    HP1_Comp2_Speed := HP1_MaxEff_Curve[OptIndex] * 1.08; // HP Stage displacement ratio
    
    // Non-linear Interpolation for HP2 Ammonia Compression Curve
    OptIndex := REAL_TO_INT(HP2_CapacityReq / 10.0);
    IF OptIndex > 10 THEN OptIndex := 10; END_IF;
    IF OptIndex < 0 THEN OptIndex := 0; END_IF;
    HP2_Comp1_Speed := HP2_MaxEff_Curve[OptIndex] * 0.92;
    HP2_Comp2_Speed := HP2_MaxEff_Curve[OptIndex] * 1.08;
    
    // Peak Shaving and Power Capacity Constraints
    TotalDemandCap := (HP1_Comp1_Speed + HP1_Comp2_Speed + HP2_Comp1_Speed + HP2_Comp2_Speed) * 0.85;
    IF TotalDemandCap > MaxPowerCap THEN
        // Throttle back linearly to meet electrical constraint
        HP1_Comp1_Speed := HP1_Comp1_Speed * (MaxPowerCap / TotalDemandCap);
        HP1_Comp2_Speed := HP1_Comp2_Speed * (MaxPowerCap / TotalDemandCap);
        HP2_Comp1_Speed := HP2_Comp1_Speed * (MaxPowerCap / TotalDemandCap);
        HP2_Comp2_Speed := HP2_Comp2_Speed * (MaxPowerCap / TotalDemandCap);
        TotalPower := MaxPowerCap;
    ELSE
        TotalPower := TotalDemandCap;
    END_IF;
    
    // Real-time Coefficient of Performance Calculation
    IF TotalPower > 1.0 THEN
        COP := (HeatLoad * 12.5) / TotalPower; 
    ELSE
        COP := 0.0;
    END_IF;
    
    // Fault Detection (Simplified)
    SystemFault := (TempError > 20.0) OR (FlowError > 50.0);
    
END_FUNCTION_BLOCK
```"""}
    ]
}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4)
