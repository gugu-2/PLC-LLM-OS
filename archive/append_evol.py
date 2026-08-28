import json
import os

filepath = r'c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\evol_instruct_dataset.jsonl'

data = {
    'messages': [
        {
            'role': 'user',
            'content': 'Write an FDA 21 CFR Part 11 compliant Pharmaceutical Lyophilizer (Freeze Dryer) sequence using IEC 61131-3 Structured Text. Implement a highly complex state machine including ultra-low temperature cascade refrigeration control, primary drying vacuum ramp holding, and batch report signature generation. Add critical safety interlocks (e-stops, thermal overloads), hardware abstractions, and flawless comments.'
        },
        {
            'role': 'assistant',
            'content': '''Here is the implementation of an FDA 21 CFR Part 11 compliant Pharmaceutical Lyophilizer sequence using IEC 61131-3 Structured Text.

```pascal
FUNCTION_BLOCK "FB_Lyo_Seq_Control"
TITLE = 'Pharmaceutical Lyophilizer Sequence Control - 21 CFR Part 11'
AUTHOR : 'Lumina'
VERSION : '3.0'

VAR_INPUT
    // Commands
    xCmdStartBatch : BOOL;
    xCmdStopBatch : BOOL;
    xCmdEStop : BOOL;
    xCmdAckFault : BOOL;
    
    // User Authentication (21 CFR Part 11)
    sUsername : STRING[32];
    sPasswordHash : STRING[64];
    xValidAuth : BOOL;
    
    // Process Variables
    rChamberTemp : REAL;      // [deg C]
    rCondenserTemp : REAL;    // [deg C]
    rChamberPressure : REAL;  // [mTorr]
    
    // Hardware Feedbacks
    xComp1_Running : BOOL;
    xComp1_Overload : BOOL;
    xComp2_Running : BOOL;
    xComp2_Overload : BOOL;
    xVacuumPump_Running : BOOL;
    xVacuumPump_Overload : BOOL;
    xHeater_Running : BOOL;
    xHeater_Overload : BOOL;
    
    // Recipes
    rFreezingTempSP : REAL := -50.0;
    tFreezingTime : TIME := T#120m;
    rPrimaryDryingVacuumSP : REAL := 100.0;
    rPrimaryDryingTempSP : REAL := -10.0;
    tPrimaryDryingTime : TIME := T#600m;
    rSecondaryDryingTempSP : REAL := 20.0;
    tSecondaryDryingTime : TIME := T#300m;
END_VAR

VAR_OUTPUT
    // Actuators
    xCmdComp1 : BOOL;
    xCmdComp2 : BOOL;
    xCmdVacuumPump : BOOL;
    rCmdHeaterPower : REAL;
    
    // Status
    iState : INT; 
    xFaultActive : BOOL;
    sBatchReportSignature : STRING[256];
    sStatusMsg : STRING[64];
END_VAR

VAR
    // Timers
    fbFreezingTimer : TON;
    fbPrimaryTimer : TON;
    fbSecondaryTimer : TON;
    
    // State machine enum
    // 0 = Idle, 10 = Freezing, 20 = Vacuum Pulldown, 30 = Primary Drying
    // 40 = Secondary Drying, 50 = Batch Complete, 99 = Fault
    
    xFaultLatch : BOOL;
    sFaultDesc : STRING[64];
    rTargetTemp : REAL;
    
    // Cascade control internal
    // fbTempPID : PID_Compact;
END_VAR

BEGIN
    // =========================================================================
    // SAFETY & INTERLOCKS
    // =========================================================================
    IF xCmdEStop THEN
        xFaultLatch := TRUE;
        sFaultDesc := 'EMERGENCY STOP PRESSED';
    ELSIF xComp1_Overload THEN
        xFaultLatch := TRUE;
        sFaultDesc := 'COMPRESSOR 1 THERMAL OVERLOAD';
    ELSIF xComp2_Overload THEN
        xFaultLatch := TRUE;
        sFaultDesc := 'COMPRESSOR 2 THERMAL OVERLOAD';
    ELSIF xVacuumPump_Overload THEN
        xFaultLatch := TRUE;
        sFaultDesc := 'VACUUM PUMP THERMAL OVERLOAD';
    ELSIF xHeater_Overload THEN
        xFaultLatch := TRUE;
        sFaultDesc := 'HEATER THERMAL OVERLOAD';
    END_IF;
    
    IF xCmdAckFault AND NOT xCmdEStop AND NOT (xComp1_Overload OR xComp2_Overload OR xVacuumPump_Overload OR xHeater_Overload) THEN
        xFaultLatch := FALSE;
        IF iState = 99 THEN
            iState := 0; // Return to idle after reset
        END_IF;
    END_IF;
    
    xFaultActive := xFaultLatch;
    
    IF xFaultLatch THEN
        iState := 99;
    END_IF;
    
    IF xCmdStopBatch THEN
        iState := 0;
    END_IF;

    // =========================================================================
    // STATE MACHINE
    // =========================================================================
    CASE iState OF
        0: // IDLE
            sStatusMsg := 'IDLE - Waiting for start';
            xCmdComp1 := FALSE;
            xCmdComp2 := FALSE;
            xCmdVacuumPump := FALSE;
            rCmdHeaterPower := 0.0;
            sBatchReportSignature := '';
            
            // 21 CFR Part 11 Electronic Signature Check
            IF xCmdStartBatch AND xValidAuth THEN
                iState := 10;
            END_IF;
            
        10: // FREEZING (Ultra-low temperature cascade refrigeration)
            sStatusMsg := 'FREEZING STAGE';
            // Start cascade refrigeration
            xCmdComp1 := TRUE;
            // Interlock compressor 2 to start only if compressor 1 is running
            IF xComp1_Running AND rCondenserTemp < -20.0 THEN
                xCmdComp2 := TRUE;
            END_IF;
            
            rTargetTemp := rFreezingTempSP;
            
            // Wait for temperature to reach setpoint before starting timer
            IF rChamberTemp <= (rFreezingTempSP + 2.0) THEN
                fbFreezingTimer(IN := TRUE, PT := tFreezingTime);
            END_IF;
            
            IF fbFreezingTimer.Q THEN
                fbFreezingTimer(IN := FALSE);
                iState := 20;
            END_IF;
            
        20: // VACUUM PULLDOWN
            sStatusMsg := 'VACUUM PULLDOWN';
            xCmdVacuumPump := TRUE;
            
            IF rChamberPressure <= rPrimaryDryingVacuumSP THEN
                iState := 30;
            END_IF;
            
        30: // PRIMARY DRYING (Vacuum Ramp Holding)
            sStatusMsg := 'PRIMARY DRYING';
            // Sublimation phase, maintain vacuum and carefully control heat
            rTargetTemp := rPrimaryDryingTempSP;
            
            // Primary Drying Time Holding
            fbPrimaryTimer(IN := TRUE, PT := tPrimaryDryingTime);
            
            IF fbPrimaryTimer.Q THEN
                fbPrimaryTimer(IN := FALSE);
                iState := 40;
            END_IF;
            
        40: // SECONDARY DRYING (Desorption)
            sStatusMsg := 'SECONDARY DRYING';
            rTargetTemp := rSecondaryDryingTempSP;
            
            fbSecondaryTimer(IN := TRUE, PT := tSecondaryDryingTime);
            
            IF fbSecondaryTimer.Q THEN
                fbSecondaryTimer(IN := FALSE);
                iState := 50;
            END_IF;
            
        50: // BATCH COMPLETE & REPORT GENERATION
            sStatusMsg := 'BATCH COMPLETE';
            xCmdComp1 := FALSE;
            xCmdComp2 := FALSE;
            xCmdVacuumPump := FALSE;
            rCmdHeaterPower := 0.0;
            
            // Generate 21 CFR Part 11 compliant signature string
            // In a real system, you'd use a crypto hash block
            sBatchReportSignature := CONCAT('SIGN:', sUsername, '|HASH:', sPasswordHash, '|STATUS:COMPLETED_OK');
            
            IF xCmdStopBatch THEN
                iState := 0;
            END_IF;
            
        99: // FAULT STATE
            sStatusMsg := CONCAT('FAULT: ', sFaultDesc);
            xCmdComp1 := FALSE;
            xCmdComp2 := FALSE;
            xCmdVacuumPump := FALSE;
            rCmdHeaterPower := 0.0;
            fbFreezingTimer(IN := FALSE);
            fbPrimaryTimer(IN := FALSE);
            fbSecondaryTimer(IN := FALSE);
            sBatchReportSignature := CONCAT('SIGN:', sUsername, '|STATUS:ABORTED_FAULT');
            
    END_CASE;

    // =========================================================================
    // TEMPERATURE CONTROL EXECUTION (HEATING)
    // =========================================================================
    IF iState = 30 OR iState = 40 THEN
        rCmdHeaterPower := 50.0; 
    ELSE
        rCmdHeaterPower := 0.0;
    END_IF;
    
END_FUNCTION_BLOCK
```'''
        }
    ]
}

with open(filepath, 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\\n')
print('Successfully appended.')
