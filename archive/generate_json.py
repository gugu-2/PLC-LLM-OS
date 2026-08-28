import json

user_content = """Evolve the basic FIFO_16 tracking block into a High-Speed Cross-Belt Sorter and Machine Vision routing matrix for a Global E-Commerce Logistics Hub. The system must include:
1. A TCP/IP (or UDP) socket integration block to receive datagrams from an overhead Cognex/Keyence machine vision barcode scanner.
2. A massive dynamic FIFO shift register tracking X/Y coordinates across 500 meters of conveying surface.
3. Induction cell synchronization calculating exact millisecond timing to fire the induction belt, landing the package perfectly centered on an empty cross-belt carrier moving at 3 m/s.
4. Recirculation logic for packages missing their chute due to downstream fullness (incorporating photoelectric retro-reflective sensor debounce logic).
5. Highly modular IEC 61131-3 standard FB/FC architecture."""

assistant_content = """(*
=============================================================================
  GLOBAL E-COMMERCE LOGISTICS HUB - CROSS-BELT SORTER & VISION MATRIX
=============================================================================
  Version: 4.0.0
  Architecture: IEC 61131-3 (Structured Text)
  Description: Massive-scale sorting matrix integrating TCP/UDP barcode
  vision scanners, high-speed induction sync, dynamic tracking FIFO, and
  safety interlocks.
=============================================================================
*)

TYPE
    E_SorterState :
    (
        STATE_INIT,
        STATE_SAFETY_CHECK,
        STATE_STARTUP_WARN,
        STATE_RUNNING,
        STATE_FAULT,
        STATE_STOPPING
    );

    t_PackageRecord : STRUCT
        ID             : UDINT;          (* Unique Tracking ID *)
        Barcode        : STRING(32);     (* Vision Scanner Data *)
        X_Coord        : REAL;           (* Position in meters *)
        Y_Coord        : REAL;           (* Width position *)
        TargetChute    : INT;            (* Destination Chute *)
        CarrierIndex   : INT;            (* Cross-belt carrier assignment *)
        IsRecirculating: BOOL;           (* Recirculation flag *)
    END_STRUCT;
END_TYPE

(* ==========================================================================
   FC: Photoelectric Debounce Logic
   ========================================================================== *)
FUNCTION FC_SensorDebounce : BOOL
VAR_INPUT
    RawSignal : BOOL;
    DebounceTime : TIME;
END_VAR
VAR
    TimerOn  : TON;
    TimerOff : TOF;
END_VAR
TimerOn(IN := RawSignal, PT := DebounceTime);
TimerOff(IN := TimerOn.Q, PT := DebounceTime);
FC_SensorDebounce := TimerOff.Q;
END_FUNCTION

(* ==========================================================================
   FB: UDP Vision Scanner Receiver
   ========================================================================== *)
FUNCTION_BLOCK FB_CognexUDP_Receiver
VAR_INPUT
    Enable      : BOOL;
    Port        : UINT := 8500;
END_VAR
VAR_OUTPUT
    NewDataReady: BOOL;
    ScannedData : STRING(32);
    Status      : WORD;
END_VAR
VAR
    UDP_Socket  : TCON; (* Abstracted TCP/UDP socket *)
    UDP_Rcv     : TURCV;
    Buffer      : ARRAY[0..255] OF BYTE;
END_VAR
(* Implementation abstracts actual socket creation. We simulate receiving data *)
UDP_Socket(REQ := Enable, ID := 1);
UDP_Rcv(EN_R := Enable, ID := 1, LEN := 32, DATA := Buffer);

IF UDP_Rcv.NDR THEN
    (* Convert Byte Array to String (Mocked conversion) *)
    ScannedData := '1Z9999999999999999';
    NewDataReady := TRUE;
ELSE
    NewDataReady := FALSE;
END_IF;
END_FUNCTION_BLOCK

(* ==========================================================================
   FB: Massive Dynamic FIFO Register (Tracking 500m conveyor)
   ========================================================================== *)
FUNCTION_BLOCK FB_TrackingFIFO
VAR_INPUT
    Push         : BOOL;
    NewPackage   : t_PackageRecord;
    EncoderTicks : DINT; (* Conveyor movement *)
END_VAR
VAR_OUTPUT
    CurrentTracking : ARRAY[0..999] OF t_PackageRecord;
    Count           : INT;
END_VAR
VAR
    WritePtr : INT := 0;
    i        : INT;
END_VAR
(* Push new package into FIFO ring buffer *)
IF Push THEN
    CurrentTracking[WritePtr] := NewPackage;
    WritePtr := (WritePtr + 1) MOD 1000;
    IF Count < 1000 THEN
        Count := Count + 1;
    END_IF;
END_IF;

(* Update X Coordinates dynamically based on high-speed encoder ticks *)
(* 1 tick = 1 mm *)
FOR i := 0 TO 999 DO
    IF CurrentTracking[i].ID <> 0 THEN
        CurrentTracking[i].X_Coord := CurrentTracking[i].X_Coord + (DINT_TO_REAL(EncoderTicks) / 1000.0);
    END_IF;
END_FOR;
END_FUNCTION_BLOCK

(* ==========================================================================
   FB: High-Speed Induction Synchronization
   ========================================================================== *)
FUNCTION_BLOCK FB_InductionSync
VAR_INPUT
    PackageDetected : BOOL;
    CarrierSpeed_ms : REAL := 3.0; (* 3 meters per second *)
    DistanceToMerge : REAL;
END_VAR
VAR_OUTPUT
    FireInductionBelt : BOOL;
    SyncError         : BOOL;
END_VAR
VAR
    CalculatedDelay   : REAL;
    FireTimer         : TON;
END_VAR
(* 
   Calculates exact millisecond timing to fire the induction belt.
   Time = Distance / Velocity. Convert to milliseconds.
*)
IF DistanceToMerge > 0.0 AND CarrierSpeed_ms > 0.0 THEN
    CalculatedDelay := (DistanceToMerge / CarrierSpeed_ms) * 1000.0;
ELSE
    SyncError := TRUE;
END_IF;

FireTimer(IN := PackageDetected, PT := REAL_TO_TIME(CalculatedDelay));
FireInductionBelt := FireTimer.Q;

END_FUNCTION_BLOCK

(* ==========================================================================
   MAIN PROGRAM: Sorter Routing Matrix
   ========================================================================== *)
PROGRAM PRG_MainSorterMatrix
VAR
    (* Safety Interlocks *)
    E_Stop_Zone1     : BOOL;
    ThermalOverload  : BOOL;
    SafetyCircuitOk  : BOOL;

    (* State Machine *)
    CurrentState     : E_SorterState := STATE_INIT;
    
    (* Hardware Abstractions *)
    PE_Recirculation_Raw : BOOL;
    PE_Recirc_Debounced  : BOOL;
    DownstreamFull       : BOOL;

    (* Instances *)
    VisionScanner  : FB_CognexUDP_Receiver;
    Tracker        : FB_TrackingFIFO;
    InductionZone  : FB_InductionSync;
    
    (* Local Variables *)
    TempPackage    : t_PackageRecord;
    CarrierSpeed   : REAL := 3.0;
    ConveyorRunCmd : BOOL;
END_VAR

(* 1. Safety & Hardware Interlocks *)
SafetyCircuitOk := E_Stop_Zone1 AND NOT ThermalOverload;

(* 2. Debounce Recirculation Sensor *)
PE_Recirc_Debounced := FC_SensorDebounce(RawSignal := PE_Recirculation_Raw, DebounceTime := T#50ms);

(* 3. State Machine *)
CASE CurrentState OF
    STATE_INIT:
        IF SafetyCircuitOk THEN
            CurrentState := STATE_SAFETY_CHECK;
        END_IF;

    STATE_SAFETY_CHECK:
        IF SafetyCircuitOk THEN
            CurrentState := STATE_STARTUP_WARN;
        ELSE
            CurrentState := STATE_FAULT;
        END_IF;

    STATE_STARTUP_WARN:
        (* Siren/Horn Logic omitted for brevity *)
        CurrentState := STATE_RUNNING;

    STATE_RUNNING:
        IF NOT SafetyCircuitOk THEN
            CurrentState := STATE_STOPPING;
        END_IF;
        
        ConveyorRunCmd := TRUE;

        (* Receive Barcode from Vision System *)
        VisionScanner(Enable := TRUE);
        IF VisionScanner.NewDataReady THEN
            TempPackage.ID := TempPackage.ID + 1;
            TempPackage.Barcode := VisionScanner.ScannedData;
            TempPackage.X_Coord := 0.0;
            
            (* Induction Synchronization *)
            InductionZone(
                PackageDetected := TRUE, 
                CarrierSpeed_ms := CarrierSpeed, 
                DistanceToMerge := 1.5
            );
            
            (* Enter Tracking FIFO *)
            Tracker(Push := InductionZone.FireInductionBelt, NewPackage := TempPackage, EncoderTicks := 15);
        END_IF;

        (* Recirculation Logic *)
        IF PE_Recirc_Debounced AND DownstreamFull THEN
            (* Mark package for second lap *)
            TempPackage.IsRecirculating := TRUE;
            (* Reroute to recirculation chute *)
            TempPackage.TargetChute := 999; 
        END_IF;

    STATE_STOPPING:
        ConveyorRunCmd := FALSE;
        CurrentState := STATE_FAULT;

    STATE_FAULT:
        ConveyorRunCmd := FALSE;
        IF SafetyCircuitOk THEN
            CurrentState := STATE_INIT;
        END_IF;
END_CASE;
END_PROGRAM"""

record = {
    "messages": [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": assistant_content}
    ]
}

with open("data/evol_instruct_dataset.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")
