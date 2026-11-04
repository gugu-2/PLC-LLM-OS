# -*- coding: utf-8 -*-
"""
Generator module: Phase 0 Matrix and Control Initialization
"""

def get_phase0_init():
    return """(* =========================================================================================== *)
(* PHASE 0: MODEL MATRICES & CONTROL COEFFICIENT INITIALIZATION                                *)
(* =========================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* --------------------------------------------------------------------------------------- *)
    (* 1.0 DISCRETE STATE TRANSITION MATRIX arrA (8x8) @ Ts = 10 ms                            *)
    (* States:                                                                                 *)
    (* x1: Delta Broth Core Temperature [deg C] (Nominal: 37.00 deg C)                         *)
    (* x2: Delta Dissolved Oxygen Concentration [ % air sat ] (Nominal: 50.00 %)               *)
    (* x3: Delta Liquid Broth Acidity [pH] (Nominal: 7.050)                                    *)
    (* x4: Delta Viable Cell Density VCD [ 10^6 cells/mL ] (Nominal: 85.00 x 10^6 cells/mL)    *)
    (* x5: Delta Glucose Substrate Concentration [g/L] (Nominal: 4.50 g/L)                     *)
    (* x6: Delta Toxic Lactate Metabolite [g/L] (Nominal: 1.20 g/L)                            *)
    (* x7: Delta Transmembrane Pressure TMP [bar] (Nominal: 0.180 bar)                         *)
    (* x8: Delta Carbon Dioxide Evolution Rate CER [mmol/(L*h)] (Nominal: 18.50 mmol/(L*h))    *)
    (* --------------------------------------------------------------------------------------- *)
    (* Row 1: Broth Temperature Dynamics *)
    arrA[1, 1] := 0.9982; (* Broth thermal inertia and convective jacket heat exchange dissipation *)
    arrA[1, 2] := 0.0000; (* Dissolved oxygen decoupling from bulk thermal enthalpy *)
    arrA[1, 3] := 0.0000; (* Liquid pH decoupling from bulk thermal inertia *)
    arrA[1, 4] := 0.0001; (* Metabolic cellular thermogenesis per million viable cells per mL *)
    arrA[1, 5] := 0.0000; (* Substrate glucose enthalpy negligible in bulk aqueous liquid *)
    arrA[1, 6] := 0.0000; (* Lactate concentration negligible in bulk thermal dynamics *)
    arrA[1, 7] := 0.0002; (* Hydraulic viscous dissipation from ATF recirculation pumping *)
    arrA[1, 8] := 0.0000; (* Off-gas CER decoupled from liquid thermal energy balance *)

    (* Row 2: Dissolved Oxygen Dynamics *)
    arrA[2, 1] := -0.0125; (* Temperature elevation reducing Henry's law oxygen solubility C* *)
    arrA[2, 2] := 0.9850; (* Gas-liquid interfacial mass transfer retention and kLa balance *)
    arrA[2, 3] := 0.0000; (* Broth pH decoupling from oxygen mass transfer coefficient *)
    arrA[2, 4] := -0.0185; (* Cellular respiratory oxygen uptake rate OUR consumption per unit VCD *)
    arrA[2, 5] := 0.0004; (* Glucose substrate availability sustaining active aerobic respiration *)
    arrA[2, 6] := -0.0008; (* Toxic lactate accumulation inhibiting mitochondrial electron transport *)
    arrA[2, 7] := -0.0012; (* Hollow-fiber boundary layer deoxygenation during tangential transit *)
    arrA[2, 8] := -0.0035; (* CO2 gas stripping cross-coupling and bubble partial pressure displacement *)

    (* Row 3: Liquid Broth pH Dynamics *)
    arrA[3, 1] := -0.0005; (* Temperature variation shifting water auto-ionization and carbonic pKa *)
    arrA[3, 2] := 0.0000; (* Dissolved oxygen decoupled from liquid hydronium ion activity *)
    arrA[3, 3] := 0.9920; (* Bicarbonate / carbonic acid buffer chemical equilibrium persistence *)
    arrA[3, 4] := -0.0008; (* Cellular acidic metabolite generation across growing biomass *)
    arrA[3, 5] := -0.0003; (* High glucose glycolysis leading to increased organic acid production *)
    arrA[3, 6] := -0.0240; (* Direct dissociation of accumulated lactic acid lowering culture pH *)
    arrA[3, 7] := 0.0000; (* Membrane filtration TMP decoupled from chemical equilibrium *)
    arrA[3, 8] := -0.0085; (* Dissolved CO2 carbonic acid accumulation from high CER evolution *)

    (* Row 4: Viable Cell Density (VCD) Dynamics *)
    arrA[4, 1] := 0.0015; (* Thermal Arrhenius enzyme acceleration around physiological 37.0 C *)
    arrA[4, 2] := 0.0080; (* Dissolved oxygen availability promoting mammalian ATP phosphorylation *)
    arrA[4, 3] := 0.0045; (* Near-neutral pH optimum maximizing cell division mitotic rate *)
    arrA[4, 4] := 0.9975; (* Net specific biomass division rate minus cellular lysis and cell bleed *)
    arrA[4, 5] := 0.0120; (* Monod substrate-dependent cellular proliferation driven by glucose *)
    arrA[4, 6] := -0.0150; (* Non-competitive inhibition and apoptotic arrest from toxic lactate *)
    arrA[4, 7] := -0.0025; (* Shear stress cell lysis induced by excessive ATF membrane shear *)
    arrA[4, 8] := 0.0000; (* Off-gas CER rate decoupled directly from biomass mass balance *)

    (* Row 5: Glucose Substrate Concentration Dynamics *)
    arrA[5, 1] := -0.0008; (* Thermal stimulation of glycolytic hexokinase enzyme consumption *)
    arrA[5, 2] := -0.0012; (* Aerobic metabolic pathway glucose oxidation rate coupling *)
    arrA[5, 3] := 0.0000; (* Liquid pH decoupled from extracellular glucose concentration *)
    arrA[5, 4] := -0.0165; (* Biomass glucose consumption rate q_glc proportional to VCD *)
    arrA[5, 5] := 0.9880; (* Fresh perfusion media substrate renewal minus chemostat wash-out *)
    arrA[5, 6] := 0.0005; (* Metabolic feedback allosteric regulation from high lactate levels *)
    arrA[5, 7] := 0.0000; (* Membrane TMP decoupled from molecular glucose transport *)
    arrA[5, 8] := 0.0000; (* Off-gas CER decoupled from extracellular dissolved substrate *)

    (* Row 6: Lactate Metabolite Accumulation Dynamics *)
    arrA[6, 1] := 0.0005; (* Elevated temperature accelerating anaerobic fermentation pathways *)
    arrA[6, 2] := -0.0025; (* Hypoxia / low dO2 triggering Warburg overflow lactic acid synthesis *)
    arrA[6, 3] := 0.0000; (* Ambient pH feedback decoupled from lactate mass stoichiometry *)
    arrA[6, 4] := 0.0095; (* Specific lactate production rate q_lac scaled by viable cell density *)
    arrA[6, 5] := 0.0085; (* Excess glycolytic flux driving Crabtree/Warburg lactate overflow *)
    arrA[6, 6] := 0.9820; (* Permeate harvest extraction washing out soluble lactate from vessel *)
    arrA[6, 7] := 0.0000; (* Transmembrane pressure decoupled from molecular lactate excretion *)
    arrA[6, 8] := 0.0010; (* Metabolic activity coupling with cellular respiration indicators *)

    (* Row 7: Transmembrane Pressure (TMP) Dynamics *)
    arrA[7, 1] := -0.0012; (* Permeate viscosity decrease with temperature lowering hydraulic resistance *)
    arrA[7, 2] := 0.0000; (* Dissolved oxygen decoupled from hollow fiber Darcy filtration *)
    arrA[7, 3] := 0.0000; (* Broth pH decoupled from micro-porous membrane fluid resistance *)
    arrA[7, 4] := 0.0035; (* Cell density concentration polarization elevating lumen boundary viscosity *)
    arrA[7, 5] := 0.0000; (* Glucose concentration decoupled from membrane hydraulic resistance *)
    arrA[7, 6] := 0.0000; (* Lactate concentration decoupled from membrane fouling layer *)
    arrA[7, 7] := 0.9910; (* Hollow-fiber cake layer accumulation and hydraulic resistance persistence *)
    arrA[7, 8] := 0.0000; (* CER decoupled from membrane filtration fluid dynamics *)

    (* Row 8: Carbon Dioxide Evolution Rate (CER) Dynamics *)
    arrA[8, 1] := 0.0020; (* Arrhenius temperature stimulation of tricarboxylic acid (TCA) cycle *)
    arrA[8, 2] := 0.0040; (* Aerobic mitochondrial metabolism driving decarboxylation reactions *)
    arrA[8, 3] := 0.0010; (* Acidic shift liberating dissolved bicarbonate into gaseous CO2 phase *)
    arrA[8, 4] := 0.0220; (* Specific respiratory CO2 evolution qCO2 scaled directly by VCD *)
    arrA[8, 5] := 0.0065; (* Glucose oxidation substrate availability accelerating TCA decarboxylation *)
    arrA[8, 6] := -0.0030; (* Metabolic acidosis and cellular senescence suppressing respiration *)
    arrA[8, 7] := 0.0000; (* ATF membrane TMP decoupled from exhaust respirometry *)
    arrA[8, 8] := 0.9750; (* Headspace gas flushing and exhaust gas mass transport clearance *)

    (* --------------------------------------------------------------------------------------- *)
    (* 2.0 ACTUATOR COUPLING MATRIX arrB (8x6) @ Ts = 10 ms                                    *)
    (* Inputs:                                                                                 *)
    (* u1: Sparger Pure O2 Mass Flow [SLPM] (0.0 to 150.0 SLPM)                                *)
    (* u2: Sparger Pure CO2 Mass Flow [SLPM] (0.0 to 50.0 SLPM)                                *)
    (* u3: Fresh Perfusion Feed Pump Speed [RPM] (0.0 to 300.0 RPM)                            *)
    (* u4: Permeate Harvest Pump Speed [RPM] (0.0 to 300.0 RPM)                                *)
    (* u5: Thermal Jacket Coolant Control Valve [%] (0.0 to 100.0 %)                           *)
    (* u6: Base Dosing Metering Pump Speed [RPM] (0.0 to 120.0 RPM)                            *)
    (* --------------------------------------------------------------------------------------- *)
    (* State x1: Broth Temp *)
    arrB[1, 1] := 0.0000; arrB[1, 2] := 0.0000; arrB[1, 3] := -0.0015; arrB[1, 4] := 0.0000; arrB[1, 5] := -0.0250; arrB[1, 6] := 0.0000;
    (* State x2: Dissolved Oxygen dO2 *)
    arrB[2, 1] := 0.0480; arrB[2, 2] := -0.0035; arrB[2, 3] := 0.0010; arrB[2, 4] := 0.0000; arrB[2, 5] := 0.0000; arrB[2, 6] := 0.0000;
    (* State x3: Broth pH *)
    arrB[3, 1] := 0.0000; arrB[3, 2] := -0.0220; arrB[3, 3] := 0.0005; arrB[3, 4] := 0.0000; arrB[3, 5] := 0.0000; arrB[3, 6] := 0.0350;
    (* State x4: Viable Cell Density VCD *)
    arrB[4, 1] := 0.0012; arrB[4, 2] := 0.0000; arrB[4, 3] := 0.0025; arrB[4, 4] := -0.0005; arrB[4, 5] := 0.0000; arrB[4, 6] := 0.0008;
    (* State x5: Glucose Concentration *)
    arrB[5, 1] := 0.0000; arrB[5, 2] := 0.0000; arrB[5, 3] := 0.0380; arrB[5, 4] := -0.0020; arrB[5, 5] := 0.0000; arrB[5, 6] := 0.0000;
    (* State x6: Lactate Concentration *)
    arrB[6, 1] := 0.0000; arrB[6, 2] := 0.0000; arrB[6, 3] := -0.0010; arrB[6, 4] := -0.0280; arrB[6, 5] := 0.0000; arrB[6, 6] := 0.0000;
    (* State x7: Transmembrane Pressure TMP *)
    arrB[7, 1] := 0.0000; arrB[7, 2] := 0.0000; arrB[7, 3] := 0.0005; arrB[7, 4] := 0.0160; arrB[7, 5] := 0.0000; arrB[7, 6] := 0.0000;
    (* State x8: CO2 Evolution Rate CER *)
    arrB[8, 1] := 0.0015; arrB[8, 2] := 0.0180; arrB[8, 3] := 0.0010; arrB[8, 4] := 0.0000; arrB[8, 5] := 0.0000; arrB[8, 6] := -0.0040;

    (* --------------------------------------------------------------------------------------- *)
    (* 3.0 OBSERVATION MATRIX arrC (8x8) & FEEDTHROUGH MATRIX arrD (8x6)                        *)
    (* --------------------------------------------------------------------------------------- *)
    FOR nIdx_i := 1 TO 8 DO
        FOR nIdx_j := 1 TO 8 DO
            IF nIdx_i = nIdx_j THEN
                arrC[nIdx_i, nIdx_j] := 1.0;
            ELSE
                arrC[nIdx_i, nIdx_j] := 0.0;
            END_IF;
        END_FOR;
        FOR nIdx_m := 1 TO 6 DO
            arrD[nIdx_i, nIdx_m] := 0.0;
        END_FOR;
    END_FOR;

    (* --------------------------------------------------------------------------------------- *)
    (* 4.0 MODEL PREDICTIVE CONTROL (MPC) PENALTY WEIGHTS & SATURATION LIMITS                  *)
    (* --------------------------------------------------------------------------------------- *)
    (* State deviation penalties Q (Penalizing VCD drop, low dO2, pH excursion, TMP rise) *)
    arrQ_Weight[1] := 120.0;    (* Broth temperature tracking penalty *)
    arrQ_Weight[2] := 85.0;     (* Dissolved oxygen regulation penalty *)
    arrQ_Weight[3] := 180.0;    (* pH tightly bounded around 7.050 *)
    arrQ_Weight[4] := 250.0;    (* Viable cell density VCD maximization penalty *)
    arrQ_Weight[5] := 95.0;     (* Glucose substrate stabilization penalty *)
    arrQ_Weight[6] := 140.0;    (* Toxic lactate suppression penalty *)
    arrQ_Weight[7] := 160.0;    (* Transmembrane pressure TMP fouling penalty *)
    arrQ_Weight[8] := 45.0;     (* Respirometric CER tracking weight *)

    (* Actuator energy penalties R *)
    arrR_Weight[1] := 1.50;     (* Sparger pure O2 consumption penalty *)
    arrR_Weight[2] := 2.00;     (* Sparger pure CO2 consumption penalty *)
    arrR_Weight[3] := 3.20;     (* Fresh media pumping effort penalty *)
    arrR_Weight[4] := 3.50;     (* Harvest permeate extraction effort penalty *)
    arrR_Weight[5] := 1.20;     (* Jacket cooling valve movement penalty *)
    arrR_Weight[6] := 4.50;     (* Base dosing expenditure penalty *)

    (* Actuator slew rate penalties S (Suppressing rapid cycling & pump wear) *)
    arrS_Weight[1] := 5.00;     (* O2 MFC slew rate penalty *)
    arrS_Weight[2] := 8.00;     (* CO2 MFC slew rate penalty *)
    arrS_Weight[3] := 12.00;    (* Fresh media feed pump slew rate penalty *)
    arrS_Weight[4] := 15.00;    (* Harvest pump slew rate penalty *)
    arrS_Weight[5] := 6.50;     (* Coolant valve slew rate penalty *)
    arrS_Weight[6] := 20.00;    (* Base dosing pump slew rate penalty *)

    (* Terminal state horizon penalties P *)
    FOR nIdx_i := 1 TO 8 DO
        arrP_Weight[nIdx_i] := arrQ_Weight[nIdx_i] * 2.50;
    END_FOR;

    (* Actuator Saturation & Slew Limits *)
    arrU_Min[1] := 0.0;    arrU_Max[1] := 150.0;  arrDeltaU_Max[1] := 2.50;  (* O2 MFC [SLPM] *)
    arrU_Min[2] := 0.0;    arrU_Max[2] := 50.0;   arrDeltaU_Max[2] := 1.20;  (* CO2 MFC [SLPM] *)
    arrU_Min[3] := 0.0;    arrU_Max[3] := 300.0;  arrDeltaU_Max[3] := 4.00;  (* Feed Pump [RPM] *)
    arrU_Min[4] := 0.0;    arrU_Max[4] := 300.0;  arrDeltaU_Max[4] := 4.00;  (* Harvest Pump [RPM] *)
    arrU_Min[5] := 0.0;    arrU_Max[5] := 100.0;  arrDeltaU_Max[5] := 5.00;  (* Cooling Valve [%] *)
    arrU_Min[6] := 0.0;    arrU_Max[6] := 120.0;  arrDeltaU_Max[6] := 3.00;  (* Base Pump [RPM] *)

    (* Projected Gradient Descent Learning Rates *)
    arrMPC_StepSize[1] := 0.0085;
    arrMPC_StepSize[2] := 0.0065;
    arrMPC_StepSize[3] := 0.0045;
    arrMPC_StepSize[4] := 0.0045;
    arrMPC_StepSize[5] := 0.0120;
    arrMPC_StepSize[6] := 0.0035;

    (* Nominal Reference Trajectory Setup *)
    arrX_Ref[1] := 37.00;  (* Setpoint Temp: 37.00 C *)
    arrX_Ref[2] := 50.00;  (* Setpoint dO2: 50.00 % *)
    arrX_Ref[3] := 7.050;  (* Setpoint pH: 7.050 *)
    arrX_Ref[4] := 85.00;  (* Setpoint VCD: 85.0 x 10^6 cells/mL *)
    arrX_Ref[5] := 4.500;  (* Setpoint Glucose: 4.50 g/L *)
    arrX_Ref[6] := 1.200;  (* Setpoint Lactate: 1.20 g/L *)
    arrX_Ref[7] := 0.180;  (* Setpoint TMP: 0.180 bar *)
    arrX_Ref[8] := 18.50;  (* Setpoint CER: 18.50 mmol/(L*h) *)

    bMatricesInitialized := TRUE;
END_IF;
"""

print("get_phase0_init ready.")
