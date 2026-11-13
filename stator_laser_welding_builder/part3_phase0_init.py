# stator_laser_welding_builder/part3_phase0_init.py

def get_phase0_init():
    return """(*
====================================================================================================
PHASE 0: ONE-SHOT FIRST-SCAN SYSTEM INITIALIZATION & CYBER-PHYSICAL MATRIX ALLOCATION
Discretization Period Ts = 0.002 [s] (2.0 ms), Oxygen-Free High-Conductivity Copper (Cu-OF/Cu-ETP)
Hairpin Cross-Section: 2.80 [mm] x 1.60 [mm], Slot Depth: 42.0 [mm], 192 Hairpin Crowns (96 Seam Welds)
====================================================================================================
*)

IF NOT bFirstScanDone THEN
    (* 1. Initialize Discrete Plant System Matrix arrA_Matrix (8x8) *)
    (* State 1: Molten Copper Weld Pool Core Temperature T_pool [deg C] *)
    arrA_Matrix[1, 1] := 0.942150;  (* Intrinsic molten pool thermal conduction and blackbody radiation loss *)
    arrA_Matrix[1, 2] := 0.045230;  (* Thermal conduction coupling from heat-affected zone back to weld pool *)
    arrA_Matrix[1, 3] := 0.008120;  (* Long-range thermal coupling from bulk hairpin copper pin *)
    arrA_Matrix[1, 4] := 125.4500;  (* Keyhole vapor capillary depth latent heat re-condensation coupling *)
    arrA_Matrix[1, 5] := -0.01850;  (* Molten nugget volume expansion thermal dilution factor *)
    arrA_Matrix[1, 6] := 0.000000;  (* Chuck angular error uncoupling *)
    arrA_Matrix[1, 7] := 0.000000;  (* Chuck rotational speed uncoupling *)
    arrA_Matrix[1, 8] := 0.052100;  (* Shielding gas boundary layer heat transfer coefficient *)

    (* State 2: Copper Heat-Affected Zone (HAZ) Temperature T_haz [deg C] *)
    arrA_Matrix[2, 1] := 0.038450;  (* Heat conduction influx from molten weld nugget boundary *)
    arrA_Matrix[2, 2] := 0.915200;  (* Intrinsic HAZ thermal dissipation along rectangular copper shank *)
    arrA_Matrix[2, 3] := 0.042180;  (* Heat conduction feedback from cooler hairpin shank *)
    arrA_Matrix[2, 4] := 18.25000;  (* Secondary vapor condensation plume thermal influx *)
    arrA_Matrix[2, 5] := 0.000000;  (* Volume independence *)
    arrA_Matrix[2, 6] := 0.000000;  (* Chuck angular uncoupling *)
    arrA_Matrix[2, 7] := 0.000000;  (* Chuck speed uncoupling *)
    arrA_Matrix[2, 8] := -0.01250;  (* Shielding gas convective boundary cooling *)

    (* State 3: Copper Hairpin Pin-Tip Bulk Temperature T_pin [deg C] *)
    arrA_Matrix[3, 1] := 0.004120;  (* Tertiary heat flux from molten pool *)
    arrA_Matrix[3, 2] := 0.028750;  (* Conduction from HAZ into pin shank towards slot liner *)
    arrA_Matrix[3, 3] := 0.965400;  (* Pin bulk thermal capacitance retention *)
    arrA_Matrix[3, 4] := 0.000000;  (* Keyhole independence *)
    arrA_Matrix[3, 5] := 0.000000;  (* Nugget volume independence *)
    arrA_Matrix[3, 6] := 0.000000;  (* Motion uncoupling *)
    arrA_Matrix[3, 7] := 0.000000;  (* Motion uncoupling *)
    arrA_Matrix[3, 8] := -0.00840;  (* Ambient shielding gas convective cooling *)

    (* State 4: Keyhole Vapor Capillary Depth h_keyhole [mm] *)
    arrA_Matrix[4, 1] := 0.000450;  (* Thermal evaporation vapor pressure recoil boost *)
    arrA_Matrix[4, 2] := 0.000000;  (* HAZ independence *)
    arrA_Matrix[4, 3] := 0.000000;  (* Pin bulk independence *)
    arrA_Matrix[4, 4] := 0.824500;  (* Keyhole capillary hydrostatic & surface tension collapse decay *)
    arrA_Matrix[4, 5] := -0.00280;  (* Nugget volume hydrostatic dampening *)
    arrA_Matrix[4, 6] := 0.000000;  (* Chuck uncoupling *)
    arrA_Matrix[4, 7] := 0.000000;  (* Chuck uncoupling *)
    arrA_Matrix[4, 8] := 0.000120;  (* Shielding gas plume stagnation pressure contribution *)

    (* State 5: Weld Nugget Molten Pool Volume V_nugget [mm3] *)
    arrA_Matrix[5, 1] := 0.001850;  (* Volumetric expansion rate per degree above melting point *)
    arrA_Matrix[5, 2] := 0.000320;  (* HAZ boundary preheating volumetric contribution *)
    arrA_Matrix[5, 3] := 0.000000;  (* Pin bulk independence *)
    arrA_Matrix[5, 4] := 0.142500;  (* Capillary keyhole penetration volume displacement *)
    arrA_Matrix[5, 5] := 0.985200;  (* Nugget volume retention and liquid surface tension equilibrium *)
    arrA_Matrix[5, 6] := 0.000000;  (* Motion uncoupling *)
    arrA_Matrix[5, 7] := 0.000000;  (* Motion uncoupling *)
    arrA_Matrix[5, 8] := 0.000000;  (* Gas flow volume uncoupling *)

    (* State 6: Rotary Chuck Angular Position Error Delta_theta [mrad] *)
    arrA_Matrix[6, 1] := 0.000000;  (* Thermal uncoupling *)
    arrA_Matrix[6, 2] := 0.000000;  (* Thermal uncoupling *)
    arrA_Matrix[6, 3] := 0.000000;  (* Thermal uncoupling *)
    arrA_Matrix[6, 4] := 0.000000;  (* Keyhole uncoupling *)
    arrA_Matrix[6, 5] := 0.000000;  (* Nugget uncoupling *)
    arrA_Matrix[6, 6] := 1.000000;  (* Kinematic pure integration of angular position *)
    arrA_Matrix[6, 7] := -0.00200;  (* Kinematic integration step: Delta_theta[k+1] = Delta_theta[k] - Ts*omega *)
    arrA_Matrix[6, 8] := 0.000000;  (* Gas uncoupling *)

    (* State 7: Direct-Drive Rotary Direct-Drive Motor Speed omega_chuck [rad/s] *)
    arrA_Matrix[7, 1] := 0.000000;  (* Thermal uncoupling *)
    arrA_Matrix[7, 2] := 0.000000;  (* Thermal uncoupling *)
    arrA_Matrix[7, 3] := 0.000000;  (* Thermal uncoupling *)
    arrA_Matrix[7, 4] := 0.000000;  (* Keyhole uncoupling *)
    arrA_Matrix[7, 5] := 0.000000;  (* Nugget uncoupling *)
    arrA_Matrix[7, 6] := 0.125000;  (* Servo position spring restorative stiffness *)
    arrA_Matrix[7, 7] := 0.981800;  (* Direct-drive magnetic bearing viscous friction damping factor *)
    arrA_Matrix[7, 8] := 0.000000;  (* Gas uncoupling *)

    (* State 8: Shielding Gas Boundary Layer Nitrogen Concentration C_N2 [%] *)
    arrA_Matrix[8, 1] := -0.00085;  (* High-temperature metal vapor displacement dilution *)
    arrA_Matrix[8, 2] := 0.000000;  (* HAZ uncoupling *)
    arrA_Matrix[8, 3] := 0.000000;  (* Pin bulk uncoupling *)
    arrA_Matrix[8, 4] := -0.01520;  (* Keyhole jet metal plume atmospheric aspiration *)
    arrA_Matrix[8, 5] := 0.000000;  (* Nugget uncoupling *)
    arrA_Matrix[8, 6] := 0.000000;  (* Motion uncoupling *)
    arrA_Matrix[8, 7] := -0.00250;  (* Chuck rotational aerodynamic shear dilution *)
    arrA_Matrix[8, 8] := 0.912500;  (* Pure gas stagnation retention coefficient *)

    (* 2. Initialize Discrete Actuator Input Coupling Matrix arrB_Matrix (8x4) *)
    (* Inputs: u1: Laser Power [kW], u2: Wobble Freq [Hz], u3: Chuck Torque [Nm], u4: Gas Flow [L/min] *)
    (* State 1: T_pool *)
    arrB_Matrix[1, 1] := 248.5000;  (* Laser delivered optical power to pool temperature gain [deg C / kW] *)
    arrB_Matrix[1, 2] := -0.14500;  (* Wobble frequency pool stirring thermal dissipation [deg C / Hz] *)
    arrB_Matrix[1, 3] := 0.000000;  (* Chuck torque uncoupling *)
    arrB_Matrix[1, 4] := -0.85000;  (* Nitrogen gas impingement convective cooling [deg C / (L/min)] *)

    (* State 2: T_haz *)
    arrB_Matrix[2, 1] := 32.40000;  (* Laser power conduction to heat-affected zone [deg C / kW] *)
    arrB_Matrix[2, 2] := 0.082000;  (* Wobble expansion broadens HAZ slightly [deg C / Hz] *)
    arrB_Matrix[2, 3] := 0.000000;  (* Chuck torque uncoupling *)
    arrB_Matrix[2, 4] := -0.42000;  (* Gas convective cooling on HAZ [deg C / (L/min)] *)

    (* State 3: T_pin *)
    arrB_Matrix[3, 1] := 4.850000;  (* Laser power conduction to pin shank base [deg C / kW] *)
    arrB_Matrix[3, 2] := 0.012000;  (* Wobble broadens pin conduction base [deg C / Hz] *)
    arrB_Matrix[3, 3] := 0.000000;  (* Chuck torque uncoupling *)
    arrB_Matrix[3, 4] := -0.15000;  (* Gas cooling on pin tip [deg C / (L/min)] *)

    (* State 4: h_keyhole *)
    arrB_Matrix[4, 1] := 0.428000;  (* Laser beam power to keyhole penetration depth [mm / kW] *)
    arrB_Matrix[4, 2] := -0.00095;  (* Wobble beam motion spreads spot, reducing keyhole depth [mm / Hz] *)
    arrB_Matrix[4, 3] := 0.000000;  (* Chuck torque uncoupling *)
    arrB_Matrix[4, 4] := 0.002400;  (* Aerodynamic gas pressure assist on keyhole opening [mm / (L/min)] *)

    (* State 5: V_nugget *)
    arrB_Matrix[5, 1] := 1.954000;  (* Laser power to molten nugget pool volume [mm3 / kW] *)
    arrB_Matrix[5, 2] := 0.002850;  (* Wobble frequency enlarges molten bead cross-section [mm3 / Hz] *)
    arrB_Matrix[5, 3] := 0.000000;  (* Chuck torque uncoupling *)
    arrB_Matrix[5, 4] := -0.00850;  (* Gas flow pool surface blow-away suppression [mm3 / (L/min)] *)

    (* State 6: Delta_theta *)
    arrB_Matrix[6, 1] := 0.000000;  (* Laser uncoupling *)
    arrB_Matrix[6, 2] := 0.000000;  (* Wobble uncoupling *)
    arrB_Matrix[6, 3] := -0.00002;  (* Direct-drive torque to angular position error delta [mrad / Nm] *)
    arrB_Matrix[6, 4] := 0.000000;  (* Gas uncoupling *)

    (* State 7: omega_chuck *)
    arrB_Matrix[7, 1] := 0.000000;  (* Laser uncoupling *)
    arrB_Matrix[7, 2] := 0.000000;  (* Wobble uncoupling *)
    arrB_Matrix[7, 3] := 0.128500;  (* Direct-drive motor electromagnetic torque to acceleration [rad/s / Nm] *)
    arrB_Matrix[7, 4] := 0.000000;  (* Gas uncoupling *)

    (* State 8: C_N2 *)
    arrB_Matrix[8, 1] := -0.04500;  (* Metal vapor plume displacement per kW laser power [% / kW] *)
    arrB_Matrix[8, 2] := 0.001200;  (* Wobble plume dispersion factor [% / Hz] *)
    arrB_Matrix[8, 3] := 0.000000;  (* Chuck torque uncoupling *)
    arrB_Matrix[8, 4] := 0.024500;  (* Mass flow delivery to boundary layer N2 concentration [% / (L/min)] *)

    (* 3. Initialize Discrete Disturbance Coupling Matrix arrEw_Matrix (8x3) *)
    (* Disturbances: w1: Gap [mm], w2: Height Mismatch [mm], w3: Surface Reflectivity Delta [-] *)
    (* State 1: T_pool *)
    arrEw_Matrix[1, 1] := -145.200; (* Hairpin gap causes beam bypass, dropping molten pool temp [deg C / mm] *)
    arrEw_Matrix[1, 2] := -85.4000; (* Pin height offset causes asymmetric heat distribution [deg C / mm] *)
    arrEw_Matrix[1, 3] := -385.000; (* Surface copper oxidation / reflectivity deviation [deg C / unit] *)

    (* State 2: T_haz *)
    arrEw_Matrix[2, 1] := -25.6000; (* Gap reduces heat conduction to neighboring pin [deg C / mm] *)
    arrEw_Matrix[2, 2] := 42.10000; (* Height offset causes upper pin overheating [deg C / mm] *)
    arrEw_Matrix[2, 3] := -48.2000; (* Reflectivity thermal absorption loss [deg C / unit] *)

    (* State 3: T_pin *)
    arrEw_Matrix[3, 1] := -8.45000; (* Gap conduction reduction [deg C / mm] *)
    arrEw_Matrix[3, 2] := 18.50000; (* Shorter pin thermal shielding loss [deg C / mm] *)
    arrEw_Matrix[3, 3] := -12.4000; (* Reflectivity loss [deg C / unit] *)

    (* State 4: h_keyhole *)
    arrEw_Matrix[4, 1] := -1.85000; (* Gap causes keyhole collapse and beam blow-through [mm / mm] *)
    arrEw_Matrix[4, 2] := -0.45000; (* Height offset alters laser focal position [mm / mm] *)
    arrEw_Matrix[4, 3] := -0.65000; (* Surface reflection drops keyhole coupling [mm / unit] *)

    (* State 5: V_nugget *)
    arrEw_Matrix[5, 1] := -4.85000; (* Gap causes molten copper loss through crown separation [mm3 / mm] *)
    arrEw_Matrix[5, 2] := -1.25000; (* Asymmetric bead volume shrinkage [mm3 / mm] *)
    arrEw_Matrix[5, 3] := -2.15000; (* Absorptivity drop reduces melted copper volume [mm3 / unit] *)

    (* State 6: Delta_theta *)
    arrEw_Matrix[6, 1] := 0.000000; (* Gap uncoupling *)
    arrEw_Matrix[6, 2] := 0.000000; (* Height uncoupling *)
    arrEw_Matrix[6, 3] := 0.000000; (* Reflectivity uncoupling *)

    (* State 7: omega_chuck *)
    arrEw_Matrix[7, 1] := 0.000000; (* Gap uncoupling *)
    arrEw_Matrix[7, 2] := 0.000000; (* Height uncoupling *)
    arrEw_Matrix[7, 3] := 0.000000; (* Reflectivity uncoupling *)

    (* State 8: C_N2 *)
    arrEw_Matrix[8, 1] := -0.08500; (* Crown gap creates aerodynamic aspiration turbulent leak [% / mm] *)
    arrEw_Matrix[8, 2] := -0.04200; (* Height step turbulence dilution [% / mm] *)
    arrEw_Matrix[8, 3] := 0.000000; (* Reflectivity uncoupling *)

    (* 4. Initialize Measurement Output Matrix arrC_Matrix (6x8) *)
    (* Outputs: y1: T_pyro, y2: P_mon, y3: Q_gas, y4: theta_pos, y5: omega_spd, y6: P_hyd *)
    (* Row 1: Coaxial Melt Pool Pyrometer Temperature y1 [deg C] *)
    arrC_Matrix[1, 1] := 1.000000;  (* Direct pyrometer observation of molten pool surface temperature *)
    arrC_Matrix[1, 2] := 0.085000;  (* Optical field of view captures portion of HAZ emission *)
    arrC_Matrix[1, 3] := 0.000000;  (* Pin bulk uncoupling *)
    arrC_Matrix[1, 4] := 45.20000;  (* Keyhole capillary high-temperature blackbody emission coupling *)
    arrC_Matrix[1, 5] := 0.000000;  (* Volume uncoupling *)
    arrC_Matrix[1, 6] := 0.000000;  (* Chuck uncoupling *)
    arrC_Matrix[1, 7] := 0.000000;  (* Chuck uncoupling *)
    arrC_Matrix[1, 8] := 0.000000;  (* Gas uncoupling *)

    (* Row 2: Laser Power Sensor Monitored Output y2 [kW] *)
    arrC_Matrix[2, 1] := 0.000000;  (* Pool temp uncoupling *)
    arrC_Matrix[2, 2] := 0.000000;  (* HAZ uncoupling *)
    arrC_Matrix[2, 3] := 0.000000;  (* Pin uncoupling *)
    arrC_Matrix[2, 4] := 0.000000;  (* Keyhole uncoupling *)
    arrC_Matrix[2, 5] := 0.000000;  (* Nugget uncoupling *)
    arrC_Matrix[2, 6] := 0.000000;  (* Chuck uncoupling *)
    arrC_Matrix[2, 7] := 0.000000;  (* Chuck uncoupling *)
    arrC_Matrix[2, 8] := 0.000000;  (* Gas uncoupling *)

    (* Row 3: Nitrogen Shielding Gas Flow Transducer y3 [L/min] *)
    arrC_Matrix[3, 1] := 0.000000;  (* Pool uncoupling *)
    arrC_Matrix[3, 2] := 0.000000;  (* HAZ uncoupling *)
    arrC_Matrix[3, 3] := 0.000000;  (* Pin uncoupling *)
    arrC_Matrix[3, 4] := 0.000000;  (* Keyhole uncoupling *)
    arrC_Matrix[3, 5] := 0.000000;  (* Nugget uncoupling *)
    arrC_Matrix[3, 6] := 0.000000;  (* Chuck uncoupling *)
    arrC_Matrix[3, 7] := 0.000000;  (* Chuck uncoupling *)
    arrC_Matrix[3, 8] := 0.428500;  (* Boundary concentration to delivery flow conversion ratio *)

    (* Row 4: Chuck Angular Position Sensor y4 [deg] *)
    arrC_Matrix[4, 1] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[4, 2] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[4, 3] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[4, 4] := 0.000000;  (* Keyhole uncoupling *)
    arrC_Matrix[4, 5] := 0.000000;  (* Nugget uncoupling *)
    arrC_Matrix[4, 6] := 0.057296;  (* Convert mrad to degrees (180 / (pi * 1000)) *)
    arrC_Matrix[4, 7] := 0.000000;  (* Speed uncoupling *)
    arrC_Matrix[4, 8] := 0.000000;  (* Gas uncoupling *)

    (* Row 5: Chuck Rotational Velocity Sensor y5 [deg/s] *)
    arrC_Matrix[5, 1] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[5, 2] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[5, 3] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[5, 4] := 0.000000;  (* Keyhole uncoupling *)
    arrC_Matrix[5, 5] := 0.000000;  (* Nugget uncoupling *)
    arrC_Matrix[5, 6] := 0.000000;  (* Position uncoupling *)
    arrC_Matrix[5, 7] := 57.29578;  (* Convert rad/s to deg/s (180 / pi) *)
    arrC_Matrix[5, 8] := 0.000000;  (* Gas uncoupling *)

    (* Row 6: Hydraulic Collet Clamping Pressure y6 [bar] *)
    arrC_Matrix[6, 1] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[6, 2] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[6, 3] := 0.000000;  (* Thermal uncoupling *)
    arrC_Matrix[6, 4] := 0.000000;  (* Keyhole uncoupling *)
    arrC_Matrix[6, 5] := 0.000000;  (* Nugget uncoupling *)
    arrC_Matrix[6, 6] := 0.000000;  (* Angular uncoupling *)
    arrC_Matrix[6, 7] := 0.000000;  (* Speed uncoupling *)
    arrC_Matrix[6, 8] := 0.000000;  (* Gas uncoupling *)

    (* 5. Initialize Direct Feedthrough Actuator Matrix arrD_Matrix (6x4) *)
    (* Row 1: y1 (T_pyro) *)
    arrD_Matrix[1, 1] := 0.000000;
    arrD_Matrix[1, 2] := 0.000000;
    arrD_Matrix[1, 3] := 0.000000;
    arrD_Matrix[1, 4] := 0.000000;

    (* Row 2: y2 (P_mon) *)
    arrD_Matrix[2, 1] := 0.998500;  (* High-speed direct optical monitor scaling *)
    arrD_Matrix[2, 2] := 0.000000;
    arrD_Matrix[2, 3] := 0.000000;
    arrD_Matrix[2, 4] := 0.000000;

    (* Row 3: y3 (Q_gas) *)
    arrD_Matrix[3, 1] := 0.000000;
    arrD_Matrix[3, 2] := 0.000000;
    arrD_Matrix[3, 3] := 0.000000;
    arrD_Matrix[3, 4] := 0.995000;  (* Direct proportional flow valve response *)

    (* Row 4: y4 (theta_pos) *)
    arrD_Matrix[4, 1] := 0.000000;
    arrD_Matrix[4, 2] := 0.000000;
    arrD_Matrix[4, 3] := 0.000000;
    arrD_Matrix[4, 4] := 0.000000;

    (* Row 5: y5 (omega_spd) *)
    arrD_Matrix[5, 1] := 0.000000;
    arrD_Matrix[5, 2] := 0.000000;
    arrD_Matrix[5, 3] := 0.000000;
    arrD_Matrix[5, 4] := 0.000000;

    (* Row 6: y6 (P_hyd) *)
    arrD_Matrix[6, 1] := 0.000000;
    arrD_Matrix[6, 2] := 0.000000;
    arrD_Matrix[6, 3] := 0.000000;
    arrD_Matrix[6, 4] := 0.000000;

    (* 6. Initialize Discrete Luenberger Observer / Kalman Gain Matrix arrKe_Matrix (8x6) *)
    (* State 1: T_pool correction from measurement innovations *)
    arrKe_Matrix[1, 1] := 0.385000; (* Heavy correction from coaxial pyrometer *)
    arrKe_Matrix[1, 2] := 0.042000; (* Secondary laser power sensor correction *)
    arrKe_Matrix[1, 3] := 0.000000;
    arrKe_Matrix[1, 4] := 0.000000;
    arrKe_Matrix[1, 5] := 0.000000;
    arrKe_Matrix[1, 6] := 0.000000;

    (* State 2: T_haz correction *)
    arrKe_Matrix[2, 1] := 0.092000; (* Pyrometer innovation propagates into HAZ estimate *)
    arrKe_Matrix[2, 2] := 0.015000;
    arrKe_Matrix[2, 3] := 0.000000;
    arrKe_Matrix[2, 4] := 0.000000;
    arrKe_Matrix[2, 5] := 0.000000;
    arrKe_Matrix[2, 6] := 0.000000;

    (* State 3: T_pin correction *)
    arrKe_Matrix[3, 1] := 0.024000; (* Long-term thermal drift correction *)
    arrKe_Matrix[3, 2] := 0.005000;
    arrKe_Matrix[3, 3] := 0.000000;
    arrKe_Matrix[3, 4] := 0.000000;
    arrKe_Matrix[3, 5] := 0.000000;
    arrKe_Matrix[3, 6] := 0.000000;

    (* State 4: h_keyhole correction *)
    arrKe_Matrix[4, 1] := 0.001250; (* Pyrometer emission flash correlates to keyhole depth *)
    arrKe_Matrix[4, 2] := 0.000850;
    arrKe_Matrix[4, 3] := 0.000000;
    arrKe_Matrix[4, 4] := 0.000000;
    arrKe_Matrix[4, 5] := 0.000000;
    arrKe_Matrix[4, 6] := 0.000000;

    (* State 5: V_nugget correction *)
    arrKe_Matrix[5, 1] := 0.003500; (* Pyrometer integrated thermal mass indicates nugget size *)
    arrKe_Matrix[5, 2] := 0.001200;
    arrKe_Matrix[5, 3] := 0.000000;
    arrKe_Matrix[5, 4] := 0.000000;
    arrKe_Matrix[5, 5] := 0.000000;
    arrKe_Matrix[5, 6] := 0.000000;

    (* State 6: Delta_theta correction *)
    arrKe_Matrix[6, 1] := 0.000000;
    arrKe_Matrix[6, 2] := 0.000000;
    arrKe_Matrix[6, 3] := 0.000000;
    arrKe_Matrix[6, 4] := 14.25000; (* Chuck encoder position innovation correction (deg to mrad) *)
    arrKe_Matrix[6, 5] := 0.125000;
    arrKe_Matrix[6, 6] := 0.000000;

    (* State 7: omega_chuck correction *)
    arrKe_Matrix[7, 1] := 0.000000;
    arrKe_Matrix[7, 2] := 0.000000;
    arrKe_Matrix[7, 3] := 0.000000;
    arrKe_Matrix[7, 4] := 0.850000;
    arrKe_Matrix[7, 5] := 0.015200; (* Direct velocity observer correction *)
    arrKe_Matrix[7, 6] := 0.000000;

    (* State 8: C_N2 correction *)
    arrKe_Matrix[8, 1] := 0.000000;
    arrKe_Matrix[8, 2] := 0.000000;
    arrKe_Matrix[8, 3] := 0.021500; (* Flowmeter residual updates boundary concentration *)
    arrKe_Matrix[8, 4] := 0.000000;
    arrKe_Matrix[8, 5] := 0.000000;
    arrKe_Matrix[8, 6] := 0.000000;

    (* 7. Initialize MPC Quadratic Penalty Weights (State Q, Control R, Slew R_slew, Terminal P) *)
    arrQ_DiagWeights[1] := 0.0450;   (* Pool temperature deviation penalty *)
    arrQ_DiagWeights[2] := 0.0250;   (* HAZ temperature containment penalty *)
    arrQ_DiagWeights[3] := 0.0800;   (* Pin base thermal protection (protect insulation) *)
    arrQ_DiagWeights[4] := 125.000;  (* Keyhole depth strict tracking (prevent blowout / lack of fusion) *)
    arrQ_DiagWeights[5] := 15.5000;  (* Weld nugget volume consistency penalty *)
    arrQ_DiagWeights[6] := 250.000;  (* Chuck angular alignment strict lock during welding *)
    arrQ_DiagWeights[7] := 1.25000;  (* Chuck velocity settling penalty *)
    arrQ_DiagWeights[8] := 0.55000;  (* Nitrogen boundary concentration penalty *)

    arrR_DiagWeights[1] := 0.1200;   (* Laser power effort penalty *)
    arrR_DiagWeights[2] := 0.0008;   (* Wobble frequency modulation penalty *)
    arrR_DiagWeights[3] := 0.0045;   (* Chuck torque effort penalty *)
    arrR_DiagWeights[4] := 0.0150;   (* Shielding gas flow conservation penalty *)

    arrR_SlewWeights[1] := 0.8500;   (* Laser power fast slew penalty (damped power ramp) *)
    arrR_SlewWeights[2] := 0.0025;   (* Wobble frequency slew penalty *)
    arrR_SlewWeights[3] := 0.0350;   (* Chuck torque jerk penalty *)
    arrR_SlewWeights[4] := 0.0550;   (* Shielding gas flow surge penalty *)

    arrP_TerminalWeights[1] := 0.0950;
    arrP_TerminalWeights[2] := 0.0520;
    arrP_TerminalWeights[3] := 0.1650;
    arrP_TerminalWeights[4] := 260.00;
    arrP_TerminalWeights[5] := 32.500;
    arrP_TerminalWeights[6] := 520.00;
    arrP_TerminalWeights[7] := 2.6000;
    arrP_TerminalWeights[8] := 1.1500;

    (* 8. Initialize 192-Pin (96-Pair) Quality Tracking Arrays *)
    FOR iIndex_Loop1 := 1 TO 96 DO
        arrPairWeldScore_pct[iIndex_Loop1] := 100.0;
        arrPairJointResist_uOhm[iIndex_Loop1] := 1.85;
        arrPairPeakMeltTemp_degC[iIndex_Loop1] := 1850.0;
        arrPairMeasuredGap_mm[iIndex_Loop1] := 0.015;
        arrPairStatusFlags[iIndex_Loop1] := 16#0000;
    END_FOR;

    bFirstScanDone := TRUE;
END_IF;
"""
