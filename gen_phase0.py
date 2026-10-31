# gen_phase0.py - Generates Phase 0: Matrix Initialization

def generate_phase0():
    return """(* ==================================================================================================================== *)
(* PHASE 0: ONE-TIME DETERMINISTIC INITIALIZATION OF 16x16 STATE-SPACE & RECEDING-HORIZON MPC MATRICES                  *)
(* ==================================================================================================================== *)
IF NOT bFirstScanInitDone THEN
    (* --- 16x16 Discrete System Matrix A: x[k+1] = A * x[k] + B * u[k] --- *)
    (* Row 1: T_inlet_oil (Syltherm XLT circulation inlet temperature) *)
    aA_Lyo[1, 1] := 0.9420; aA_Lyo[1, 2] := 0.0480; aA_Lyo[1, 3] := 0.0080; aA_Lyo[1, 4] := 0.0000;
    aA_Lyo[1, 5] := 0.0000; aA_Lyo[1, 6] := 0.0000; aA_Lyo[1, 7] := 0.0000; aA_Lyo[1, 8] := 0.0000;
    aA_Lyo[1, 9] := 0.0000; aA_Lyo[1, 10]:= 0.0000; aA_Lyo[1, 11]:= 0.0000; aA_Lyo[1, 12]:= 0.0000;
    aA_Lyo[1, 13]:= 0.0000; aA_Lyo[1, 14]:= 0.0000; aA_Lyo[1, 15]:= 0.0000; aA_Lyo[1, 16]:= 0.0000;

    (* Row 2: T_outlet_oil (Syltherm XLT circulation outlet temperature after shelf heat exchange) *)
    aA_Lyo[2, 1] := 0.1250; aA_Lyo[2, 2] := 0.8150; aA_Lyo[2, 3] := 0.0580; aA_Lyo[2, 4] := 0.0000;
    aA_Lyo[2, 5] := 0.0000; aA_Lyo[2, 6] := 0.0000; aA_Lyo[2, 7] := 0.0000; aA_Lyo[2, 8] := 0.0000;
    aA_Lyo[2, 9] := 0.0000; aA_Lyo[2, 10]:= 0.0000; aA_Lyo[2, 11]:= 0.0000; aA_Lyo[2, 12]:= 0.0000;
    aA_Lyo[2, 13]:= -0.0012;aA_Lyo[2, 14]:= 0.0000; aA_Lyo[2, 15]:= 0.0000; aA_Lyo[2, 16]:= 0.0000;

    (* Row 3: T_shelf_plate (316L Stainless steel shelf surface plate average temperature) *)
    aA_Lyo[3, 1] := 0.0450; aA_Lyo[3, 2] := 0.0650; aA_Lyo[3, 3] := 0.8720; aA_Lyo[3, 4] := 0.0180;
    aA_Lyo[3, 5] := 0.0000; aA_Lyo[3, 6] := 0.0000; aA_Lyo[3, 7] := 0.0000; aA_Lyo[3, 8] := 0.0000;
    aA_Lyo[3, 9] := 0.0000; aA_Lyo[3, 10]:= 0.0000; aA_Lyo[3, 11]:= 0.0000; aA_Lyo[3, 12]:= 0.0000;
    aA_Lyo[3, 13]:= -0.0028;aA_Lyo[3, 14]:= 0.0000; aA_Lyo[3, 15]:= 0.0000; aA_Lyo[3, 16]:= 0.0000;

    (* Row 4: T_vial_base (Borosilicate glass vial base contact temperature) *)
    aA_Lyo[4, 1] := 0.0000; aA_Lyo[4, 2] := 0.0000; aA_Lyo[4, 3] := 0.0820; aA_Lyo[4, 4] := 0.8450;
    aA_Lyo[4, 5] := 0.0710; aA_Lyo[4, 6] := 0.0020; aA_Lyo[4, 7] := 0.0000; aA_Lyo[4, 8] := 0.0000;
    aA_Lyo[4, 9] := 0.0005; aA_Lyo[4, 10]:= 0.0000; aA_Lyo[4, 11]:= 0.0000; aA_Lyo[4, 12]:= 0.0000;
    aA_Lyo[4, 13]:= -0.0035;aA_Lyo[4, 14]:= 0.0000; aA_Lyo[4, 15]:= 0.0000; aA_Lyo[4, 16]:= 0.0000;

    (* Row 5: T_sublim_front (Moving frozen interface temperature - must remain < T_collapse) *)
    aA_Lyo[5, 1] := 0.0000; aA_Lyo[5, 2] := 0.0000; aA_Lyo[5, 3] := 0.0120; aA_Lyo[5, 4] := 0.1150;
    aA_Lyo[5, 5] := 0.8120; aA_Lyo[5, 6] := 0.0580; aA_Lyo[5, 7] := 0.0032; aA_Lyo[5, 8] := 0.0000;
    aA_Lyo[5, 9] := -0.0018;aA_Lyo[5, 10]:= 0.0000; aA_Lyo[5, 11]:= 0.0000; aA_Lyo[5, 12]:= 0.0000;
    aA_Lyo[5, 13]:= -0.0084;aA_Lyo[5, 14]:= 0.0000; aA_Lyo[5, 15]:= 0.0000; aA_Lyo[5, 16]:= 0.0000;

    (* Row 6: T_dried_cake (Upper porous dry product layer temperature) *)
    aA_Lyo[6, 1] := 0.0000; aA_Lyo[6, 2] := 0.0000; aA_Lyo[6, 3] := 0.0240; aA_Lyo[6, 4] := 0.0450;
    aA_Lyo[6, 5] := 0.0650; aA_Lyo[6, 6] := 0.8650; aA_Lyo[6, 7] := 0.0000; aA_Lyo[6, 8] := 0.0000;
    aA_Lyo[6, 9] := 0.0008; aA_Lyo[6, 10]:= 0.0000; aA_Lyo[6, 11]:= 0.0000; aA_Lyo[6, 12]:= 0.0000;
    aA_Lyo[6, 13]:= 0.0000; aA_Lyo[6, 14]:= -0.0042;aA_Lyo[6, 15]:= 0.0000; aA_Lyo[6, 16]:= 0.0000;

    (* Row 7: P_vapor_H2O (Partial pressure of water vapor sublimating from vials) *)
    aA_Lyo[7, 1] := 0.0000; aA_Lyo[7, 2] := 0.0000; aA_Lyo[7, 3] := 0.0000; aA_Lyo[7, 4] := 0.0000;
    aA_Lyo[7, 5] := 0.0145; aA_Lyo[7, 6] := 0.0000; aA_Lyo[7, 7] := 0.7650; aA_Lyo[7, 8] := 0.0000;
    aA_Lyo[7, 9] := 0.1250; aA_Lyo[7, 10]:= 0.0000; aA_Lyo[7, 11]:= -0.0045;aA_Lyo[7, 12]:= 0.0000;
    aA_Lyo[7, 13]:= 0.0980; aA_Lyo[7, 14]:= 0.0000; aA_Lyo[7, 15]:= 0.0000; aA_Lyo[7, 16]:= 0.0000;

    (* Row 8: P_inert_N2 (Partial pressure of injected sterile nitrogen gas) *)
    aA_Lyo[8, 1] := 0.0000; aA_Lyo[8, 2] := 0.0000; aA_Lyo[8, 3] := 0.0000; aA_Lyo[8, 4] := 0.0000;
    aA_Lyo[8, 5] := 0.0000; aA_Lyo[8, 6] := 0.0000; aA_Lyo[8, 7] := 0.0000; aA_Lyo[8, 8] := 0.8850;
    aA_Lyo[8, 9] := 0.0820; aA_Lyo[8, 10]:= 0.0000; aA_Lyo[8, 11]:= 0.0000; aA_Lyo[8, 12]:= 0.0000;
    aA_Lyo[8, 13]:= 0.0000; aA_Lyo[8, 14]:= 0.0000; aA_Lyo[8, 15]:= 0.0000; aA_Lyo[8, 16]:= 0.0000;

    (* Row 9: P_chamber_total (Total chamber absolute pressure = P_H2O + P_N2) *)
    aA_Lyo[9, 1] := 0.0000; aA_Lyo[9, 2] := 0.0000; aA_Lyo[9, 3] := 0.0000; aA_Lyo[9, 4] := 0.0000;
    aA_Lyo[9, 5] := 0.0120; aA_Lyo[9, 6] := 0.0000; aA_Lyo[9, 7] := 0.4450; aA_Lyo[9, 8] := 0.4550;
    aA_Lyo[9, 9] := 0.8920; aA_Lyo[9, 10]:= 0.0000; aA_Lyo[9, 11]:= -0.0035;aA_Lyo[9, 12]:= 0.0000;
    aA_Lyo[9, 13]:= 0.0850; aA_Lyo[9, 14]:= 0.0000; aA_Lyo[9, 15]:= 0.0000; aA_Lyo[9, 16]:= 0.0000;

    (* Row 10: P_pirani_apparent (Pirani thermal conductivity indicated pressure) *)
    aA_Lyo[10, 1] := 0.0000; aA_Lyo[10, 2] := 0.0000; aA_Lyo[10, 3] := 0.0000; aA_Lyo[10, 4] := 0.0000;
    aA_Lyo[10, 5] := 0.0150; aA_Lyo[10, 6] := 0.0000; aA_Lyo[10, 7] := 0.6850; aA_Lyo[10, 8] := 0.2850;
    aA_Lyo[10, 9] := 0.0000; aA_Lyo[10, 10]:= 0.8850; aA_Lyo[10, 11]:= 0.0000; aA_Lyo[10, 12]:= 0.0000;
    aA_Lyo[10, 13]:= 0.0920; aA_Lyo[10, 14]:= 0.0000; aA_Lyo[10, 15]:= 0.0000; aA_Lyo[10, 16]:= 0.0000;

    (* Row 11: T_condenser_surface (Ice condenser refrigeration surface temperature) *)
    aA_Lyo[11, 1] := 0.0000; aA_Lyo[11, 2] := 0.0000; aA_Lyo[11, 3] := 0.0000; aA_Lyo[11, 4] := 0.0000;
    aA_Lyo[11, 5] := 0.0000; aA_Lyo[11, 6] := 0.0000; aA_Lyo[11, 7] := 0.0025; aA_Lyo[11, 8] := 0.0000;
    aA_Lyo[11, 9] := 0.0000; aA_Lyo[11, 10]:= 0.0000; aA_Lyo[11, 11]:= 0.9320; aA_Lyo[11, 12]:= 0.0185;
    aA_Lyo[11, 13]:= 0.0065; aA_Lyo[11, 14]:= 0.0000; aA_Lyo[11, 15]:= 0.0000; aA_Lyo[11, 16]:= 0.0000;

    (* Row 12: Delta_ice_frost (Condenser coil frost layer thickness accumulation) *)
    aA_Lyo[12, 1] := 0.0000; aA_Lyo[12, 2] := 0.0000; aA_Lyo[12, 3] := 0.0000; aA_Lyo[12, 4] := 0.0000;
    aA_Lyo[12, 5] := 0.0000; aA_Lyo[12, 6] := 0.0000; aA_Lyo[12, 7] := 0.0000; aA_Lyo[12, 8] := 0.0000;
    aA_Lyo[12, 9] := 0.0000; aA_Lyo[12, 10]:= 0.0000; aA_Lyo[12, 11]:= 0.0000; aA_Lyo[12, 12]:= 0.9995;
    aA_Lyo[12, 13]:= 0.0015; aA_Lyo[12, 14]:= 0.0000; aA_Lyo[12, 15]:= 0.0000; aA_Lyo[12, 16]:= 0.0000;

    (* Row 13: mdot_sublimation (Total instantaneous sublimation mass flux rate) *)
    aA_Lyo[13, 1] := 0.0000; aA_Lyo[13, 2] := 0.0000; aA_Lyo[13, 3] := 0.0450; aA_Lyo[13, 4] := 0.0650;
    aA_Lyo[13, 5] := 0.1250; aA_Lyo[13, 6] := 0.0000; aA_Lyo[13, 7] := -0.0850;aA_Lyo[13, 8] := 0.0000;
    aA_Lyo[13, 9] := -0.0650;aA_Lyo[13, 10]:= 0.0000; aA_Lyo[13, 11]:= 0.0000; aA_Lyo[13, 12]:= 0.0000;
    aA_Lyo[13, 13]:= 0.8420; aA_Lyo[13, 14]:= 0.0000; aA_Lyo[13, 15]:= 0.0000; aA_Lyo[13, 16]:= 0.0000;

    (* Row 14: C_bound_moisture (Secondary drying residual bound water percentage) *)
    aA_Lyo[14, 1] := 0.0000; aA_Lyo[14, 2] := 0.0000; aA_Lyo[14, 3] := 0.0000; aA_Lyo[14, 4] := 0.0000;
    aA_Lyo[14, 5] := 0.0000; aA_Lyo[14, 6] := -0.0085;aA_Lyo[14, 7] := 0.0000; aA_Lyo[14, 8] := 0.0000;
    aA_Lyo[14, 9] := 0.0000; aA_Lyo[14, 10]:= 0.0000; aA_Lyo[14, 11]:= 0.0000; aA_Lyo[14, 12]:= 0.0000;
    aA_Lyo[14, 13]:= 0.0000; aA_Lyo[14, 14]:= 0.9850; aA_Lyo[14, 15]:= 0.0000; aA_Lyo[14, 16]:= 0.0000;

    (* Row 15: Pos_hydraulic_ram (Hydraulic cylinder vertical stroke displacement) *)
    aA_Lyo[15, 1] := 0.0000; aA_Lyo[15, 2] := 0.0000; aA_Lyo[15, 3] := 0.0000; aA_Lyo[15, 4] := 0.0000;
    aA_Lyo[15, 5] := 0.0000; aA_Lyo[15, 6] := 0.0000; aA_Lyo[15, 7] := 0.0000; aA_Lyo[15, 8] := 0.0000;
    aA_Lyo[15, 9] := 0.0000; aA_Lyo[15, 10]:= 0.0000; aA_Lyo[15, 11]:= 0.0000; aA_Lyo[15, 12]:= 0.0000;
    aA_Lyo[15, 13]:= 0.0000; aA_Lyo[15, 14]:= 0.0000; aA_Lyo[15, 15]:= 0.9980; aA_Lyo[15, 16]:= -0.0002;

    (* Row 16: Force_stoppering (Compaction force transmitted through collapsing shelf stacks) *)
    aA_Lyo[16, 1] := 0.0000; aA_Lyo[16, 2] := 0.0000; aA_Lyo[16, 3] := 0.0000; aA_Lyo[16, 4] := 0.0000;
    aA_Lyo[16, 5] := 0.0000; aA_Lyo[16, 6] := 0.0000; aA_Lyo[16, 7] := 0.0000; aA_Lyo[16, 8] := 0.0000;
    aA_Lyo[16, 9] := 0.0000; aA_Lyo[16, 10]:= 0.0000; aA_Lyo[16, 11]:= 0.0000; aA_Lyo[16, 12]:= 0.0000;
    aA_Lyo[16, 13]:= 0.0000; aA_Lyo[16, 14]:= 0.0000; aA_Lyo[16, 15]:= 0.4250; aA_Lyo[16, 16]:= 0.9150;

    (* --- 16x8 Actuator Input Matrix B --- *)
    (* Inputs: 1:SCR_Duty, 2:SlideValve, 3:LN2_Valve, 4:Roots_Speed, 5:N2_Bleed, 6:TXV_Cond, 7:Hydr_Servo, 8:Nucleation *)
    aB_Lyo[1, 1] := 0.0850;  aB_Lyo[1, 2] := -0.0750; aB_Lyo[1, 3] := -0.1450; aB_Lyo[1, 4] := 0.0000;
    aB_Lyo[1, 5] := 0.0000;  aB_Lyo[1, 6] := 0.0000;  aB_Lyo[1, 7] := 0.0000;  aB_Lyo[1, 8] := 0.0000;

    aB_Lyo[2, 1] := 0.0250;  aB_Lyo[2, 2] := -0.0220; aB_Lyo[2, 3] := -0.0450; aB_Lyo[2, 4] := 0.0000;
    aB_Lyo[2, 5] := 0.0000;  aB_Lyo[2, 6] := 0.0000;  aB_Lyo[2, 7] := 0.0000;  aB_Lyo[2, 8] := 0.0000;

    aB_Lyo[3, 1] := 0.0150;  aB_Lyo[3, 2] := -0.0140; aB_Lyo[3, 3] := -0.0280; aB_Lyo[3, 4] := 0.0000;
    aB_Lyo[3, 5] := 0.0000;  aB_Lyo[3, 6] := 0.0000;  aB_Lyo[3, 7] := 0.0000;  aB_Lyo[3, 8] := 0.0000;

    aB_Lyo[4, 1] := 0.0050;  aB_Lyo[4, 2] := -0.0040; aB_Lyo[4, 3] := -0.0080; aB_Lyo[4, 4] := 0.0000;
    aB_Lyo[4, 5] := 0.0002;  aB_Lyo[4, 6] := 0.0000;  aB_Lyo[4, 7] := 0.0000;  aB_Lyo[4, 8] := 0.0000;

    aB_Lyo[5, 1] := 0.0015;  aB_Lyo[5, 2] := -0.0010; aB_Lyo[5, 3] := -0.0020; aB_Lyo[5, 4] := 0.0000;
    aB_Lyo[5, 5] := 0.0001;  aB_Lyo[5, 6] := 0.0000;  aB_Lyo[5, 7] := 0.0000;  aB_Lyo[5, 8] := -0.0450;

    aB_Lyo[6, 1] := 0.0080;  aB_Lyo[6, 2] := -0.0060; aB_Lyo[6, 3] := -0.0120; aB_Lyo[6, 4] := 0.0000;
    aB_Lyo[6, 5] := 0.0005;  aB_Lyo[6, 6] := 0.0000;  aB_Lyo[6, 7] := 0.0000;  aB_Lyo[6, 8] := 0.0000;

    aB_Lyo[7, 1] := 0.0005;  aB_Lyo[7, 2] := 0.0000;  aB_Lyo[7, 3] := 0.0000;  aB_Lyo[7, 4] := -0.0185;
    aB_Lyo[7, 5] := 0.0000;  aB_Lyo[7, 6] := -0.0245; aB_Lyo[7, 7] := 0.0000;  aB_Lyo[7, 8] := 0.0000;

    aB_Lyo[8, 1] := 0.0000;  aB_Lyo[8, 2] := 0.0000;  aB_Lyo[8, 3] := 0.0000;  aB_Lyo[8, 4] := -0.0150;
    aB_Lyo[8, 5] := 0.0385;  aB_Lyo[8, 6] := 0.0000;  aB_Lyo[8, 7] := 0.0000;  aB_Lyo[8, 8] := -0.0850;

    aB_Lyo[9, 1] := 0.0005;  aB_Lyo[9, 2] := 0.0000;  aB_Lyo[9, 3] := 0.0000;  aB_Lyo[9, 4] := -0.0335;
    aB_Lyo[9, 5] := 0.0385;  aB_Lyo[9, 6] := -0.0245; aB_Lyo[9, 7] := 0.0000;  aB_Lyo[9, 8] := -0.0850;

    aB_Lyo[10, 1] := 0.0008; aB_Lyo[10, 2] := 0.0000; aB_Lyo[10, 3] := 0.0000; aB_Lyo[10, 4] := -0.0450;
    aB_Lyo[10, 5] := 0.0385; aB_Lyo[10, 6] := -0.0385; aB_Lyo[10, 7] := 0.0000; aB_Lyo[10, 8] := -0.1150;

    aB_Lyo[11, 1] := 0.0000; aB_Lyo[11, 2] := 0.0000; aB_Lyo[11, 3] := 0.0000; aB_Lyo[11, 4] := 0.0000;
    aB_Lyo[11, 5] := 0.0000; aB_Lyo[11, 6] := -0.1650; aB_Lyo[11, 7] := 0.0000; aB_Lyo[11, 8] := 0.0000;

    aB_Lyo[12, 1] := 0.0000; aB_Lyo[12, 2] := 0.0000; aB_Lyo[12, 3] := 0.0000; aB_Lyo[12, 4] := 0.0000;
    aB_Lyo[12, 5] := 0.0000; aB_Lyo[12, 6] := 0.0000;  aB_Lyo[12, 7] := 0.0000; aB_Lyo[12, 8] := 0.0000;

    aB_Lyo[13, 1] := 0.0125; aB_Lyo[13, 2] := -0.0100; aB_Lyo[13, 3] := -0.0220; aB_Lyo[13, 4] := 0.0085;
    aB_Lyo[13, 5] := 0.0045; aB_Lyo[13, 6] := 0.0000;  aB_Lyo[13, 7] := 0.0000; aB_Lyo[13, 8] := 0.0000;

    aB_Lyo[14, 1] := -0.0020;aB_Lyo[14, 2] := 0.0000;  aB_Lyo[14, 3] := 0.0000;  aB_Lyo[14, 4] := -0.0015;
    aB_Lyo[14, 5] := 0.0000;  aB_Lyo[14, 6] := 0.0000;  aB_Lyo[14, 7] := 0.0000; aB_Lyo[14, 8] := 0.0000;

    aB_Lyo[15, 1] := 0.0000; aB_Lyo[15, 2] := 0.0000;  aB_Lyo[15, 3] := 0.0000;  aB_Lyo[15, 4] := 0.0000;
    aB_Lyo[15, 5] := 0.0000;  aB_Lyo[15, 6] := 0.0000;  aB_Lyo[15, 7] := 0.2850; aB_Lyo[15, 8] := 0.0000;

    aB_Lyo[16, 1] := 0.0000; aB_Lyo[16, 2] := 0.0000;  aB_Lyo[16, 3] := 0.0000;  aB_Lyo[16, 4] := 0.0000;
    aB_Lyo[16, 5] := 0.0000;  aB_Lyo[16, 6] := 0.0000;  aB_Lyo[16, 7] := 1.8500; aB_Lyo[16, 8] := 0.0000;

    (* Receding-Horizon MPC Quadratic State Weight Matrix Q (16 Diagonal Penalties) *)
    aQ_LyoDiag[1]  := 2.50;  (* Shelf Inlet Oil Temp Tracking Error Penalty *)
    aQ_LyoDiag[2]  := 2.50;  (* Shelf Outlet Oil Temp Error Penalty *)
    aQ_LyoDiag[3]  := 4.80;  (* Shelf Plate Metal Uniformity Penalty *)
    aQ_LyoDiag[4]  := 5.20;  (* Vial Bottom Base Contact Temp Penalty *)
    aQ_LyoDiag[5]  := 18.50; (* Critical Sublimation Front Temp Penalty (High weight to prevent melt/collapse) *)
    aQ_LyoDiag[6]  := 3.10;  (* Porous Cake Layer Thermal Penalty *)
    aQ_LyoDiag[7]  := 8.40;  (* Sublimated Water Vapor Partial Pressure Deviation Penalty *)
    aQ_LyoDiag[8]  := 6.20;  (* Inert Gas N2 Dosing Balance Penalty *)
    aQ_LyoDiag[9]  := 12.00; (* Total Chamber Pressure Tracking Penalty (Kv optimization) *)
    aQ_LyoDiag[10] := 4.50;  (* Pirani Apparent Vacuum Divergence Penalty *)
    aQ_LyoDiag[11] := 14.00; (* Ice Condenser Cold Trap Surface Temp Penalty (Must maintain <-75 deg C) *)
    aQ_LyoDiag[12] := 2.00;  (* Ice Layer Accumulation Penalty *)
    aQ_LyoDiag[13] := 6.50;  (* Sublimation Mass Flux Maximization *)
    aQ_LyoDiag[14] := 9.80;  (* Desorption Bound Moisture Removal Penalty *)
    aQ_LyoDiag[15] := 7.50;  (* Stoppering Ram Stroke Position Penalty *)
    aQ_LyoDiag[16] := 15.00; (* Stoppering Final Compaction Force Penalty *)

    (* Actuator Slew Rate Penalties Matrix R (8 Diagonal Penalties) *)
    aR_LyoDiag[1] := 0.22;   (* SCR Heater Duty Slew Rate Penalty *)
    aR_LyoDiag[2] := 0.35;   (* Compressor Slide Valve Modulation Slew Rate Penalty *)
    aR_LyoDiag[3] := 0.18;   (* LN2 Cryogenic Injection Valve Penalty *)
    aR_LyoDiag[4] := 0.45;   (* Roots Vacuum Blower Inverter Rate Penalty *)
    aR_LyoDiag[5] := 0.08;   (* Sterile N2 Piezo Bleed Valve Fast Modulation Penalty *)
    aR_LyoDiag[6] := 0.28;   (* Ice Condenser Direct Expansion TXV Penalty *)
    aR_LyoDiag[7] := 0.50;   (* Hydraulic Stoppering Directional Servo Rate Penalty *)
    aR_LyoDiag[8] := 0.15;   (* Nucleation Depressurization Valve Rate Penalty *)

    (* Terminal State Penalties Matrix P (16 Diagonal Penalties) *)
    aP_LyoDiag[1]  := 12.5;  aP_LyoDiag[2]  := 12.5;  aP_LyoDiag[3]  := 24.0;  aP_LyoDiag[4]  := 26.0;
    aP_LyoDiag[5]  := 95.0;  aP_LyoDiag[6]  := 15.5;  aP_LyoDiag[7]  := 42.0;  aP_LyoDiag[8]  := 31.0;
    aP_LyoDiag[9]  := 60.0;  aP_LyoDiag[10] := 22.5;  aP_LyoDiag[11] := 70.0;  aP_LyoDiag[12] := 10.0;
    aP_LyoDiag[13] := 32.5;  aP_LyoDiag[14] := 49.0;  aP_LyoDiag[15] := 37.5;  aP_LyoDiag[16] := 75.0;

    (* Actuator Slew Rate Dynamic Limits [%/s] *)
    aActuatorSlewRateLimit[1] := 5.0;   (* SCR Heater max 5.0 %/s *)
    aActuatorSlewRateLimit[2] := 2.5;   (* Screw Compressor Slide max 2.5 %/s *)
    aActuatorSlewRateLimit[3] := 10.0;  (* LN2 Booster valve max 10.0 %/s *)
    aActuatorSlewRateLimit[4] := 4.0;   (* Roots Blower VFD max 4.0 %/s *)
    aActuatorSlewRateLimit[5] := 15.0;  (* N2 Piezo Bleed valve max 15.0 %/s *)
    aActuatorSlewRateLimit[6] := 5.0;   (* Condenser TXV max 5.0 %/s *)
    aActuatorSlewRateLimit[7] := 8.0;   (* Hydraulic Stoppering Servo max 8.0 %/s *)
    aActuatorSlewRateLimit[8] := 50.0;  (* Nucleation Pulse valve fast opening *)

    (* Actuator Physical Saturation Lower & Upper Limits [%] *)
    FOR nInputIdx := 1 TO 8 DO
        aActuatorLowerLimit[nInputIdx] := 0.0;
        aActuatorUpperLimit[nInputIdx] := 100.0;
        au_LyoPrevious[nInputIdx] := 0.0;
        au_LyoInput[nInputIdx] := 0.0;
    END_FOR;

    bFirstScanInitDone := TRUE;
END_IF;
"""

print("generate_phase0 loaded.")
