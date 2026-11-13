# biw_laser_brazing_builder/part3_phase0_init.py
"""
Part 3: Phase 0 - First-Scan Initialization
Function Block: FB_Automotive_BIW_LaserBrazing_StructuralAdhesive
"""

def get_phase0_init():
    return """(* ============================================================================================== *)
(* PHASE 0: FIRST-SCAN INITIALIZATION OF MATRICES, MPC WEIGHTS & BOUNDS                           *)
(* ============================================================================================== *)
IF bFirstScan THEN
    bFirstScan := FALSE;
    udiCycleCounter := 0;
    tBlockUpTime := T#0s;
    
    (* ---------------------------------------------------------------------------------------------- *)
    (* DISCRETE SYSTEM DYNAMICS MATRIX A [8x8] (Ts = 2.0 ms)                                          *)
    (* Models melt pool enthalpy, wire dynamics, seam offset, fluid line pressure, volumetric flux,  *)
    (* bead geometry, sheet buckling strain, and pneumatic clamp reaction mechanics.                  *)
    (* ---------------------------------------------------------------------------------------------- *)
    (* Row 1: x1 = Melt Pool Temperature [deg C] *)
    a_A[1, 1] := 0.8850;   (* Thermal conduction dissipation along ditch seam *)
    a_A[1, 2] := -0.4200;  (* Cold CuSi3 wire latent melting enthalpy extraction sink *)
    a_A[1, 3] := -0.0150;  (* Seam tracking gap deviation beam spillover loss *)
    a_A[1, 4] := 0.0000;   (* Uncoupled from adhesive line pressure *)
    a_A[1, 5] := 0.0000;   (* Uncoupled from adhesive volumetric flux *)
    a_A[1, 6] := 0.0000;   (* Uncoupled from adhesive bead geometry *)
    a_A[1, 7] := -0.0820;  (* Sheet metal thermal buckling altering optical focus standoff *)
    a_A[1, 8] := 0.0045;   (* Clamp contact thermal sink heat extraction *)

    (* Row 2: x2 = CuSi3 Filler Wire Linear Feed Velocity [mm/s] *)
    a_A[2, 1] := 0.0025;   (* Liquid capillary surface tension pulling wire *)
    a_A[2, 2] := 0.7200;   (* Feeder drive servo velocity loop closed-loop response *)
    a_A[2, 3] := -0.0080;  (* Seam wall friction opposing wire feed motion *)
    a_A[2, 4] := 0.0000;   (* Uncoupled *)
    a_A[2, 5] := 0.0000;   (* Uncoupled *)
    a_A[2, 6] := 0.0000;   (* Uncoupled *)
    a_A[2, 7] := -0.0040;  (* Sheet buckling altering wire incident angle *)
    a_A[2, 8] := 0.0000;   (* Uncoupled *)

    (* Row 3: x3 = Joint Seam Lateral Tracking Deviation [um] *)
    a_A[3, 1] := 0.0035;   (* Asymmetric roof heat input inducing lateral thermal expansion *)
    a_A[3, 2] := 0.0120;   (* Wire lateral stiffness reaction force on joint wall *)
    a_A[3, 3] := 0.8250;   (* Optical seam tracker predictive lead-lag servo tracking *)
    a_A[3, 4] := 0.0000;   (* Uncoupled *)
    a_A[3, 5] := 0.0000;   (* Uncoupled *)
    a_A[3, 6] := 0.0000;   (* Uncoupled *)
    a_A[3, 7] := 0.0380;   (* Roof sheet thermal distortion directly warping seam centerline *)
    a_A[3, 8] := -0.0055;  (* Tooling geo-clamp structural constraint resisting seam shift *)

    (* Row 4: x4 = Structural Adhesive Dynamic Line Pressure [bar] *)
    a_A[4, 1] := 0.0000;   (* Uncoupled *)
    a_A[4, 2] := 0.0000;   (* Uncoupled *)
    a_A[4, 3] := 0.0000;   (* Uncoupled *)
    a_A[4, 4] := 0.8450;   (* High-pressure hose fluid bulk modulus & hydraulic resistance decay *)
    a_A[4, 5] := -12.450;  (* Extrusion nozzle volumetric discharge relieving manifold pressure *)
    a_A[4, 6] := 0.0000;   (* Uncoupled *)
    a_A[4, 7] := 0.0000;   (* Uncoupled *)
    a_A[4, 8] := 0.0000;   (* Uncoupled *)

    (* Row 5: x5 = Adhesive Dispense Volumetric Flux [mL/s] *)
    a_A[5, 1] := 0.0000;   (* Uncoupled *)
    a_A[5, 2] := 0.0000;   (* Uncoupled *)
    a_A[5, 3] := 0.0000;   (* Uncoupled *)
    a_A[5, 4] := 0.0145;   (* Manifold line pressure driving fluid discharge through nozzle orifice *)
    a_A[5, 5] := 0.7600;   (* Fluid inertial acceleration decay in delivery conduit *)
    a_A[5, 6] := 0.0000;   (* Uncoupled *)
    a_A[5, 7] := 0.0000;   (* Uncoupled *)
    a_A[5, 8] := 0.0000;   (* Uncoupled *)

    (* Row 6: x6 = Dispensed Adhesive Bead Cross-Section Area [mm2] *)
    a_A[6, 1] := 0.0000;   (* Uncoupled *)
    a_A[6, 2] := 0.0000;   (* Uncoupled *)
    a_A[6, 3] := -0.0045;  (* Lateral seam tracking error shifting bead off centerline *)
    a_A[6, 4] := 0.0018;   (* Dynamic pressure transient effect on extrudate swell *)
    a_A[6, 5] := 6.4500;   (* Volumetric flux accumulation depositing physical bead mass *)
    a_A[6, 6] := 0.9100;   (* Deposited bead physical persistence along path *)
    a_A[6, 7] := -0.0180;  (* Sheet thermal buckling stretching and thinning bead geometry *)
    a_A[6, 8] := 0.0015;   (* Clamp compression maintaining bead target containment flange *)

    (* Row 7: x7 = Roof Panel Thermal Buckling Displacement [um] *)
    a_A[7, 1] := 0.0450;   (* Laser melt pool temperature generating longitudinal thermal stress *)
    a_A[7, 2] := -0.0065;  (* Wire deposition cooling quenching local peak temperature *)
    a_A[7, 3] := 0.0020;   (* Seam deviation asymmetry *)
    a_A[7, 4] := 0.0000;   (* Uncoupled *)
    a_A[7, 5] := 0.0000;   (* Uncoupled *)
    a_A[7, 6] := 0.0000;   (* Uncoupled *)
    a_A[7, 7] := 0.9450;   (* Elastic plate post-buckling deflection memory / damping *)
    a_A[7, 8] := -0.0220;  (* Framing geo-clamp restraint force actively suppressing deflection *)

    (* Row 8: x8 = Pneumatic Framing Clamping Differential Force [N] *)
    a_A[8, 1] := 0.1250;   (* Thermal expansion of roof skin generating compressive reaction *)
    a_A[8, 2] := 0.0000;   (* Uncoupled *)
    a_A[8, 3] := -0.0450;  (* Seam lateral movement shifting moment arm on clamp jaws *)
    a_A[8, 4] := 0.0000;   (* Uncoupled *)
    a_A[8, 5] := 0.0000;   (* Uncoupled *)
    a_A[8, 6] := 0.0000;   (* Uncoupled *)
    a_A[8, 7] := 3.6500;   (* Sheet buckling displacement directly compressing load cell elastomer *)
    a_A[8, 8] := 0.8100;   (* Pneumatic cylinder compliance and regulator servo settling *)

    (* ---------------------------------------------------------------------------------------------- *)
    (* CONTROL INPUT DISTRIBUTION MATRIX B [8x6]                                                      *)
    (* Controls: u1=Laser [W], u2=Wire [mm/s], u3=Seam [um], u4=Pump [rpm], u5=Heat [%], u6=Robot [%] *)
    (* ---------------------------------------------------------------------------------------------- *)
    (* Row 1: x1 = Melt Pool Temperature [deg C] *)
    a_B[1, 1] := 0.1850;   (* Laser optical absorption heating gain [deg C / W] *)
    a_B[1, 2] := -0.3800;  (* Cold filler wire feed cooling effect [deg C / (mm/s)] *)
    a_B[1, 3] := 0.0050;   (* Seam tracking alignment optimizing spot coupling *)
    a_B[1, 4] := 0.0000;   (* Adhesive pump uncoupled *)
    a_B[1, 5] := 0.0000;   (* Adhesive heater uncoupled *)
    a_B[1, 6] := -0.8500;  (* Robot speed increase reduces line energy density [deg C / %] *)

    (* Row 2: x2 = Wire Feed Speed [mm/s] *)
    a_B[2, 1] := 0.0010;   (* Laser beam melt pressure assisting wire draw *)
    a_B[2, 2] := 0.2800;   (* Wire feed servo command gain [(mm/s) / (mm/s)] *)
    a_B[2, 3] := 0.0000;   (* Uncoupled *)
    a_B[2, 4] := 0.0000;   (* Uncoupled *)
    a_B[2, 5] := 0.0000;   (* Uncoupled *)
    a_B[2, 6] := 0.0000;   (* Uncoupled *)

    (* Row 3: x3 = Seam Lateral Deviation [um] *)
    a_B[3, 1] := -0.0005;  (* Asymmetric laser plume pressure *)
    a_B[3, 2] := 0.0020;   (* Wire stiffness side-thrust *)
    a_B[3, 3] := 0.1750;   (* Seam tracking cross-slide servo drive gain [um / um] *)
    a_B[3, 4] := 0.0000;   (* Uncoupled *)
    a_B[3, 5] := 0.0000;   (* Uncoupled *)
    a_B[3, 6] := 0.0150;   (* Robot speed contour centrifugal deviation *)

    (* Row 4: x4 = Adhesive Dynamic Line Pressure [bar] *)
    a_B[4, 1] := 0.0000;   (* Uncoupled *)
    a_B[4, 2] := 0.0000;   (* Uncoupled *)
    a_B[4, 3] := 0.0000;   (* Uncoupled *)
    a_B[4, 4] := 0.0850;   (* Dispense gear pump speed gain [bar / rpm] *)
    a_B[4, 5] := -0.2200;  (* Heating jacket reducing fluid viscosity and pressure [bar / %] *)
    a_B[4, 6] := 0.0000;   (* Uncoupled *)

    (* Row 5: x5 = Adhesive Volumetric Flux [mL/s] *)
    a_B[5, 1] := 0.0000;   (* Uncoupled *)
    a_B[5, 2] := 0.0000;   (* Uncoupled *)
    a_B[5, 3] := 0.0000;   (* Uncoupled *)
    a_B[5, 4] := 0.00155;  (* Direct pump volumetric displacement displacement [mL/s per rpm] *)
    a_B[5, 5] := 0.00420;  (* Viscosity reduction increasing flow through nozzle [(mL/s) / %] *)
    a_B[5, 6] := 0.0000;   (* Uncoupled *)

    (* Row 6: x6 = Adhesive Bead Area [mm2] *)
    a_B[6, 1] := 0.0000;   (* Uncoupled *)
    a_B[6, 2] := 0.0000;   (* Uncoupled *)
    a_B[6, 3] := 0.0000;   (* Uncoupled *)
    a_B[6, 4] := 0.00850;  (* Pump RPM increasing laid bead volume [mm2 / rpm] *)
    a_B[6, 5] := 0.01200;  (* Thermal expansion & wetting of structural epoxy *)
    a_B[6, 6] := -0.1250;  (* Higher robot speed stretches bead, reducing area [mm2 / %] *)

    (* Row 7: x7 = Roof Panel Thermal Buckling [um] *)
    a_B[7, 1] := 0.00850;  (* Laser optical power heat input driving sheet distortion [um / W] *)
    a_B[7, 2] := -0.0015;  (* Wire feed absorption quenching peak thermal distortion *)
    a_B[7, 3] := 0.0000;   (* Uncoupled *)
    a_B[7, 4] := 0.0000;   (* Uncoupled *)
    a_B[7, 5] := 0.0000;   (* Uncoupled *)
    a_B[7, 6] := -0.0450;  (* Higher travel velocity distributes heat, lowering peak strain *)

    (* Row 8: x8 = Framing Clamp Differential Force [N] *)
    a_B[8, 1] := 0.02500;  (* Laser heating causing thermal expansion against clamps [N / W] *)
    a_B[8, 2] := 0.0000;   (* Uncoupled *)
    a_B[8, 3] := 0.0000;   (* Uncoupled *)
    a_B[8, 4] := 0.0000;   (* Uncoupled *)
    a_B[8, 5] := 0.0000;   (* Uncoupled *)
    a_B[8, 6] := -0.0800;  (* Rapid robot travel reducing localized thermal clamp reaction *)

    (* ---------------------------------------------------------------------------------------------- *)
    (* STATE-TO-MEASUREMENT OUTPUT MATRIX C [6x8]                                                     *)
    (* Measurements: y1=Pyro, y2=WireV, y3=Seam, y4=AdhP, y5=AdhF, y6=ClampF                          *)
    (* ---------------------------------------------------------------------------------------------- *)
    (* Row 1: y1 = Pyrometer [deg C] *)
    a_C[1, 1] := 1.0000; a_C[1, 2] := 0.0000; a_C[1, 3] := -0.0080; a_C[1, 4] := 0.0000;
    a_C[1, 5] := 0.0000; a_C[1, 6] := 0.0000; a_C[1, 7] := -0.0150; a_C[1, 8] := 0.0000;

    (* Row 2: y2 = Wire Velocity Encoder [mm/s] *)
    a_C[2, 1] := 0.0000; a_C[2, 2] := 1.0000; a_C[2, 3] := 0.0000;  a_C[2, 4] := 0.0000;
    a_C[2, 5] := 0.0000; a_C[2, 6] := 0.0000; a_C[2, 7] := 0.0000;  a_C[2, 8] := 0.0000;

    (* Row 3: y3 = 3D Seam Profilometer [um] *)
    a_C[3, 1] := 0.0000; a_C[3, 2] := 0.0000; a_C[3, 3] := 1.0000;  a_C[3, 4] := 0.0000;
    a_C[3, 5] := 0.0000; a_C[3, 6] := 0.0000; a_C[3, 7] := 0.0240;  a_C[3, 8] := 0.0000;

    (* Row 4: y4 = Adhesive Manifold Pressure [bar] *)
    a_C[4, 1] := 0.0000; a_C[4, 2] := 0.0000; a_C[4, 3] := 0.0000;  a_C[4, 4] := 1.0000;
    a_C[4, 5] := 0.0000; a_C[4, 6] := 0.0000; a_C[4, 7] := 0.0000;  a_C[4, 8] := 0.0000;

    (* Row 5: y5 = Coriolis Flow Equivalent Volumetric Flux [mL/s] *)
    a_C[5, 1] := 0.0000; a_C[5, 2] := 0.0000; a_C[5, 3] := 0.0000;  a_C[5, 4] := 0.0000;
    a_C[5, 5] := 0.78125;(* Convert mass flow g/s to volumetric mL/s: 1 / 1.28 g/mL *)
    a_C[5, 6] := 0.0000; a_C[5, 7] := 0.0000; a_C[5, 8] := 0.0000;

    (* Row 6: y6 = Framing Clamp Load Cell [N] *)
    a_C[6, 1] := 0.0000; a_C[6, 2] := 0.0000; a_C[6, 3] := 0.0000;  a_C[6, 4] := 0.0000;
    a_C[6, 5] := 0.0000; a_C[6, 6] := 0.0000; a_C[6, 7] := 2.4500;  a_C[6, 8] := 1.0000;

    (* ---------------------------------------------------------------------------------------------- *)
    (* DIRECT TRANSMISSION FEEDTHROUGH MATRIX D [6x6]                                                 *)
    (* High-frequency sensory coupling and instantaneous instrument compliance                        *)
    (* ---------------------------------------------------------------------------------------------- *)
    a_D[1, 1] := 0.0005; a_D[1, 2] := 0.0000; a_D[1, 3] := 0.0000; a_D[1, 4] := 0.0000; a_D[1, 5] := 0.0000; a_D[1, 6] := -0.0010;
    a_D[2, 1] := 0.0000; a_D[2, 2] := 0.0020; a_D[2, 3] := 0.0000; a_D[2, 4] := 0.0000; a_D[2, 5] := 0.0000; a_D[2, 6] := 0.0000;
    a_D[3, 1] := 0.0000; a_D[3, 2] := 0.0000; a_D[3, 3] := 0.0010; a_D[3, 4] := 0.0000; a_D[3, 5] := 0.0000; a_D[3, 6] := 0.0005;
    a_D[4, 1] := 0.0000; a_D[4, 2] := 0.0000; a_D[4, 3] := 0.0000; a_D[4, 4] := 0.0015; a_D[4, 5] := -0.0020;a_D[4, 6] := 0.0000;
    a_D[5, 1] := 0.0000; a_D[5, 2] := 0.0000; a_D[5, 3] := 0.0000; a_D[5, 4] := 0.0002; a_D[5, 5] := 0.0005; a_D[5, 6] := 0.0000;
    a_D[6, 1] := 0.0010; a_D[6, 2] := 0.0000; a_D[6, 3] := 0.0000; a_D[6, 4] := 0.0000; a_D[6, 5] := 0.0000; a_D[6, 6] := -0.0050;

    (* ---------------------------------------------------------------------------------------------- *)
    (* STEADY-STATE LUENBERGER OBSERVER GAIN MATRIX L [8x6]                                           *)
    (* Derived via Discrete Algebraic Riccati Equation (DARE) for optimal noise rejection             *)
    (* ---------------------------------------------------------------------------------------------- *)
    (* Row 1: x1 = Melt Pool Temperature *)
    a_L[1, 1] := 0.2450; a_L[1, 2] := -0.0120; a_L[1, 3] := 0.0050; a_L[1, 4] := 0.0000; a_L[1, 5] := 0.0000; a_L[1, 6] := 0.0020;
    (* Row 2: x2 = CuSi3 Wire Feed Speed *)
    a_L[2, 1] := 0.0010; a_L[2, 2] := 0.2850; a_L[2, 3] := -0.0040; a_L[2, 4] := 0.0000; a_L[2, 5] := 0.0000; a_L[2, 6] := 0.0000;
    (* Row 3: x3 = Seam Lateral Deviation *)
    a_L[3, 1] := 0.0020; a_L[3, 2] := 0.0010; a_L[3, 3] := 0.3150; a_L[3, 4] := 0.0000; a_L[3, 5] := 0.0000; a_L[3, 6] := -0.0030;
    (* Row 4: x4 = Adhesive Dynamic Line Pressure *)
    a_L[4, 1] := 0.0000; a_L[4, 2] := 0.0000; a_L[4, 3] := 0.0000; a_L[4, 4] := 0.2650; a_L[4, 5] := -0.4500; a_L[4, 6] := 0.0000;
    (* Row 5: x5 = Adhesive Volumetric Flux *)
    a_L[5, 1] := 0.0000; a_L[5, 2] := 0.0000; a_L[5, 3] := 0.0000; a_L[5, 4] := 0.0085; a_L[5, 5] := 0.3200; a_L[5, 6] := 0.0000;
    (* Row 6: x6 = Dispensed Adhesive Bead Area *)
    a_L[6, 1] := 0.0000; a_L[6, 2] := 0.0000; a_L[6, 3] := -0.0010; a_L[6, 4] := 0.0025; a_L[6, 5] := 0.4500; a_L[6, 6] := 0.0010;
    (* Row 7: x7 = Roof Panel Thermal Buckling *)
    a_L[7, 1] := 0.0120; a_L[7, 2] := -0.0020; a_L[7, 3] := 0.0080; a_L[7, 4] := 0.0000; a_L[7, 5] := 0.0000; a_L[7, 6] := -0.0150;
    (* Row 8: x8 = Framing Clamp Differential Force *)
    a_L[8, 1] := 0.0350; a_L[8, 2] := 0.0000; a_L[8, 3] := -0.0120; a_L[8, 4] := 0.0000; a_L[8, 5] := 0.0000; a_L[8, 6] := 0.2950;

    (* ---------------------------------------------------------------------------------------------- *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST WEIGHTS & CONSTRAINT VECTORS                               *)
    (* ---------------------------------------------------------------------------------------------- *)
    (* State Tracking Error Penalties Q [1..8] *)
    a_Q[1] := 0.0450;   (* x1: Pool Temp tracking penalty *)
    a_Q[2] := 0.0800;   (* x2: Wire Feed speed tracking penalty *)
    a_Q[3] := 0.2500;   (* x3: Seam lateral deviation penalty (Strict class-A finish requirement) *)
    a_Q[4] := 0.0150;   (* x4: Adhesive line pressure penalty *)
    a_Q[5] := 0.1200;   (* x5: Adhesive volumetric flux penalty *)
    a_Q[6] := 0.4500;   (* x6: Adhesive bead area penalty (Crash-worthiness adhesive integrity) *)
    a_Q[7] := 0.0650;   (* x7: Roof panel buckling penalty (Class-A panel cosmetic surface) *)
    a_Q[8] := 0.0200;   (* x8: Framing clamp force deviation penalty *)

    (* Actuator Control Effort Penalties R [1..6] *)
    a_R[1] := 0.000025; (* u1: Laser power expenditure penalty *)
    a_R[2] := 0.000150; (* u2: Wire feeder motor effort *)
    a_R[3] := 0.000080; (* u3: Seam tracking cross-slide servo effort *)
    a_R[4] := 0.000045; (* u4: Adhesive gear pump speed effort *)
    a_R[5] := 0.000010; (* u5: Heating jacket duty penalty *)
    a_R[6] := 0.000120; (* u6: Robot speed override variation penalty *)

    (* Actuator Slew Rate Penalties S [1..6] *)
    a_S[1] := 0.000500; (* du1: Laser power rate of change penalty *)
    a_S[2] := 0.002500; (* du2: Wire feeder acceleration rate penalty *)
    a_S[3] := 0.001800; (* du3: Cross-slide jerk penalty *)
    a_S[4] := 0.000850; (* du4: Adhesive pump acceleration penalty *)
    a_S[5] := 0.000150; (* du5: Thermal heating slew penalty *)
    a_S[6] := 0.004000; (* du6: Robot path acceleration penalty *)

    (* Terminal State Penalties P [1..8] *)
    a_P[1] := 0.0900;
    a_P[2] := 0.1600;
    a_P[3] := 0.5000;
    a_P[4] := 0.0300;
    a_P[5] := 0.2400;
    a_P[6] := 0.9000;
    a_P[7] := 0.1300;
    a_P[8] := 0.0400;

    (* Actuator Saturation Limits [u_min .. u_max] *)
    a_u_min[1] := 0.0;      a_u_max[1] := 5000.0;   (* u1: Laser Optical Power [0..5000 W] *)
    a_u_min[2] := 0.0;      a_u_max[2] := 150.0;    (* u2: Wire Feed Velocity [0..150 mm/s] *)
    a_u_min[3] := -25000.0; a_u_max[3] := 25000.0;  (* u3: Seam Tracker Servo Correction [-25000..+25000 um] *)
    a_u_min[4] := 0.0;      a_u_max[4] := 2500.0;   (* u4: Adhesive Gear Pump [0..2500 rpm] *)
    a_u_min[5] := 0.0;      a_u_max[5] := 100.0;    (* u5: Heating Jacket Duty [0..100 %] *)
    a_u_min[6] := 10.0;     a_u_max[6] := 100.0;    (* u6: Robot Speed Override [10..100 %] *)

    (* Actuator Maximum Dynamic Slew Rates Per 2.0 ms Scan Cycle *)
    a_du_max[1] := 150.0;   (* Slew u1: Max 75 kW/s laser power rise/fall *)
    a_du_max[2] := 4.50;    (* Slew u2: Max 2250 mm/s^2 wire acceleration *)
    a_du_max[3] := 250.0;   (* Slew u3: Max 125 mm/s cross-slide lateral speed *)
    a_du_max[4] := 45.0;    (* Slew u4: Max 22,500 rpm/s gear pump acceleration *)
    a_du_max[5] := 1.50;    (* Slew u5: Max 750 %/s heating duty rate *)
    a_du_max[6] := 1.20;    (* Slew u6: Max 600 %/s robot speed override rate *)

    (* Initialize State Reference Target Vector x_ref *)
    a_x_ref[1] := 1050.0;   (* Target Melt Pool Temperature [deg C] *)
    a_x_ref[2] := 85.0;     (* Target Wire Feed Velocity [mm/s] *)
    a_x_ref[3] := 0.0;      (* Target Seam Lateral Offset [um] *)
    a_x_ref[4] := 145.0;    (* Target Adhesive Manifold Line Pressure [bar] *)
    a_x_ref[5] := 1.14;     (* Target Adhesive Volumetric Flux [mL/s] *)
    a_x_ref[6] := 12.0;     (* Target Structural Adhesive Bead Area [mm2] *)
    a_x_ref[7] := 15.0;     (* Permissible Roof Panel Thermal Deflection [um] *)
    a_x_ref[8] := 2400.0;   (* Target Framing Tooling Clamp Force [N] *)

    (* Initialize Nominal Actuator Vector u_ref *)
    a_u_ref[1] := 3200.0;   (* Nominal Laser Power [W] *)
    a_u_ref[2] := 85.0;     (* Nominal Wire Speed [mm/s] *)
    a_u_ref[3] := 0.0;      (* Nominal Seam Correction [um] *)
    a_u_ref[4] := 690.0;    (* Nominal Gear Pump Speed [rpm] *)
    a_u_ref[5] := 45.0;     (* Nominal Heating Duty [%] *)
    a_u_ref[6] := 100.0;    (* Nominal Robot Contouring Speed Override [%] *)

    (* Seed State Vectors and Control Histories *)
    FOR i := 1 TO 8 DO
        a_x[i] := a_x_ref[i];
        a_x_pred[i] := a_x_ref[i];
        a_x_err[i] := 0.0;
    END_FOR;
    
    FOR j := 1 TO 6 DO
        a_u[j] := a_u_ref[j];
        a_u_prev[j] := a_u_ref[j];
        a_du[j] := 0.0;
        a_y_meas[j] := 0.0;
        a_y_est[j] := 0.0;
        a_innov[j] := 0.0;
    END_FOR;

    (* Seed Receding Horizon Prediction Buffers *)
    FOR k := 1 TO 5 DO
        FOR j := 1 TO 6 DO
            a_u_traj[k, j] := a_u_ref[j];
            a_grad[k, j] := 0.0;
        END_FOR;
        FOR i := 1 TO 8 DO
            a_x_traj[k, i] := a_x_ref[i];
        END_FOR;
    END_FOR;
END_IF;

(* Advance Real-Time Scan Cycle Clock *)
udiCycleCounter := udiCycleCounter + 1;
tBlockUpTime := tBlockUpTime + tScanCycleTime;
"""
