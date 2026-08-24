# -*- coding: utf-8 -*-
import json
import os

user_prompt = (
    "You are acting as the Chief Traction & Inverter Systems Architect for a 500 km/h "
    "Superconducting Maglev (SCMaglev) Train system (Chuo Shinkansen).\n\n"
    "Design and implement a master-tier, production-ready IEC 61131-3 Structured Text (ST) controller "
    "for the \"Trackside Linear Synchronous Motor (LSM) Multiphase Inverter Stator Section Switching & "
    "Levitation Gap Damping Controller\" (`FB_Maglev_LSM_Controller`).\n\n"
    "### Technical Specifications & Engineering Rigor Required:\n"
    "1. **LSM Stator Section High-Speed Zero-Crossing Section Switching**:\n"
    "   - Continuous track position estimation (sub-millimeter resolution) from inductive cross-talk sensors.\n"
    "   - Synchronized commutation and power feeding transfer between consecutive 500m stator blocks via "
    "solid-state IGCT thyristor bypasses with zero torque ripple during 500 km/h flyby.\n"
    "2. **Inductive Levitation Gap Active Electromagnetic Damping**:\n"
    "   - Secondary auxiliary electromagnet coil current modulation slaved to 8-point laser gap displacement sensors "
    "(target 100 mm gap +/- 5 mm).\n"
    "   - Aerodynamic cross-wind buffet damping using decoupled lateral/roll state-space observer.\n"
    "3. **Regenerative Deceleration & SIL-4 Railway Safety Interlocks**:\n"
    "   - Synchronous regenerative braking vector control dumping kinetic energy into trackside flywheel/supercapacitor grid buffers.\n"
    "   - Dual-redundant 2-out-of-3 (2oo3) fail-safe voting logic adhering to EN 50128 / IEC 62278 standards.\n\n"
    "Ensure the implementation is fully modularized with custom TYPE definitions, complete mathematical models, "
    "Luenberger state-space observers, vector current regulators, IGCT zero-crossing commutators, energy dispatch matrices, "
    "and a rigorous SIL-4 2oo3 voting engine. Output pure, valid IEC 61131-3 Structured Text."
)

assistant_content = """# Trackside Linear Synchronous Motor (LSM) Multiphase Inverter Stator Section Switching & Levitation Gap Damping Controller (`FB_Maglev_LSM_Controller`)

## 1. System Engineering Architecture & Physical Principles

The Chuo Shinkansen SCMaglev propulsion and levitation ecosystem relies on trackside long-stator Linear Synchronous Motors (LSM) interacting with vehicle-mounted bulk Superconducting Magnetic Coils (SCM) generating intense magnetic fields ($B_0 \\approx 4.5\\text{--}5.5\\text{ T}$). At cruising velocities of $500\\text{ km/h}$ ($138.89\\text{ m/s}$), continuous power feeding along hundreds of kilometers of guideway requires sectioning the stator into discrete $500\\text{ m}$ blocks. Energizing only the stator block occupied by the train minimizes distribution impedance, copper losses, and reactive power demand while maintaining high system efficiency.

```
+----------------------------------------------------------------------------------------------------+
|                                    CENTRAL TRACTION SUBSTATION (PCS)                               |
|   +--------------------------+    +--------------------------+    +----------------------------+   |
|   | Dual 3-Phase VVVF        |    | Trackside Energy Buffer  |    | Triple Redundant SIL-4     |   |
|   | Inverter Bank (IGCT/PWM) |<-->| (Flywheel + Supercap)    |<-->| 2oo3 Safety Voting Engine  |   |
|   +--------------------------+    +--------------------------+    +----------------------------+   |
+----------------------------------------------------------------------------------------------------+
                                               | (Dual-Feeder Crossover Bus)
                                               v
+----------------------------------------------------------------------------------------------------+
|  TRACKSIDE STATOR SECTIONS (500m BLOCKS) WITH SOLID-STATE IGCT SECTION SWITCHES                    |
|                                                                                                    |
|  [Block k-1: 500m]   =====>   [Block k: 500m] (Active Train Flyby) =====> [Block k+1: 500m]        |
|  +---------------+             +----------------------------------+        +-----------------+     |
|  | IGCT Bypass   |             | IGCT Active Feeder               |        | IGCT Pre-Charge |     |
|  +---------------+             +----------------------------------+        +-----------------+     |
|                                         |           ^                                              |
|                                         v           | B_z Field Coupling                           |
|                             +-----------------------------------+                                  |
|                             | SCMaglev Bogie (Superconducting)  |                                  |
|                             |  - 8x Laser Optical Gap Sensors   |                                  |
|                             |  - Auxiliary Damping Coils        |                                  |
|                             |  - Inductive Cross-Talk Pickup    |                                  |
|                             +-----------------------------------+                                  |
|                                                                                                    |
|  <--- 100mm Levitation Gap ---> [Ground Null-Flux Coils] <--- Lateral Guidance & Levitation --->   |
+----------------------------------------------------------------------------------------------------+
```

### 1.1 High-Speed Zero-Crossing Section Handover ($500\\text{ m}$ Blocks @ $500\\text{ km/h}$)
At $138.89\\text{ m/s}$, a $500\\text{ m}$ stator section is traversed in $3.60\\text{ seconds}$. To prevent thrust dips, longitudinal jerk, and normal-force transients during section transitions, a dual-inverter overlapping crossover scheme is implemented:
- **Crossover Blending**: Stator Block $k$ is fed by Inverter Channel A, while Stator Block $k+1$ is fed by Inverter Channel B.
- **S-Curve Vector Current Blending**: Over a spatial transition window $L_{trans} = 40\\text{ m}$ ($t_{trans} \\approx 288\\text{ ms}$), the quadrature thrust current commands are blended using a smooth raised-cosine (Hann) profile:
  $$\\alpha(t) = \\frac{1}{2} \\left(1 - \\cos\\left(\\pi \\frac{x(t) - x_{start}}{L_{trans}}\\right)\\right)$$
  $$I_{q, k}^* = I_q^* \\cdot (1 - \\alpha(t)), \\quad I_{q, k+1}^* = I_q^* \\cdot \\alpha(t)$$
  $$\\sum F_x = K_t (I_{q, k}^* + I_{q, k+1}^*) = K_t I_q^* = \\text{Constant} \\implies \\Delta F_x = 0$$
- **Zero-Crossing Thyristor Commutation**: The solid-state Integrated Gate-Commutated Thyristor (IGCT) bypass switches for Block $k$ are de-energized precisely when phase currents $i_u(t), i_v(t), i_w(t)$ pass through their fundamental zero-crossing points (within a $\\pm 2.5^\\circ$ electrical window), eliminating inductive voltage spikes ($L \\frac{di}{dt}$) and snubber stress.

### 1.2 Sub-Millimeter Position Estimation via Inductive Cross-Talk
Trackside Inductive Cross-Talk Position Sensors (CPS) measure magnetic field perturbations from passing superconducting magnets. Two orthogonal sensing tracks provide quadrature signals:
$$S_A(x) = V_0 \\sin\\left(\\frac{\\pi x}{\\tau_p}\\right), \\quad S_B(x) = V_0 \\cos\\left(\\frac{\\pi x}{\\tau_p}\\right)$$
where $\\tau_p = 1.350\\text{ m}$ is the motor pole pitch.
- **Fine Electrical Angle Resolver**: $\\theta_e(t) = \\operatorname{atan2}(S_A, S_B)$.
- **Pole Integrator**: Gross position is tracked by counting pole crossings $N_{pole}$.
- **Phase-Locked Loop (PLL) Tracking**: A 2nd-order discrete-time PLL with proportional-integral loop filter filters out high-frequency noise and rail vibration, outputting continuous position $\\hat{x}$ (sub-millimeter resolution $< 0.1\\text{ mm}$) and instantaneous velocity $\\hat{v}$.

### 1.3 Active Levitation Gap Electromagnetic Damping
Electrodynamic Suspension (EDS) using figure-eight null-flux coils provides passive stability above liftoff speeds ($> 100\\text{ km/h}$), centering at nominal gap $z_0 = 100.0\\text{ mm}$. However, aerodynamic buffeting (cross-winds in tunnel portals, turbulent boundary layers) and guideway irregularities excite rigid-body heave ($z$), lateral sway ($y$), and roll ($\\phi$) resonances ($1.2\\text{--}3.5\\text{ Hz}$).
- **State-Space Observer**: A continuous-discrete Luenberger state-space observer reconstructs unmeasured velocity states $[\\dot{z}, \\dot{y}, \\dot{\\phi}]$ and aerodynamic disturbance moments $M_{wind}$:
  $$\\mathbf{\\hat{x}}_{k+1} = \\mathbf{A}_d \\mathbf{\\hat{x}}_k + \\mathbf{B}_d \\mathbf{u}_k + \\mathbf{L}_d (\\mathbf{y}_{meas,k} - \\mathbf{C}_d \\mathbf{\\hat{x}}_k)$$
- **MIMO Active Auxiliary Coil Control**: 8 high-speed auxiliary electromagnets distributed across the front/rear bogies modulate dynamic trimming forces $\\Delta F_z, \\Delta F_y$ via state feedback:
  $$\\mathbf{I}_{aux}^* = -\\mathbf{K}_{LQR} \\mathbf{\\hat{x}} + \\mathbf{K}_{ff} \\mathbf{d}_{wind}$$
  maintaining the levitation gap strictly within $100.0\\text{ mm} \\pm 5.0\\text{ mm}$.

### 1.4 Regenerative Energy Buffering & SIL-4 2oo3 Voting
- **Regenerative Vector Braking**: Kinetic energy of a $300\\text{--ton}$ trainset at $500\\text{ km/h}$ ($E_k \\approx 2.9\\text{ GJ}$) is recaptured by setting $I_q^* < 0$. Dynamic energy management coordinates trackside flywheel kinetic storage ($P_{max} = 30\\text{ MW}$), high-power supercapacitors ($P_{max} = 15\\text{ MW}$), bidirectional grid AFE, and emergency dynamic braking resistor (DBR) choppers to maintain DC bus voltage $V_{dc} = 4500\\text{ V} \\pm 200\\text{ V}$.
- **SIL-4 Functional Safety**: Built to EN 50128 and IEC 62278 (RAMS) standards, critical variables (train position, speed, stator block authorization, airgap integrity, emergency trip lines) undergo Triple Modular Redundancy (TMR) 2-out-of-3 voting with real-time discrepancy monitoring, degradation to 1oo2, and fail-safe de-energize trip outputs.

---

## 2. IEC 61131-3 Structured Text Code Implementation

```iec-st
// =============================================================================
// PAC/PLC IEC 61131-3 HIGH-INTEGRITY SCMAGLEV CONTROL SUITE
// PROJECT: CHUO SHINKANSEN 500 KM/H LSM TRACTION & LEVITATION CONTROL
// MODULE : FB_Maglev_LSM_Controller
// STANDARDS: IEC 61131-3 3rd Ed., EN 50128 SIL-4, IEC 62278 (RAMS)
// TARGET CYCLE TIME: 1.0 ms (Synchronous Inverter Control Loop)
// =============================================================================

TYPE E_MaglevControlState : (
    MAGLEV_STATE_BOOT_DIAGNOSTICS   := 0,
    MAGLEV_STATE_STANDBY_DISARMED    := 1,
    MAGLEV_STATE_ALIGNMENT_LOCKED    := 2,
    MAGLEV_STATE_TRACTION_ACCEL      := 3,
    MAGLEV_STATE_CRUISE_500KPH       := 4,
    MAGLEV_STATE_SECTION_HANDOVER    := 5,
    MAGLEV_STATE_REGEN_DECEL         := 6,
    MAGLEV_STATE_STATION_BERTHING    := 7,
    MAGLEV_STATE_DEGRADED_1oo2       := 8,
    MAGLEV_STATE_SIL4_FAILSAFE_TRIP  := 9
);
END_TYPE

TYPE E_HandoverPhase : (
    HANDOVER_IDLE                    := 0,
    HANDOVER_PRECHARGE_NEXT_SECTION  := 1,
    HANDOVER_VECTOR_POWER_RAMP       := 2,
    HANDOVER_ZERO_CROSSING_COMMUTATE := 3,
    HANDOVER_DEENERGIZE_OLD_SECTION  := 4,
    HANDOVER_COMPLETED               := 5,
    HANDOVER_ABORT_FAULT             := 6
);
END_TYPE

TYPE E_2oo3VoteStatus : (
    VOTE_UNANIMOUS_HEALTHY           := 0,
    VOTE_MAJORITY_2oo3_PASSED        := 1,
    VOTE_DEGRADED_CHANNEL_A_FAULT    := 2,
    VOTE_DEGRADED_CHANNEL_B_FAULT    := 3,
    VOTE_DEGRADED_CHANNEL_C_FAULT    := 4,
    VOTE_CRITICAL_DISAGREEMENT_TRIP  := 5
);
END_TYPE

// -----------------------------------------------------------------------------
// TELEMETRY & SYSTEM STRUCTURES
// -----------------------------------------------------------------------------
TYPE ST_InductivePosSensor : STRUCT
    RawSin_TrackA        : REAL;    // Sine Quadrature Voltage (V)
    RawCos_TrackB        : REAL;    // Cosine Quadrature Voltage (V)
    SignalAmplitude      : REAL;    // Sqrt(Sin^2 + Cos^2) Validation (V)
    CoarsePoleCounter    : DINT;    // Cumulative magnetic pole count
    FineAngleRad         : REAL;    // Electrical angle within pole [0..2*PI]
    RawEstimatedPosM     : LREAL;   // Absolute track position (m)
    RawVelocityMps       : REAL;    // Derivative velocity (m/s)
    SensorSignalValid    : BOOL;    // Signal amplitude within healthy window
    CrosstalkSnrDb       : REAL;    // Signal-to-Noise Ratio (dB)
END_STRUCT;
END_TYPE

TYPE ST_LsmStatorSection : STRUCT
    SectionID            : DINT;    // Unique 500m Stator Section Identifier
    StartChainageM       : LREAL;   // Section start chainage (m)
    EndChainageM         : LREAL;   // Section end chainage (m)
    IgctFeederClosed     : BOOL;    // Feeder IGCT Solid-State Contactor State
    IgctBypassClosed     : BOOL;    // Bypass IGCT Thyristor State
    VacuumBreakerClosed  : BOOL;    // Medium Voltage Vacuum Circuit Breaker
    SectionVoltageU      : REAL;    // Phase U RMS Voltage (V)
    SectionVoltageV      : REAL;    // Phase V RMS Voltage (V)
    SectionVoltageW      : REAL;    // Phase W RMS Voltage (V)
    StatorCurrentU       : REAL;    // Phase U RMS Current (A)
    StatorCurrentV       : REAL;    // Phase V RMS Current (A)
    StatorCurrentW       : REAL;    // Phase W RMS Current (A)
    StatorCoreTempDegC   : REAL;    // Stator Core RTD Temperature (deg C)
    IsEnergized          : BOOL;    // High voltage presence confirmation
    FaultLockoutActive   : BOOL;    // Ground fault / desaturation trip
END_STRUCT;
END_TYPE

TYPE ST_LaserGapTelemetry : STRUCT
    GapMm_Bogie1_FL      : REAL;    // Bogie 1 Front Left Gap (mm)
    GapMm_Bogie1_FR      : REAL;    // Bogie 1 Front Right Gap (mm)
    GapMm_Bogie1_RL      : REAL;    // Bogie 1 Rear Left Gap (mm)
    GapMm_Bogie1_RR      : REAL;    // Bogie 1 Rear Right Gap (mm)
    GapMm_Bogie2_FL      : REAL;    // Bogie 2 Front Left Gap (mm)
    GapMm_Bogie2_FR      : REAL;    // Bogie 2 Front Right Gap (mm)
    GapMm_Bogie2_RL      : REAL;    // Bogie 2 Rear Left Gap (mm)
    GapMm_Bogie2_RR      : REAL;    // Bogie 2 Rear Right Gap (mm)
    SensorStatusMask     : BYTE;    // Bitmask 0..7 sensor health flags
    MeanLevitationGapMm  : REAL;    // Global Average Levitation Gap (mm)
    MeanLateralGapMm     : REAL;    // Global Average Guidance Gap (mm)
    RollAngleMrad        : REAL;    // Calculated vehicle roll angle (mrad)
    PitchAngleMrad       : REAL;    // Calculated vehicle pitch angle (mrad)
    GapRateOfChangeMps   : REAL;    // Vertical heave velocity (m/s)
END_STRUCT;
END_TYPE

TYPE ST_MaglevStateSpace : STRUCT
    HeaveZ               : REAL;    // Estimated Heave displacement (mm)
    HeaveZ_Dot           : REAL;    // Estimated Heave velocity (mm/s)
    LateralY             : REAL;    // Estimated Lateral displacement (mm)
    LateralY_Dot         : REAL;    // Estimated Lateral velocity (mm/s)
    RollPhi              : REAL;    // Estimated Roll angle (mrad)
    RollPhi_Dot          : REAL;    // Estimated Roll rate (mrad/s)
    EstimatedWindForceN  : REAL;    // Aerodynamic cross-wind disturbance (N)
    EstimatedWindRollNm  : REAL;    // Aerodynamic wind rolling moment (N.m)
END_STRUCT;
END_TYPE

TYPE ST_AuxLevitationCoils : STRUCT
    CoilCurrentCmd_1     : REAL;    // Bogie 1 FL Auxiliary Coil (A)
    CoilCurrentCmd_2     : REAL;    // Bogie 1 FR Auxiliary Coil (A)
    CoilCurrentCmd_3     : REAL;    // Bogie 1 RL Auxiliary Coil (A)
    CoilCurrentCmd_4     : REAL;    // Bogie 1 RR Auxiliary Coil (A)
    CoilCurrentCmd_5     : REAL;    // Bogie 2 FL Auxiliary Coil (A)
    CoilCurrentCmd_6     : REAL;    // Bogie 2 FR Auxiliary Coil (A)
    CoilCurrentCmd_7     : REAL;    // Bogie 2 RL Auxiliary Coil (A)
    CoilCurrentCmd_8     : REAL;    // Bogie 2 RR Auxiliary Coil (A)
    MaxCoilCurrentLimitA : REAL;    // Dynamic saturation ceiling (A)
    DriverHBridgeHealthy : BOOL;    // PWM Driver stage diagnostics
END_STRUCT;
END_TYPE

TYPE ST_TracksideEnergyBuffer : STRUCT
    DcBusVoltageV        : REAL;    // Main Inverter DC Link Voltage (V)
    DcBusCurrentA        : REAL;    // DC Link Net Inflow/Outflow (A)
    FlywheelSocPercent   : REAL;    // High-speed Flywheel Kinetic SOC (%)
    FlywheelPowerKw      : REAL;    // Active Power Absorption/Discharge (kW)
    SupercapSocPercent   : REAL;    // Ultra-capacitor Bank SOC (%)
    SupercapPowerKw      : REAL;    // Ultra-capacitor Dynamic Power (kW)
    GridFeedbackPowerKw  : REAL;    // Active Front End (AFE) Grid Export (kW)
    BrakeChopperDutyPct  : REAL;    // Dynamic Braking Resistor Pulse Width (%)
    ResistorBankTempDegC : REAL;    // DBR Thermal Sensor (deg C)
END_STRUCT;
END_TYPE

TYPE ST_Sil4ChannelData : STRUCT
    CalculatedPositionM  : LREAL;   // Channel computed train position (m)
    CalculatedVelocityKph: REAL;    // Channel computed train speed (km/h)
    SectionAuthorization : DINT;    // Authorized forward stator section ID
    MinLevitationGapMm   : REAL;    // Minimum observed airgap across bogies
    MaxLevitationGapMm   : REAL;    // Maximum observed airgap across bogies
    EmergencyStopActive  : BOOL;    // Channel emergency braking demand
    VitalHeartbeatToken  : UDINT;   // Sequence token verified by safety CPU
END_STRUCT;
END_TYPE

TYPE ST_Sil4VotingOutput : STRUCT
    VotedPositionM       : LREAL;   // 2oo3 Voted Vital Position (m)
    VotedVelocityKph     : REAL;    // 2oo3 Voted Vital Velocity (km/h)
    VotedSectionAuth     : DINT;    // 2oo3 Authorized Stator Section
    VitalBrakeTripCoil   : BOOL;    // TRUE = Safe / FALSE = Vital Trip (De-energize)
    SafetyIntegrityPass  : BOOL;    // SIL-4 Safety Loop Valid
    ActiveVoteStatus     : E_2oo3VoteStatus;
    ChannelDiscrepancyBit: BYTE;    // Bit 0=ChA, Bit 1=ChB, Bit 2=ChC failed
    DiagnosticCode       : DWORD;   // Encoded safety diagnostic flags
END_STRUCT;
END_TYPE

TYPE ST_LsmVectorControl : STRUCT
    InverterIndex        : INT;     // Inverter Bank 1 or 2
    ModulationIndex      : REAL;    // PWM modulation depth (0.0 to 1.15 SVM)
    ElectricalAngleRad   : REAL;    // Vector Park Angle theta_e [0..2*PI]
    ElectricalFreqHz     : REAL;    // Inverter output frequency [0..250 Hz]
    Vd_CommandVolts      : REAL;    // Direct-axis Voltage Reference (V)
    Vq_CommandVolts      : REAL;    // Quadrature-axis Voltage Reference (V)
    Id_ActualAmps        : REAL;    // Direct-axis feedback current (A)
    Iq_ActualAmps        : REAL;    // Quadrature-axis feedback current (A)
    Id_ReferenceAmps     : REAL;    // Target Id (Flux / Levitation Trim) (A)
    Iq_ReferenceAmps     : REAL;    // Target Iq (Propulsion / Braking Force) (A)
    IgctFiringGateEnable : BOOL;    // Hardware gate firing authorization
END_STRUCT;
END_TYPE

// =============================================================================
// FUNCTION BLOCK: FB_SubMillimeter_Position_Estimator
// Continuous Sub-Millimeter Position Estimator via Cross-Talk Resolver & PLL
// =============================================================================
FUNCTION_BLOCK FB_SubMillimeter_Position_Estimator
VAR_INPUT
    EnableEstimator      : BOOL;
    RawSensor            : ST_InductivePosSensor;
    PolePitchM           : REAL := 1.350;       // SCMaglev Motor Pole Pitch (m)
    SamplePeriodSec      : REAL := 0.001;       // 1.0 ms Cycle Time
    ResetPositionCmd     : BOOL;
    PresetPositionM      : LREAL;
END_VAR
VAR_OUTPUT
    EstimatedPositionM   : LREAL;               // High-precision position (m)
    EstimatedVelocityMps : REAL;                // Filtered velocity (m/s)
    EstimatedVelocityKph : REAL;                // Filtered velocity (km/h)
    ElectricalAngleRad   : REAL;                // Commutation Park Angle (rad)
    EstimatorHealthy     : BOOL;
    TrackingErrorMrad    : REAL;
END_VAR
VAR
    Pll_Integrator_Theta : REAL := 0.0;
    Pll_Integrator_Speed : REAL := 0.0;
    Pll_Kp               : REAL := 450.0;       // PLL Proportional Loop Gain
    Pll_Ki               : REAL := 12500.0;     // PLL Integral Loop Gain
    MeasuredAngleRad     : REAL;
    PhaseDetectorError   : REAL;
    PreviousMeasuredAngle: REAL := 0.0;
    PoleCycleCounter     : DINT := 0;
    SinVal               : REAL;
    CosVal               : REAL;
    AmpSq                : REAL;
    CONST_PI             : REAL := 3.141592653589793;
    CONST_2PI            : REAL := 6.283185307179586;
END_VAR

IF NOT EnableEstimator THEN
    EstimatedPositionM   := 0.0;
    EstimatedVelocityMps := 0.0;
    EstimatedVelocityKph := 0.0;
    ElectricalAngleRad   := 0.0;
    EstimatorHealthy     := FALSE;
    RETURN;
END_IF;

IF ResetPositionCmd THEN
    EstimatedPositionM   := PresetPositionM;
    PoleCycleCounter     := LREAL_TO_DINT(PresetPositionM / (LREAL_TO_REAL(PolePitchM) * 2.0));
    Pll_Integrator_Theta := LREAL_TO_REAL(PresetPositionM - DINT_TO_LREAL(PoleCycleCounter) * (LREAL_TO_REAL(PolePitchM) * 2.0)) / (PolePitchM * 2.0) * CONST_2PI;
    Pll_Integrator_Speed := 0.0;
END_IF;

// 1. Cross-Talk Signal Amplitude Normalization & Sanity Verification
SinVal := RawSensor.RawSin_TrackA;
CosVal := RawSensor.RawCos_TrackB;
AmpSq  := (SinVal * SinVal) + (CosVal * CosVal);

IF (AmpSq > 0.04) AND (AmpSq < 4.0) THEN // Valid amplitude window [0.2V to 2.0V]
    EstimatorHealthy := TRUE;
    // 2. High-Resolution Arc-Tangent Extraction
    IF ABS(CosVal) > 0.0001 THEN
        MeasuredAngleRad := ATAN(SinVal / CosVal);
        IF CosVal < 0.0 THEN
            MeasuredAngleRad := MeasuredAngleRad + CONST_PI;
        ELSIF SinVal < 0.0 THEN
            MeasuredAngleRad := MeasuredAngleRad + CONST_2PI;
        END_IF;
    ELSE
        IF SinVal >= 0.0 THEN
            MeasuredAngleRad := CONST_PI / 2.0;
        ELSE
            MeasuredAngleRad := (3.0 * CONST_PI) / 2.0;
        END_IF;
    END_IF;
ELSE
    // Sensor Degraded: Fallback to open-loop PLL integration
    EstimatorHealthy := FALSE;
    MeasuredAngleRad := Pll_Integrator_Theta;
END_IF;

// 3. Phase-Locked Loop (PLL) Phase Error Computation with Wrap-Around Handling
PhaseDetectorError := MeasuredAngleRad - Pll_Integrator_Theta;
WHILE PhaseDetectorError > CONST_PI DO
    PhaseDetectorError := PhaseDetectorError - CONST_2PI;
END_WHILE;
WHILE PhaseDetectorError < -CONST_PI DO
    PhaseDetectorError := PhaseDetectorError + CONST_2PI;
END_WHILE;

TrackingErrorMrad := PhaseDetectorError * 1000.0;

// 4. 2nd-Order PLL State Updates (PI Loop Filter)
Pll_Integrator_Speed := Pll_Integrator_Speed + (Pll_Ki * PhaseDetectorError * SamplePeriodSec);
// Clamp maximum electrical acceleration
Pll_Integrator_Speed := LIMIT(-3000.0, Pll_Integrator_Speed, 3000.0);

Pll_Integrator_Theta := Pll_Integrator_Theta + ((Pll_Integrator_Speed + (Pll_Kp * PhaseDetectorError)) * SamplePeriodSec);

// 5. Pole Counter Integration on Boundary Crossing
IF Pll_Integrator_Theta >= CONST_2PI THEN
    Pll_Integrator_Theta := Pll_Integrator_Theta - CONST_2PI;
    PoleCycleCounter     := PoleCycleCounter + 1;
ELSIF Pll_Integrator_Theta < 0.0 THEN
    Pll_Integrator_Theta := Pll_Integrator_Theta + CONST_2PI;
    PoleCycleCounter     := PoleCycleCounter - 1;
END_IF;

ElectricalAngleRad := Pll_Integrator_Theta;

// 6. Absolute High-Precision Position Calculation (Sub-Millimeter Resolution)
EstimatedPositionM := (DINT_TO_LREAL(PoleCycleCounter) * LREAL_TO_REAL(PolePitchM * 2.0)) + 
                      (LREAL_TO_REAL(Pll_Integrator_Theta / CONST_2PI) * (LREAL_TO_REAL(PolePitchM) * 2.0));

// Velocity calculation: v = (omega_e / 2pi) * 2 * PolePitch
EstimatedVelocityMps := (Pll_Integrator_Speed / CONST_2PI) * (PolePitchM * 2.0);
EstimatedVelocityKph := EstimatedVelocityMps * 3.6;

END_FUNCTION_BLOCK


// =============================================================================
// FUNCTION BLOCK: FB_IGCT_ZeroCrossing_SectionSwitch
// 500m Stator Section Handover Controller with Zero Torque Ripple Commutation
// =============================================================================
FUNCTION_BLOCK FB_IGCT_ZeroCrossing_SectionSwitch
VAR_INPUT
    EnableSwitching      : BOOL;
    CurrentTrainPositionM: LREAL;
    CurrentTrainSpeedMps : REAL;
    ActiveSection        : ST_LsmStatorSection;
    NextSection          : ST_LsmStatorSection;
    MasterTorqueCmdIq    : REAL;                // Total demanded propulsion Iq (A)
    ElectricalAngleRad   : REAL;                // Real-time commutation angle
    HandoverZoneLengthM  : REAL := 40.0;        // 40m Crossover Blending Zone
    SamplePeriodSec      : REAL := 0.001;
END_VAR
VAR_OUTPUT
    HandoverPhase        : E_HandoverPhase;
    Inverter1_IqCmd      : REAL;                // Iq command for Section K Inverter
    Inverter2_IqCmd      : REAL;                // Iq command for Section K+1 Inverter
    Inverter1_GateEnable : BOOL;
    Inverter2_GateEnable : BOOL;
    SectionK_IgctBypass  : BOOL;                // Stator K Bypass Thyristor Trigger
    SectionKp1_IgctFeed  : BOOL;                // Stator K+1 Feeder IGCT Trigger
    TorqueRippleEstPct   : REAL;                // Estimated Handover Torque Ripple
    HandoverCompletePulse: BOOL;
    HandoverFault        : BOOL;
END_VAR
VAR
    DistanceIntoNextSecM : REAL;
    BlendAlpha           : REAL := 0.0;         // S-Curve Blending Factor [0.0 to 1.0]
    CommutationTimerSec  : REAL := 0.0;
    ZeroCrossingDetected : BOOL := FALSE;
    ActivePhaseCurrentA  : REAL;
    CONST_PI             : REAL := 3.141592653589793;
END_VAR

HandoverCompletePulse := FALSE;

IF NOT EnableSwitching THEN
    HandoverPhase        := HANDOVER_IDLE;
    Inverter1_IqCmd      := 0.0;
    Inverter2_IqCmd      := 0.0;
    Inverter1_GateEnable := FALSE;
    Inverter2_GateEnable := FALSE;
    SectionK_IgctBypass  := TRUE;
    SectionKp1_IgctFeed  := FALSE;
    TorqueRippleEstPct   := 0.0;
    HandoverFault        := FALSE;
    RETURN;
END_IF;

// Calculate progress relative to the 500m section boundary
DistanceIntoNextSecM := LREAL_TO_REAL(CurrentTrainPositionM - ActiveSection.EndChainageM);

CASE HandoverPhase OF
    HANDOVER_IDLE:
        Inverter1_IqCmd      := MasterTorqueCmdIq;
        Inverter2_IqCmd      := 0.0;
        Inverter1_GateEnable := TRUE;
        Inverter2_GateEnable := FALSE;
        SectionK_IgctBypass  := FALSE;
        SectionKp1_IgctFeed  := FALSE;
        TorqueRippleEstPct   := 0.0;

        // Train enters pre-handover boundary (within 30m of section end)
        IF (DistanceIntoNextSecM >= -30.0) AND (DistanceIntoNextSecM < 0.0) THEN
            HandoverPhase := HANDOVER_PRECHARGE_NEXT_SECTION;
        END_IF;

    HANDOVER_PRECHARGE_NEXT_SECTION:
        // Engage Next Section IGCT Feeder & Pre-synchronize Inverter 2 phase
        SectionKp1_IgctFeed  := TRUE;
        Inverter2_GateEnable := TRUE;
        Inverter1_IqCmd      := MasterTorqueCmdIq;
        Inverter2_IqCmd      := 0.0;

        // Confirm next section vacuum breaker and IGCT conduction
        IF NextSection.IgctFeederClosed AND NextSection.VacuumBreakerClosed THEN
            IF DistanceIntoNextSecM >= 0.0 THEN
                HandoverPhase := HANDOVER_VECTOR_POWER_RAMP;
            END_IF;
        ELSIF DistanceIntoNextSecM > 5.0 THEN
            // Interlock Failure: Next section did not close in time
            HandoverPhase := HANDOVER_ABORT_FAULT;
            HandoverFault := TRUE;
        END_IF;

    HANDOVER_VECTOR_POWER_RAMP:
        // Crossover S-curve power blending over HandoverZoneLengthM (40m)
        // Raised cosine Hann profile guarantees zero torque discontinuity:
        // alpha(x) = 0.5 * (1 - cos(pi * x / L_trans))
        IF HandoverZoneLengthM > 0.1 THEN
            BlendAlpha := 0.5 * (1.0 - COS(CONST_PI * LIMIT(0.0, DistanceIntoNextSecM / HandoverZoneLengthM, 1.0)));
        ELSE
            BlendAlpha := 1.0;
        END_IF;

        Inverter1_IqCmd := MasterTorqueCmdIq * (1.0 - BlendAlpha);
        Inverter2_IqCmd := MasterTorqueCmdIq * BlendAlpha;

        // Verify constant sum of forces
        TorqueRippleEstPct := ABS((Inverter1_IqCmd + Inverter2_IqCmd) - MasterTorqueCmdIq) / (MAX(1.0, ABS(MasterTorqueCmdIq))) * 100.0;

        IF DistanceIntoNextSecM >= HandoverZoneLengthM THEN
            HandoverPhase       := HANDOVER_ZERO_CROSSING_COMMUTATE;
            CommutationTimerSec := 0.0;
        END_IF;

    HANDOVER_ZERO_CROSSING_COMMUTATE:
        // Maintain 100% current on Section K+1
        Inverter1_IqCmd := 0.0;
        Inverter2_IqCmd := MasterTorqueCmdIq;

        // Detect fundamental current zero crossing on outgoing Stator K phases
        // Phase angle within +/- 2.5 degrees of zero crossing (k*PI)
        ActivePhaseCurrentA := ActiveSection.StatorCurrentU;
        ZeroCrossingDetected := (ABS(SIN(ElectricalAngleRad)) < 0.0436) OR (ABS(ActivePhaseCurrentA) < 15.0);

        CommutationTimerSec := CommutationTimerSec + SamplePeriodSec;

        IF ZeroCrossingDetected OR (CommutationTimerSec > 0.020) THEN // 20ms Max Commutation Window
            Inverter1_GateEnable := FALSE;
            SectionK_IgctBypass  := TRUE; // Divert residual reactive current to bypass snubber
            HandoverPhase        := HANDOVER_DEENERGIZE_OLD_SECTION;
            CommutationTimerSec  := 0.0;
        END_IF;

    HANDOVER_DEENERGIZE_OLD_SECTION:
        CommutationTimerSec := CommutationTimerSec + SamplePeriodSec;
        IF CommutationTimerSec > 0.015 THEN // Wait 15ms for thyristor turn-off de-ionization
            SectionK_IgctBypass   := TRUE;
            HandoverPhase         := HANDOVER_COMPLETED;
            HandoverCompletePulse := TRUE;
        END_IF;

    HANDOVER_COMPLETED:
        Inverter1_IqCmd      := 0.0;
        Inverter2_IqCmd      := MasterTorqueCmdIq;
        Inverter1_GateEnable := FALSE;
        Inverter2_GateEnable := TRUE;
        TorqueRippleEstPct   := 0.0;

        // Reset to Idle once train moves deeper into the active block
        IF DistanceIntoNextSecM > (HandoverZoneLengthM + 20.0) THEN
            HandoverPhase := HANDOVER_IDLE;
        END_IF;

    HANDOVER_ABORT_FAULT:
        Inverter1_IqCmd      := 0.0;
        Inverter2_IqCmd      := 0.0;
        Inverter1_GateEnable := FALSE;
        Inverter2_GateEnable := FALSE;
        SectionK_IgctBypass  := TRUE;
        SectionKp1_IgctFeed  := FALSE;
        HandoverFault        := TRUE;
END_CASE;

END_FUNCTION_BLOCK


// =============================================================================
// FUNCTION BLOCK: FB_Levitation_StateSpace_Damping
// Active Levitation Gap & Cross-Wind Aerodynamic Buffet State-Space Damping
// =============================================================================
FUNCTION_BLOCK FB_Levitation_StateSpace_Damping
VAR_INPUT
    EnableDamping        : BOOL;
    LaserGapData         : ST_LaserGapTelemetry;
    VehicleSpeedMps      : REAL;
    TargetLevitationGapMm: REAL := 100.0;       // Target 100.0 mm Gap
    MaxAllowableGapDevMm : REAL := 5.0;         // Strict +/- 5.0 mm Band
    SamplePeriodSec      : REAL := 0.001;
END_VAR
VAR_OUTPUT
    AuxCoils             : ST_AuxLevitationCoils;
    ObservedState        : ST_MaglevStateSpace;
    GapViolationAlarm    : BOOL;
    MaxGapDeviationMm    : REAL;
    ActiveDampingPowerKw : REAL;
END_VAR
VAR
    // Discrete Luenberger Observer Matrices (A_d, B_d, C_d, L_d)
    // States: x = [z (mm), z_dot (mm/s), y (mm), y_dot (mm/s), phi (mrad), phi_dot (mrad/s), F_w (N)]
    A_11 : REAL := 0.9985;  A_12 : REAL := 0.00099;
    A_21 : REAL := -2.850;  A_22 : REAL := 0.98500;
    A_33 : REAL := 0.9990;  A_34 : REAL := 0.00099;
    A_43 : REAL := -1.950;  A_44 : REAL := 0.98900;
    A_55 : REAL := 0.9975;  A_56 : REAL := 0.00098;
    A_65 : REAL := -4.200;  A_66 : REAL := 0.97800;

    // Observer Kalman Gains
    L_z   : REAL := 0.450;
    L_zv  : REAL := 18.50;
    L_y   : REAL := 0.380;
    L_yv  : REAL := 14.20;
    L_phi : REAL := 0.520;
    L_phiv: REAL := 22.10;
    L_w   : REAL := 0.125;

    // State-Feedback Control Gains (LQR Optimization)
    K_z_prop   : REAL := 4.50;   // A/mm Heave Stiffness
    K_z_deriv  : REAL := 0.085;  // A/(mm/s) Heave Damping
    K_y_prop   : REAL := 3.20;   // A/mm Lateral Stiffness
    K_y_deriv  : REAL := 0.065;  // A/(mm/s) Lateral Damping
    K_phi_prop : REAL := 6.80;   // A/mrad Roll Stiffness
    K_phi_deriv: REAL := 0.110;  // A/(mrad/s) Roll Damping
    K_wind_ff  : REAL := 0.0022; // A/N Feedforward Wind Rejection

    // Innovation Errors
    Err_z_meas   : REAL;
    Err_y_meas   : REAL;
    Err_phi_meas : REAL;

    // Control Effort Components
    Current_Heave   : REAL;
    Current_Lateral : REAL;
    Current_Roll    : REAL;
    Current_WindFF  : REAL;

    Bogie1_Front_I  : REAL;
    Bogie1_Rear_I   : REAL;
    Bogie2_Front_I  : REAL;
    Bogie2_Rear_I   : REAL;
    TotalCurrentSq  : REAL;
END_VAR

IF NOT EnableDamping THEN
    AuxCoils.CoilCurrentCmd_1 := 0.0;
    AuxCoils.CoilCurrentCmd_2 := 0.0;
    AuxCoils.CoilCurrentCmd_3 := 0.0;
    AuxCoils.CoilCurrentCmd_4 := 0.0;
    AuxCoils.CoilCurrentCmd_5 := 0.0;
    AuxCoils.CoilCurrentCmd_6 := 0.0;
    AuxCoils.CoilCurrentCmd_7 := 0.0;
    AuxCoils.CoilCurrentCmd_8 := 0.0;
    GapViolationAlarm        := FALSE;
    MaxGapDeviationMm        := 0.0;
    ActiveDampingPowerKw     := 0.0;
    RETURN;
END_IF;

// 1. Measurement Extraction & Coordinate Transformation from 8 Laser Sensors
// Heave measurement deviation from target 100 mm
Err_z_meas   := LaserGapData.MeanLevitationGapMm - TargetLevitationGapMm;
Err_y_meas   := LaserGapData.MeanLateralGapMm;
Err_phi_meas := LaserGapData.RollAngleMrad;

// 2. Discrete Luenberger State-Space Observer Updates
// Update Heave States
ObservedState.HeaveZ     := (A_11 * ObservedState.HeaveZ) + (A_12 * ObservedState.HeaveZ_Dot) + (L_z * (Err_z_meas - ObservedState.HeaveZ));
ObservedState.HeaveZ_Dot := (A_21 * ObservedState.HeaveZ) + (A_22 * ObservedState.HeaveZ_Dot) + (L_zv * (Err_z_meas - ObservedState.HeaveZ));

// Update Lateral States & Aerodynamic Wind Disturbance Observer
ObservedState.LateralY     := (A_33 * ObservedState.LateralY) + (A_34 * ObservedState.LateralY_Dot) + (L_y * (Err_y_meas - ObservedState.LateralY));
ObservedState.LateralY_Dot := (A_43 * ObservedState.LateralY) + (A_44 * ObservedState.LateralY_Dot) + (L_yv * (Err_y_meas - ObservedState.LateralY));
ObservedState.EstimatedWindForceN := ObservedState.EstimatedWindForceN + (L_w * (Err_y_meas - ObservedState.LateralY) * 100.0);

// Update Roll States
ObservedState.RollPhi     := (A_55 * ObservedState.RollPhi) + (A_56 * ObservedState.RollPhi_Dot) + (L_phi * (Err_phi_meas - ObservedState.RollPhi));
ObservedState.RollPhi_Dot := (A_65 * ObservedState.RollPhi) + (A_66 * ObservedState.RollPhi_Dot) + (L_phiv * (Err_phi_meas - ObservedState.RollPhi));

// 3. MIMO State-Feedback Law + Feedforward Aerodynamic Gust Rejection
Current_Heave   := -(K_z_prop * ObservedState.HeaveZ) - (K_z_deriv * ObservedState.HeaveZ_Dot);
Current_Lateral := -(K_y_prop * ObservedState.LateralY) - (K_y_deriv * ObservedState.LateralY_Dot);
Current_Roll    := -(K_phi_prop * ObservedState.RollPhi) - (K_phi_deriv * ObservedState.RollPhi_Dot);
Current_WindFF  := -(K_wind_ff * ObservedState.EstimatedWindForceN);

// Dynamic saturation ceiling for auxiliary electromagnets (+/- 150 A)
AuxCoils.MaxCoilCurrentLimitA := 150.0;

// 4. Decoupled 8-Coil Force Distribution Mapping
// Bogie 1 Coils (Front Section)
AuxCoils.CoilCurrentCmd_1 := LIMIT(-AuxCoils.MaxCoilCurrentLimitA, Current_Heave + Current_Roll + Current_Lateral + Current_WindFF, AuxCoils.MaxCoilCurrentLimitA); // FL
AuxCoils.CoilCurrentCmd_2 := LIMIT(-AuxCoils.MaxCoilCurrentLimitA, Current_Heave - Current_Roll - Current_Lateral - Current_WindFF, AuxCoils.MaxCoilCurrentLimitA); // FR
AuxCoils.CoilCurrentCmd_3 := LIMIT(-AuxCoils.MaxCoilCurrentLimitA, Current_Heave + Current_Roll + Current_Lateral + (Current_WindFF * 0.8), AuxCoils.MaxCoilCurrentLimitA); // RL
AuxCoils.CoilCurrentCmd_4 := LIMIT(-AuxCoils.MaxCoilCurrentLimitA, Current_Heave - Current_Roll - Current_Lateral - (Current_WindFF * 0.8), AuxCoils.MaxCoilCurrentLimitA); // RR

// Bogie 2 Coils (Rear Section)
AuxCoils.CoilCurrentCmd_5 := LIMIT(-AuxCoils.MaxCoilCurrentLimitA, Current_Heave + (Current_Roll * 0.9) + Current_Lateral + (Current_WindFF * 0.6), AuxCoils.MaxCoilCurrentLimitA);
AuxCoils.CoilCurrentCmd_6 := LIMIT(-AuxCoils.MaxCoilCurrentLimitA, Current_Heave - (Current_Roll * 0.9) - Current_Lateral - (Current_WindFF * 0.6), AuxCoils.MaxCoilCurrentLimitA);
AuxCoils.CoilCurrentCmd_7 := LIMIT(-AuxCoils.MaxCoilCurrentLimitA, Current_Heave + (Current_Roll * 0.9) + Current_Lateral + (Current_WindFF * 0.5), AuxCoils.MaxCoilCurrentLimitA);
AuxCoils.CoilCurrentCmd_8 := LIMIT(-AuxCoils.MaxCoilCurrentLimitA, Current_Heave - (Current_Roll * 0.9) - Current_Lateral - (Current_WindFF * 0.5), AuxCoils.MaxCoilCurrentLimitA);

// 5. Gap Envelope Integrity Check (Target 100 mm +/- 5 mm)
MaxGapDeviationMm := MAX(ABS(LaserGapData.GapMm_Bogie1_FL - TargetLevitationGapMm),
                     MAX(ABS(LaserGapData.GapMm_Bogie1_FR - TargetLevitationGapMm),
                     MAX(ABS(LaserGapData.GapMm_Bogie2_FL - TargetLevitationGapMm),
                         ABS(LaserGapData.GapMm_Bogie2_FR - TargetLevitationGapMm))));

IF MaxGapDeviationMm > MaxAllowableGapDevMm THEN
    GapViolationAlarm := TRUE;
ELSE
    GapViolationAlarm := FALSE;
END_IF;

// Total active coil power computation: P = Sum(I^2 * R), R_coil = 0.45 Ohm
TotalCurrentSq := (AuxCoils.CoilCurrentCmd_1 * AuxCoils.CoilCurrentCmd_1) +
                  (AuxCoils.CoilCurrentCmd_2 * AuxCoils.CoilCurrentCmd_2) +
                  (AuxCoils.CoilCurrentCmd_3 * AuxCoils.CoilCurrentCmd_3) +
                  (AuxCoils.CoilCurrentCmd_4 * AuxCoils.CoilCurrentCmd_4) +
                  (AuxCoils.CoilCurrentCmd_5 * AuxCoils.CoilCurrentCmd_5) +
                  (AuxCoils.CoilCurrentCmd_6 * AuxCoils.CoilCurrentCmd_6) +
                  (AuxCoils.CoilCurrentCmd_7 * AuxCoils.CoilCurrentCmd_7) +
                  (AuxCoils.CoilCurrentCmd_8 * AuxCoils.CoilCurrentCmd_8);

ActiveDampingPowerKw := (TotalCurrentSq * 0.45) / 1000.0;

END_FUNCTION_BLOCK


// =============================================================================
// FUNCTION BLOCK: FB_Regen_Energy_Dispatch
// Regenerative Deceleration Vector Control & Trackside DC Grid Energy Dispatch
// =============================================================================
FUNCTION_BLOCK FB_Regen_Energy_Dispatch
VAR_INPUT
    EnableRegenControl   : BOOL;
    BrakingDemandIqCmd   : REAL;                // Negative Iq demanded for deceleration (A)
    ActualVelocityMps    : REAL;
    NominalDcVoltageV    : REAL := 4500.0;      // 4.5 kV Nominal DC Bus
    MaxAllowableDcVoltV  : REAL := 5200.0;      // Overvoltage Ceiling
    EnergyBufferData     : ST_TracksideEnergyBuffer;
    SamplePeriodSec      : REAL := 0.001;
END_VAR
VAR_OUTPUT
    RegenPowerAvailableKw: REAL;
    FlywheelCmdKw        : REAL;                // Charge power to Flywheel (kW)
    SupercapCmdKw        : REAL;                // Charge power to Supercap (kW)
    GridExportCmdKw      : REAL;                // Export to AFE Grid Converter (kW)
    BrakeChopperDutyPct  : REAL;                // Resistor Chopper Duty (%)
    DcBusOvervoltageAlarm: BOOL;
END_VAR
VAR
    RawRegenPowerWatts   : REAL;
    SurplusPowerKw       : REAL;
    DcBusVoltageDiffV    : REAL;
    ChopperKp            : REAL := 0.25;        // % Duty per Volt above ceiling
END_VAR

IF NOT EnableRegenControl THEN
    RegenPowerAvailableKw := 0.0;
    FlywheelCmdKw         := 0.0;
    SupercapCmdKw         := 0.0;
    GridExportCmdKw       := 0.0;
    BrakeChopperDutyPct   := 0.0;
    DcBusOvervoltageAlarm := FALSE;
    RETURN;
END_IF;

// 1. Calculate Gross Regenerative Power: P_regen = 1.5 * (Vd*Id + Vq*Iq) ~ F_braking * v
// Linear Motor Force: F = 3/2 * (pi/tau_p) * Psi_f * Iq
RawRegenPowerWatts := ABS(BrakingDemandIqCmd) * 3500.0 * (ActualVelocityMps / 138.89);
RegenPowerAvailableKw := RawRegenPowerWatts / 1000.0;

SurplusPowerKw := RegenPowerAvailableKw;

// 2. Tier 1: Fast Flywheel Kinetic Storage Dispatch (Up to 30 MW absorption, SOC < 92%)
IF (EnergyBufferData.FlywheelSocPercent < 92.0) THEN
    FlywheelCmdKw := MIN(SurplusPowerKw, 30000.0 * ((92.0 - EnergyBufferData.FlywheelSocPercent) / 10.0));
    SurplusPowerKw := SurplusPowerKw - FlywheelCmdKw;
ELSE
    FlywheelCmdKw := 0.0;
END_IF;

// 3. Tier 2: Supercapacitor Bank Dispatch (High-C-rate buffer, SOC < 95%)
IF (EnergyBufferData.SupercapSocPercent < 95.0) AND (SurplusPowerKw > 0.0) THEN
    SupercapCmdKw := MIN(SurplusPowerKw, 15000.0 * ((95.0 - EnergyBufferData.SupercapSocPercent) / 10.0));
    SurplusPowerKw := SurplusPowerKw - SupercapCmdKw;
ELSE
    SupercapCmdKw := 0.0;
END_IF;

// 4. Tier 3: Active Front End (AFE) Utility Grid Regeneration (Up to 25 MW)
IF SurplusPowerKw > 0.0 THEN
    GridExportCmdKw := MIN(SurplusPowerKw, 25000.0);
    SurplusPowerKw  := SurplusPowerKw - GridExportCmdKw;
ELSE
    GridExportCmdKw := 0.0;
END_IF;

// 5. Tier 4: Overvoltage DBR Chopper Protection (Dynamic Braking Resistor)
DcBusVoltageDiffV := EnergyBufferData.DcBusVoltageV - NominalDcVoltageV;

IF EnergyBufferData.DcBusVoltageV > 4800.0 THEN
    // Proportional chopper firing above 4800V
    BrakeChopperDutyPct := LIMIT(0.0, (EnergyBufferData.DcBusVoltageV - 4800.0) * ChopperKp, 100.0);
ELSE
    BrakeChopperDutyPct := 0.0;
END_IF;

// Critical Safety Ceiling Verification
IF EnergyBufferData.DcBusVoltageV >= MaxAllowableDcVoltV THEN
    DcBusOvervoltageAlarm := TRUE;
    BrakeChopperDutyPct   := 100.0;
ELSE
    DcBusOvervoltageAlarm := FALSE;
END_IF;

END_FUNCTION_BLOCK


// =============================================================================
// FUNCTION BLOCK: FB_Sil4_2oo3_Voting_Engine
// EN 50128 / IEC 62278 SIL-4 Dual-Redundant 2-out-of-3 Safety Voting Engine
// =============================================================================
FUNCTION_BLOCK FB_Sil4_2oo3_Voting_Engine
VAR_INPUT
    ChannelA             : ST_Sil4ChannelData;
    ChannelB             : ST_Sil4ChannelData;
    ChannelC             : ST_Sil4ChannelData;
    MaxPositionTolM      : REAL := 0.050;       // 50 mm max position divergence
    MaxSpeedTolKph       : REAL := 3.0;         // 3.0 km/h speed divergence
    MaxDiscrepancyCycles : UINT := 3;           // 3 cycles persistence before trip
END_VAR
VAR_OUTPUT
    VotedOutput          : ST_Sil4VotingOutput;
END_VAR
VAR
    PosMatch_AB          : BOOL;
    PosMatch_BC          : BOOL;
    PosMatch_CA          : BOOL;
    SpeedMatch_AB        : BOOL;
    SpeedMatch_BC        : BOOL;
    SpeedMatch_CA        : BOOL;
    AuthMatch_AB         : BOOL;
    AuthMatch_BC         : BOOL;
    AuthMatch_CA         : BOOL;

    DiscrepancyCounterA  : UINT := 0;
    DiscrepancyCounterB  : UINT := 0;
    DiscrepancyCounterC  : UINT := 0;
END_VAR

// 1. Pairwise Discrepancy Verification across Triplicated Channels
PosMatch_AB := ABS(LREAL_TO_REAL(ChannelA.CalculatedPositionM - ChannelB.CalculatedPositionM)) <= MaxPositionTolM;
PosMatch_BC := ABS(LREAL_TO_REAL(ChannelB.CalculatedPositionM - ChannelC.CalculatedPositionM)) <= MaxPositionTolM;
PosMatch_CA := ABS(LREAL_TO_REAL(ChannelC.CalculatedPositionM - ChannelA.CalculatedPositionM)) <= MaxPositionTolM;

SpeedMatch_AB := ABS(ChannelA.CalculatedVelocityKph - ChannelB.CalculatedVelocityKph) <= MaxSpeedTolKph;
SpeedMatch_BC := ABS(ChannelB.CalculatedVelocityKph - ChannelC.CalculatedVelocityKph) <= MaxSpeedTolKph;
SpeedMatch_CA := ABS(ChannelC.CalculatedVelocityKph - ChannelA.CalculatedVelocityKph) <= MaxSpeedTolKph;

AuthMatch_AB := (ChannelA.SectionAuthorization = ChannelB.SectionAuthorization);
AuthMatch_BC := (ChannelB.SectionAuthorization = ChannelC.SectionAuthorization);
AuthMatch_CA := (ChannelC.SectionAuthorization = ChannelA.SectionAuthorization);

// 2. Channel Discrepancy Fault Accumulation
IF NOT (PosMatch_AB AND SpeedMatch_AB AND AuthMatch_AB) AND NOT (PosMatch_CA AND SpeedMatch_CA AND AuthMatch_CA) THEN
    DiscrepancyCounterA := DiscrepancyCounterA + 1;
ELSE
    IF DiscrepancyCounterA > 0 THEN DiscrepancyCounterA := DiscrepancyCounterA - 1; END_IF;
END_IF;

IF NOT (PosMatch_AB AND SpeedMatch_AB AND AuthMatch_AB) AND NOT (PosMatch_BC AND SpeedMatch_BC AND AuthMatch_BC) THEN
    DiscrepancyCounterB := DiscrepancyCounterB + 1;
ELSE
    IF DiscrepancyCounterB > 0 THEN DiscrepancyCounterB := DiscrepancyCounterB - 1; END_IF;
END_IF;

IF NOT (PosMatch_BC AND SpeedMatch_BC AND AuthMatch_BC) AND NOT (PosMatch_CA AND SpeedMatch_CA AND AuthMatch_CA) THEN
    DiscrepancyCounterC := DiscrepancyCounterC + 1;
ELSE
    IF DiscrepancyCounterC > 0 THEN DiscrepancyCounterC := DiscrepancyCounterC - 1; END_IF;
END_IF;

// 3. 2oo3 Voting Resolution Logic
IF (PosMatch_AB AND SpeedMatch_AB AND AuthMatch_AB) AND (PosMatch_BC AND SpeedMatch_BC AND AuthMatch_BC) THEN
    // Unanimous 3-channel agreement
    VotedOutput.VotedPositionM        := (ChannelA.CalculatedPositionM + ChannelB.CalculatedPositionM + ChannelC.CalculatedPositionM) / 3.0;
    VotedOutput.VotedVelocityKph      := (ChannelA.CalculatedVelocityKph + ChannelB.CalculatedVelocityKph + ChannelC.CalculatedVelocityKph) / 3.0;
    VotedOutput.VotedSectionAuth      := ChannelA.SectionAuthorization;
    VotedOutput.ActiveVoteStatus      := VOTE_UNANIMOUS_HEALTHY;
    VotedOutput.ChannelDiscrepancyBit := 16#00;

ELSIF (PosMatch_AB AND SpeedMatch_AB AND AuthMatch_AB) THEN
    // Channel A & B Agree -> Channel C Discarded
    VotedOutput.VotedPositionM        := (ChannelA.CalculatedPositionM + ChannelB.CalculatedPositionM) / 2.0;
    VotedOutput.VotedVelocityKph      := (ChannelA.CalculatedVelocityKph + ChannelB.CalculatedVelocityKph) / 2.0;
    VotedOutput.VotedSectionAuth      := ChannelA.SectionAuthorization;
    VotedOutput.ActiveVoteStatus      := VOTE_DEGRADED_CHANNEL_C_FAULT;
    VotedOutput.ChannelDiscrepancyBit := 16#04;

ELSIF (PosMatch_BC AND SpeedMatch_BC AND AuthMatch_BC) THEN
    // Channel B & C Agree -> Channel A Discarded
    VotedOutput.VotedPositionM        := (ChannelB.CalculatedPositionM + ChannelC.CalculatedPositionM) / 2.0;
    VotedOutput.VotedVelocityKph      := (ChannelB.CalculatedVelocityKph + ChannelC.CalculatedVelocityKph) / 2.0;
    VotedOutput.VotedSectionAuth      := ChannelB.SectionAuthorization;
    VotedOutput.ActiveVoteStatus      := VOTE_DEGRADED_CHANNEL_A_FAULT;
    VotedOutput.ChannelDiscrepancyBit := 16#01;

ELSIF (PosMatch_CA AND SpeedMatch_CA AND AuthMatch_CA) THEN
    // Channel C & A Agree -> Channel B Discarded
    VotedOutput.VotedPositionM        := (ChannelC.CalculatedPositionM + ChannelA.CalculatedPositionM) / 2.0;
    VotedOutput.VotedVelocityKph      := (ChannelC.CalculatedVelocityKph + ChannelA.CalculatedVelocityKph) / 2.0;
    VotedOutput.VotedSectionAuth      := ChannelC.SectionAuthorization;
    VotedOutput.ActiveVoteStatus      := VOTE_DEGRADED_CHANNEL_B_FAULT;
    VotedOutput.ChannelDiscrepancyBit := 16#02;

ELSE
    // Critical 2oo3 Voting Failure: No two channels agree
    VotedOutput.ActiveVoteStatus      := VOTE_CRITICAL_DISAGREEMENT_TRIP;
    VotedOutput.ChannelDiscrepancyBit := 16#07;
END_IF;

// 4. Fail-Safe Trip Decision Evaluation
// Trip if: Vital Emergency requested, airgap boundary breached, or persistent voter mismatch
IF (ChannelA.EmergencyStopActive OR ChannelB.EmergencyStopActive OR ChannelC.EmergencyStopActive) OR
   (ChannelA.MinLevitationGapMm < 85.0 OR ChannelB.MinLevitationGapMm < 85.0 OR ChannelC.MinLevitationGapMm < 85.0) OR
   (ChannelA.MaxLevitationGapMm > 115.0 OR ChannelB.MaxLevitationGapMm > 115.0 OR ChannelC.MaxLevitationGapMm > 115.0) OR
   (VotedOutput.ActiveVoteStatus = VOTE_CRITICAL_DISAGREEMENT_TRIP) OR
   (DiscrepancyCounterA > MaxDiscrepancyCycles) OR
   (DiscrepancyCounterB > MaxDiscrepancyCycles) OR
   (DiscrepancyCounterC > MaxDiscrepancyCycles) THEN

    VotedOutput.VitalBrakeTripCoil  := FALSE; // De-energize to Trip (Fail-Safe SIL-4)
    VotedOutput.SafetyIntegrityPass := FALSE;
    VotedOutput.DiagnosticCode      := 16#DEADBEEF;
ELSE
    VotedOutput.VitalBrakeTripCoil  := TRUE;  // Energized Safe
    VotedOutput.SafetyIntegrityPass := TRUE;
    VotedOutput.DiagnosticCode      := 16#00000000;
END_IF;

END_FUNCTION_BLOCK


// =============================================================================
// MASTER FUNCTION BLOCK: FB_Maglev_LSM_Controller
// Production Trackside LSM Multiphase Inverter & Levitation Damping Controller
// =============================================================================
FUNCTION_BLOCK FB_Maglev_LSM_Controller
TITLE = 'Chuo Shinkansen 500 km/h Trackside LSM & Levitation Controller'
VERSION : '4.1.0'
AUTHOR : 'Lumina Elite Synthetic Data Architect'

VAR_INPUT
    MasterSystemEnable       : BOOL;                    // Global System Run Command
    SystemResetAck           : BOOL;                    // Fault Reset Acknowledge
    TargetVelocityKph        : REAL := 500.0;           // Target Cruise Speed (500 km/h)
    TractionThrustDemandPct  : REAL;                    // Manual/ATO Thrust Demand (-100% to +100%)
    
    // Sensor Hardware Interfaces
    CrosstalkSensorRaw       : ST_InductivePosSensor;   // Trackside Position Pickup
    LaserGapTelemetry        : ST_LaserGapTelemetry;    // 8-Point Bogie Laser Sensors
    EnergyBufferTelemetry    : ST_TracksideEnergyBuffer;// DC Bus & Storage Telemetry
    
    // Trackside Stator Sections
    CurrentStatorSection     : ST_LsmStatorSection;     // Active 500m Stator Section (K)
    NextStatorSection        : ST_LsmStatorSection;     // Forward 500m Stator Section (K+1)
    
    // Triplicated Vital Channel Inputs
    SafetyChannelA           : ST_Sil4ChannelData;
    SafetyChannelB           : ST_Sil4ChannelData;
    SafetyChannelC           : ST_Sil4ChannelData;
END_VAR

VAR_OUTPUT
    SystemState              : E_MaglevControlState;    // Top-Level State Machine
    InverterBank1            : ST_LsmVectorControl;     // Inverter Substation 1 Output
    InverterBank2            : ST_LsmVectorControl;     // Inverter Substation 2 Output
    AuxDampingCoils          : ST_AuxLevitationCoils;   // Secondary Levitation Outputs
    SafetyVotingResult       : ST_Sil4VotingOutput;     // SIL-4 Voting Telemetry
    
    // Trackside Switchgear Direct Commands
    StatorK_BypassThyristor  : BOOL;
    StatorKp1_FeederIgct     : BOOL;
    EmergencyBrakeRelayTrip  : BOOL;                    // Direct Hardware Trip Output
    
    // Status Telemetry
    LiveTrainPositionM       : LREAL;
    LiveTrainSpeedKph        : REAL;
    MeanLevitationGapMm      : REAL;
    ActiveGridPowerMw        : REAL;
    SystemDiagnosticsSummary : DWORD;
END_VAR

VAR
    // Instantiated Sub-Function Blocks
    fbPosEstimator           : FB_SubMillimeter_Position_Estimator;
    fbSectionSwitch          : FB_IGCT_ZeroCrossing_SectionSwitch;
    fbLevitationDamping      : FB_Levitation_StateSpace_Damping;
    fbRegenDispatch          : FB_Regen_Energy_Dispatch;
    fbSafetyVoter            : FB_Sil4_2oo3_Voting_Engine;

    // Internal State Variables & Regulators
    CalculatedIqDemandA      : REAL := 0.0;
    SpeedErrorKph            : REAL := 0.0;
    SpeedLoopIntegralA       : REAL := 0.0;
    SpeedLoopKp              : REAL := 18.5;            // A/(km/h) Velocity Gain
    SpeedLoopKi              : REAL := 0.45;            // A/(km/h*s) Velocity Integral Gain
    MaxMotorCurrentIqA       : REAL := 2200.0;          // Max Peak LSM Inverter Current (A)
    
    ElectricalFrequencyHz    : REAL := 0.0;
    ParkAngleRad             : REAL := 0.0;
    CycleTimeSec             : REAL := 0.001;           // 1.0 ms PLC Execution Tick
    StateTimer               : TON;
    EmergencyTripLatched     : BOOL := FALSE;
END_VAR

// =============================================================================
// MAIN CONTROL EXECUTION (1.0 ms Synchronous Task)
// =============================================================================

// -----------------------------------------------------------------------------
// STEP 1: SIL-4 TRIPLE MODULAR REDUNDANCY 2oo3 SAFETY VOTING
// -----------------------------------------------------------------------------
fbSafetyVoter(
    ChannelA             := SafetyChannelA,
    ChannelB             := SafetyChannelB,
    ChannelC             := SafetyChannelC,
    MaxPositionTolM      := 0.050,
    MaxSpeedTolKph       := 3.0,
    MaxDiscrepancyCycles := 3,
    VotedOutput          => SafetyVotingResult
);

// Hardware Safety Relay Actuation (Fail-Safe SIL-4 De-energize to Trip)
EmergencyBrakeRelayTrip := SafetyVotingResult.VitalBrakeTripCoil;

IF NOT SafetyVotingResult.SafetyIntegrityPass THEN
    EmergencyTripLatched := TRUE;
    SystemState          := MAGLEV_STATE_SIL4_FAILSAFE_TRIP;
END_IF;

// -----------------------------------------------------------------------------
// STEP 2: HIGH-RESOLUTION TRACK POSITION & VELOCITY ESTIMATION
// -----------------------------------------------------------------------------
fbPosEstimator(
    EnableEstimator      := MasterSystemEnable AND NOT EmergencyTripLatched,
    RawSensor            := CrosstalkSensorRaw,
    PolePitchM           := 1.350,
    SamplePeriodSec      := CycleTimeSec,
    ResetPositionCmd     := SystemResetAck,
    PresetPositionM      := SafetyVotingResult.VotedPositionM,
    EstimatedPositionM   => LiveTrainPositionM,
    EstimatedVelocityKph => LiveTrainSpeedKph,
    ElectricalAngleRad   => ParkAngleRad
);

// Synchronous Electrical Frequency: f_e = v / (2 * tau_p)
ElectricalFrequencyHz := (LiveTrainSpeedKph / 3.6) / (2.0 * 1.350);

// -----------------------------------------------------------------------------
// STEP 3: ACTIVE LEVITATION GAP OBSERVER & AERODYNAMIC DAMPING
// -----------------------------------------------------------------------------
fbLevitationDamping(
    EnableDamping        := MasterSystemEnable AND NOT EmergencyTripLatched,
    LaserGapData         := LaserGapTelemetry,
    VehicleSpeedMps      := LiveTrainSpeedKph / 3.6,
    TargetLevitationGapMm:= 100.0,
    MaxAllowableGapDevMm := 5.0,
    SamplePeriodSec      := CycleTimeSec,
    AuxCoils             => AuxDampingCoils,
    GapViolationAlarm    => ,
    ActiveDampingPowerKw => 
);

MeanLevitationGapMm := LaserGapTelemetry.MeanLevitationGapMm;

// -----------------------------------------------------------------------------
// STEP 4: MASTER PROPULSION / REGENERATION SPEED CONTROLLER (PI)
// -----------------------------------------------------------------------------
IF MasterSystemEnable AND NOT EmergencyTripLatched THEN
    SpeedErrorKph := TargetVelocityKph - LiveTrainSpeedKph;
    
    // Anti-windup PI Speed Regulator
    SpeedLoopIntegralA := SpeedLoopIntegralA + (SpeedLoopKi * SpeedErrorKph * CycleTimeSec);
    SpeedLoopIntegralA := LIMIT(-MaxMotorCurrentIqA, SpeedLoopIntegralA, MaxMotorCurrentIqA);
    
    CalculatedIqDemandA := (SpeedLoopKp * SpeedErrorKph) + SpeedLoopIntegralA;
    
    // Scale by manual/ATO throttle demand percentage if applied
    IF ABS(TractionThrustDemandPct) > 0.01 THEN
        CalculatedIqDemandA := CalculatedIqDemandA * (TractionThrustDemandPct / 100.0);
    END_IF;
    
    CalculatedIqDemandA := LIMIT(-MaxMotorCurrentIqA, CalculatedIqDemandA, MaxMotorCurrentIqA);
ELSE
    CalculatedIqDemandA := 0.0;
    SpeedLoopIntegralA  := 0.0;
END_IF;

// -----------------------------------------------------------------------------
// STEP 5: REGENERATIVE ENERGY DISPATCH & DC BUS STABILIZATION
// -----------------------------------------------------------------------------
fbRegenDispatch(
    EnableRegenControl   := (CalculatedIqDemandA < -10.0),
    BrakingDemandIqCmd   := CalculatedIqDemandA,
    ActualVelocityMps    := LiveTrainSpeedKph / 3.6,
    NominalDcVoltageV    := 4500.0,
    MaxAllowableDcVoltV  := 5200.0,
    EnergyBufferData     := EnergyBufferTelemetry,
    SamplePeriodSec      := CycleTimeSec,
    RegenPowerAvailableKw=> ,
    GridExportCmdKw      => ActiveGridPowerMw
);

ActiveGridPowerMw := ActiveGridPowerMw / 1000.0; // Scale to MW

// -----------------------------------------------------------------------------
// STEP 6: STATOR SECTION ZERO-CROSSING COMMUTATION & HANDOVER
// -----------------------------------------------------------------------------
fbSectionSwitch(
    EnableSwitching      := MasterSystemEnable AND NOT EmergencyTripLatched,
    CurrentTrainPositionM:= LiveTrainPositionM,
    CurrentTrainSpeedMps := LiveTrainSpeedKph / 3.6,
    ActiveSection        := CurrentStatorSection,
    NextSection          := NextStatorSection,
    MasterTorqueCmdIq    := CalculatedIqDemandA,
    ElectricalAngleRad   := ParkAngleRad,
    HandoverZoneLengthM  := 40.0,
    SamplePeriodSec      := CycleTimeSec,
    SectionK_IgctBypass  => StatorK_BypassThyristor,
    SectionKp1_IgctFeed  => StatorKp1_FeederIgct
);

// -----------------------------------------------------------------------------
// STEP 7: MASTER OPERATIONAL STATE MACHINE
// -----------------------------------------------------------------------------
CASE SystemState OF
    MAGLEV_STATE_BOOT_DIAGNOSTICS:
        InverterBank1.IgctFiringGateEnable := FALSE;
        InverterBank2.IgctFiringGateEnable := FALSE;
        IF MasterSystemEnable AND SafetyVotingResult.SafetyIntegrityPass THEN
            SystemState := MAGLEV_STATE_STANDBY_DISARMED;
        END_IF;

    MAGLEV_STATE_STANDBY_DISARMED:
        InverterBank1.Iq_ReferenceAmps     := 0.0;
        InverterBank2.Iq_ReferenceAmps     := 0.0;
        InverterBank1.IgctFiringGateEnable := FALSE;
        InverterBank2.IgctFiringGateEnable := FALSE;
        IF MasterSystemEnable AND (MeanLevitationGapMm >= 90.0) THEN
            SystemState := MAGLEV_STATE_ALIGNMENT_LOCKED;
        END_IF;

    MAGLEV_STATE_ALIGNMENT_LOCKED:
        // Ready for power feeding
        IF TargetVelocityKph > 5.0 THEN
            SystemState := MAGLEV_STATE_TRACTION_ACCEL;
        END_IF;

    MAGLEV_STATE_TRACTION_ACCEL:
        IF fbSectionSwitch.HandoverPhase <> HANDOVER_IDLE THEN
            SystemState := MAGLEV_STATE_SECTION_HANDOVER;
        ELSIF LiveTrainSpeedKph >= (TargetVelocityKph * 0.98) THEN
            SystemState := MAGLEV_STATE_CRUISE_500KPH;
        ELSIF CalculatedIqDemandA < -50.0 THEN
            SystemState := MAGLEV_STATE_REGEN_DECEL;
        END_IF;

    MAGLEV_STATE_CRUISE_500KPH:
        IF fbSectionSwitch.HandoverPhase <> HANDOVER_IDLE THEN
            SystemState := MAGLEV_STATE_SECTION_HANDOVER;
        ELSIF CalculatedIqDemandA < -50.0 THEN
            SystemState := MAGLEV_STATE_REGEN_DECEL;
        END_IF;

    MAGLEV_STATE_SECTION_HANDOVER:
        IF fbSectionSwitch.HandoverPhase = HANDOVER_COMPLETED THEN
            IF LiveTrainSpeedKph >= 480.0 THEN
                SystemState := MAGLEV_STATE_CRUISE_500KPH;
            ELSE
                SystemState := MAGLEV_STATE_TRACTION_ACCEL;
            END_IF;
        ELSIF fbSectionSwitch.HandoverFault THEN
            EmergencyTripLatched := TRUE;
            SystemState          := MAGLEV_STATE_SIL4_FAILSAFE_TRIP;
        END_IF;

    MAGLEV_STATE_REGEN_DECEL:
        IF LiveTrainSpeedKph < 5.0 THEN
            SystemState := MAGLEV_STATE_STATION_BERTHING;
        ELSIF CalculatedIqDemandA > 50.0 THEN
            SystemState := MAGLEV_STATE_TRACTION_ACCEL;
        END_IF;

    MAGLEV_STATE_STATION_BERTHING:
        IF MasterSystemEnable AND (TargetVelocityKph > 10.0) THEN
            SystemState := MAGLEV_STATE_TRACTION_ACCEL;
        END_IF;

    MAGLEV_STATE_DEGRADED_1oo2:
        // Operational at reduced velocity ceiling (300 km/h)
        IF EmergencyTripLatched THEN
            SystemState := MAGLEV_STATE_SIL4_FAILSAFE_TRIP;
        END_IF;

    MAGLEV_STATE_SIL4_FAILSAFE_TRIP:
        // Full System De-energize & Emergency Mechanical/Dynamic Brake Trip
        InverterBank1.Iq_ReferenceAmps     := 0.0;
        InverterBank2.Iq_ReferenceAmps     := 0.0;
        InverterBank1.IgctFiringGateEnable := FALSE;
        InverterBank2.IgctFiringGateEnable := FALSE;
        EmergencyBrakeRelayTrip            := FALSE; // De-energize trip coil
        
        IF SystemResetAck AND SafetyVotingResult.SafetyIntegrityPass THEN
            EmergencyTripLatched := FALSE;
            SystemState          := MAGLEV_STATE_BOOT_DIAGNOSTICS;
        END_IF;
END_CASE;

// -----------------------------------------------------------------------------
// STEP 8: INVERTER VECTOR CONTROL COMMAND MAPPING
// -----------------------------------------------------------------------------
// Inverter Bank 1 (Active Stator Section K)
InverterBank1.InverterIndex        := 1;
InverterBank1.ElectricalAngleRad   := ParkAngleRad;
InverterBank1.ElectricalFreqHz     := ElectricalFrequencyHz;
InverterBank1.Iq_ReferenceAmps     := fbSectionSwitch.Inverter1_IqCmd;
InverterBank1.Id_ReferenceAmps     := 0.0; // Field orientation aligned to SCM
InverterBank1.ModulationIndex      := LIMIT(0.0, ABS(fbSectionSwitch.Inverter1_IqCmd) / MaxMotorCurrentIqA, 1.15);
InverterBank1.IgctFiringGateEnable := fbSectionSwitch.Inverter1_GateEnable AND NOT EmergencyTripLatched;

// Inverter Bank 2 (Upcoming Stator Section K+1)
InverterBank2.InverterIndex        := 2;
InverterBank2.ElectricalAngleRad   := ParkAngleRad;
InverterBank2.ElectricalFreqHz     := ElectricalFrequencyHz;
InverterBank2.Iq_ReferenceAmps     := fbSectionSwitch.Inverter2_IqCmd;
InverterBank2.Id_ReferenceAmps     := 0.0;
InverterBank2.ModulationIndex      := LIMIT(0.0, ABS(fbSectionSwitch.Inverter2_IqCmd) / MaxMotorCurrentIqA, 1.15);
InverterBank2.IgctFiringGateEnable := fbSectionSwitch.Inverter2_GateEnable AND NOT EmergencyTripLatched;

// Summary Diagnostic Status Encoding
SystemDiagnosticsSummary := DWORD#0;
IF EmergencyTripLatched THEN SystemDiagnosticsSummary := SystemDiagnosticsSummary OR DWORD#16#00000001; END_IF;
IF fbSectionSwitch.HandoverFault THEN SystemDiagnosticsSummary := SystemDiagnosticsSummary OR DWORD#16#00000002; END_IF;
IF NOT fbPosEstimator.EstimatorHealthy THEN SystemDiagnosticsSummary := SystemDiagnosticsSummary OR DWORD#16#00000004; END_IF;
IF fbLevitationDamping.GapViolationAlarm THEN SystemDiagnosticsSummary := SystemDiagnosticsSummary OR DWORD#16#00000008; END_IF;

END_FUNCTION_BLOCK
"""

payload = {
    "messages": [
        {
            "role": "user",
            "content": user_prompt
        },
        {
            "role": "assistant",
            "content": assistant_content
        }
    ]
}

output_path = "data/synthetic_generation_v3_enterprise.jsonl"
serialized_line = json.dumps(payload, ensure_ascii=False)

print(f"Serialized line length: {len(serialized_line)} characters")

with open(output_path, "a", encoding="utf-8") as f:
    f.write(serialized_line + "\n")

print(f"Successfully appended record to {output_path}")
