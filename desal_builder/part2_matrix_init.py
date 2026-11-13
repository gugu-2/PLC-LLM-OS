# desal_builder/part2_matrix_init.py
# First-Scan Initialization of Discrete State-Space and MPC Quadratic Weighting Matrices

def get_part2_matrix_init():
    code = """
(* ====================================================================================================
   PHASE 0: ONE-SHOT FIRST-SCAN SYSTEM INITIALIZATION & CYBER-PHYSICAL MATRIX ALLOCATION
   Ts = 10 ms (0.010 s) Discrete Sample Period
   State Vector x in R^8:
     x[1]: HP Feed Pressure P_feed [bar]
     x[2]: Membrane Net Driving Pressure NDP [bar]
     x[3]: Membrane Permeate Flux J_v [LMH]
     x[4]: Average Membrane Osmotic Pressure Pi_bar [bar]
     x[5]: ERD Isobaric HP Brine Pressure P_erd [bar]
     x[6]: ERD Volumetric Overflush / Salinity Mixing Delta_C_mix [ppm]
     x[7]: Permeate Salinity / Conductivity C_perm [uS/cm]
     x[8]: Membrane Normalized Specific Permeability Kw [LMH/bar]
   Control Vector u in R^6:
     u[1]: HPP VFD Output Frequency f_hpp [Hz]
     u[2]: PX Booster VFD Frequency f_bp [Hz]
     u[3]: Brine Reject Throttle Valve Pos V_brine [%]
     u[4]: Antiscalant Chemical Pump Stroke f_as [%]
     u[5]: Sodium Bisulfite Chemical Pump Stroke f_sbs [%]
     u[6]: Permeate Flush / Bypass Valve Pos V_flush [%]
   ==================================================================================================== *)

IF NOT bInitialized THEN
    (* ------------------------------------------------------------------------------------------------
       MATRIX A: DISCRETE STATE TRANSITION MATRIX (8x8) at Ts = 10 ms
       Derived from linearized Navier-Stokes, Darcy-Poiseuille resistance-in-series,
       van 't Hoff osmotic thermodynamics, and isobaric ceramic rotor momentum balance.
       ------------------------------------------------------------------------------------------------ *)
    (* Row 1: Dynamics of HP Membrane Feed Pressure P_feed [bar] *)
    matA[1, 1] := 0.942500;   (* Pressure dissipation and fluid compressibility damping *)
    matA[1, 2] := 0.038400;   (* Back-coupling from membrane net driving pressure *)
    matA[1, 3] := -0.015200;  (* Permeate volumetric flow extraction depressurization *)
    matA[1, 4] := 0.004200;   (* Osmotic resistance induced backpressure coupling *)
    matA[1, 5] := 0.018500;   (* Isobaric PX high pressure header hydraulic coupling *)
    matA[1, 6] := 0.000000;   (* Salinity mixing uncoupled to bulk momentum *)
    matA[1, 7] := 0.000000;   (* Permeate salinity uncoupled to feed pressure *)
    matA[1, 8] := -0.021000;  (* Permeability flux expansion pressure decay *)

    (* Row 2: Dynamics of Membrane Net Driving Pressure NDP [bar] *)
    matA[2, 1] := 0.884000;   (* Direct hydraulic transmission from feed manifold *)
    matA[2, 2] := 0.912000;   (* Viscous friction and hydraulic membrane resistance decay *)
    matA[2, 3] := -0.045000;  (* Convective flux filtration head loss *)
    matA[2, 4] := -0.865000;  (* Direct thermodynamic osmotic pressure counter-force *)
    matA[2, 5] := 0.012500;   (* ERD return pressure contribution to header NDP *)
    matA[2, 6] := -0.001800;  (* Local osmotic penalty from PX salinity mixing *)
    matA[2, 7] := 0.000000;   (* Permeate salinity negligible back-effect *)
    matA[2, 8] := -0.054000;  (* Membrane specific permeability load factor *)

    (* Row 3: Dynamics of Membrane Permeate Flux J_v [LMH] *)
    matA[3, 1] := 0.018500;   (* Feed pressure direct convective acceleration *)
    matA[3, 2] := 0.635000;   (* Darcy-Starling flux driving acceleration from NDP *)
    matA[3, 3] := 0.887500;   (* Boundary layer momentum persistence and inertial decay *)
    matA[3, 4] := -0.425000;  (* Osmotic back-diffusion flux retarding force *)
    matA[3, 5] := 0.004500;   (* PX boosted feed flow cross-flux contribution *)
    matA[3, 6] := -0.008500;  (* Overflush salinity leak polarization impact *)
    matA[3, 7] := -0.002200;  (* Product backpressure concentration effect *)
    matA[3, 8] := 11.850000;  (* Normalized membrane specific permeability gain Kw *)

    (* Row 4: Dynamics of Membrane Surface Osmotic Pressure Pi_bar [bar] *)
    matA[4, 1] := 0.002400;   (* Compression density osmotic modulation *)
    matA[4, 2] := 0.014200;   (* NDP driving salt concentration to membrane boundary *)
    matA[4, 3] := 0.198500;   (* Concentration polarization beta enhancement with flux *)
    matA[4, 4] := 0.968000;   (* Solute boundary layer diffusion dissipation persistence *)
    matA[4, 5] := 0.001800;   (* ERD concentrate recycle mass transport *)
    matA[4, 6] := 0.034500;   (* Overflush salinity enrichment to boundary layer *)
    matA[4, 7] := -0.012000;  (* Salt permeation solute loss relaxation *)
    matA[4, 8] := 0.000000;   (* Permeability decoupled from thermodynamic chemical potential *)

    (* Row 5: Dynamics of ERD Isobaric HP Brine Pressure P_erd [bar] *)
    matA[5, 1] := 0.892000;   (* Membrane vessel concentrate discharge coupling *)
    matA[5, 2] := -0.024000;  (* Permeate extraction pressure drop across vessel rack *)
    matA[5, 3] := -0.038000;  (* Hydraulic friction loss inside feed spacer channels *)
    matA[5, 4] := 0.000000;   (* Osmotic pressure uncoupled to ERD mechanical pressure *)
    matA[5, 5] := 0.925000;   (* Ceramic rotor hydraulic duct inertial persistence *)
    matA[5, 6] := 0.000000;   (* Rotor fluid density negligible pressure impact *)
    matA[5, 7] := 0.000000;   (* Permeate salinity uncoupled *)
    matA[5, 8] := 0.000000;   (* Membrane permeability uncoupled *)

    (* Row 6: Dynamics of ERD Rotor Overflush / Salinity Mixing Delta_C_mix [ppm] *)
    matA[6, 1] := 0.004500;   (* HP feed header cross-mixing leakage gradient *)
    matA[6, 2] := 0.000000;   (* NDP decoupled from PX ceramic seal lubrication *)
    matA[6, 3] := -0.012000;  (* Permeate sweep dilution effect *)
    matA[6, 4] := 0.082000;   (* Brine osmotic solute gradient across rotor duct interface *)
    matA[6, 5] := 0.016500;   (* Differential pressure axial clearance leakage *)
    matA[6, 6] := 0.865000;   (* Duct Taylor-Aris dispersion washout time constant *)
    matA[6, 7] := 0.000000;   (* Permeate salinity uncoupled *)
    matA[6, 8] := 0.000000;   (* Membrane permeability uncoupled *)

    (* Row 7: Dynamics of Permeate Salinity / Conductivity C_perm [uS/cm] *)
    matA[7, 1] := 0.003500;   (* Pressure compaction micro-pore solute migration *)
    matA[7, 2] := -0.048000;  (* Dilution effect: higher NDP increases water flux faster than salt *)
    matA[7, 3] := -0.092000;  (* Direct convective dilution of permeate solute concentration *)
    matA[7, 4] := 0.078500;   (* Fickian solute diffusive driving force across active skin *)
    matA[7, 5] := 0.000000;   (* ERD pressure uncoupled to permeate collection header *)
    matA[7, 6] := 0.024500;   (* PX salinity leakage passing through feed into permeate *)
    matA[7, 7] := 0.932000;   (* Permeate collector pipe hydraulic residence time delay *)
    matA[7, 8] := -0.015000;  (* High clean permeability aids water transport ratio *)

    (* Row 8: Dynamics of Membrane Normalized Specific Permeability Kw [LMH/bar] *)
    matA[8, 1] := -0.000018;  (* Mechanical compaction decay under sustained high pressure *)
    matA[8, 2] := -0.000012;  (* Hydrodynamic compaction stress on polysulfone porous support *)
    matA[8, 3] := -0.000145;  (* Colloidal and biological particulate deposition fouling rate *)
    matA[8, 4] := -0.000065;  (* Mineral scaling crystallization pore blockage coefficient *)
    matA[8, 5] := 0.000000;   (* ERD pressure uncoupled to membrane skin aging *)
    matA[8, 6] := -0.000035;  (* Recycled scaling ions deposition acceleration *)
    matA[8, 7] := 0.000000;   (* Permeate salinity uncoupled *)
    matA[8, 8] := 0.999850;   (* Intrinsic membrane polymer integrity persistence *)

    (* ------------------------------------------------------------------------------------------------
       MATRIX B: CONTROL INPUT DISTRIBUTION MATRIX (8x6)
       Inputs: u[1]=f_hpp, u[2]=f_bp, u[3]=V_brine, u[4]=f_as, u[5]=f_sbs, u[6]=V_flush
       ------------------------------------------------------------------------------------------------ *)
    (* State 1: P_feed *)
    matB[1, 1] := 0.485000;   (* HPP pump speed frequency head gain [bar/Hz] *)
    matB[1, 2] := 0.162000;   (* PX Booster pump frequency head gain [bar/Hz] *)
    matB[1, 3] := 0.085000;   (* Brine throttle valve backpressure gain [bar/%] *)
    matB[1, 4] := 0.000000;   (* Antiscalant no hydraulic pressure effect *)
    matB[1, 5] := 0.000000;   (* SBS no hydraulic pressure effect *)
    matB[1, 6] := -0.145000;  (* Permeate flush bypass depressurization gain [bar/%] *)

    (* State 2: NDP *)
    matB[2, 1] := 0.442000;   (* HPP pump driving NDP acceleration [bar/Hz] *)
    matB[2, 2] := 0.148000;   (* PX Booster driving NDP acceleration [bar/Hz] *)
    matB[2, 3] := 0.065000;   (* Brine throttle valve NDP gain [bar/%] *)
    matB[2, 4] := 0.000500;   (* Antiscalant scaling prevention NDP preservation *)
    matB[2, 5] := 0.000000;   (* SBS no direct NDP effect *)
    matB[2, 6] := -0.165000;  (* Permeate flush bypass NDP reduction *)

    (* State 3: J_v (Flux) *)
    matB[3, 1] := 0.315000;   (* HPP VFD speed direct flux gain [LMH/Hz] *)
    matB[3, 2] := 0.098000;   (* PX Booster VFD speed flux gain [LMH/Hz] *)
    matB[3, 3] := 0.042000;   (* Brine valve throttle flux contribution [LMH/%] *)
    matB[3, 4] := 0.001200;   (* Antiscalant fouling inhibition flux gain [LMH/%] *)
    matB[3, 5] := 0.000000;   (* SBS neutral to flux *)
    matB[3, 6] := -0.085000;  (* Flush valve bypass flow loss [LMH/%] *)

    (* State 4: Pi_bar (Osmotic Pressure) *)
    matB[4, 1] := 0.085000;   (* HPP speed increases recovery, elevating concentrate osmotic head *)
    matB[4, 2] := 0.025000;   (* PX Booster pressure contribution to concentration polarization *)
    matB[4, 3] := 0.062000;   (* Brine throttling increases salt concentration *)
    matB[4, 4] := -0.008500;  (* Antiscalant disperses ionic crystallization nucleators *)
    matB[4, 5] := 0.000000;   (* SBS neutral to osmotic pressure *)
    matB[4, 6] := -0.095000;  (* Flush water displaces brine, dropping osmotic head *)

    (* State 5: P_erd *)
    matB[5, 1] := 0.412000;   (* HPP pressure propagating to membrane reject inlet of ERD *)
    matB[5, 2] := 0.045000;   (* PX Booster suction backpressure coupling *)
    matB[5, 3] := 0.125000;   (* Brine valve restriction directly pressurizing PX manifold *)
    matB[5, 4] := 0.000000;   (* Antiscalant neutral *)
    matB[5, 5] := 0.000000;   (* SBS neutral *)
    matB[5, 6] := -0.115000;  (* Depressurization valve blowdown *)

    (* State 6: Delta_C_mix (ERD Rotor Salinity Leak) *)
    matB[6, 1] := 0.085000;   (* Higher HPP flow slightly increases rotor mixing turbulence *)
    matB[6, 2] := -0.185000;  (* PX Booster corrects pressure mismatch, minimizing cross-leak *)
    matB[6, 3] := 0.145000;   (* Brine throttling imbalances rotor barrier boundary *)
    matB[6, 4] := 0.000000;   (* Antiscalant neutral *)
    matB[6, 5] := 0.000000;   (* SBS neutral *)
    matB[6, 6] := -0.250000;  (* Flush displacement clears rotor mixing salinity *)

    (* State 7: C_perm (Permeate Salinity) *)
    matB[7, 1] := -0.850000;  (* Higher HPP speed dilutes permeate salinity by increasing pure water flux *)
    matB[7, 2] := -0.240000;  (* PX Booster speed improves membrane flux dilution *)
    matB[7, 3] := 0.520000;   (* Brine restriction increases salt passage into permeate *)
    matB[7, 4] := -0.015000;  (* Antiscalant prevents crystal pore punctures *)
    matB[7, 5] := -0.008000;  (* SBS protects polyamide active layer from chlorine degradation *)
    matB[7, 6] := -1.850000;  (* Permeate flush purges salt ions from collector headers *)

    (* State 8: Kw (Membrane Specific Permeability) *)
    matB[8, 1] := -0.000025;  (* High HPP frequency increases compaction stress *)
    matB[8, 2] := -0.000008;  (* PX Booster minor compaction contribution *)
    matB[8, 3] := -0.000015;  (* Brine throttling promotes boundary layer salt cake formation *)
    matB[8, 4] := 0.000185;   (* Antiscalant active cleaning and threshold inhibition restores Kw *)
    matB[8, 5] := 0.000045;   (* SBS prevents chlorine halogenation oxidation of polyamide chains *)
    matB[8, 6] := 0.000220;   (* Pure permeate flush dissolves dynamic cake layer, recovering Kw *)

    (* ------------------------------------------------------------------------------------------------
       MATRIX Bd: EXOGENOUS DISTURBANCE COUPLING MATRIX (8x6)
       Disturbances: d[1]=C_sea, d[2]=T_sea, d[3]=P_intake, d[4]=ORP, d[5]=SDI15, d[6]=pH
       ------------------------------------------------------------------------------------------------ *)
    (* State 1: P_feed *)
    matBd[1, 1] := 0.000120;  matBd[1, 2] := -0.045000; matBd[1, 3] := 0.850000;
    matBd[1, 4] := 0.000000;  matBd[1, 5] := 0.012000;  matBd[1, 6] := 0.000000;

    (* State 2: NDP *)
    matBd[2, 1] := -0.000480; matBd[2, 2] := 0.085000;  matBd[2, 3] := 0.780000;
    matBd[2, 4] := 0.000000;  matBd[2, 5] := -0.035000; matBd[2, 6] := -0.015000;

    (* State 3: J_v *)
    matBd[3, 1] := -0.000350; matBd[3, 2] := 0.285000;  matBd[3, 3] := 0.120000;
    matBd[3, 4] := 0.000000;  matBd[3, 5] := -0.085000; matBd[3, 6] := -0.025000;

    (* State 4: Pi_bar *)
    matBd[4, 1] := 0.000985;  matBd[4, 2] := 0.125000;  matBd[4, 3] := 0.000000;
    matBd[4, 4] := 0.000000;  matBd[4, 5] := 0.008000;  matBd[4, 6] := 0.042000;

    (* State 5: P_erd *)
    matBd[5, 1] := 0.000150;  matBd[5, 2] := -0.035000; matBd[5, 3] := 0.720000;
    matBd[5, 4] := 0.000000;  matBd[5, 5] := 0.015000;  matBd[5, 6] := 0.000000;

    (* State 6: Delta_C_mix *)
    matBd[6, 1] := 0.024500;  matBd[6, 2] := 0.145000;  matBd[6, 3] := -0.085000;
    matBd[6, 4] := 0.000000;  matBd[6, 5] := 0.022000;  matBd[6, 6] := 0.000000;

    (* State 7: C_perm *)
    matBd[7, 1] := 0.008500;  matBd[7, 2] := 3.450000;  matBd[7, 3] := -0.150000;
    matBd[7, 4] := 0.045000;  matBd[7, 5] := 1.250000;  matBd[7, 6] := 1.150000;

    (* State 8: Kw *)
    matBd[8, 1] := -0.000005; matBd[8, 2] := 0.000450;  matBd[8, 3] := 0.000000;
    matBd[8, 4] := -0.000350; matBd[8, 5] := -0.000850; matBd[8, 6] := -0.000120;

    (* ------------------------------------------------------------------------------------------------
       MATRIX C: MEASUREMENT OBSERVATION MATRIX (6x8)
       Maps State Vector to Plant Transmitters: y[1]=P_feed, y[2]=Q_perm, y[3]=Q_brine,
       y[4]=Cond_perm, y[5]=Delta_P_erd, y[6]=SEC
       ------------------------------------------------------------------------------------------------ *)
    (* Row 1: y[1] = HP Feed Pressure [bar] *)
    matC[1, 1] := 1.000000; matC[1, 2] := 0.000000; matC[1, 3] := 0.000000; matC[1, 4] := 0.000000;
    matC[1, 5] := 0.000000; matC[1, 6] := 0.000000; matC[1, 7] := 0.000000; matC[1, 8] := 0.000000;

    (* Row 2: y[2] = Permeate Volumetric Flow Q_perm [m3/h] (Total Area = 125,000 m2 / 1000 = 125.0) *)
    matC[2, 1] := 0.000000; matC[2, 2] := 0.000000; matC[2, 3] := 125.0000; matC[2, 4] := 0.000000;
    matC[2, 5] := 0.000000; matC[2, 6] := 0.000000; matC[2, 7] := 0.000000; matC[2, 8] := 0.000000;

    (* Row 3: y[3] = Brine Reject Flow Q_brine [m3/h] (Mass balance: Q_feed - Q_perm) *)
    matC[3, 1] := 42.50000; matC[3, 2] := 0.000000; matC[3, 3] := -125.000; matC[3, 4] := 0.000000;
    matC[3, 5] := 12.80000; matC[3, 6] := 0.000000; matC[3, 7] := 0.000000; matC[3, 8] := 0.000000;

    (* Row 4: y[4] = Permeate Conductivity [uS/cm] *)
    matC[4, 1] := 0.000000; matC[4, 2] := 0.000000; matC[4, 3] := 0.000000; matC[4, 4] := 0.000000;
    matC[4, 5] := 0.000000; matC[4, 6] := 0.000000; matC[4, 7] := 1.000000; matC[4, 8] := 0.000000;

    (* Row 5: y[5] = ERD Differential Pressure Delta_P_erd [bar] (P_erd - P_px_disch) *)
    matC[5, 1] := 0.000000; matC[5, 2] := 0.000000; matC[5, 3] := 0.000000; matC[5, 4] := 0.000000;
    matC[5, 5] := 1.000000; matC[5, 6] := 0.000000; matC[5, 7] := 0.000000; matC[5, 8] := 0.000000;

    (* Row 6: y[6] = Specific Energy Consumption SEC [kWh/m3] *)
    matC[6, 1] := 0.038500; matC[6, 2] := 0.000000; matC[6, 3] := -0.00125; matC[6, 4] := 0.004500;
    matC[6, 5] := -0.02450; matC[6, 6] := 0.000120; matC[6, 7] := 0.000000; matC[6, 8] := -0.21500;

    (* ------------------------------------------------------------------------------------------------
       MATRIX D: DIRECT FEEDTHROUGH MATRIX (6x6)
       ------------------------------------------------------------------------------------------------ *)
    FOR i := 1 TO 6 DO
        FOR j := 1 TO 6 DO
            matD[i, j] := 0.000000;
        END_FOR;
    END_FOR;
    matD[1, 1] := 0.025000;   (* Instantaneous HPP pump pressure response *)
    matD[5, 2] := -0.045000;  (* Instantaneous PX Booster suction reaction *)
    matD[6, 1] := 0.018500;   (* Instantaneous HPP power draw contribution to SEC *)
    matD[6, 2] := 0.006200;   (* Instantaneous PX Booster power draw contribution to SEC *)

    (* ------------------------------------------------------------------------------------------------
       MATRIX L: LUENBERGER OBSERVER KALMAN-FILTER INNOVATION GAIN (8x6)
       ------------------------------------------------------------------------------------------------ *)
    (* State 1: P_feed *)
    matL[1, 1] := 0.325000; matL[1, 2] := -0.00045; matL[1, 3] := 0.000210;
    matL[1, 4] := 0.000000; matL[1, 5] := 0.045000; matL[1, 6] := 0.125000;

    (* State 2: NDP *)
    matL[2, 1] := 0.285000; matL[2, 2] := 0.001850; matL[2, 3] := -0.00085;
    matL[2, 4] := -0.00120; matL[2, 5] := 0.012500; matL[2, 6] := -0.08500;

    (* State 3: J_v *)
    matL[3, 1] := 0.012000; matL[3, 2] := 0.006850; matL[3, 3] := -0.00320;
    matL[3, 4] := -0.00450; matL[3, 5] := 0.001200; matL[3, 6] := -0.14500;

    (* State 4: Pi_bar *)
    matL[4, 1] := 0.018500; matL[4, 2] := 0.002400; matL[4, 3] := 0.001850;
    matL[4, 4] := 0.008500; matL[4, 5] := 0.000500; matL[4, 6] := 0.095000;

    (* State 5: P_erd *)
    matL[5, 1] := 0.065000; matL[5, 2] := -0.00025; matL[5, 3] := 0.002850;
    matL[5, 4] := 0.000000; matL[5, 5] := 0.385000; matL[5, 6] := -0.06500;

    (* State 6: Delta_C_mix *)
    matL[6, 1] := 0.004500; matL[6, 2] := 0.001200; matL[6, 3] := 0.008500;
    matL[6, 4] := 0.145000; matL[6, 5] := 0.024500; matL[6, 6] := 0.000000;

    (* State 7: C_perm *)
    matL[7, 1] := 0.000850; matL[7, 2] := -0.00450; matL[7, 3] := 0.002100;
    matL[7, 4] := 0.425000; matL[7, 5] := 0.000000; matL[7, 6] := 0.000000;

    (* State 8: Kw *)
    matL[8, 1] := -0.00005; matL[8, 2] := 0.000185; matL[8, 3] := -0.00008;
    matL[8, 4] := -0.00012; matL[8, 5] := 0.000000; matL[8, 6] := -0.00850;

    (* ------------------------------------------------------------------------------------------------
       MPC WEIGHTING MATRICES: Q (State), R (Actuator Energy), S (Slew Rate), P (Terminal Riccati)
       ------------------------------------------------------------------------------------------------ *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            matQ[i, j] := 0.000000;
            matP[i, j] := 0.000000;
        END_FOR;
    END_FOR;
    FOR i := 1 TO 6 DO
        FOR j := 1 TO 6 DO
            matR[i, j] := 0.000000;
            matS[i, j] := 0.000000;
        END_FOR;
    END_FOR;

    (* State Tracking Penalties Q *)
    matQ[1, 1] := 2.500000;   (* P_feed tracking penalty *)
    matQ[2, 2] := 4.200000;   (* NDP tracking penalty *)
    matQ[3, 3] := 8.500000;   (* Permeate flux tracking penalty (High Priority Production Target) *)
    matQ[4, 4] := 1.800000;   (* Osmotic pressure minimization penalty *)
    matQ[5, 5] := 2.200000;   (* ERD HP brine pressure balance penalty *)
    matQ[6, 6] := 0.850000;   (* ERD mixing salinity minimization penalty *)
    matQ[7, 7] := 12.50000;   (* Permeate conductivity penalty (High Priority Drinking Water Standard) *)
    matQ[8, 8] := 25.00000;   (* Permeability degradation penalty (Fouling prevention) *)

    (* Actuator Control Energy Penalties R *)
    matR[1, 1] := 0.450000;   (* HPP VFD energy cost (Massive Electrical Load ~2.5 MW) *)
    matR[2, 2] := 0.280000;   (* PX Booster VFD energy cost (~150 kW) *)
    matR[3, 3] := 0.050000;   (* Brine throttle valve positioning effort *)
    matR[4, 4] := 0.120000;   (* Antiscalant chemical consumption cost *)
    matR[5, 5] := 0.180000;   (* Sodium Bisulfite chemical consumption cost *)
    matR[6, 6] := 0.080000;   (* Permeate flush valve operation *)

    (* Actuator Slew Rate Penalties S (Mechanical Stress & Water Hammer Dampening) *)
    matS[1, 1] := 1.850000;   (* Slew penalty on HPP frequency acceleration *)
    matS[2, 2] := 1.250000;   (* Slew penalty on PX Booster acceleration *)
    matS[3, 3] := 0.650000;   (* Slew penalty on brine throttle valve *)
    matS[4, 4] := 0.350000;   (* Slew penalty on antiscalant stroke *)
    matS[5, 5] := 0.450000;   (* Slew penalty on SBS stroke *)
    matS[6, 6] := 0.550000;   (* Slew penalty on flush valve *)

    (* Terminal State Penalties P (Discrete Algebraic Riccati Solution) *)
    matP[1, 1] := 5.800000;
    matP[2, 2] := 8.400000;
    matP[3, 3] := 18.50000;
    matP[4, 4] := 3.600000;
    matP[5, 5] := 4.800000;
    matP[6, 6] := 1.700000;
    matP[7, 7] := 28.50000;
    matP[8, 8] := 65.00000;

    (* Actuator Physical Box Constraints *)
    u_min[1] := 30.000;   u_max[1] := 60.000;   (* HPP VFD Frequency [Hz] *)
    u_min[2] := 25.000;   u_max[2] := 60.000;   (* PX Booster VFD Frequency [Hz] *)
    u_min[3] := 10.000;   u_max[3] := 100.00;   (* Brine Reject Throttle [%] *)
    u_min[4] := 5.0000;   u_max[4] := 100.00;   (* Antiscalant Chemical Pump [%] *)
    u_min[5] := 0.0000;   u_max[5] := 100.00;   (* Sodium Bisulfite Pump [%] *)
    u_min[6] := 0.0000;   u_max[6] := 100.00;   (* Permeate Flush / Bypass [%] *)

    (* Actuator Dynamic Slew Rate Limits Per Scan (Ts = 10 ms -> e.g. 0.5 Hz/s = 0.005 Hz/scan) *)
    du_max[1] := 0.0050;  (* HPP Max Acceleration: 0.5 Hz/s *)
    du_max[2] := 0.0100;  (* PX Booster Max Acceleration: 1.0 Hz/s *)
    du_max[3] := 0.0500;  (* Brine Valve Max Rate: 5.0 %/s *)
    du_max[4] := 0.1000;  (* Antiscalant Stroke Max Rate: 10.0 %/s *)
    du_max[5] := 0.1000;  (* SBS Stroke Max Rate: 10.0 %/s *)
    du_max[6] := 0.2000;  (* Flush Valve Max Rate: 20.0 %/s *)

    (* Initial State Vector Baseline Allocation *)
    x_state[1] := 65.00;  (* Initial P_feed [bar] *)
    x_state[2] := 16.50;  (* Initial NDP [bar] *)
    x_state[3] := 16.67;  (* Initial Permeate Flux J_v [LMH] (2083.3 m3/h / 125,000 m2) *)
    x_state[4] := 38.50;  (* Initial Osmotic Pressure Pi_bar [bar] *)
    x_state[5] := 63.50;  (* Initial ERD HP Brine Pressure [bar] *)
    x_state[6] := 250.0;  (* Initial ERD Rotor Mixing Salinity [ppm] *)
    x_state[7] := 280.0;  (* Initial Permeate Salinity [uS/cm] *)
    x_state[8] := 1.850;  (* Initial Permeability Kw [LMH/bar] *)

    FOR i := 1 TO 8 DO
        x_hat[i]  := x_state[i];
        x_pred[i] := x_state[i];
        x_ref[i]  := x_state[i];
    END_FOR;

    (* Target Reference Setpoint Vector for Steady State Production *)
    x_ref[1] := 68.50;    (* Target Feed Pressure [bar] *)
    x_ref[2] := 18.20;    (* Target NDP [bar] *)
    x_ref[3] := 16.67;    (* Target Permeate Flux [LMH] -> 50,000 m3/day *)
    x_ref[4] := 39.80;    (* Target Osmotic Pressure [bar] at 42% Recovery *)
    x_ref[5] := 66.80;    (* Target ERD HP Pressure [bar] *)
    x_ref[6] := 180.0;    (* Target ERD Mixing Salinity [ppm] *)
    x_ref[7] := 250.0;    (* Target Permeate Conductivity [uS/cm] *)
    x_ref[8] := 1.850;    (* Target Clean Permeability [LMH/bar] *)

    FOR i := 1 TO 6 DO
        u_ctrl[i] := 0.0;
        u_prev[i] := 0.0;
    END_FOR;
    u_ctrl[3] := 100.0;   (* Full open brine valve at start *)
    u_prev[3] := 100.0;

    bInitialized := TRUE;
END_IF;
"""
    return code
