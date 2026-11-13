# Phase 0 Builder for FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration
import os, sys

def get_phase0_code():
    lines = []
    lines.append("""(*
====================================================================================================
PHASE 0: ONE-SHOT FIRST-SCAN SYSTEM INITIALIZATION & CYBER-PHYSICAL MATRIX ALLOCATION
Sampling Period Ts = 0.010 [s] (10.0 [ms]), Downstream mAb Ultrafiltration / Diafiltration Skid
30 kDa Regenerated Cellulose Membrane Cassettes, Area = 10.0 [m2], Channel Height = 0.5 [mm]
State Vector: x = [TMP, J_flux, C_ret, Rg_gel, gamma_w, DV_count, T_ret, delta_M_sump]^T
Actuator Vector: u = [N_feed_pump, V_ret_valve, N_buf_pump, V_perm_valve, V_chiller, V_divert]^T
Output Vector: y = [TMP_meas, J_meas, C_meas, Q_feed_meas, T_meas, delta_M_meas]^T
====================================================================================================
*)
IF NOT bFirstScanDone THEN
    (* ---------------------------------------------------------------------------------------------
     * 1. Discrete System Plant Transition Matrix arrA_Matrix (8x8)
     * Continuous-time linearized Jacobian Ad = exp(Ac * Ts) discretized at Ts = 0.010 [s]
     * --------------------------------------------------------------------------------------------- *)
    (* Row 1: Transmembrane Pressure Dynamics x1 (TMP) [bar] *)
    arrA_Matrix[1, 1] := 0.965420;  (* Intrinsic hydraulic pressure relaxation and cassette fluid compliance *)
    arrA_Matrix[1, 2] := -0.008450; (* Permeate filtrate flux backpressure relief factor *)
    arrA_Matrix[1, 3] := 0.001820;  (* Retentate fluid viscosity elevation induced feed-channel pressure drop *)
    arrA_Matrix[1, 4] := 0.000640;  (* Gel layer polarization hydrodynamic hydraulic flow resistance coupling *)
    arrA_Matrix[1, 5] := 0.000015;  (* High wall shear cross-flow momentum coupling to channel pressure *)
    arrA_Matrix[1, 6] := 0.000000;  (* Diafiltration volume counter decoupling *)
    arrA_Matrix[1, 7] := -0.000350; (* Fluid viscosity thermal reduction coefficient (-0.02 cP/degC) *)
    arrA_Matrix[1, 8] := 0.000000;  (* Sump scale mass balance decoupling *)

    (* Row 2: Permeate Volumetric Flux Dynamics x2 (J_flux) [L/m2/h LMH] *)
    arrA_Matrix[2, 1] := 0.285400;  (* Darcy hydraulic driving force: dJ/dTMP = 1 / (mu * (Rm + Rg)) *)
    arrA_Matrix[2, 2] := 0.942150;  (* Intrinsic boundary layer mass transfer retention & concentration decay *)
    arrA_Matrix[2, 3] := -0.048200; (* Osmotic pressure back-potential and concentration polarization retarding *)
    arrA_Matrix[2, 4] := -0.038400; (* Secondary protein gel layer hydraulic resistance fouling degradation *)
    arrA_Matrix[2, 5] := 0.001250;  (* Boundary layer shear sweep-off and back-diffusion enhancement *)
    arrA_Matrix[2, 6] := 0.000000;  (* Diafiltration exchange volume counter independence *)
    arrA_Matrix[2, 7] := 0.018500;  (* Fluid temperature increase permeate flux enhancement (viscosity drop) *)
    arrA_Matrix[2, 8] := 0.000000;  (* Sump scale deviation decoupling *)

    (* Row 3: Retentate Monoclonal Antibody Concentration x3 (C_ret) [g/L] *)
    arrA_Matrix[3, 1] := 0.000000;  (* TMP direct mass balance decoupling *)
    arrA_Matrix[3, 2] := 0.012450;  (* Volume reduction concentration rate: dC/dt = (J * A_mem / V_ret) * C *)
    arrA_Matrix[3, 3] := 0.998850;  (* Bulk solute mass conservation retention (mAb rejection coefficient R > 99.8%) *)
    arrA_Matrix[3, 4] := 0.000000;  (* Gel layer resistance indirect coupling *)
    arrA_Matrix[3, 5] := 0.000000;  (* Shear rate direct mass balance decoupling *)
    arrA_Matrix[3, 6] := -0.000450; (* Diafiltration buffer dilution displacement damping *)
    arrA_Matrix[3, 7] := 0.000000;  (* Temperature mass conservation decoupling *)
    arrA_Matrix[3, 8] := -0.000085; (* Sump mass deviation retentate fluid volume dilution effect *)

    (* Row 4: Membrane Gel Polarization Resistance x4 (Rg_gel) [10^11 m-1] *)
    arrA_Matrix[4, 1] := 0.004200;  (* Pressure-driven solute convective deposition flux: J * C_wall *)
    arrA_Matrix[4, 2] := 0.024500;  (* Permeate flux convective drag force accumulating surface protein cake *)
    arrA_Matrix[4, 3] := 0.018200;  (* Bulk protein concentration driving boundary layer wall concentration *)
    arrA_Matrix[4, 4] := 0.984500;  (* Gel layer structural compaction and persistence retention *)
    arrA_Matrix[4, 5] := -0.005850; (* Retentate channel cross-flow wall shear hydrodynamic scour rate *)
    arrA_Matrix[4, 6] := -0.001200; (* Buffer salt/osmolyte exchange induced gel layer relaxation *)
    arrA_Matrix[4, 7] := -0.002100; (* Thermal kinetic protein solubility enhancement & gel desorption *)
    arrA_Matrix[4, 8] := 0.000000;  (* Sump scale deviation decoupling *)

    (* Row 5: Retentate Flow Channel Wall Shear Rate x5 (gamma_w) [s-1] *)
    arrA_Matrix[5, 1] := 0.085000;  (* Channel differential pressure gradient cross-flow acceleration *)
    arrA_Matrix[5, 2] := 0.000000;  (* Permeate flux cross-flow velocity decoupling *)
    arrA_Matrix[5, 3] := -0.450000; (* Viscosity elevation velocity profile blunting (shear rate reduction) *)
    arrA_Matrix[5, 4] := 0.000000;  (* Gel layer thickness negligible boundary obstruction *)
    arrA_Matrix[5, 5] := 0.952100;  (* Intrinsic hydraulic fluid inertia momentum decay in narrow slit channel *)
    arrA_Matrix[5, 6] := 0.000000;  (* Diafiltration counter decoupling *)
    arrA_Matrix[5, 7] := 0.125000;  (* Temperature fluid thinning velocity gradient steepening *)
    arrA_Matrix[5, 8] := 0.000000;  (* Sump scale deviation decoupling *)

    (* Row 6: Diafiltration Buffer Volume Exchange Counter x6 (DV) [-] *)
    arrA_Matrix[6, 1] := 0.000000;  (* TMP direct decoupling *)
    arrA_Matrix[6, 2] := 0.000028;  (* Permeate filtrate removal accumulation rate into DV counter *)
    arrA_Matrix[6, 3] := 0.000000;  (* Solute concentration decoupling *)
    arrA_Matrix[6, 4] := 0.000000;  (* Gel resistance decoupling *)
    arrA_Matrix[6, 5] := 0.000000;  (* Shear rate decoupling *)
    arrA_Matrix[6, 6] := 1.000000;  (* Pure non-leaking mathematical discrete integrator pole (z = 1.0) *)
    arrA_Matrix[6, 7] := 0.000000;  (* Thermal decoupling *)
    arrA_Matrix[6, 8] := 0.000000;  (* Sump scale deviation decoupling *)

    (* Row 7: Retentate Recirculation Loop Process Temperature x7 (T_ret) [deg C] *)
    arrA_Matrix[7, 1] := 0.000450;  (* Hydraulic pump throttling viscous pressure drop dissipation *)
    arrA_Matrix[7, 2] := 0.000000;  (* Permeate mass extraction thermal loss *)
    arrA_Matrix[7, 3] := 0.000850;  (* Elevated protein viscosity increasing viscous shear power dissipation *)
    arrA_Matrix[7, 4] := 0.000000;  (* Gel resistance decoupling *)
    arrA_Matrix[7, 5] := 0.000120;  (* High shear laminar friction viscous heat generation *)
    arrA_Matrix[7, 6] := 0.000000;  (* DV counter decoupling *)
    arrA_Matrix[7, 7] := 0.988200;  (* Skid thermal retention and ambient convective dissipation *)
    arrA_Matrix[7, 8] := 0.000000;  (* Sump mass scale decoupling *)

    (* Row 8: Diafiltration Sump Mass Balance Scale Weight Deviation x8 (delta_M_sump) [g] *)
    arrA_Matrix[8, 1] := 0.000000;  (* TMP decoupling *)
    arrA_Matrix[8, 2] := -0.027800; (* Permeate extraction mass loss rate from retentate vessel (-g/s) *)
    arrA_Matrix[8, 3] := 0.000000;  (* Solute concentration decoupling *)
    arrA_Matrix[8, 4] := 0.000000;  (* Gel resistance decoupling *)
    arrA_Matrix[8, 5] := 0.000000;  (* Shear rate decoupling *)
    arrA_Matrix[8, 6] := 0.000000;  (* DV counter decoupling *)
    arrA_Matrix[8, 7] := 0.000000;  (* Temperature thermal expansion negligible *)
    arrA_Matrix[8, 8] := 0.999500;  (* Mass balance error integral persistence *)

    (* ---------------------------------------------------------------------------------------------
     * 2. Discrete Plant Actuator Input Coupling Matrix arrB_Matrix (8x6)
     * Actuators: u1=FeedPump[rpm], u2=RetValve[%], u3=BufPump[%], u4=PermValve[%], u5=Chiller[%], u6=Divert[%]
     * --------------------------------------------------------------------------------------------- *)
    (* State 1: Transmembrane Pressure TMP [bar] *)
    arrB_Matrix[1, 1] := 0.000850;  (* Feed pump speed boost raises cassette inlet feed pressure *)
    arrB_Matrix[1, 2] := -0.028500; (* Retentate valve opening reduces backpressure, dropping TMP *)
    arrB_Matrix[1, 3] := 0.000020;  (* Buffer addition pump minor hydraulic influx *)
    arrB_Matrix[1, 4] := -0.012500; (* Permeate control valve opening reduces permeate backpressure *)
    arrB_Matrix[1, 5] := 0.000000;  (* Chiller valve hydraulic decoupling *)
    arrB_Matrix[1, 6] := -0.035000; (* Product divert valve dump drops loop pressure immediately *)

    (* State 2: Permeate Volumetric Flux J_flux [L/m2/h LMH] *)
    arrB_Matrix[2, 1] := 0.015200;  (* Feed pump speed boost increases cross-flow driving permeate flux *)
    arrB_Matrix[2, 2] := -0.245000; (* Retentate valve opening lowers TMP, thereby reducing permeate flux *)
    arrB_Matrix[2, 3] := 0.000000;  (* Buffer metering pump decoupling *)
    arrB_Matrix[2, 4] := 0.385000;  (* Permeate modulating valve directly opens filtrate line flow *)
    arrB_Matrix[2, 5] := -0.004500; (* Chiller cooling increases fluid viscosity, slight flux reduction *)
    arrB_Matrix[2, 6] := -0.150000; (* Divert valve opening depressurizes cassette and halts flux *)

    (* State 3: Retentate mAb Concentration C_ret [g/L] *)
    arrB_Matrix[3, 1] := 0.000000;  (* Feed pump speed mass conservation decoupling *)
    arrB_Matrix[3, 2] := 0.000000;  (* Retentate valve mass conservation decoupling *)
    arrB_Matrix[3, 3] := -0.008500; (* Buffer addition pump adds pure buffer, diluting concentration *)
    arrB_Matrix[3, 4] := 0.002800;  (* Permeate valve opening removes solvent, increasing concentration *)
    arrB_Matrix[3, 5] := 0.000000;  (* Chiller valve decoupling *)
    arrB_Matrix[3, 6] := 0.000000;  (* Divert valve removes bulk solution without altering concentration *)

    (* State 4: Membrane Gel Polarization Resistance Rg_gel [10^11 m-1] *)
    arrB_Matrix[4, 1] := -0.003500; (* Feed pump shear rate boost scours and erodes gel layer *)
    arrB_Matrix[4, 2] := 0.018500;  (* Retentate valve throttle increases TMP, packing protein gel cake *)
    arrB_Matrix[4, 3] := -0.000850; (* Fresh buffer wash clears loosely bound polarized protein *)
    arrB_Matrix[4, 4] := 0.012500;  (* Permeate valve opening increases convective solute drag to wall *)
    arrB_Matrix[4, 5] := 0.000450;  (* Chiller cooling decreases protein solubility, promoting gel layer *)
    arrB_Matrix[4, 6] := 0.000000;  (* Divert valve decoupling *)

    (* State 5: Retentate Flow Channel Wall Shear Rate gamma_w [s-1] *)
    arrB_Matrix[5, 1] := 4.250000;  (* Feed pump VFD speed directly drives channel volumetric cross-flow *)
    arrB_Matrix[5, 2] := 18.50000;  (* Retentate valve opening reduces downstream restriction, boosting flow *)
    arrB_Matrix[5, 3] := 0.000000;  (* Buffer metering pump decoupling *)
    arrB_Matrix[5, 4] := -0.850000; (* Permeate extraction diverts slight fluid from retentate stream *)
    arrB_Matrix[5, 5] := 0.000000;  (* Chiller valve decoupling *)
    arrB_Matrix[5, 6] := 25.00000;  (* Divert valve open drops restriction, surging cross-flow *)

    (* State 6: Diafiltration Buffer Volume Counter DV [-] *)
    arrB_Matrix[6, 1] := 0.000000;  (* Feed pump decoupling *)
    arrB_Matrix[6, 2] := 0.000000;  (* Retentate valve decoupling *)
    arrB_Matrix[6, 3] := 0.000045;  (* Buffer metering pump stroke increments cumulative volume counter *)
    arrB_Matrix[6, 4] := 0.000000;  (* Permeate valve decoupling *)
    arrB_Matrix[6, 5] := 0.000000;  (* Chiller valve decoupling *)
    arrB_Matrix[6, 6] := 0.000000;  (* Divert valve decoupling *)

    (* State 7: Retentate Recirculation Loop Process Temperature T_ret [deg C] *)
    arrB_Matrix[7, 1] := 0.001850;  (* Feed pump mechanical impeller dissipation into process fluid *)
    arrB_Matrix[7, 2] := -0.000450; (* Valve throttling frictional dissipation factor *)
    arrB_Matrix[7, 3] := -0.002500; (* Cold formulation buffer addition thermal cooling influx *)
    arrB_Matrix[7, 4] := 0.000000;  (* Permeate valve decoupling *)
    arrB_Matrix[7, 5] := -0.045000; (* Heat exchanger chiller glycol valve strong negative cooling gain *)
    arrB_Matrix[7, 6] := 0.000000;  (* Divert valve decoupling *)

    (* State 8: Diafiltration Sump Mass Balance Weight Deviation delta_M_sump [g] *)
    arrB_Matrix[8, 1] := 0.000000;  (* Feed pump decoupling *)
    arrB_Matrix[8, 2] := 0.000000;  (* Retentate valve decoupling *)
    arrB_Matrix[8, 3] := 0.278000;  (* Buffer metering pump adds mass to retentate sump (+g/s) *)
    arrB_Matrix[8, 4] := -0.278000; (* Permeate control valve extracts filtrate mass from sump (-g/s) *)
    arrB_Matrix[8, 5] := 0.000000;  (* Chiller valve decoupling *)
    arrB_Matrix[8, 6] := 0.000000;  (* Divert valve decoupling *)

    (* ---------------------------------------------------------------------------------------------
     * 3. Discrete Sensor Measurement Output Matrix arrC_Matrix (6x8)
     * Sensor Outputs: y1=TMP[bar], y2=J[LMH], y3=UV_Conc[g/L], y4=Q_feed[L/h], y5=Temp[degC], y6=delta_M[g]
     * --------------------------------------------------------------------------------------------- *)
    (* Measurement 1: Transmembrane Pressure TMP [bar] *)
    arrC_Matrix[1, 1] := 1.000000;  (* Direct physical identity mapping to State 1 *)
    arrC_Matrix[1, 2] := 0.000000;
    arrC_Matrix[1, 3] := 0.000000;
    arrC_Matrix[1, 4] := 0.000000;
    arrC_Matrix[1, 5] := 0.000000;
    arrC_Matrix[1, 6] := 0.000000;
    arrC_Matrix[1, 7] := 0.000000;
    arrC_Matrix[1, 8] := 0.000000;

    (* Measurement 2: Permeate Volumetric Flux J_flux [L/m2/h LMH] *)
    arrC_Matrix[2, 1] := 0.000000;
    arrC_Matrix[2, 2] := 1.000000;  (* Direct physical identity mapping to State 2 *)
    arrC_Matrix[2, 3] := 0.000000;
    arrC_Matrix[2, 4] := 0.000000;
    arrC_Matrix[2, 5] := 0.000000;
    arrC_Matrix[2, 6] := 0.000000;
    arrC_Matrix[2, 7] := 0.000000;
    arrC_Matrix[2, 8] := 0.000000;

    (* Measurement 3: Inline UV-Vis 280 nm Protein Concentration [g/L] *)
    arrC_Matrix[3, 1] := 0.000000;
    arrC_Matrix[3, 2] := 0.000000;
    arrC_Matrix[3, 3] := 1.000000;  (* Beer-Lambert extinction mapping to State 3 *)
    arrC_Matrix[3, 4] := 0.000000;
    arrC_Matrix[3, 5] := 0.000000;
    arrC_Matrix[3, 6] := 0.000000;
    arrC_Matrix[3, 7] := 0.000000;
    arrC_Matrix[3, 8] := 0.000000;

    (* Measurement 4: Feed Recirculation Coriolis Mass Flow Rate [L/h] *)
    arrC_Matrix[4, 1] := 0.000000;
    arrC_Matrix[4, 2] := 0.000000;
    arrC_Matrix[4, 3] := 0.000000;
    arrC_Matrix[4, 4] := 0.000000;
    arrC_Matrix[4, 5] := 0.098500;  (* Hydrodynamic conversion from Wall Shear Rate to Volumetric Flow [L/h] *)
    arrC_Matrix[4, 6] := 0.000000;
    arrC_Matrix[4, 7] := 0.000000;
    arrC_Matrix[4, 8] := 0.000000;

    (* Measurement 5: Retentate Process Temperature [deg C] *)
    arrC_Matrix[5, 1] := 0.000000;
    arrC_Matrix[5, 2] := 0.000000;
    arrC_Matrix[5, 3] := 0.000000;
    arrC_Matrix[5, 4] := 0.000000;
    arrC_Matrix[5, 5] := 0.000000;
    arrC_Matrix[5, 6] := 0.000000;
    arrC_Matrix[5, 7] := 1.000000;  (* Direct physical identity mapping to State 7 *)
    arrC_Matrix[5, 8] := 0.000000;

    (* Measurement 6: Diafiltration Sump Mass Scale Weight Deviation [g] *)
    arrC_Matrix[6, 1] := 0.000000;
    arrC_Matrix[6, 2] := 0.000000;
    arrC_Matrix[6, 3] := 0.000000;
    arrC_Matrix[6, 4] := 0.000000;
    arrC_Matrix[6, 5] := 0.000000;
    arrC_Matrix[6, 6] := 0.000000;
    arrC_Matrix[6, 7] := 0.000000;
    arrC_Matrix[6, 8] := 1.000000;  (* Direct physical identity mapping to State 8 *)

    (* ---------------------------------------------------------------------------------------------
     * 4. Discrete Direct Actuator Feedthrough Matrix arrD_Matrix (6x6)
     * Strictly strictly proper physical dynamics with minor high-frequency hydrodynamic feedthrough
     * --------------------------------------------------------------------------------------------- *)
    FOR iLoopIndex := 1 TO 6 DO
        FOR jLoopIndex := 1 TO 6 DO
            arrD_Matrix[iLoopIndex, jLoopIndex] := 0.000000;
        END_FOR;
    END_FOR;
    arrD_Matrix[1, 1] := 0.000120;  (* Instantaneous hydraulic pressure pulse from diaphragm stroke *)
    arrD_Matrix[4, 1] := 0.155000;  (* Direct positive displacement pump flow response on Coriolis meter *)

    (* ---------------------------------------------------------------------------------------------
     * 5. Steady-State Luenberger Observer Innovation Matrix arrL_Gain (8x6)
     * Optimal Kalman filter innovation gain matrix balancing plant covariance W and sensor noise V
     * --------------------------------------------------------------------------------------------- *)
    (* Correction for State 1: TMP [bar] *)
    arrL_Gain[1, 1] := 0.385000;   arrL_Gain[1, 2] := -0.012500;  arrL_Gain[1, 3] := 0.000000;
    arrL_Gain[1, 4] := 0.000450;   arrL_Gain[1, 5] := -0.000850;  arrL_Gain[1, 6] := 0.000000;

    (* Correction for State 2: Permeate Flux J_flux [LMH] *)
    arrL_Gain[2, 1] := 0.045000;   arrL_Gain[2, 2] := 0.425000;   arrL_Gain[2, 3] := -0.008500;
    arrL_Gain[2, 4] := 0.001200;   arrL_Gain[2, 5] := 0.002400;   arrL_Gain[2, 6] := 0.000000;

    (* Correction for State 3: Retentate mAb Concentration C_ret [g/L] *)
    arrL_Gain[3, 1] := 0.000000;   arrL_Gain[3, 2] := 0.018500;   arrL_Gain[3, 3] := 0.315000;
    arrL_Gain[3, 4] := 0.000000;   arrL_Gain[3, 5] := 0.000000;   arrL_Gain[3, 6] := -0.000450;

    (* Correction for State 4: Gel Polarization Resistance Rg_gel [10^11 m-1] *)
    arrL_Gain[4, 1] := 0.014200;   arrL_Gain[4, 2] := -0.085000;  arrL_Gain[4, 3] := 0.024000;
    arrL_Gain[4, 4] := -0.000850;  arrL_Gain[4, 5] := -0.001500;  arrL_Gain[4, 6] := 0.000000;

    (* Correction for State 5: Retentate Wall Shear Rate gamma_w [s-1] *)
    arrL_Gain[5, 1] := 0.125000;   arrL_Gain[5, 2] := 0.000000;   arrL_Gain[5, 3] := -0.450000;
    arrL_Gain[5, 4] := 4.850000;   arrL_Gain[5, 5] := 0.000000;   arrL_Gain[5, 6] := 0.000000;

    (* Correction for State 6: Diafiltration Buffer Volume Counter DV [-] *)
    arrL_Gain[6, 1] := 0.000000;   arrL_Gain[6, 2] := 0.000015;   arrL_Gain[6, 3] := 0.000000;
    arrL_Gain[6, 4] := 0.000000;   arrL_Gain[6, 5] := 0.000000;   arrL_Gain[6, 6] := 0.000000;

    (* Correction for State 7: Retentate Process Temperature T_ret [deg C] *)
    arrL_Gain[7, 1] := 0.000250;   arrL_Gain[7, 2] := 0.000000;   arrL_Gain[7, 3] := 0.000000;
    arrL_Gain[7, 4] := 0.000000;   arrL_Gain[7, 5] := 0.365000;   arrL_Gain[7, 6] := 0.000000;

    (* Correction for State 8: Sump Mass Balance Scale Weight Deviation delta_M_sump [g] *)
    arrL_Gain[8, 1] := 0.000000;   arrL_Gain[8, 2] := -0.015000;  arrL_Gain[8, 3] := 0.000000;
    arrL_Gain[8, 4] := 0.000000;   arrL_Gain[8, 5] := 0.000000;   arrL_Gain[8, 6] := 0.450000;

    (* ---------------------------------------------------------------------------------------------
     * 6. MPC State Quadratic Penalty Weight Matrix arrQ_Weight (8x8)
     * Heavy penalties on TMP overshoots, protein shear stress, and temperature excursions
     * --------------------------------------------------------------------------------------------- *)
    FOR iLoopIndex := 1 TO 8 DO
        FOR jLoopIndex := 1 TO 8 DO
            arrQ_Weight[iLoopIndex, jLoopIndex] := 0.000000;
        END_FOR;
    END_FOR;
    arrQ_Weight[1, 1] := 85.00000;  (* Transmembrane pressure tight tracking weight *)
    arrQ_Weight[2, 2] := 45.00000;  (* Permeate volumetric flux optimization weight *)
    arrQ_Weight[3, 3] := 120.0000;  (* Retentate protein concentration precision target weight *)
    arrQ_Weight[4, 4] := 35.00000;  (* Membrane fouling / gel polarization suppression weight *)
    arrQ_Weight[5, 5] := 0.025000;  (* Channel wall shear rate maintenance weight *)
    arrQ_Weight[6, 6] := 250.0000;  (* Diafiltration buffer exchange volume precision weight *)
    arrQ_Weight[7, 7] := 150.0000;  (* Temperature regulation penalty (protein stability protection) *)
    arrQ_Weight[8, 8] := 18.50000;  (* Sump scale mass balance deviation penalty *)

    (* ---------------------------------------------------------------------------------------------
     * 7. MPC Actuator Effort & Slew Penalty Matrix arrR_Weight (6x6)
     * Penalizes valve hunting and abrupt pump speed changes to prevent pressure hammer
     * --------------------------------------------------------------------------------------------- *)
    FOR iLoopIndex := 1 TO 6 DO
        FOR jLoopIndex := 1 TO 6 DO
            arrR_Weight[iLoopIndex, jLoopIndex] := 0.000000;
        END_FOR;
    END_FOR;
    arrR_Weight[1, 1] := 0.015000;  (* Feed pump VFD speed slew penalty *)
    arrR_Weight[2, 2] := 1.250000;  (* Retentate pinch/diaphragm valve movement penalty *)
    arrR_Weight[3, 3] := 0.850000;  (* Buffer metering pump stroke modulation penalty *)
    arrR_Weight[4, 4] := 1.500000;  (* Permeate modulating valve wear penalty *)
    arrR_Weight[5, 5] := 0.650000;  (* Chiller glycol valve hunting penalty *)
    arrR_Weight[6, 6] := 10.00000;  (* Product divert valve safety state penalty *)

    (* ---------------------------------------------------------------------------------------------
     * 8. MPC Terminal State Cost-To-Go Matrix arrP_Terminal (8x8)
     * Algebraic Riccati Equation steady-state terminal cost solution for infinite-horizon stability
     * --------------------------------------------------------------------------------------------- *)
    FOR iLoopIndex := 1 TO 8 DO
        FOR jLoopIndex := 1 TO 8 DO
            arrP_Terminal[iLoopIndex, jLoopIndex] := 0.000000;
        END_FOR;
    END_FOR;
    arrP_Terminal[1, 1] := 145.2000; (* Terminal TMP stability Riccati weight *)
    arrP_Terminal[2, 2] := 82.50000; (* Terminal flux stability Riccati weight *)
    arrP_Terminal[3, 3] := 285.0000; (* Terminal protein concentration Riccati weight *)
    arrP_Terminal[4, 4] := 55.00000; (* Terminal gel resistance Riccati weight *)
    arrP_Terminal[5, 5] := 0.055000; (* Terminal wall shear Riccati weight *)
    arrP_Terminal[6, 6] := 450.0000; (* Terminal diafiltration volume Riccati weight *)
    arrP_Terminal[7, 7] := 320.0000; (* Terminal temperature Riccati weight *)
    arrP_Terminal[8, 8] := 38.00000; (* Terminal sump mass balance Riccati weight *)

    (* ---------------------------------------------------------------------------------------------
     * 9. Actuator Saturation Clamps and Maximum Dynamic Slew Rate Limits
     * --------------------------------------------------------------------------------------------- *)
    (* Actuator 1: Feed Quaternary Diaphragm Pump [rpm] *)
    arrU_Min[1] := 0.0;
    arrU_Max[1] := 3000.0;
    arrDeltaU_Max[1] := 35.0;       (* Max slew: 35.0 [rpm] per 10 ms cycle = 3,500 [rpm/s] ramp *)

    (* Actuator 2: Retentate Proportional Backpressure Valve [%] *)
    arrU_Min[2] := 0.0;
    arrU_Max[2] := 100.0;
    arrDeltaU_Max[2] := 1.5;        (* Max slew: 1.5% per 10 ms cycle = 150 [%/s] *)

    (* Actuator 3: Diafiltration Buffer Metering Pump [%] *)
    arrU_Min[3] := 0.0;
    arrU_Max[3] := 100.0;
    arrDeltaU_Max[3] := 2.0;        (* Max slew: 2.0% per 10 ms cycle *)

    (* Actuator 4: Permeate Sanitary Modulating Valve [%] *)
    arrU_Min[4] := 0.0;
    arrU_Max[4] := 100.0;
    arrDeltaU_Max[4] := 2.5;        (* Max slew: 2.5% per 10 ms cycle *)

    (* Actuator 5: Chiller Glycol Modulating Valve [%] *)
    arrU_Min[5] := 0.0;
    arrU_Max[5] := 100.0;
    arrDeltaU_Max[5] := 1.0;        (* Max slew: 1.0% per 10 ms cycle *)

    (* Actuator 6: Product Divert / Drain 3-Way Valve [%] *)
    arrU_Min[6] := 0.0;
    arrU_Max[6] := 100.0;
    arrDeltaU_Max[6] := 10.0;       (* Rapid pneumatic switching: 10.0% per cycle *)

    (* Initialize State Vectors to Safe Quiescent Operating State *)
    arrX_State[1] := 0.0;   (* Initial TMP: 0.0 [bar] *)
    arrX_State[2] := 0.0;   (* Initial Permeate Flux: 0.0 [LMH] *)
    arrX_State[3] := 10.0;  (* Initial Feed mAb Concentration: 10.0 [g/L] *)
    arrX_State[4] := 0.15;  (* Initial Clean Membrane Hydraulic Resistance: 0.15 [10^11 m-1] *)
    arrX_State[5] := 0.0;   (* Initial Wall Shear Rate: 0.0 [s-1] *)
    arrX_State[6] := 0.0;   (* Initial Diafiltration Counter: 0.0 [DV] *)
    arrX_State[7] := 18.0;  (* Ambient Starting Temperature: 18.0 [deg C] *)
    arrX_State[8] := 0.0;   (* Initial Sump Scale Mass Balance Deviation: 0.0 [g] *)

    FOR iLoopIndex := 1 TO 6 DO
        arrU_Act[iLoopIndex] := 0.0;
        arrU_Prev[iLoopIndex] := 0.0;
        arrU_Ref[iLoopIndex] := 0.0;
    END_FOR;

    bFirstScanDone := TRUE;
END_IF;""")

    return "\n".join(lines)

print("Phase 0 builder ready")
