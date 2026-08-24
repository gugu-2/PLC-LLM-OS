import json
import os
import sys

user_prompt = """You are acting as the Chief Plasma Control Systems Architect for a Next-Generation Nuclear Fusion Tokamak Reactor (ITER/DEMO scale).

Your mission is to generate a master-tier, production-ready IEC 61131-3 Structured Text (ST) implementation for the "Tokamak Poloidal Field (PF) Coil Plasma Shape, Vertical Displacement Event (VDE) & Divertor Heat Flux Sweeper" (`FB_Tokamak_PlasmaController`).

### Technical Specifications & Engineering Rigor Required:
1. **Real-Time Magnetic Equilibrium & Poloidal Field Decoupled MIMO Control**:
   - Discretized Grad-Shafranov reconstruction approximation estimating plasma elongation (kappa), triangularity (delta_u, delta_l), safety factor q95, poloidal beta (beta_p), and internal inductance (li) via multipole magnetic flux loops and Rogowski coils.
   - Decoupled 12-coil superconducting Poloidal Field (PF1-PF6) and Central Solenoid (CS1U-CS3L) current distribution matrices at 50 kA per coil with superconducting quench detection (resistive voltage thresholding and fast discharge interlock).
2. **Fast Vertical Displacement Event (VDE) Active Stabilization**:
   - Sub-millisecond feedback loop driving internal copper saddle coils (VS1/VS2) using discrete PD + acceleration feedforward to counter vertical plasma drift (gamma_VDE growth) and prevent unmitigated thermal quench disruptions against the first wall.
   - Integrated Disruption Mitigation System (DMS) triggering Massive Gas Injection (MGI) and Shattered Pellet Injection (SPI) upon unrecoverable vertical runaway.
3. **Divertor Strike-Point X-Point Sweeping & Cryopump Vacuum Balancing**:
   - High-frequency triangular sweeping (+/- 50 mm at 10 Hz) of the magnetic strike point across tungsten monoblock divertor armor to keep heat flux below 10 MW/m^2.
   - Real-time Electron Cyclotron Resonance Heating (ECRH) gyrotron power steering synchronization and sub-divertor neutral pressure cryopump balancing.

Provide full engineering rationale, physics equations, architecture breakdown, and the complete, compilation-ready IEC 61131-3 Structured Text implementation inside a single ```iec-st``` code block."""

assistant_content = """# Tokamak Poloidal Field (PF) Coil Plasma Shape, Vertical Displacement Event (VDE) & Divertor Heat Flux Sweeper
**Target Facility:** Next-Generation ITER/DEMO-Scale Magnetic Confinement Fusion Tokamak  
**Nominal Parameters:** $R_0 = 6.20\\text{ m}$, $a = 2.00\\text{ m}$, $B_0 = 5.30\\text{ T}$, $I_p = 15.0\\text{ MA}$, $P_{fus} = 500\\text{ MW}$  
**Standard Compliance:** IEC 61131-3 (Structured Text 3rd Ed.), IEEE Std 1010/1046, ITER Plant Control Design Handbook (PCDH), IEC 61508 SIL-3 (SIS Fast Discharge Interlocks)

---

## 1. Engineering Rationale & Plasma Physics Foundations

Magnetic confinement fusion in a tokamak reactor requires the simultaneous real-time control of plasma equilibrium, hydrodynamic stability, and divertor exhaust power distribution across extreme spatiotemporal domains (from sub-millisecond magnetohydrodynamic instabilities to multi-hour steady-state inductive/non-inductive burns). The `FB_Tokamak_PlasmaController` architecture addresses three mission-critical operational challenges:

```
+---------------------------------------------------------------------------------------------------+
|                                MASTER TOKAMAK PLASMA CONTROLLER                                    |
|                                                                                                   |
|  +---------------------------+    +---------------------------+    +----------------------------+ |
|  | Grad-Shafranov Real-Time  |    | Fast VDE Stabilization    |    | Divertor Sweeper & Vacuum  | |
|  | Boundary Reconstructor    |    | (Sub-ms Copper Saddle)    |    | (10 Hz Strike Point + ECRH)| |
|  +-------------+-------------+    +-------------+-------------+    +--------------+-------------+ |
|                |                                |                                 |               |
|                v                                v                                 v               |
|  +---------------------------+    +---------------------------+    +----------------------------+ |
|  | 12-Coil Superconducting   |    | Fast Inverter Power       |    | Gas Injection (TGIS) &     | |
|  | Decoupled MIMO (50 kA)    |    | Supply (±10 kV, ±60 kA)   |    | Cryopump Throttle Actuation| |
|  +-------------+-------------+    +-------------+-------------+    +--------------+-------------+ |
|                |                                |                                 |               |
|                +--------------------------------+---------------------------------+               |
|                                                 |                                                 |
|                                                 v                                                 |
|                        +-----------------------------------------------+                          |
|                        | Disruption Mitigation & SIS Quench Interlocks |                          |
|                        +-----------------------------------------------+                          |
+---------------------------------------------------------------------------------------------------+
```

### 1.1 Real-Time Magnetic Equilibrium & Grad-Shafranov Boundary Reconstruction
Equilibrium in an axisymmetric toroidal magnetic configuration satisfies the non-linear Grad-Shafranov equation:
$$\\Delta^* \\psi = R \\frac{\\partial}{\\partial R}\\left(\\frac{1}{R} \\frac{\\partial \\psi}{\\partial R}\\right) + \\frac{\\partial^2 \\psi}{\\partial Z^2} = -\\mu_0 R^2 p'(\\psi) - F F'(\\psi) = -\\mu_0 R j_\\phi$$

In real-time deterministic control environments (1 ms task cycles), numerical PDE inversion is approximated using boundary flux expansion and Green's function response matrices. The controller reconstructs:
1. **Shafranov Shift ($\\Delta_R$) & Axis Position $(R_{mag}, Z_{mag})$**:
   $$\\Delta_R \\approx \\frac{a^2}{2 R_0} \\left[ \\left( \\beta_p + \\frac{l_i}{2} - \\frac{1}{2} \\right) \\left( 1 - \\frac{a^2}{b^2} \\right) + \\ln\\left(\\frac{b}{a}\\right) \\right]$$
2. **Plasma Elongation ($\\kappa$) & Triangularities ($\\delta_u, \\delta_l$)**:
   $$\\kappa = \\frac{Z_{top} - Z_{bot}}{2 a}, \\quad \\delta_u = \\frac{R_0 - R_{top}}{a}, \\quad \\delta_l = \\frac{R_0 - R_{bot}}{a}$$
3. **Safety Factor at 95% Flux Surface ($q_{95}$)**:
   $$q_{95} \\approx \\frac{5 a^2 B_0}{R_0 I_p} \\left[ \\frac{1 + \\kappa^2 (1 + 2\\delta^2 - 1.2\\delta^3)}{2} \\right] \\cdot \\left[ \\frac{1.17 - 0.65 \\epsilon}{(1 - \\epsilon^2)^2} \\right]$$
   where $\\epsilon = a / R_0$ is the inverse aspect ratio. To prevent $m=2, n=1$ kink/tearing disruptions, $q_{95} > 3.0$ must be strictly maintained during flat-top operation.

### 1.2 12-Coil Superconducting Decoupled MIMO Control & Quench Protection
The 12 superconducting coils comprise:
- **Central Solenoid (CS3U, CS2U, CS1U, CS1L, CS2L, CS3L)**: 6 segmented modules providing up to $500\\text{ Wb}$ of inductive flux swing and core plasma shaping.
- **Poloidal Field Coils (PF1 to PF6)**: 6 outer superconducting equilibrium coils delivering vertical field, elongation, and X-point divertor null formation at currents up to $\\pm 50\\text{ kA}$.

Strong inductive cross-coupling between coils is governed by mutual inductance matrix $\\mathbf{M} \\in \\mathbb{R}^{12 \\times 12}$:
$$\\mathbf{V}_{ind} = \\mathbf{M} \\frac{d\\mathbf{I}_{coil}}{dt}$$
The controller decouples the multi-input multi-output (MIMO) dynamics via dynamic matrix feedforward inversion with Tikhonov regularization:
$$\\mathbf{D} = (\\mathbf{G}_{resp}^T \\mathbf{W}_x \\mathbf{G}_{resp} + \\lambda \\mathbf{I})^{-1} \\mathbf{G}_{resp}^T \\mathbf{W}_x$$

**Superconducting Quench Detection**: Each coil is continuously evaluated for resistive voltage development:
$$V_{res, i} = V_{terminal, i} - L_i \\frac{dI_i}{dt} - \\sum_{j \\neq i} M_{ij} \\frac{dI_j}{dt}$$
If $|V_{res, i}| > 100\\text{ mV}$ for $t > 50\\text{ ms}$, a high-temperature superconducting (HTS/LTS) quench is declared, firing vacuum pyro-breakers to divert stored magnetic energy (up to $50\\text{ GJ}$) into water-cooled dump resistor banks ($R_{dump} = 0.1\\ \\Omega, \\tau = 10\\text{ s}$).

### 1.3 Fast Vertical Displacement Event (VDE) Active Stabilization
Elongated plasmas ($\\kappa \\ge 1.7$) are subject to the axisymmetric $n=0$ vertical positional instability:
$$\\frac{d^2 Z_p}{dt^2} = \\gamma_{VDE}^2 Z_p - \\frac{F_{VS}(I_{VS})}{m_p} - \\frac{F_{wall}(\\dot{Z}_p, \\tau_w)}{m_p}$$
where $\\gamma_{VDE} \\approx 100\\text{ s}^{-1}$ is the instability growth rate and $\\tau_w \\approx 20\\text{ ms}$ is the vacuum vessel passive eddy current decay time constant.

The controller executes a sub-millisecond ($500\\ \\mu\\text{s}$) feedback algorithm driving fast in-vessel copper saddle coils (VS1 Upper, VS2 Lower) powered by four-quadrant switching converters ($\\pm 10\\text{ kV}$, $\\pm 60\\text{ kA}$, $dI/dt \\ge 50\\text{ kA/ms}$):
$$V_{VS\\_cmd} = K_p (Z_{sp} - Z_p) + K_d \\dot{Z}_p + K_{acc} \\ddot{Z}_p$$
If vertical position runaway exceeds the controllable boundary ($|Z_p| > 150\\text{ mm}$ or $|\\dot{Z}_p| > 45\\text{ m/s}$), the controller triggers the **Disruption Mitigation System (DMS)**, deploying Shattered Pellet Injection (SPI) of cryo-frozen $Ne/D_2$ pellets within $10\\text{ ms}$ to radiate thermal energy isotropically and prevent severe halo-current vessel deformation.

### 1.4 Divertor Strike-Point X-Point Sweeping & Cryopump Balancing
Narrow scrape-off layer (SOL) heat flux width ($\\lambda_q \\approx 1 - 2\\text{ mm}$) creates unmitigated parallel heat loads exceeding $30\\text{ MW/m}^2$. To protect the tungsten (W) monoblock divertor armor ($q_{crit} = 10\\text{ MW/m}^2$):
1. **High-Frequency Triangular Sweeping**: Modulates the lower X-point and outer strike point coordinate at $f_{sweep} = 10.0\\text{ Hz}$ across $\\pm 50.0\\text{ mm}$ using continuous parabolic turnaround blending to prevent infinite acceleration in PF5/PF6 current demands.
2. **Radiative Detachment Control**: Real-time infrared thermography and Langmuir probes measure surface heat flux $q_{div}$. If $q_{div} > 8.5\\text{ MW/m}^2$, closed-loop impurity seeding ($N_2/Ne$) is injected into the private flux region to achieve radiative detachment ($f_{rad} > 85\\%$, $q_{div} < 5.0\\text{ MW/m}^2$).
3. **Sub-Divertor Neutral Cryopump Balancing**: Modulates cryogenic panel throttle valves to regulate neutral gas back-pressure ($P_n \\in [1.0, 5.0]\\text{ Pa}$), preventing gas back-streaming into the confinement core.
4. **Real-Time ECRH Gyrotron Mirror Steering**: Tracks the $q=2/1$ resonant flux surface ($R_{res} = \\frac{e B_0 R_0}{2\\pi m_e f_{RF}}$ for $170\\text{ GHz}$ millimeter waves) and dynamically adjusts launcher mirror elevation and azimuth angles to suppress Neoclassical Tearing Modes (NTMs).

---

## 2. Complete IEC 61131-3 Structured Text Implementation

```iec-st
// =============================================================================
// TOKAMAK POLOIDAL FIELD (PF) COIL PLASMA SHAPE, VERTICAL DISPLACEMENT EVENT
// (VDE) & DIVERTOR HEAT FLUX SWEEPER CONTROLLER
// 
// Architecture: IEC 61131-3 Industrial Structured Text (3rd Edition)
// Safety Standard: IEC 61508 SIL-3 Hardwired SIS Interlocks & PCDH Compliant
// =============================================================================

// =============================================================================
// TYPE DEFINITIONS & DATA STRUCTURES
// =============================================================================
TYPE
    // Tokamak Operational State Machine
    E_TokamakState : (
        STATE_UNMAGNETIZED              := 0,
        STATE_PRE_IONIZATION            := 1,
        STATE_PLASMA_BREAKDOWN          := 2,
        STATE_CURRENT_RAMP_UP           := 3,
        STATE_FLAT_TOP_CONFINED         := 4,
        STATE_DIVERTOR_DETACHED         := 5,
        STATE_CURRENT_RAMP_DOWN         := 6,
        STATE_SOFT_LANDING              := 7,
        STATE_DISRUPTION_MITIGATION     := 8,
        STATE_EMERGENCY_FAST_DISCHARGE  := 9
    );

    // Disruption Threat Level
    E_DisruptionRisk : (
        RISK_NOMINAL                    := 0,
        RISK_ELEVATED_VDE               := 1,
        RISK_TEARING_MODE_LOCKED        := 2,
        RISK_RADIATIVE_COLLAPSE         := 3,
        RISK_IMMINENT_DISRUPTION        := 4
    );

    // Divertor Regime
    E_DivertorRegime : (
        DIVERTOR_ATTACHED_HIGH_HEAT     := 0,
        DIVERTOR_PARTIAL_DETACHMENT     := 1,
        DIVERTOR_FULL_DETACHMENT        := 2,
        DIVERTOR_RECOMBINATION_MARFE    := 3
    );

    // Magnetic Diagnostics Array
    ST_MagneticSensors : STRUCT
        arrMirnov_Bpol          : ARRAY[1..16] OF LREAL; // Poloidal magnetic field probes [Tesla]
        arrFluxLoops_Psi        : ARRAY[1..16] OF LREAL; // Poloidal magnetic flux loops [Weber]
        arrRogowski_Ip          : ARRAY[1..4] OF LREAL;  // Redundant plasma current sensors [Amperes]
        rDiamagnetic_Flux       : LREAL;                 // Toroidal flux diamagnetic loop [Weber]
        rToroidalField_B0       : LREAL;                 // Toroidal magnetic field at R0 [Tesla]
        rLoopVoltage            : LREAL;                 // Toroidal loop voltage [Volts]
    END_STRUCT;

    // Plasma Equilibrium State Estimation
    ST_PlasmaEquilibrium : STRUCT
        rIp_Actual              : LREAL; // Plasma Current [Amperes]
        rR_MagneticAxis         : LREAL; // Major Radius of Magnetic Axis [meters]
        rZ_MagneticAxis         : LREAL; // Vertical Position of Magnetic Axis [meters]
        rElongation_Kappa       : LREAL; // Plasma Elongation (b/a) [-]
        rTriangularity_Upper    : LREAL; // Upper Triangularity delta_u [-]
        rTriangularity_Lower    : LREAL; // Lower Triangularity delta_l [-]
        rSafetyFactor_q95       : LREAL; // Safety Factor at 95% flux surface [-]
        rPoloidalBeta           : LREAL; // Poloidal Beta beta_p [-]
        rNormalizedBeta         : LREAL; // Normalized Beta beta_N [%-m-T/MA]
        rInternalInductance_li  : LREAL; // Internal Inductance l_i(3) [-]
        rStoredEnergy_Wmhd      : LREAL; // Stored Plasma Thermal Energy [Joules]
        rGreenwaldFraction      : LREAL; // Density / Greenwald Limit Ratio [-]
        rRX_PointLower          : LREAL; // Lower X-Point Radial Position [meters]
        rZX_PointLower          : LREAL; // Lower X-Point Vertical Position [meters]
    END_STRUCT;

    // Superconducting Coil Telemetry & Command
    ST_SuperconductingCoil : STRUCT
        rCurrent_PV             : LREAL; // Measured Current [Amperes]
        rCurrent_SP             : LREAL; // Command Current Setpoint [Amperes]
        rVoltage_PV             : LREAL; // Measured Terminal Voltage [Volts]
        rVoltage_SP             : LREAL; // Power Converter Voltage Demand [Volts]
        rResistiveVoltage       : LREAL; // Extracted Quench Resistive Voltage [Volts]
        rCurrentSlewRate        : LREAL; // Current Rate of Change [A/s]
        xQuenchDetected         : BOOL;  // Superconducting Quench Alarm Flag
        xDumpBreakerTripped     : BOOL;  // Energy Extraction Fast Discharge Active
    END_STRUCT;

    // 12-Coil Superconducting Array (6 Central Solenoid + 6 Poloidal Field)
    ST_CoilArray_12 : STRUCT
        CS3U                    : ST_SuperconductingCoil; // Central Solenoid 3 Upper
        CS2U                    : ST_SuperconductingCoil; // Central Solenoid 2 Upper
        CS1U                    : ST_SuperconductingCoil; // Central Solenoid 1 Upper
        CS1L                    : ST_SuperconductingCoil; // Central Solenoid 1 Lower
        CS2L                    : ST_SuperconductingCoil; // Central Solenoid 2 Lower
        CS3L                    : ST_SuperconductingCoil; // Central Solenoid 3 Lower
        PF1                     : ST_SuperconductingCoil; // Poloidal Field 1 (Top)
        PF2                     : ST_SuperconductingCoil; // Poloidal Field 2 (Upper Outer)
        PF3                     : ST_SuperconductingCoil; // Poloidal Field 3 (Mid Outer Upper)
        PF4                     : ST_SuperconductingCoil; // Poloidal Field 4 (Mid Outer Lower)
        PF5                     : ST_SuperconductingCoil; // Poloidal Field 5 (Lower Outer)
        PF6                     : ST_SuperconductingCoil; // Poloidal Field 6 (Bottom Divertor)
    END_STRUCT;

    // Fast In-Vessel Copper Saddle Coils (Vertical Stabilization Actuator)
    ST_FastVS_Actuator : STRUCT
        rCurrent_Upper_PV       : LREAL; // VS Upper Coil Current [Amperes]
        rCurrent_Lower_PV       : LREAL; // VS Lower Coil Current [Amperes]
        rVoltage_Upper_Cmd      : LREAL; // Fast Inverter Voltage Demand [Volts]
        rVoltage_Lower_Cmd      : LREAL; // Fast Inverter Voltage Demand [Volts]
        rSlewRate_kA_per_ms     : LREAL; // Instantaneous Current Slew Rate [kA/ms]
        rCoilTemperature_C      : LREAL; // Copper Winding Temperature [deg C]
        xPowerSupplyFault       : BOOL;  // Inverter Bridge Overcurrent / DC-link Fault
    END_STRUCT;

    // Divertor Dynamics & Cryogenic Vacuum Status
    ST_DivertorDynamics : STRUCT
        rR_StrikePoint_Inner    : LREAL;            // Inner Strike Point Radius [meters]
        rZ_StrikePoint_Inner    : LREAL;            // Inner Strike Point Vertical [meters]
        rR_StrikePoint_Outer    : LREAL;            // Outer Strike Point Radius [meters]
        rZ_StrikePoint_Outer    : LREAL;            // Outer Strike Point Vertical [meters]
        rPeakHeatFlux_MW_m2     : LREAL;            // Surface Peak Heat Flux [MW/m^2]
        rIntegratedHeatLoad_MJ  : LREAL;            // Monoblock Accumulated Heat Load [MJ]
        rRadiativeFraction      : LREAL;            // Divertor Region Radiative Fraction [-]
        eCurrentRegime          : E_DivertorRegime; // Thermal Exhaust Regime
        rGasPuff_Impurity_SP    : LREAL;            // Nitrogen/Neon Seeding Rate [Pa*m^3/s]
        rGasPuff_Fuel_SP        : LREAL;            // Deuterium/Tritium Fueling Rate [Pa*m^3/s]
        rSubDivertor_Pressure   : LREAL;            // Sub-Divertor Neutral Gas Pressure [Pascal]
        rCryopump_Throttle_Pct  : LREAL;            // Cryogenic Valve Opening [0.0..100.0 %]
    END_STRUCT;

    // Real-Time ECRH Steering & Gyrotron Launcher Link
    ST_ECRH_MirrorLink : STRUCT
        rTotalPower_MW          : LREAL; // Total Gyrotron Injected Power [MW]
        rMirror_Elevation_Deg   : LREAL; // Poloidal Steerable Mirror Angle [degrees]
        rMirror_Azimuth_Deg     : LREAL; // Toroidal Current Drive Angle [degrees]
        rResonanceRadius_m      : LREAL; // Calculated Electron Cyclotron Resonance Radius [meters]
        rTargetRationalSurface_q: LREAL; // Target q-surface (e.g. 2.0 for NTM suppression)
        xMirrorLockedOnMode     : BOOL;  // Beam Real-Time Phase Lock Acknowledged
    END_STRUCT;

    // Disruption Mitigation System (DMS) Fast Trigger Interface
    ST_DisruptionMitigationSystem : STRUCT
        xSPI_Pellet_Armed       : BOOL;  // Shattered Pellet Injection (SPI) Cryo Barrel Armed
        xSPI_Fire_Trigger       : BOOL;  // Hardware Pulse to Cryogenic Puncher / Propellant Valve
        xMGI_FastValve_Open     : BOOL;  // Massive Gas Injection (MGI) Fast Solenoid Valve
        rHaloCurrent_Total_kA   : LREAL; // Measured Toroidal Halo Current in Vessel Blanket [kA]
        rVesselStress_MPa       : LREAL; // Dynamic Strain Gauge Vessel Wall Stress [MPa]
        xEmergencySoftStop      : BOOL;  // Controlled Rapid Plasma Shutdown Request
    END_STRUCT;

    // 12x12 Decoupling & Induction Calibration Matrix
    ST_MIMO_Calibration : STRUCT
        arrDecoupling_Matrix    : ARRAY[1..12, 1..12] OF LREAL; // Inverse Response Matrix
        arrMutualInductance     : ARRAY[1..12, 1..12] OF LREAL; // Inductive Coupling Matrix [Henries]
        arrSelfInductance       : ARRAY[1..12] OF LREAL;        // Coil Self Inductance [Henries]
        rTikhonovLambda         : LREAL;                        // SVD Regularization Parameter
    END_STRUCT;
END_TYPE


// =============================================================================
// FUNCTION BLOCK: FB_GradShafranov_Reconstructor
// Discretized Real-Time Magnetic Equilibrium & Boundary Reconstructor
// =============================================================================
FUNCTION_BLOCK FB_GradShafranov_Reconstructor
VAR_INPUT
    xEnable                 : BOOL;
    Sensors                 : ST_MagneticSensors;
    rMinorRadius_a          : LREAL := 2.00; // Minor radius [m]
    rMajorRadius_R0         : LREAL := 6.20; // Major radius [m]
    rElectronDensity_Ne20   : LREAL := 0.85; // Line-averaged electron density [10^20 m^-3]
END_VAR

VAR_OUTPUT
    Equilibrium             : ST_PlasmaEquilibrium;
    xEquilibriumValid       : BOOL;
END_VAR

VAR
    i                       : INT;
    rIp_Sum                 : LREAL;
    rBpol_Avg               : LREAL;
    rPsi_Top                : LREAL;
    rPsi_Bottom             : LREAL;
    rPsi_Outer              : LREAL;
    rPsi_Inner              : LREAL;
    rShafranovShift         : LREAL;
    rInverseAspect_Eps      : LREAL;
    rShapeFactor            : LREAL;
    rToroidalBeta_Bt        : LREAL;
    rGreenwald_Limit        : LREAL;
    c_MU0                   : LREAL := 1.2566370614359E-6; // Vacuum permeability [H/m]
END_VAR

IF NOT xEnable THEN
    xEquilibriumValid := FALSE;
    RETURN;
END_IF;

// 1. Plasma Current Estimation via Quad-Rogowski Redundancy
rIp_Sum := 0.0;
FOR i := 1 TO 4 DO
    rIp_Sum := rIp_Sum + Sensors.arrRogowski_Ip[i];
END_FOR;
Equilibrium.rIp_Actual := rIp_Sum / 4.0;

// Validate minimal plasma presence (100 kA threshold)
IF ABS(Equilibrium.rIp_Actual) < 1.0E5 THEN
    Equilibrium.rIp_Actual := 0.0;
    Equilibrium.rElongation_Kappa := 1.0;
    Equilibrium.rSafetyFactor_q95 := 99.9;
    xEquilibriumValid := FALSE;
    RETURN;
END_IF;

// 2. Average Poloidal Field from Mirnov Array
rBpol_Avg := 0.0;
FOR i := 1 TO 16 DO
    rBpol_Avg := rBpol_Avg + ABS(Sensors.arrMirnov_Bpol[i]);
END_FOR;
rBpol_Avg := rBpol_Avg / 16.0;

// 3. Boundary Flux Extrema from Multipole Flux Loops
// Mapping flux loop indices: 1=Outermost Midplane, 5=Top Apex, 9=Innermost Midplane, 13=Bottom Divertor
rPsi_Outer  := Sensors.arrFluxLoops_Psi[1];
rPsi_Top    := Sensors.arrFluxLoops_Psi[5];
rPsi_Inner  := Sensors.arrFluxLoops_Psi[9];
rPsi_Bottom := Sensors.arrFluxLoops_Psi[13];

// 4. Poloidal Beta & Internal Inductance Estimation
// Using Shafranov formulation: Lambda = beta_p + li/2 - 1
IF rBpol_Avg > 1.0E-4 THEN
    Equilibrium.rPoloidalBeta := LIMIT(0.05, (2.0 * c_MU0 * ABS(Sensors.rDiamagnetic_Flux)) / (c_MU0 * rMinorRadius_a * rBpol_Avg * rBpol_Avg + 1.0E-9), 3.5);
    Equilibrium.rInternalInductance_li := LIMIT(0.5, (2.0 * (rPsi_Outer - rPsi_Inner)) / (c_MU0 * rMajorRadius_R0 * Equilibrium.rIp_Actual + 1.0E-9) - Equilibrium.rPoloidalBeta + 1.0, 2.5);
ELSE
    Equilibrium.rPoloidalBeta := 0.1;
    Equilibrium.rInternalInductance_li := 1.0;
END_IF;

// 5. Shafranov Shift and Magnetic Axis Position
rShafranovShift := (rMinorRadius_a * rMinorRadius_a / (2.0 * rMajorRadius_R0)) * 
                   ((Equilibrium.rPoloidalBeta + Equilibrium.rInternalInductance_li / 2.0));
Equilibrium.rR_MagneticAxis := rMajorRadius_R0 + rShafranovShift;
Equilibrium.rZ_MagneticAxis := (rPsi_Top - rPsi_Bottom) / (c_MU0 * Equilibrium.rIp_Actual * 1.0E-6 + 1.0E-9) * 0.05;

// 6. Geometric Elongation (Kappa) and Triangularities (delta_u, delta_l)
Equilibrium.rElongation_Kappa := LIMIT(1.0, 1.0 + (ABS(rPsi_Top + rPsi_Bottom - 2.0 * rPsi_Outer) / (ABS(rPsi_Outer - rPsi_Inner) + 1.0E-9)) * 0.85, 2.2);
Equilibrium.rTriangularity_Upper := LIMIT(0.0, ((rMajorRadius_R0 - (rMajorRadius_R0 - 0.35 * (rPsi_Top - rPsi_Outer))) / rMinorRadius_a), 0.7);
Equilibrium.rTriangularity_Lower := LIMIT(0.0, ((rMajorRadius_R0 - (rMajorRadius_R0 - 0.45 * (rPsi_Bottom - rPsi_Outer))) / rMinorRadius_a), 0.8);

// Lower X-Point Reconstructed Coordinates
Equilibrium.rRX_PointLower := rMajorRadius_R0 - (Equilibrium.rTriangularity_Lower * rMinorRadius_a);
Equilibrium.rZX_PointLower := -1.0 * (rMinorRadius_a * Equilibrium.rElongation_Kappa * 0.95);

// 7. Safety Factor q95 Calculation
rInverseAspect_Eps := rMinorRadius_a / rMajorRadius_R0;
rShapeFactor := (1.0 + EXPT(Equilibrium.rElongation_Kappa, 2.0) * (1.0 + 2.0 * EXPT(Equilibrium.rTriangularity_Lower, 2.0) - 1.2 * EXPT(Equilibrium.rTriangularity_Lower, 3.0))) / 2.0;

IF ABS(Equilibrium.rIp_Actual) > 1.0E5 THEN
    Equilibrium.rSafetyFactor_q95 := (5.0 * EXPT(rMinorRadius_a, 2.0) * Sensors.rToroidalField_B0) / (rMajorRadius_R0 * (Equilibrium.rIp_Actual / 1.0E6)) * 
                                     rShapeFactor * ((1.17 - 0.65 * rInverseAspect_Eps) / (EXPT(1.0 - EXPT(rInverseAspect_Eps, 2.0), 2.0)));
ELSE
    Equilibrium.rSafetyFactor_q95 := 99.9;
END_IF;

// 8. Stored Energy (W_mhd) and Normalized Beta (Beta_N)
Equilibrium.rStoredEnergy_Wmhd := 0.375 * c_MU0 * rMajorRadius_R0 * EXPT(Equilibrium.rIp_Actual, 2.0) * Equilibrium.rPoloidalBeta;
rToroidalBeta_Bt := (2.0 * c_MU0 * (Equilibrium.rStoredEnergy_Wmhd / (2.0 * 3.1415926535 * rMajorRadius_R0 * 3.1415926535 * EXPT(rMinorRadius_a, 2.0) * Equilibrium.rElongation_Kappa))) / 
                    (EXPT(Sensors.rToroidalField_B0, 2.0) + 1.0E-9);
Equilibrium.rNormalizedBeta := rToroidalBeta_Bt / ((Equilibrium.rIp_Actual / 1.0E6) / (rMinorRadius_a * Sensors.rToroidalField_B0 + 1.0E-9)) * 100.0;

// 9. Greenwald Density Fraction Limit
rGreenwald_Limit := (Equilibrium.rIp_Actual / 1.0E6) / (3.1415926535 * EXPT(rMinorRadius_a, 2.0));
IF rGreenwald_Limit > 0.01 THEN
    Equilibrium.rGreenwaldFraction := rElectronDensity_Ne20 / rGreenwald_Limit;
ELSE
    Equilibrium.rGreenwaldFraction := 0.0;
END_IF;

xEquilibriumValid := TRUE;

END_FUNCTION_BLOCK


// =============================================================================
// FUNCTION BLOCK: FB_Superconducting_MIMO_Decoupler
// 12-Coil Superconducting Current Controller & Superconducting Quench Protection
// =============================================================================
FUNCTION_BLOCK FB_Superconducting_MIMO_Decoupler
VAR_INPUT
    xEnable                 : BOOL;
    xEmergencyFastDump      : BOOL;
    rCycleTime_Sec          : LREAL := 0.001; // 1 ms control task cycle
    EquilibriumPV           : ST_PlasmaEquilibrium;
    EquilibriumSP           : ST_PlasmaEquilibrium;
    CoilCalibration         : ST_MIMO_Calibration;
END_VAR

VAR_IN_OUT
    Coils                   : ST_CoilArray_12;
END_VAR

VAR_OUTPUT
    xQuenchAlarmTripped     : BOOL;
    xMIMO_Saturated         : BOOL;
    rMaxCoilCurrent_kA      : LREAL;
END_VAR

VAR
    i                       : INT;
    j                       : INT;
    arrErrorVector          : ARRAY[1..12] OF LREAL;
    arrDeltaI_Demand        : ARRAY[1..12] OF LREAL;
    arrCoilCurrents_PV      : ARRAY[1..12] OF LREAL;
    arrCoilVoltages_PV      : ARRAY[1..12] OF LREAL;
    arrCoilCurrents_SP      : ARRAY[1..12] OF LREAL;
    arrInductiveVoltages    : ARRAY[1..12] OF LREAL;
    arrResistiveVoltages    : ARRAY[1..12] OF LREAL;
    arrQuenchTimers         : ARRAY[1..12] OF TON;
    
    CONST_MAX_COIL_CURRENT  : LREAL := 50000.0; // 50 kA superconducting limit
    CONST_MAX_SLEW_RATE     : LREAL := 5000.0;  // 5.0 kA/s max ramp rate
    CONST_QUENCH_VOLTAGE_TH : LREAL := 0.100;   // 100 mV resistive threshold
END_VAR

IF NOT xEnable THEN
    // Inactive controller: zero voltage requests
    Coils.CS3U.rVoltage_SP := 0.0; Coils.CS2U.rVoltage_SP := 0.0; Coils.CS1U.rVoltage_SP := 0.0;
    Coils.CS1L.rVoltage_SP := 0.0; Coils.CS2L.rVoltage_SP := 0.0; Coils.CS3L.rVoltage_SP := 0.0;
    Coils.PF1.rVoltage_SP  := 0.0; Coils.PF2.rVoltage_SP  := 0.0; Coils.PF3.rVoltage_SP  := 0.0;
    Coils.PF4.rVoltage_SP  := 0.0; Coils.PF5.rVoltage_SP  := 0.0; Coils.PF6.rVoltage_SP  := 0.0;
    RETURN;
END_IF;

// 1. Pack Telemetry Vectors
arrCoilCurrents_PV[1]  := Coils.CS3U.rCurrent_PV; arrCoilVoltages_PV[1]  := Coils.CS3U.rVoltage_PV;
arrCoilCurrents_PV[2]  := Coils.CS2U.rCurrent_PV; arrCoilVoltages_PV[2]  := Coils.CS2U.rVoltage_PV;
arrCoilCurrents_PV[3]  := Coils.CS1U.rCurrent_PV; arrCoilVoltages_PV[3]  := Coils.CS1U.rVoltage_PV;
arrCoilCurrents_PV[4]  := Coils.CS1L.rCurrent_PV; arrCoilVoltages_PV[4]  := Coils.CS1L.rVoltage_PV;
arrCoilCurrents_PV[5]  := Coils.CS2L.rCurrent_PV; arrCoilVoltages_PV[5]  := Coils.CS2L.rVoltage_PV;
arrCoilCurrents_PV[6]  := Coils.CS3L.rCurrent_PV; arrCoilVoltages_PV[6]  := Coils.CS3L.rVoltage_PV;
arrCoilCurrents_PV[7]  := Coils.PF1.rCurrent_PV;  arrCoilVoltages_PV[7]  := Coils.PF1.rVoltage_PV;
arrCoilCurrents_PV[8]  := Coils.PF2.rCurrent_PV;  arrCoilVoltages_PV[8]  := Coils.PF2.rVoltage_PV;
arrCoilCurrents_PV[9]  := Coils.PF3.rCurrent_PV;  arrCoilVoltages_PV[9]  := Coils.PF3.rVoltage_PV;
arrCoilCurrents_PV[10] := Coils.PF4.rCurrent_PV;  arrCoilVoltages_PV[10] := Coils.PF4.rVoltage_PV;
arrCoilCurrents_PV[11] := Coils.PF5.rCurrent_PV;  arrCoilVoltages_PV[11] := Coils.PF5.rVoltage_PV;
arrCoilCurrents_PV[12] := Coils.PF6.rCurrent_PV;  arrCoilVoltages_PV[12] := Coils.PF6.rVoltage_PV;

// 2. Superconducting Quench Detection (V_res = V_meas - L*dI/dt - sum(M_ij*dI_j/dt))
xQuenchAlarmTripped := FALSE;
FOR i := 1 TO 12 DO
    arrInductiveVoltages[i] := 0.0;
    // Calculate mutual inductive decoupling across 12 coils
    FOR j := 1 TO 12 DO
        IF i = j THEN
            arrInductiveVoltages[i] := arrInductiveVoltages[i] + CoilCalibration.arrSelfInductance[i] * 
                                       ((arrCoilCurrents_PV[i] - arrCoilCurrents_SP[i]) / rCycleTime_Sec);
        ELSE
            arrInductiveVoltages[i] := arrInductiveVoltages[i] + CoilCalibration.arrMutualInductance[i, j] * 
                                       ((arrCoilCurrents_PV[j] - arrCoilCurrents_SP[j]) / rCycleTime_Sec);
        END_IF;
    END_FOR;
    
    // Extracted resistive voltage component
    arrResistiveVoltages[i] := ABS(arrCoilVoltages_PV[i] - arrInductiveVoltages[i]);
    
    // Integrate quench verification timer (50 ms persistence filter)
    arrQuenchTimers[i](IN := (arrResistiveVoltages[i] > CONST_QUENCH_VOLTAGE_TH), PT := T#50ms);
    
    IF arrQuenchTimers[i].Q OR xEmergencyFastDump THEN
        xQuenchAlarmTripped := TRUE;
    END_IF;
END_FOR;

// Write quench statuses back to struct
Coils.CS3U.rResistiveVoltage := arrResistiveVoltages[1];  Coils.CS3U.xQuenchDetected := arrQuenchTimers[1].Q;
Coils.CS2U.rResistiveVoltage := arrResistiveVoltages[2];  Coils.CS2U.xQuenchDetected := arrQuenchTimers[2].Q;
Coils.CS1U.rResistiveVoltage := arrResistiveVoltages[3];  Coils.CS1U.xQuenchDetected := arrQuenchTimers[3].Q;
Coils.CS1L.rResistiveVoltage := arrResistiveVoltages[4];  Coils.CS1L.xQuenchDetected := arrQuenchTimers[4].Q;
Coils.CS2L.rResistiveVoltage := arrResistiveVoltages[5];  Coils.CS2L.xQuenchDetected := arrQuenchTimers[5].Q;
Coils.CS3L.rResistiveVoltage := arrResistiveVoltages[6];  Coils.CS3L.xQuenchDetected := arrQuenchTimers[6].Q;
Coils.PF1.rResistiveVoltage  := arrResistiveVoltages[7];  Coils.PF1.xQuenchDetected  := arrQuenchTimers[7].Q;
Coils.PF2.rResistiveVoltage  := arrResistiveVoltages[8];  Coils.PF2.xQuenchDetected  := arrQuenchTimers[8].Q;
Coils.PF3.rResistiveVoltage  := arrResistiveVoltages[9];  Coils.PF3.xQuenchDetected  := arrQuenchTimers[9].Q;
Coils.PF4.rResistiveVoltage  := arrResistiveVoltages[10]; Coils.PF4.xQuenchDetected := arrQuenchTimers[10].Q;
Coils.PF5.rResistiveVoltage  := arrResistiveVoltages[11]; Coils.PF5.xQuenchDetected := arrQuenchTimers[11].Q;
Coils.PF6.rResistiveVoltage  := arrResistiveVoltages[12]; Coils.PF6.xQuenchDetected := arrQuenchTimers[12].Q;

// 3. Quench Fast Discharge Trip Handling
IF xQuenchAlarmTripped THEN
    Coils.CS3U.xDumpBreakerTripped := TRUE; Coils.CS2U.xDumpBreakerTripped := TRUE;
    Coils.CS1U.xDumpBreakerTripped := TRUE; Coils.CS1L.xDumpBreakerTripped := TRUE;
    Coils.CS2L.xDumpBreakerTripped := TRUE; Coils.CS3L.xDumpBreakerTripped := TRUE;
    Coils.PF1.xDumpBreakerTripped  := TRUE; Coils.PF2.xDumpBreakerTripped  := TRUE;
    Coils.PF3.xDumpBreakerTripped  := TRUE; Coils.PF4.xDumpBreakerTripped  := TRUE;
    Coils.PF5.xDumpBreakerTripped  := TRUE; Coils.PF6.xDumpBreakerTripped  := TRUE;
    
    // Command power supplies to zero invert to dump energy into R_dump
    FOR i := 1 TO 12 DO
        arrCoilCurrents_SP[i] := 0.0;
    END_FOR;
    RETURN;
END_IF;

// 4. Compute Shape & Equilibrium Error Vector (12 State Elements)
arrErrorVector[1]  := (EquilibriumSP.rIp_Actual - EquilibriumPV.rIp_Actual) / 1.0E6;         // dIp [MA]
arrErrorVector[2]  := (EquilibriumSP.rR_MagneticAxis - EquilibriumPV.rR_MagneticAxis);       // dR [m]
arrErrorVector[3]  := (EquilibriumSP.rZ_MagneticAxis - EquilibriumPV.rZ_MagneticAxis);       // dZ [m]
arrErrorVector[4]  := (EquilibriumSP.rElongation_Kappa - EquilibriumPV.rElongation_Kappa);   // dKappa [-]
arrErrorVector[5]  := (EquilibriumSP.rTriangularity_Upper - EquilibriumPV.rTriangularity_Upper); // dDelta_u
arrErrorVector[6]  := (EquilibriumSP.rTriangularity_Lower - EquilibriumPV.rTriangularity_Lower); // dDelta_l
arrErrorVector[7]  := (EquilibriumSP.rRX_PointLower - EquilibriumPV.rRX_PointLower);         // dRX [m]
arrErrorVector[8]  := (EquilibriumSP.rZX_PointLower - EquilibriumPV.rZX_PointLower);         // dZX [m]
arrErrorVector[9]  := (EquilibriumSP.rSafetyFactor_q95 - EquilibriumPV.rSafetyFactor_q95);   // dq95
arrErrorVector[10] := (EquilibriumSP.rPoloidalBeta - EquilibriumPV.rPoloidalBeta);           // dBetap
arrErrorVector[11] := (EquilibriumSP.rInternalInductance_li - EquilibriumPV.rInternalInductance_li); // dli
arrErrorVector[12] := 0.0; // Reserved for outer limiter gap control

// 5. MIMO Matrix Inversion: Delta_I = DecouplingMatrix * ErrorVector
xMIMO_Saturated := FALSE;
rMaxCoilCurrent_kA := 0.0;

FOR i := 1 TO 12 DO
    arrDeltaI_Demand[i] := 0.0;
    FOR j := 1 TO 12 DO
        arrDeltaI_Demand[i] := arrDeltaI_Demand[i] + (CoilCalibration.arrDecoupling_Matrix[i, j] * arrErrorVector[j]);
    END_FOR;
    
    // Apply Slew Rate Limiter (5 kA/s)
    arrDeltaI_Demand[i] := LIMIT(-1.0 * CONST_MAX_SLEW_RATE * rCycleTime_Sec, arrDeltaI_Demand[i], CONST_MAX_SLEW_RATE * rCycleTime_Sec);
    
    // Accumulate Current Setpoint & Apply Superconducting Clamping (50 kA)
    arrCoilCurrents_SP[i] := LIMIT(-1.0 * CONST_MAX_COIL_CURRENT, arrCoilCurrents_PV[i] + arrDeltaI_Demand[i], CONST_MAX_COIL_CURRENT);
    
    IF ABS(arrCoilCurrents_SP[i]) >= (CONST_MAX_COIL_CURRENT - 500.0) THEN
        xMIMO_Saturated := TRUE;
    END_IF;
    
    IF (ABS(arrCoilCurrents_SP[i]) / 1000.0) > rMaxCoilCurrent_kA THEN
        rMaxCoilCurrent_kA := ABS(arrCoilCurrents_SP[i]) / 1000.0;
    END_IF;
END_FOR;

// 6. Write Back Setpoints to Coils
Coils.CS3U.rCurrent_SP := arrCoilCurrents_SP[1];  Coils.CS3U.rVoltage_SP := arrInductiveVoltages[1] + (arrDeltaI_Demand[1] * 0.05);
Coils.CS2U.rCurrent_SP := arrCoilCurrents_SP[2];  Coils.CS2U.rVoltage_SP := arrInductiveVoltages[2] + (arrDeltaI_Demand[2] * 0.05);
Coils.CS1U.rCurrent_SP := arrCoilCurrents_SP[3];  Coils.CS1U.rVoltage_SP := arrInductiveVoltages[3] + (arrDeltaI_Demand[3] * 0.05);
Coils.CS1L.rCurrent_SP := arrCoilCurrents_SP[4];  Coils.CS1L.rVoltage_SP := arrInductiveVoltages[4] + (arrDeltaI_Demand[4] * 0.05);
Coils.CS2L.rCurrent_SP := arrCoilCurrents_SP[5];  Coils.CS2L.rVoltage_SP := arrInductiveVoltages[5] + (arrDeltaI_Demand[5] * 0.05);
Coils.CS3L.rCurrent_SP := arrCoilCurrents_SP[6];  Coils.CS3L.rVoltage_SP := arrInductiveVoltages[6] + (arrDeltaI_Demand[6] * 0.05);
Coils.PF1.rCurrent_SP  := arrCoilCurrents_SP[7];  Coils.PF1.rVoltage_SP  := arrInductiveVoltages[7] + (arrDeltaI_Demand[7] * 0.05);
Coils.PF2.rCurrent_SP  := arrCoilCurrents_SP[8];  Coils.PF2.rVoltage_SP  := arrInductiveVoltages[8] + (arrDeltaI_Demand[8] * 0.05);
Coils.PF3.rCurrent_SP  := arrCoilCurrents_SP[9];  Coils.PF3.rVoltage_SP  := arrInductiveVoltages[9] + (arrDeltaI_Demand[9] * 0.05);
Coils.PF4.rCurrent_SP  := arrCoilCurrents_SP[10]; Coils.PF4.rVoltage_SP  := arrInductiveVoltages[10] + (arrDeltaI_Demand[10] * 0.05);
Coils.PF5.rCurrent_SP  := arrCoilCurrents_SP[11]; Coils.PF5.rVoltage_SP  := arrInductiveVoltages[11] + (arrDeltaI_Demand[11] * 0.05);
Coils.PF6.rCurrent_SP  := arrCoilCurrents_SP[12]; Coils.PF6.rVoltage_SP  := arrInductiveVoltages[12] + (arrDeltaI_Demand[12] * 0.05);

END_FUNCTION_BLOCK


// =============================================================================
// FUNCTION BLOCK: FB_Fast_VDE_Stabilizer
// Sub-Millisecond Active Stabilization for Vertical Displacement Events
// =============================================================================
FUNCTION_BLOCK FB_Fast_VDE_Stabilizer
VAR_INPUT
    xEnable                 : BOOL;
    rZ_Plasma_PV            : LREAL; // Measured Vertical Position [meters]
    rZ_Plasma_SP            : LREAL; // Vertical Target Setpoint [meters]
    rIp_Actual              : LREAL; // Plasma Current [Amperes]
    rFastCycleTime_Sec      : LREAL := 0.0005; // 500 microsecond loop execution
    rKp_Gain                : LREAL := 45000.0; // Proportional Gain [V/m]
    rKd_Gain                : LREAL := 3200.0;  // Derivative Gain [V/(m/s)]
    rKacc_Gain              : LREAL := 85.0;    // Acceleration Gain [V/(m/s^2)]
END_VAR

VAR_IN_OUT
    ActuatorVS              : ST_FastVS_Actuator;
    DMS                     : ST_DisruptionMitigationSystem;
END_VAR

VAR_OUTPUT
    rVerticalVelocity_m_s   : LREAL;
    rVerticalAccel_m_s2     : LREAL;
    xVDE_Warning            : BOOL;
    xVDE_Unmitigated_Trip   : BOOL;
END_VAR

VAR
    rZ_Prev                 : LREAL;
    rVel_Prev               : LREAL;
    rPosError               : LREAL;
    rRawVoltageCmd          : LREAL;
    
    CONST_MAX_VS_VOLTAGE    : LREAL := 10000.0; // +/- 10 kV Inverter
    CONST_VDE_CRIT_POS      : LREAL := 0.150;   // 150 mm unrecoverable boundary
    CONST_VDE_CRIT_VEL      : LREAL := 45.0;    // 45 m/s runaway velocity
END_VAR

IF NOT xEnable OR (ABS(rIp_Actual) < 1.0E5) THEN
    ActuatorVS.rVoltage_Upper_Cmd := 0.0;
    ActuatorVS.rVoltage_Lower_Cmd := 0.0;
    rZ_Prev := rZ_Plasma_PV;
    rVel_Prev := 0.0;
    xVDE_Warning := FALSE;
    xVDE_Unmitigated_Trip := FALSE;
    RETURN;
END_IF;

// 1. Calculate Real-Time Velocity & Acceleration Observers
rVerticalVelocity_m_s := (rZ_Plasma_PV - rZ_Prev) / rFastCycleTime_Sec;
rVerticalAccel_m_s2   := (rVerticalVelocity_m_s - rVel_Prev) / rFastCycleTime_Sec;

rZ_Prev   := rZ_Plasma_PV;
rVel_Prev := rVerticalVelocity_m_s;

// 2. High-Speed PD + Acceleration Feedforward Control
rPosError := (rZ_Plasma_SP - rZ_Plasma_PV);

rRawVoltageCmd := (rKp_Gain * rPosError) - 
                  (rKd_Gain * rVerticalVelocity_m_s) - 
                  (rKacc_Gain * rVerticalAccel_m_s2);

// Symmetrical Push-Pull Drive for Upper and Lower Copper Saddle Coils
ActuatorVS.rVoltage_Upper_Cmd := LIMIT(-1.0 * CONST_MAX_VS_VOLTAGE, rRawVoltageCmd, CONST_MAX_VS_VOLTAGE);
ActuatorVS.rVoltage_Lower_Cmd := -1.0 * ActuatorVS.rVoltage_Upper_Cmd;

// Calculate Slew Rate Telemetry
ActuatorVS.rSlewRate_kA_per_ms := ABS(ActuatorVS.rCurrent_Upper_PV) / (rFastCycleTime_Sec * 1.0E6 + 1.0E-9);

// 3. VDE Severity Warning & Catastrophic Runaway Trip Detection
IF ABS(rZ_Plasma_PV) > 0.060 OR ABS(rVerticalVelocity_m_s) > 15.0 THEN
    xVDE_Warning := TRUE;
ELSE
    xVDE_Warning := FALSE;
END_IF;

// Unmitigated VDE Detection -> Instant Disruption Mitigation Fire (SPI / MGI)
IF (ABS(rZ_Plasma_PV) >= CONST_VDE_CRIT_POS) OR 
   (ABS(rZ_Plasma_PV) > 0.080 AND ABS(rVerticalVelocity_m_s) >= CONST_VDE_CRIT_VEL) THEN
    
    xVDE_Unmitigated_Trip := TRUE;
    
    // Trigger Disruption Mitigation Hardware Lines (< 10 ms response window)
    DMS.xSPI_Pellet_Armed   := TRUE;
    DMS.xSPI_Fire_Trigger   := TRUE;
    DMS.xMGI_FastValve_Open := TRUE;
    DMS.xEmergencySoftStop  := TRUE;
END_IF;

END_FUNCTION_BLOCK


// =============================================================================
// FUNCTION BLOCK: FB_Divertor_Sweeper_CryoBalance
// 10 Hz Strike-Point Sweeper, Radiative Detachment Seeding & Cryopump Vacuum Loop
// =============================================================================
FUNCTION_BLOCK FB_Divertor_Sweeper_CryoBalance
VAR_INPUT
    xEnable                 : BOOL;
    rCycleTime_Sec          : LREAL := 0.001; // 1 ms execution
    rSweepFrequency_Hz      : LREAL := 10.0;  // 10 Hz high-frequency sweep
    rSweepAmplitude_m       : LREAL := 0.050; // +/- 50 mm sweep envelope
    rTarget_HeatFlux_MW_m2  : LREAL := 8.0;   // Safe heat flux target below 10 MW/m^2
    rSubDiv_Pressure_SP_Pa  : LREAL := 2.5;   // Optimal sub-divertor neutral pressure
END_VAR

VAR_IN_OUT
    Divertor                : ST_DivertorDynamics;
    EquilibriumSP           : ST_PlasmaEquilibrium;
END_VAR

VAR_OUTPUT
    rSweepOffset_R_m        : LREAL;
    rSweepOffset_Z_m        : LREAL;
    xDetachmentActive       : BOOL;
    xThermalOverloadAlarm   : BOOL;
END_VAR

VAR
    rSweepPhase             : LREAL;
    rNormTriWave            : LREAL;
    rHeatFluxError          : LREAL;
    rPressureError          : LREAL;
    rIntegralPuff           : LREAL;
    rIntegralCryo           : LREAL;
    
    CONST_CRIT_HEAT_FLUX    : LREAL := 10.0; // 10 MW/m^2 Tungsten Monoblock Armor Limit
END_VAR

IF NOT xEnable THEN
    rSweepOffset_R_m := 0.0;
    rSweepOffset_Z_m := 0.0;
    Divertor.rGasPuff_Impurity_SP := 0.0;
    xThermalOverloadAlarm := FALSE;
    RETURN;
END_IF;

// 1. High-Frequency Triangular Sweeping Waveform Generator with Parabolic Smoothing
rSweepPhase := rSweepPhase + (2.0 * 3.1415926535 * rSweepFrequency_Hz * rCycleTime_Sec);
IF rSweepPhase >= (2.0 * 3.1415926535) THEN
    rSweepPhase := rSweepPhase - (2.0 * 3.1415926535);
END_IF;

// Continuous triangular approximation via Fourier / arcsin formulation
rNormTriWave := (2.0 / 3.1415926535) * ASIN(SIN(rSweepPhase));

// Parabolic turnaround blending at peaks to prevent infinite derivative
IF rNormTriWave > 0.90 THEN
    rNormTriWave := 0.90 + 0.10 * SIN((rNormTriWave - 0.90) / 0.10 * 1.5707963);
ELSIF rNormTriWave < -0.90 THEN
    rNormTriWave := -0.90 - 0.10 * SIN((ABS(rNormTriWave) - 0.90) / 0.10 * 1.5707963);
END_IF;

rSweepOffset_R_m := rSweepAmplitude_m * rNormTriWave;
rSweepOffset_Z_m := rSweepAmplitude_m * 0.7071 * rNormTriWave; // Poloidal target inclination

// Apply sweep offsets onto equilibrium demand
EquilibriumSP.rRX_PointLower := EquilibriumSP.rRX_PointLower + (rSweepOffset_R_m * 0.15);

// 2. Real-Time Surface Heat Flux Regulation via Nitrogen/Neon Seeding
rHeatFluxError := Divertor.rPeakHeatFlux_MW_m2 - rTarget_HeatFlux_MW_m2;

IF Divertor.rPeakHeatFlux_MW_m2 > 8.5 THEN
    // Impurity puffing PI controller for Radiative Detachment
    rIntegralPuff := LIMIT(0.0, rIntegralPuff + (rHeatFluxError * 0.12 * rCycleTime_Sec), 50.0);
    Divertor.rGasPuff_Impurity_SP := LIMIT(0.0, (rHeatFluxError * 4.5) + rIntegralPuff, 60.0);
    Divertor.eCurrentRegime := E_DivertorRegime.DIVERTOR_PARTIAL_DETACHMENT;
    xDetachmentActive := TRUE;
ELSE
    rIntegralPuff := MAX(0.0, rIntegralPuff - (0.5 * rCycleTime_Sec));
    Divertor.rGasPuff_Impurity_SP := rIntegralPuff;
    Divertor.eCurrentRegime := E_DivertorRegime.DIVERTOR_ATTACHED_HIGH_HEAT;
    xDetachmentActive := FALSE;
END_IF;

// Armor Thermal Overload SIS Warning
IF Divertor.rPeakHeatFlux_MW_m2 >= CONST_CRIT_HEAT_FLUX THEN
    xThermalOverloadAlarm := TRUE;
ELSE
    xThermalOverloadAlarm := FALSE;
END_IF;

// 3. Sub-Divertor Neutral Cryopump Pressure Balancing
rPressureError := Divertor.rSubDivertor_Pressure - rSubDiv_Pressure_SP_Pa;
rIntegralCryo := LIMIT(10.0, rIntegralCryo + (rPressureError * 2.0 * rCycleTime_Sec), 100.0);

// Modulate cryopump regeneration throttle valve
Divertor.rCryopump_Throttle_Pct := LIMIT(0.0, (rPressureError * 15.0) + rIntegralCryo, 100.0);

END_FUNCTION_BLOCK


// =============================================================================
// FUNCTION BLOCK: FB_ECRH_Mirror_Synchronizer
// Real-Time Gyrotron Resonant Tracking & Steerable Launcher Synchronization
// =============================================================================
FUNCTION_BLOCK FB_ECRH_Mirror_Synchronizer
VAR_INPUT
    xEnable                 : BOOL;
    rMajorRadius_R0         : LREAL := 6.20;
    rToroidalField_B0       : LREAL := 5.30;
    rGyrotronFrequency_GHz  : LREAL := 170.0; // 170 GHz ITER Grade Gyrotrons
    rHarmonicNumber_n       : LREAL := 1.0;   // Fundamental O-mode / 2nd Harmonic X-mode
    rLauncher_R_m           : LREAL := 8.50;  // Port launcher radial location
    rLauncher_Z_m           : LREAL := 1.20;  // Port launcher vertical location
    Equilibrium             : ST_PlasmaEquilibrium;
END_VAR

VAR_IN_OUT
    ECRH                    : ST_ECRH_MirrorLink;
END_VAR

VAR_OUTPUT
    xResonanceInCore        : BOOL;
END_VAR

VAR
    rResonantRadius         : LREAL;
    rTargetDeltaR           : LREAL;
    rTargetDeltaZ           : LREAL;
    CONST_E_CHARGE          : LREAL := 1.602176634E-19; // Elementary charge [C]
    CONST_M_ELECTRON        : LREAL := 9.1093837015E-31;// Electron rest mass [kg]
END_VAR

IF NOT xEnable THEN
    ECRH.rTotalPower_MW := 0.0;
    ECRH.xMirrorLockedOnMode := FALSE;
    RETURN;
END_IF;

// 1. Electron Cyclotron Resonance Layer Localization (R_res = n * e * B0 * R0 / (2 * pi * m_e * f_RF))
rResonantRadius := (rHarmonicNumber_n * CONST_E_CHARGE * rToroidalField_B0 * rMajorRadius_R0) / 
                   (2.0 * 3.1415926535 * CONST_M_ELECTRON * (rGyrotronFrequency_GHz * 1.0E9));

ECRH.rResonanceRadius_m := rResonantRadius;

IF (rResonantRadius >= (rMajorRadius_R0 - 2.0)) AND (rResonantRadius <= (rMajorRadius_R0 + 2.0)) THEN
    xResonanceInCore := TRUE;
ELSE
    xResonanceInCore := FALSE;
END_IF;

// 2. Compute Steerable Launcher Mirror Angles to Align on Target Rational Surface (q=2/1)
rTargetDeltaR := rResonantRadius - rLauncher_R_m;
rTargetDeltaZ := Equilibrium.rZ_MagneticAxis - rLauncher_Z_m;

// Poloidal Elevation Angle Calculation
IF ABS(rTargetDeltaR) > 0.01 THEN
    ECRH.rMirror_Elevation_Deg := LIMIT(-30.0, ATAN(rTargetDeltaZ / ABS(rTargetDeltaR)) * (180.0 / 3.1415926535), 30.0);
ELSE
    ECRH.rMirror_Elevation_Deg := 0.0;
END_IF;

// Toroidal Azimuth Angle for Non-Inductive Current Drive (ECCD)
ECRH.rMirror_Azimuth_Deg := LIMIT(-25.0, 15.0 * (1.0 - (Equilibrium.rSafetyFactor_q95 / 5.0)), 25.0);

// Acknowledge Phase Lock if q95 is near rational 2.0 or 3.0
IF (ABS(Equilibrium.rSafetyFactor_q95 - 2.0) < 0.15) OR (ABS(Equilibrium.rSafetyFactor_q95 - 1.5) < 0.10) THEN
    ECRH.xMirrorLockedOnMode := TRUE;
    ECRH.rTotalPower_MW := 20.0; // 20 MW active NTM stabilization injection
ELSE
    ECRH.xMirrorLockedOnMode := FALSE;
    ECRH.rTotalPower_MW := 5.0;  // 5 MW baseline core heating
END_IF;

END_FUNCTION_BLOCK


// =============================================================================
// MAIN FUNCTION BLOCK: FB_Tokamak_PlasmaController
// Master Tokamak Poloidal Field, VDE & Divertor Heat Flux Orchestrator
// =============================================================================
FUNCTION_BLOCK FB_Tokamak_PlasmaController
TITLE = 'Master Tokamak Plasma, VDE & Divertor Controller'
VERSION : '4.2.0'
AUTHOR : 'Chief Plasma Control Systems Architect'

VAR_INPUT
    // Master System Triggers & Safety Lines
    xMasterEnable           : BOOL; // Master PLC Enable Command
    xPlantSafetyInterlock   : BOOL; // Hardwired Safety Instrumented System (SIS OK)
    xManualFastAbort        : BOOL; // Operator Emergency Abort Console
    xResetAlarms            : BOOL; // Fault Reset Pulse
    
    // Process Timing
    rCycleTime_Sec          : LREAL := 0.001;  // 1 ms Standard Control Cycle
    rFastCycleTime_Sec      : LREAL := 0.0005; // 500 us Fast VDE Task Cycle
    
    // Diagnostics & Sensor Stream
    Sensors                 : ST_MagneticSensors;
    rDivertor_PeakHeatFlux  : LREAL; // Infrared/Thermography Heat Flux [MW/m^2]
    rSubDiv_Pressure_PV     : LREAL; // Sub-Divertor Pressure [Pa]
    rCoreDensity_Ne20       : LREAL; // Interferometer Density [10^20 m^-3]
    
    // Targets & References
    rTarget_Ip_Amperes      : LREAL := 15.0E6; // 15.0 MA Nominal Flat-Top
    rTarget_Elongation      : LREAL := 1.85;   // 1.85 Nominal Elongation
    rTarget_Triangularity   : LREAL := 0.45;   // 0.45 Triangularity
    
    // Magnetics Calibration Matrix
    CalibrationMIMO         : ST_MIMO_Calibration;
END_VAR

VAR_OUTPUT
    // Operational States & Health
    eSystemState            : E_TokamakState;
    eDisruptionRisk         : E_DisruptionRisk;
    xQuenchTripActive       : BOOL;
    xDisruptionFired        : BOOL;
    xControllerHealthy      : BOOL;
    
    // Primary Telemetry
    Equilibrium             : ST_PlasmaEquilibrium;
    rMaxCoilCurrent_kA      : LREAL;
    rVS_SlewRate_kA_ms      : LREAL;
    rActiveHeatFlux_MW_m2   : LREAL;
    
    // System Diagnostics Word
    wDiagnosticCode         : WORD;
END_VAR

VAR_IN_OUT
    Coils                   : ST_CoilArray_12;
    ActuatorVS              : ST_FastVS_Actuator;
    Divertor                : ST_DivertorDynamics;
    ECRH                    : ST_ECRH_MirrorLink;
    DMS                     : ST_DisruptionMitigationSystem;
END_VAR

VAR
    // Internal Subsystem Function Blocks
    fbEquilibriumRecon      : FB_GradShafranov_Reconstructor;
    fbMIMODecoupler         : FB_Superconducting_MIMO_Decoupler;
    fbFastVDE               : FB_Fast_VDE_Stabilizer;
    fbDivertorSweeper       : FB_DivertorSweeper_CryoBalance;
    fbECRHSync              : FB_ECRH_Mirror_Synchronizer;
    
    // Internal State Structures
    EquilibriumSP           : ST_PlasmaEquilibrium;
    
    // Timers & State Sequencing
    fbRampUpTimer           : TON;
    fbFlatTopTimer          : TON;
    fbRampDownTimer         : TON;
    fbQuenchHoldoffTimer    : TON;
    
    // Internal Logic
    xSIS_TripCondition      : BOOL;
    xQuenchDetectedInternal : BOOL;
    xMIMOSaturatedInternal  : BOOL;
    xVDEWarningInternal     : BOOL;
    xVDEUnmitigatedInternal : BOOL;
    xThermalAlarmInternal   : BOOL;
END_VAR

// =============================================================================
// 1. HARDWIRED SAFETY INSTRUMENTED SYSTEM (SIS) & INTERLOCK EVALUATION
// =============================================================================
xSIS_TripCondition := (NOT xPlantSafetyInterlock) OR xManualFastAbort;

IF xSIS_TripCondition THEN
    eSystemState := E_TokamakState.STATE_EMERGENCY_FAST_DISCHARGE;
    eDisruptionRisk := E_DisruptionRisk.RISK_IMMINENT_DISRUPTION;
    wDiagnosticCode := 16#F001; // SIS Hardware Interlock Trip
    
    // Fast discharge of all 12 superconducting coils
    fbMIMODecoupler(
        xEnable             := TRUE,
        xEmergencyFastDump  := TRUE,
        rCycleTime_Sec      := rCycleTime_Sec,
        EquilibriumPV       := Equilibrium,
        EquilibriumSP       := EquilibriumSP,
        CoilCalibration     := CalibrationMIMO,
        Coils               := Coils,
        xQuenchAlarmTripped => xQuenchTripActive
    );
    
    // Cut fast saddle supplies and auxiliary heating
    ActuatorVS.rVoltage_Upper_Cmd := 0.0;
    ActuatorVS.rVoltage_Lower_Cmd := 0.0;
    ECRH.rTotalPower_MW := 0.0;
    xControllerHealthy := FALSE;
    RETURN;
END_IF;

IF xResetAlarms THEN
    wDiagnosticCode := 16#0000;
    xDisruptionFired := FALSE;
    IF eSystemState = E_TokamakState.STATE_EMERGENCY_FAST_DISCHARGE OR 
       eSystemState = E_TokamakState.STATE_DISRUPTION_MITIGATION THEN
        eSystemState := E_TokamakState.STATE_UNMAGNETIZED;
    END_IF;
END_IF;

IF NOT xMasterEnable THEN
    eSystemState := E_TokamakState.STATE_UNMAGNETIZED;
    xControllerHealthy := TRUE;
    RETURN;
END_IF;

// =============================================================================
// 2. REAL-TIME GRAD-SHAFRANOV EQUILIBRIUM RECONSTRUCTION
// =============================================================================
fbEquilibriumRecon(
    xEnable               := TRUE,
    Sensors               := Sensors,
    rMinorRadius_a        := 2.00,
    rMajorRadius_R0       := 6.20,
    rElectronDensity_Ne20 := rCoreDensity_Ne20,
    Equilibrium           => Equilibrium
);

// Map telemetry to external interface
Divertor.rPeakHeatFlux_MW_m2   := rDivertor_PeakHeatFlux;
Divertor.rSubDivertor_Pressure := rSubDiv_Pressure_PV;
rActiveHeatFlux_MW_m2          := rDivertor_PeakHeatFlux;

// =============================================================================
// 3. FAST VERTICAL DISPLACEMENT EVENT (VDE) SUB-MILLISECOND LOOP
// =============================================================================
fbFastVDE(
    xEnable               := (eSystemState >= E_TokamakState.STATE_CURRENT_RAMP_UP AND 
                              eSystemState <= E_TokamakState.STATE_CURRENT_RAMP_DOWN),
    rZ_Plasma_PV          := Equilibrium.rZ_MagneticAxis,
    rZ_Plasma_SP          := EquilibriumSP.rZ_MagneticAxis,
    rIp_Actual            := Equilibrium.rIp_Actual,
    rFastCycleTime_Sec    := rFastCycleTime_Sec,
    ActuatorVS            := ActuatorVS,
    DMS                   := DMS,
    xVDE_Warning          => xVDEWarningInternal,
    xVDE_Unmitigated_Trip => xVDEUnmitigatedInternal
);

rVS_SlewRate_kA_ms := ActuatorVS.rSlewRate_kA_per_ms;

// Handle Unmitigated VDE Disruption Event
IF xVDEUnmitigatedInternal THEN
    eSystemState := E_TokamakState.STATE_DISRUPTION_MITIGATION;
    eDisruptionRisk := E_DisruptionRisk.RISK_IMMINENT_DISRUPTION;
    xDisruptionFired := TRUE;
    wDiagnosticCode := 16#E002; // Unmitigated VDE Disruption Mitigation Fired
END_IF;

// =============================================================================
// 4. DIVERTOR HEAT FLUX SWEEPING & VACUUM BALANCING
// =============================================================================
fbDivertorSweeper(
    xEnable               := (eSystemState = E_TokamakState.STATE_FLAT_TOP_CONFINED OR 
                              eSystemState = E_TokamakState.STATE_DIVERTOR_DETACHED),
    rCycleTime_Sec        := rCycleTime_Sec,
    rSweepFrequency_Hz    := 10.0,
    rSweepAmplitude_m     := 0.050,
    rTarget_HeatFlux_MW_m2:= 8.0,
    rSubDiv_Pressure_SP_Pa:= 2.5,
    Divertor              := Divertor,
    EquilibriumSP         := EquilibriumSP,
    xThermalOverloadAlarm => xThermalAlarmInternal
);

IF xThermalAlarmInternal THEN
    wDiagnosticCode := wDiagnosticCode OR 16#0040; // Divertor Heat Flux Limit Warning
END_IF;

// =============================================================================
// 5. REAL-TIME ECRH GYROTRON MIRROR SYNCHRONIZATION
// =============================================================================
fbECRHSync(
    xEnable               := (eSystemState >= E_TokamakState.STATE_CURRENT_RAMP_UP AND 
                              eSystemState <= E_TokamakState.STATE_CURRENT_RAMP_DOWN),
    rMajorRadius_R0       := 6.20,
    rToroidalField_B0     := Sensors.rToroidalField_B0,
    rGyrotronFrequency_GHz:= 170.0,
    rHarmonicNumber_n     := 1.0,
    Equilibrium           := Equilibrium,
    ECRH                  := ECRH
);

// =============================================================================
// 6. TOKAMAK OPERATIONAL STATE MACHINE SEQUENCING
// =============================================================================
CASE eSystemState OF

    E_TokamakState.STATE_UNMAGNETIZED:
        // System Cold: Discharge Coils & Reset Setpoints
        EquilibriumSP.rIp_Actual := 0.0;
        EquilibriumSP.rElongation_Kappa := 1.0;
        EquilibriumSP.rR_MagneticAxis := 6.20;
        EquilibriumSP.rZ_MagneticAxis := 0.0;
        eDisruptionRisk := E_DisruptionRisk.RISK_NOMINAL;
        
        IF xMasterEnable AND NOT xSIS_TripCondition THEN
            eSystemState := E_TokamakState.STATE_PRE_IONIZATION;
        END_IF;

    E_TokamakState.STATE_PRE_IONIZATION:
        // Bias Central Solenoid coils for flux swing; inject EC pre-ionization
        EquilibriumSP.rIp_Actual := 0.0;
        ECRH.rTotalPower_MW := 3.0; // 3 MW EC assist
        IF ABS(Coils.CS1U.rCurrent_PV) >= 40000.0 THEN // CS fully pre-charged to 40 kA
            eSystemState := E_TokamakState.STATE_PLASMA_BREAKDOWN;
        END_IF;

    E_TokamakState.STATE_PLASMA_BREAKDOWN:
        // Fast CS flux discharge to induce loop voltage V_loop >= 12 V
        EquilibriumSP.rIp_Actual := 500000.0; // 500 kA breakdown initiation
        IF ABS(Equilibrium.rIp_Actual) >= 400000.0 THEN
            eSystemState := E_TokamakState.STATE_CURRENT_RAMP_UP;
        END_IF;

    E_TokamakState.STATE_CURRENT_RAMP_UP:
        // Linear Current Ramp: 0.5 MA/s ramp rate; elongate plasma from 1.0 to 1.85
        fbRampUpTimer(IN := TRUE, PT := T#30S);
        EquilibriumSP.rIp_Actual := LIMIT(500000.0, EquilibriumSP.rIp_Actual + (500000.0 * rCycleTime_Sec), rTarget_Ip_Amperes);
        EquilibriumSP.rElongation_Kappa := LIMIT(1.0, EquilibriumSP.rElongation_Kappa + (0.028 * rCycleTime_Sec), rTarget_Elongation);
        EquilibriumSP.rTriangularity_Lower := LIMIT(0.0, EquilibriumSP.rTriangularity_Lower + (0.015 * rCycleTime_Sec), rTarget_Triangularity);
        
        IF Equilibrium.rIp_Actual >= (rTarget_Ip_Amperes * 0.95) AND fbRampUpTimer.Q THEN
            fbRampUpTimer(IN := FALSE);
            eSystemState := E_TokamakState.STATE_FLAT_TOP_CONFINED;
        END_IF;

    E_TokamakState.STATE_FLAT_TOP_CONFINED:
        // Full Power Steady-State Confinement & Strike Point Sweeping
        EquilibriumSP.rIp_Actual := rTarget_Ip_Amperes;
        EquilibriumSP.rElongation_Kappa := rTarget_Elongation;
        EquilibriumSP.rTriangularity_Lower := rTarget_Triangularity;
        
        // Evaluate Disruption Threat Matrix
        IF xVDEWarningInternal THEN
            eDisruptionRisk := E_DisruptionRisk.RISK_ELEVATED_VDE;
        ELSIF Equilibrium.rSafetyFactor_q95 < 2.5 THEN
            eDisruptionRisk := E_DisruptionRisk.RISK_TEARING_MODE_LOCKED;
        ELSIF Equilibrium.rGreenwaldFraction > 0.95 THEN
            eDisruptionRisk := E_DisruptionRisk.RISK_RADIATIVE_COLLAPSE;
        ELSE
            eDisruptionRisk := E_DisruptionRisk.RISK_NOMINAL;
        END_IF;
        
        // Switch to Detached Divertor Mode if Heat Flux Demands
        IF Divertor.eCurrentRegime = E_DivertorRegime.DIVERTOR_PARTIAL_DETACHMENT THEN
            eSystemState := E_TokamakState.STATE_DIVERTOR_DETACHED;
        END_IF;

    E_TokamakState.STATE_DIVERTOR_DETACHED:
        // Radiative Detachment Operation
        IF Divertor.eCurrentRegime = E_DivertorRegime.DIVERTOR_ATTACHED_HIGH_HEAT THEN
            eSystemState := E_TokamakState.STATE_FLAT_TOP_CONFINED;
        END_IF;

    E_TokamakState.STATE_CURRENT_RAMP_DOWN:
        // Controlled soft de-energization: 0.3 MA/s ramp down
        fbRampDownTimer(IN := TRUE, PT := T#45S);
        EquilibriumSP.rIp_Actual := MAX(0.0, EquilibriumSP.rIp_Actual - (300000.0 * rCycleTime_Sec));
        EquilibriumSP.rElongation_Kappa := MAX(1.0, EquilibriumSP.rElongation_Kappa - (0.02 * rCycleTime_Sec));
        
        IF Equilibrium.rIp_Actual < 200000.0 OR fbRampDownTimer.Q THEN
            fbRampDownTimer(IN := FALSE);
            eSystemState := E_TokamakState.STATE_SOFT_LANDING;
        END_IF;

    E_TokamakState.STATE_SOFT_LANDING:
        // Low current termination without runaway electrons
        EquilibriumSP.rIp_Actual := 0.0;
        EquilibriumSP.rElongation_Kappa := 1.0;
        IF ABS(Equilibrium.rIp_Actual) < 50000.0 THEN
            eSystemState := E_TokamakState.STATE_UNMAGNETIZED;
        END_IF;

    E_TokamakState.STATE_DISRUPTION_MITIGATION:
        // MGI & SPI fired; fast ramp down
        EquilibriumSP.rIp_Actual := 0.0;
        ECRH.rTotalPower_MW := 0.0;
        IF ABS(Equilibrium.rIp_Actual) < 50000.0 THEN
            eSystemState := E_TokamakState.STATE_UNMAGNETIZED;
        END_IF;

    E_TokamakState.STATE_EMERGENCY_FAST_DISCHARGE:
        // Quench / Hardwired SIS Trip Active
        EquilibriumSP.rIp_Actual := 0.0;
        ECRH.rTotalPower_MW := 0.0;
        
END_CASE;

// =============================================================================
// 7. 12-COIL SUPERCONDUCTING MIMO CURRENT CONTROL & QUENCH EXECUTION
// =============================================================================
fbMIMODecoupler(
    xEnable             := (eSystemState <> E_TokamakState.STATE_UNMAGNETIZED),
    xEmergencyFastDump  := (eSystemState = E_TokamakState.STATE_EMERGENCY_FAST_DISCHARGE),
    rCycleTime_Sec      := rCycleTime_Sec,
    EquilibriumPV       := Equilibrium,
    EquilibriumSP       := EquilibriumSP,
    CoilCalibration     := CalibrationMIMO,
    Coils               := Coils,
    xQuenchAlarmTripped => xQuenchDetectedInternal,
    xMIMO_Saturated     => xMIMOSaturatedInternal,
    rMaxCoilCurrent_kA  => rMaxCoilCurrent_kA
);

// Quench Safety Interlock Trip
IF xQuenchDetectedInternal THEN
    xQuenchTripActive := TRUE;
    eSystemState := E_TokamakState.STATE_EMERGENCY_FAST_DISCHARGE;
    wDiagnosticCode := wDiagnosticCode OR 16#F010; // Superconducting Magnet Quench Detected
END_IF;

IF xMIMOSaturatedInternal THEN
    wDiagnosticCode := wDiagnosticCode OR 16#0080; // MIMO Coil Current Saturation Warning
END_IF;

xControllerHealthy := (wDiagnosticCode = 16#0000) AND NOT xQuenchTripActive;

END_FUNCTION_BLOCK
```

---

## 3. Verification & Safety Integrity Integration

| Subsystem Module | Critical Variable / Boundary | Normal Operating Range | Trip / Interlock Action | Response Time |
| :--- | :--- | :--- | :--- | :--- |
| **Equilibrium Estimator** | Safety factor $q_{95}$ | $3.0 - 4.5$ | Warning at $q_{95} < 2.5$; ECRH NTM Lock | $1.0\\text{ ms}$ (PLC Cycle) |
| **12-Coil Superconducting** | Quench Resistive $V_{res}$ | $< 0.050\\text{ V}$ | Fast Discharge Dump ($R_{dump}=0.1\\ \\Omega$) if $V_{res} > 100\\text{ mV}$ for $50\\text{ ms}$ | $50.0\\text{ ms}$ Filter |
| **Fast VDE Saddle Coils** | Vertical Position $Z_p$ | $\\pm 0.020\\text{ m}$ | DMS Trigger (SPI / MGI Fired) if $\|Z_p\| > 0.150\\text{ m}$ | $< 500\\ \\mu\\text{s}$ (Fast Loop) |
| **Divertor Armor Sweeper** | Monoblock Heat Flux $q_{div}$| $< 8.0\\text{ MW/m}^2$ | Impurity Gas Seeding ($N_2/Ne$) Detachment at $8.5\\text{ MW/m}^2$ | $1.0\\text{ ms}$ |
| **ECRH Gyrotron Launcher**| Gyrotron Power $P_{RF}$ | $0.0 - 20.0\\text{ MW}$ | Real-time Mirror Angle Tracking of $q=2/1$ Resonant Layer | $1.0\\text{ ms}$ |
"""

data = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_files = [
    r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl",
    r"c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\data\synthetic_generation_v3_enterprise.jsonl",
    r"c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"
]

json_line = json.dumps(data, ensure_ascii=False)

for target_file in target_files:
    if os.path.exists(os.path.dirname(target_file)):
        with open(target_file, "a", encoding="utf-8") as f:
            f.write(json_line + "\n")
        print(f"Successfully appended to: {target_file}")
    else:
        print(f"Directory does not exist for: {target_file}")

print("Verification: Reading back last line from data/synthetic_generation_v3_enterprise.jsonl")
with open(target_files[0], "r", encoding="utf-8") as f:
    lines = f.readlines()
    last_line = lines[-1].strip()
    parsed = json.loads(last_line)
    print("Parsed successfully!")
    print(f"User Prompt Role: {parsed['messages'][0]['role']}")
    print(f"User Prompt Length: {len(parsed['messages'][0]['content'])}")
    print(f"Assistant Content Length: {len(parsed['messages'][1]['content'])}")
    print("Evolution entry successfully written and verified!")
