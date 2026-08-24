import json
import os

prompt = """You are acting as the Chief Metrology Architect for a Global Timekeeping & Metrology Laboratory.

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Strontium-87 Optical Lattice Clock & Femtosecond Optical Frequency Comb Controller" (`FB_OpticalLattice_Clock`).

### Technical Specifications & Engineering Rigor Required:
1. **Magic Wavelength Optical Lattice Trapping**:
   - Closed-loop PID stabilization of a 813.42 nm trapping laser to exactly the "magic wavelength," holding thousands of Strontium-87 atoms in a 1D optical standing wave while completely nulling the differential AC Stark shift.
2. **Clock Laser & Femtosecond Frequency Comb**:
   - Ultra-stable 698 nm clock laser locking to a high-finesse Fabry-Perot cavity using Pound-Drever-Hall (PDH) feedback with active piezoelectric acoustic damping.
   - Mode-locked Titanium-Sapphire femtosecond frequency comb repetition rate ($f_{rep}$) and carrier-envelope offset ($f_{ceo}$) synchronization to down-convert the 429 THz optical frequency into a countable microwave RF signal.
3. **Code Quality**: Strict IEC 61131-3 ST, LREAL datatypes, comprehensive `VAR_INPUT`/`VAR_OUTPUT`, matrix equations for atomic state transitions, PackML states."""

response = """```iec-st
(*
  FB_OpticalLattice_Clock - Strontium-87 Optical Lattice Clock & Femtosecond Optical Frequency Comb Controller
  
  Chief Metrology Architect - Global Timekeeping & Metrology Laboratory
  
  Implements:
  1. Magic Wavelength Optical Lattice Trapping (813.42 nm)
  2. Ultra-stable Clock Laser (698 nm) with PDH locking
  3. Femtosecond Frequency Comb Control (frep and fceo)
  4. PackML State Machine for rigorous operational state management
*)

FUNCTION_BLOCK FB_OpticalLattice_Clock
VAR_INPUT
    bExecute            : BOOL;          (* Command to execute PackML sequence *)
    bStop               : BOOL;          (* Command to stop sequence *)
    bAbort              : BOOL;          (* Command to abort sequence *)
    bClear              : BOOL;          (* Clear faults *)
    
    // Magic Wavelength Trapping Inputs (813.42 nm)
    fTrappingLaserFreq  : LREAL;         (* Current trapping laser frequency [THz] *)
    fTrappingLaserPower : LREAL;         (* Current trapping laser power [W] *)
    fLatticeTrapDepth   : LREAL;         (* Measured trap depth [E_R] *)
    
    // Clock Laser (698 nm) & PDH Inputs
    fCavityTrans        : LREAL;         (* Fabry-Perot cavity transmission signal [V] *)
    fPDHErrorSignal     : LREAL;         (* Pound-Drever-Hall error signal [V] *)
    fPiezoFeedback      : LREAL;         (* Acoustic damping piezo feedback [V] *)
    
    // Frequency Comb Inputs
    fRepRateBeat        : LREAL;         (* Measured repetition rate beat note (f_rep) [Hz] *)
    fCEODetect          : LREAL;         (* Measured Carrier-Envelope Offset (f_ceo) [Hz] *)
    
    // Atomic Physics Inputs
    aAtomicPopulations  : ARRAY[0..2] OF LREAL; (* State populations: [0]=5s2 1S0, [1]=5s5p 3P0, [2]=Excited states *)
END_VAR

VAR_OUTPUT
    ePackMLState        : INT;            (* Current PackML State (0=Cleared,1=Stopped,2=Starting,3=Execute,4=Holding,5=Aborting,6=Aborted,7=Stopping) *)
    bError              : BOOL;           (* System Error Flag *)
    nErrorID            : UDINT;          (* Error ID code *)
    
    // Laser Tuning Outputs
    fTrappingLaserTuning: LREAL;          (* AOM/PZT tuning voltage for 813.42 nm laser [V] *)
    fClockLaserTuning   : LREAL;          (* PZT tuning voltage for 698 nm laser [V] *)
    fPiezoDrive         : LREAL;          (* Acoustic damping piezoelectric drive [V] *)
    
    // Comb Actuation Outputs
    fPumpPowerTuning    : LREAL;          (* f_ceo tuning via pump power modulation [V] *)
    fCavityLengthTuning : LREAL;          (* f_rep tuning via cavity length PZT [V] *)
    
    // Process Data
    fClockFrequencyHz   : LREAL;          (* Calculated Output Clock Frequency [Hz] *)
    fStarkShiftNull     : LREAL;          (* Calculated Differential AC Stark Shift [Hz] *)
END_VAR

VAR
    // PackML State Machine
    
    // PID Controllers for Various Loops
    fbPID_Trapping      : FB_PIDController;
    fbPID_PDH           : FB_PIDController;
    fbPID_fRep          : FB_PIDController;
    fbPID_fCEO          : FB_PIDController;
    fbPID_Piezo         : FB_PIDController;
    
    // Magic Wavelength Constants
    cMagicWavelengthTHz : LREAL := 368.554465; (* Magic wavelength for Sr-87 in THz *)
    cClockFreqTHz       : LREAL := 429.228004229873; (* Sr-87 clock transition 1S0 -> 3P0 *)
    
    // State Space Matrices for Atomic System Evolution
    // d(rho)/dt = -i/hbar [H, rho] + L(rho)
    matHamiltonian      : ARRAY[0..2, 0..2] OF LREAL;
    matDensity          : ARRAY[0..2, 0..2] OF LREAL;
    
    fDelta              : LREAL;          (* Detuning *)
    fOmega              : LREAL;          (* Rabi Frequency *)
    
    nCycleCount         : ULINT := 0;
END_VAR

(* 
    ========================================================================
    STATE MACHINE IMPLEMENTATION (PackML)
    ========================================================================
*)
IF bAbort THEN
    ePackMLState := 5; (* Aborting *)
ELSIF bStop THEN
    IF ePackMLState <> 1 (* Stopped *) AND ePackMLState <> 7 (* Stopping *) THEN
        ePackMLState := 7; (* Stopping *)
    END_IF
END_IF

CASE ePackMLState OF
    
    0: (* Cleared *)
        bError := FALSE;
        nErrorID := 0;
        IF bExecute THEN
            ePackMLState := 2; (* Starting *)
        END_IF
        
    1: (* Stopped *)
        IF bClear THEN
            ePackMLState := 0; (* Cleared *)
        END_IF
        
    2: (* Starting *)
        // Initialize PID controllers
        fbPID_Trapping(Kp:=2.5, Ki:=0.1, Kd:=0.01, fSetpoint:=cMagicWavelengthTHz, fActualValue:=fTrappingLaserFreq);
        fbPID_PDH(Kp:=10.0, Ki:=50.0, Kd:=0.001, fSetpoint:=0.0, fActualValue:=fPDHErrorSignal);
        fbPID_Piezo(Kp:=5.0, Ki:=0.2, Kd:=0.0, fSetpoint:=0.0, fActualValue:=fPiezoFeedback);
        fbPID_fRep(Kp:=1.0, Ki:=0.05, Kd:=0.0, fSetpoint:=250000000.0, fActualValue:=fRepRateBeat); (* 250 MHz rep rate *)
        fbPID_fCEO(Kp:=0.5, Ki:=0.01, Kd:=0.0, fSetpoint:=20000000.0, fActualValue:=fCEODetect);  (* 20 MHz offset *)
        
        // Initialize State Matrices
        matDensity[0,0] := 1.0; (* Start with 100% ground state *)
        
        ePackMLState := 3; (* Execute *)
        
    3: (* Execute *)
        // Main Control Routines
        
        // 1. Magic Wavelength Optical Lattice Trapping Loop
        // Nulling AC Stark Shift by driving to the magic wavelength
        fbPID_Trapping(fActualValue:=fTrappingLaserFreq);
        fTrappingLaserTuning := fbPID_Trapping.fOutput;
        fStarkShiftNull := (fTrappingLaserFreq - cMagicWavelengthTHz) * 1.5e-3; (* Approximated coefficient *)
        
        // 2. Clock Laser & Pound-Drever-Hall Feedback
        // Active locking to high-finesse cavity
        fbPID_PDH(fActualValue:=fPDHErrorSignal);
        fClockLaserTuning := fbPID_PDH.fOutput;
        
        // Piezo acoustic damping
        fbPID_Piezo(fActualValue:=fPiezoFeedback);
        fPiezoDrive := -fbPID_Piezo.fOutput; (* Negative feedback *)
        
        // 3. Femtosecond Frequency Comb Control
        fbPID_fRep(fActualValue:=fRepRateBeat);
        fCavityLengthTuning := fbPID_fRep.fOutput;
        
        fbPID_fCEO(fActualValue:=fCEODetect);
        fPumpPowerTuning := fbPID_fCEO.fOutput;
        
        // 4. Atomic Physics Transition Matrix Evolution (Rabi oscillations)
        fDelta := (cClockFreqTHz * 1e12) - ((fRepRateBeat * 1716912.0) + fCEODetect);
        fOmega := (fTrappingLaserPower) * 5.0; // Approximation of Rabi frequency
        IF fOmega < 0.0 THEN fOmega := -fOmega; END_IF; // Absolute value alternative
        
        matHamiltonian[0,1] := fOmega / 2.0;
        matHamiltonian[1,0] := fOmega / 2.0;
        matHamiltonian[1,1] := fDelta;
        
        // Calculate Output Clock Frequency (Optical -> RF Downconversion)
        fClockFrequencyHz := (1716912.0 * fRepRateBeat) + fCEODetect + fStarkShiftNull;
        
        nCycleCount := nCycleCount + 1;
        
        // Condition to move to completed or error
        IF fPDHErrorSignal > 5.0 OR fPDHErrorSignal < -5.0 THEN
            bError := TRUE;
            nErrorID := 16#C0FFEE;
            ePackMLState := 4; (* Holding *)
        END_IF
        
    4: (* Holding *)
        IF NOT bError THEN
            ePackMLState := 3; (* Execute *)
        END_IF
        IF bAbort THEN
            ePackMLState := 5; (* Aborting *)
        END_IF
        
    5: (* Aborting *)
        fTrappingLaserTuning := 0.0;
        fClockLaserTuning := 0.0;
        fPiezoDrive := 0.0;
        fPumpPowerTuning := 0.0;
        fCavityLengthTuning := 0.0;
        ePackMLState := 6; (* Aborted *)
        
    6: (* Aborted *)
        IF bClear THEN
            ePackMLState := 0; (* Cleared *)
        END_IF
        
    7: (* Stopping *)
        fTrappingLaserTuning := 0.0;
        fClockLaserTuning := 0.0;
        ePackMLState := 1; (* Stopped *)
        
END_CASE

END_FUNCTION_BLOCK

(* Dummy PID Controller implementation for completeness *)
FUNCTION_BLOCK FB_PIDController
VAR_INPUT
    Kp          : LREAL;
    Ki          : LREAL;
    Kd          : LREAL;
    fSetpoint   : LREAL;
    fActualValue: LREAL;
END_VAR
VAR_OUTPUT
    fOutput     : LREAL;
END_VAR
VAR
    fError      : LREAL;
    fLastError  : LREAL;
    fIntegral   : LREAL;
    fDerivative : LREAL;
END_VAR
    fError := fSetpoint - fActualValue;
    fIntegral := fIntegral + fError;
    fDerivative := fError - fLastError;
    fOutput := (Kp * fError) + (Ki * fIntegral) + (Kd * fDerivative);
    fLastError := fError;
END_FUNCTION_BLOCK
```"""

entry = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

file_path = "c:\\\\Users\\\\majip\\\\Downloads\\\\LLM REASEARCH\\\\data\\\\synthetic_generation_v3_enterprise.jsonl"
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\\n")
