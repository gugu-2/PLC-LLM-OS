import json
import os

content = """PROGRAM AutomatedStraddleCarrier_RoutingMatrix
// Automated Straddle Carrier Routing Matrix & Drive Management
// IEC 61131-3 Structured Text

TYPE
    Position3D : STRUCT
        X : LREAL; // mm
        Y : LREAL; // mm
        Z : LREAL; // mm
        Heading : LREAL; // degrees
    END_STRUCT;

    LidarData : STRUCT
        FrontLeftCasting : Position3D;
        FrontRightCasting : Position3D;
        RearLeftCasting : Position3D;
        RearRightCasting : Position3D;
        ScanQuality : REAL; // 0.0 to 100.0%
        IsValid : BOOL;
    END_STRUCT;

    QuayCrane : STRUCT
        ID : INT;
        CurrentPos : Position3D;
        Velocity : LREAL;
        Direction : LREAL;
        IsMoving : BOOL;
    END_STRUCT;

    DriveState : STRUCT
        DieselEngineRPM : REAL;
        GeneratorOutputKW : REAL;
        SupercapVoltage : REAL;
        SupercapSOC : REAL; // State of Charge 0-100%
        TractionMotorTorqueCmd : REAL;
        BrakingPowerKW : REAL;
        IsRegenActive : BOOL;
    END_STRUCT;

    ObstacleMap : ARRAY[1..100] OF Position3D; // Dynamic grid map
END_TYPE

VAR_INPUT
    CurrentLidarScan : LidarData;
    ActiveCranes : ARRAY[1..10] OF QuayCrane;
    TargetContainerPos : Position3D;
    ActualCarrierPos : Position3D;
    ActualVelocity : LREAL; // m/s
    BrakePedalCmd : REAL; // 0-100%
    AccelPedalCmd : REAL; // 0-100%
END_VAR

VAR_OUTPUT
    DriveCommand : DriveState;
    SteeringAngle : LREAL;
    SpreaderTwistlockCmd : BOOL;
    HoistPositionCmd : LREAL;
    SystemFault : BOOL;
    FaultCode : INT;
END_VAR

VAR
    TargetPath : ARRAY[1..50] OF Position3D;
    AlignmentErrorX : LREAL;
    AlignmentErrorY : LREAL;
    AlignmentErrorHeading : LREAL;
    ToleranceX : LREAL := 2.5; // mm
    ToleranceY : LREAL := 2.5; // mm
    ToleranceHeading : LREAL := 0.1; // degrees
    i : INT;
    CraneSafetyZone : LREAL := 15000.0; // 15m radius
    DistanceToCrane : LREAL;
    MaxRegenPower : REAL := 500.0; // kW
    NominalSupercapVoltage : REAL := 800.0; // V
END_VAR

// --- 1. LIDAR-BASED CONTAINER CORNER-CASTING ALIGNMENT ---
IF CurrentLidarScan.IsValid AND CurrentLidarScan.ScanQuality > 95.0 THEN
    // Calculate geometric center of the 4 castings
    AlignmentErrorX := TargetContainerPos.X - ((CurrentLidarScan.FrontLeftCasting.X + CurrentLidarScan.FrontRightCasting.X + CurrentLidarScan.RearLeftCasting.X + CurrentLidarScan.RearRightCasting.X) / 4.0);
    AlignmentErrorY := TargetContainerPos.Y - ((CurrentLidarScan.FrontLeftCasting.Y + CurrentLidarScan.FrontRightCasting.Y + CurrentLidarScan.RearLeftCasting.Y + CurrentLidarScan.RearRightCasting.Y) / 4.0);
    
    // Calculate heading error (simplified differential)
    AlignmentErrorHeading := TargetContainerPos.Heading - ATAN2(CurrentLidarScan.FrontRightCasting.Y - CurrentLidarScan.RearRightCasting.Y, CurrentLidarScan.FrontRightCasting.X - CurrentLidarScan.RearRightCasting.X) * 180.0 / 3.14159265;

    IF ABS(AlignmentErrorX) <= ToleranceX AND ABS(AlignmentErrorY) <= ToleranceY AND ABS(AlignmentErrorHeading) <= ToleranceHeading THEN
        SpreaderTwistlockCmd := TRUE; // Millimeter-perfect, engage!
        HoistPositionCmd := TargetContainerPos.Z; // Lower hoist
    ELSE
        // Micro-adjustments via drive and steering
        SteeringAngle := LIMIT(-15.0, AlignmentErrorHeading * 0.5, 15.0);
        DriveCommand.TractionMotorTorqueCmd := LIMIT(-50.0, AlignmentErrorX * 0.1, 50.0);
    END_IF;
ELSE
    SystemFault := TRUE;
    FaultCode := 1001; // LIDAR Quality Low
END_IF;

// --- 2. DYNAMIC PATHFINDING AROUND MOVING QUAY CRANES ---
// Predictive avoidance based on crane velocity vector
FOR i := 1 TO 10 DO
    IF ActiveCranes[i].ID <> 0 AND ActiveCranes[i].IsMoving THEN
        DistanceToCrane := SQRT(EXPT(ActualCarrierPos.X - ActiveCranes[i].CurrentPos.X, 2) + EXPT(ActualCarrierPos.Y - ActiveCranes[i].CurrentPos.Y, 2));
        
        // Dynamic safety zone based on crane speed
        IF DistanceToCrane < (CraneSafetyZone + (ActiveCranes[i].Velocity * 5000.0)) THEN
            // Trigger emergency re-route (A* or D* Lite implementation abstracted to waypoint shift)
            // Shift target path orthogonally to crane movement
            TargetPath[1].X := ActualCarrierPos.X + 5000.0 * COS(ActiveCranes[i].Direction + 90.0);
            TargetPath[1].Y := ActualCarrierPos.Y + 5000.0 * SIN(ActiveCranes[i].Direction + 90.0);
            SteeringAngle := ATAN2(TargetPath[1].Y - ActualCarrierPos.Y, TargetPath[1].X - ActualCarrierPos.X);
        END_IF;
    END_IF;
END_FOR;

// --- 3. HYBRID DIESEL-ELECTRIC DRIVE & REGENERATIVE BRAKING ---
// Determine power demand based on pedal commands and current velocity
IF BrakePedalCmd > 0.0 THEN
    // Regenerative braking mode
    DriveCommand.IsRegenActive := TRUE;
    DriveCommand.BrakingPowerKW := MaxRegenPower * (BrakePedalCmd / 100.0);
    
    // Route power to supercapacitors if not full
    IF DriveCommand.SupercapSOC < 95.0 THEN
        DriveCommand.SupercapVoltage := DriveCommand.SupercapVoltage + (DriveCommand.BrakingPowerKW * 0.05); // Simplified charge model
        DriveCommand.DieselEngineRPM := 800.0; // Idle
        DriveCommand.GeneratorOutputKW := 0.0;
    ELSE
        // Supercaps full, route to dynamic braking resistors (abstracted)
        DriveCommand.SupercapVoltage := NominalSupercapVoltage;
    END_IF;
    
    DriveCommand.TractionMotorTorqueCmd := -1.0 * DriveCommand.BrakingPowerKW * 2.0; // Negative torque for braking
    
ELSIF AccelPedalCmd > 0.0 THEN
    DriveCommand.IsRegenActive := FALSE;
    // Acceleration mode: Load sharing between Supercaps and Diesel Gen
    IF DriveCommand.SupercapSOC > 30.0 THEN
        // Primary power from supercapacitors for peak shaving
        DriveCommand.SupercapVoltage := DriveCommand.SupercapVoltage - (AccelPedalCmd * 2.0);
        DriveCommand.DieselEngineRPM := 1200.0; // Base load
        DriveCommand.GeneratorOutputKW := 150.0;
    ELSE
        // Supercaps depleted, full diesel power
        DriveCommand.DieselEngineRPM := 1800.0; // Peak load
        DriveCommand.GeneratorOutputKW := 400.0;
    END_IF;
    
    DriveCommand.TractionMotorTorqueCmd := AccelPedalCmd * 15.0; // Proportional torque
ELSE
    // Coasting
    DriveCommand.IsRegenActive := FALSE;
    DriveCommand.TractionMotorTorqueCmd := 0.0;
    DriveCommand.DieselEngineRPM := 800.0; // Idle
    DriveCommand.GeneratorOutputKW := 0.0;
END_IF;

// Calculate generic SOC for supercaps based on voltage
DriveCommand.SupercapSOC := LIMIT(0.0, (DriveCommand.SupercapVoltage / NominalSupercapVoltage) * 100.0, 100.0);

END_PROGRAM
"""

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Port Automation Engineer. Evolve a basic routing block into an Automated Straddle Carrier routing matrix. Technical Specs: 1. LIDAR-based container corner-casting alignment for millimeter-perfect lifting. 2. Dynamic pathfinding around moving quay cranes. 3. Hybrid diesel-electric drive load sharing and regenerative braking into supercapacitors."
        },
        {
            "role": "assistant",
            "content": content
        }
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\\n')
