# ammonia_refrigeration_builder/build_st_matrices.py

def get_matrices_initialization():
    return """(* ==================================================================================================================== *)
(* PHASE 0: ONE-SHOT FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE & MPC MATRIX INITIALIZATION                            *)
(* ==================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* 0.1: DISCRETE STATE TRANSITION MATRIX matA (8x8) @ Sample Time dt = 100 ms                                       *)
    (* States: x1=dP_suct, x2=dh_suct, x3=dP_disch, x4=dT_disch, x5=dT_oil, x6=dP_eco, x7=dT_sump, x8=dSH_suct          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    matA[1, 1] := 0.9620; (* Suction header pressure self-decay due to suction plenum accumulator acoustic damping *)
    matA[1, 2] := 0.0015; (* Suction vapor specific enthalpy coupling to suction pressure via ideal gas relation *)
    matA[1, 3] := 0.0008; (* Discharge pressure back-leakage past screw rotor contact mesh seals *)
    matA[1, 4] := 0.0000; (* Discharge temperature decoupling *)
    matA[1, 5] := 0.0002; (* Oil sump temperature heat conduction to suction port housing *)
    matA[1, 6] := 0.0045; (* Economizer port vapor migration into intermediate rotor flutes *)
    matA[1, 7] := 0.0000; (* Condenser sump decoupling *)
    matA[1, 8] := -0.0020; (* Suction superheat increase causing gas rarefaction & pressure drop *)

    matA[2, 1] := 0.0450; (* Pressure change Joule-Thomson expansion effect on suction enthalpy *)
    matA[2, 2] := 0.9480; (* Vapor enthalpy convective thermal dissipation decay rate *)
    matA[2, 3] := 0.0000; (* Discharge pressure decoupling *)
    matA[2, 4] := 0.0010; (* Heat conduction across compressor casing to inlet suction gas *)
    matA[2, 5] := 0.0025; (* Hot lubricating oil heat transfer to suction gas stream *)
    matA[2, 6] := 0.0120; (* Economizer subcooler vapor injection enthalpy blending *)
    matA[2, 7] := 0.0000; (* Condenser sump decoupling *)
    matA[2, 8] := 0.0850; (* Suction superheat directly driving specific enthalpy rise [kJ/(kg*K)] *)

    matA[3, 1] := 0.0120; (* Suction pressure mass flow supply feedforward to discharge line *)
    matA[3, 2] := 0.0020; (* Enthalpy density coupling *)
    matA[3, 3] := 0.9510; (* Discharge header pressure self-decay from condenser tube bundle friction *)
    matA[3, 4] := 0.0035; (* Discharge vapor thermal expansion effect on manifold pressure *)
    matA[3, 5] := 0.0005; (* Oil separator thermal mass capacitance *)
    matA[3, 6] := 0.0080; (* Economizer vapor supplementary mass contribution to discharge pressure *)
    matA[3, 7] := 0.0180; (* Evaporative condenser basin temperature driving condensing pressure equilibrium *)
    matA[3, 8] := 0.0000; (* Suction superheat decoupling *)

    matA[4, 1] := -0.0520; (* Higher suction pressure lowers isentropic compression ratio and discharge temp *)
    matA[4, 2] := 0.0210; (* Higher inlet vapor enthalpy raises compressor discharge gas temperature *)
    matA[4, 3] := 0.0680; (* Higher discharge pressure increases adiabatic heat of compression *)
    matA[4, 4] := 0.9250; (* Discharge gas temperature convective self-dissipation to cooling oil spray *)
    matA[4, 5] := 0.0450; (* Injected oil temperature directly governing twin-screw discharge gas temp *)
    matA[4, 6] := -0.0180; (* Economizer port vapor injection providing interstage cooling quench *)
    matA[4, 7] := 0.0050; (* Ambient thermal coupling *)
    matA[4, 8] := 0.0750; (* Higher suction superheat propagates directly into elevated discharge temp *)

    matA[5, 1] := 0.0000; (* Suction pressure decoupling *)
    matA[5, 2] := 0.0010; (* Minor enthalpy conduction *)
    matA[5, 3] := 0.0040; (* Oil solubility equilibrium variation with separator discharge pressure *)
    matA[5, 4] := 0.0580; (* Discharge gas intimate contact with oil separator coalescer elements *)
    matA[5, 5] := 0.9720; (* High-mass oil sump thermal capacitance retention (slow thermal time constant) *)
    matA[5, 6] := 0.0000; (* Economizer decoupling *)
    matA[5, 7] := 0.0020; (* Secondary cooling loop feedback *)
    matA[5, 8] := 0.0000; (* Suction superheat decoupling *)

    matA[6, 1] := 0.0080; (* Suction pressure acoustic reflection to economizer vessel *)
    matA[6, 2] := 0.0000; (* Enthalpy decoupling *)
    matA[6, 3] := 0.0150; (* Condenser liquid supply pressure driving economizer EEV feed *)
    matA[6, 4] := 0.0000; (* Discharge temp decoupling *)
    matA[6, 5] := 0.0000; (* Oil temp decoupling *)
    matA[6, 6] := 0.9380; (* Economizer intermediate vessel vapor pressure self-damping *)
    matA[6, 7] := 0.0040; (* Condenser subcooling variation *)
    matA[6, 8] := 0.0000; (* Superheat decoupling *)

    matA[7, 1] := 0.0000; (* Suction pressure decoupling *)
    matA[7, 2] := 0.0000; (* Enthalpy decoupling *)
    matA[7, 3] := 0.0240; (* Condenser heat rejection load heating evaporative basin water *)
    matA[7, 4] := 0.0150; (* High discharge superheat de-superheating thermal transfer to sump water *)
    matA[7, 5] := 0.0000; (* Oil decoupling *)
    matA[7, 6] := 0.0000; (* Economizer decoupling *)
    matA[7, 7] := 0.9850; (* Evaporative cooling sump thermal mass thermal inertia (large water volume) *)
    matA[7, 8] := 0.0000; (* Superheat decoupling *)

    matA[8, 1] := -0.0350; (* Rapid suction pressure drop flashes liquid drops, momentarily reducing superheat *)
    matA[8, 2] := 0.0480; (* Vapor enthalpy directly correlates with superheat delta *)
    matA[8, 3] := 0.0000; (* Discharge pressure decoupling *)
    matA[8, 4] := 0.0000; (* Discharge temp decoupling *)
    matA[8, 5] := 0.0015; (* Casing conduction to suction transducer pocket *)
    matA[8, 6] := 0.0000; (* Economizer decoupling *)
    matA[8, 7] := 0.0000; (* Condenser decoupling *)
    matA[8, 8] := 0.9420; (* Suction superheat thermal equilibrium self-decay *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* 0.2: CONTROL INPUT DISTRIBUTION MATRIX matB (8x6)                                                                *)
    (* Inputs: u1=Slide1_pct, u2=VFD1_Hz, u3=Slide2_pct, u4=EEV_Eco_pct, u5=FanBank_pct, u6=Oil3Way_pct                 *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    matB[1, 1] := -0.0145; (* Comp 1 slide-valve increase draws down suction header pressure [bar/%] *)
    matB[1, 2] := -0.0280; (* Comp 1 VFD frequency ramp-up accelerates swept volume suction draw [bar/Hz] *)
    matB[1, 3] := -0.0160; (* Comp 2 slide-valve increase draws down suction header pressure [bar/%] *)
    matB[1, 4] := 0.0010;  (* Economizer EEV expansion minor back-pressure effect *)
    matB[1, 5] := 0.0000;  (* Condenser fans do not directly alter suction pressure *)
    matB[1, 6] := 0.0000;  (* Oil 3-way valve decoupling *)

    matB[2, 1] := -0.0250; (* Increased slide valve draws colder saturated suction vapor *)
    matB[2, 2] := -0.0450; (* Increased VFD speed sweeps more low-enthalpy vapor from accumulator *)
    matB[2, 3] := -0.0280; (* Comp 2 displacement effect *)
    matB[2, 4] := 0.0350;  (* Subcooling EEV expansion flash gas feedback to economizer port *)
    matB[2, 5] := 0.0000;  (* Condenser fans decoupling *)
    matB[2, 6] := 0.0015;  (* Minor oil cooling feedback *)

    matB[3, 1] := 0.0220;  (* Comp 1 slide-valve increases mass flow, raising discharge pressure [bar/%] *)
    matB[3, 2] := 0.0420;  (* Comp 1 VFD speed increases mass flow into condenser bundle [bar/Hz] *)
    matB[3, 3] := 0.0250;  (* Comp 2 slide-valve mass flow contribution [bar/%] *)
    matB[3, 4] := 0.0080;  (* Economizer injection adds mass flow to high-stage discharge *)
    matB[3, 5] := -0.0380; (* Condenser fan speed directly increases heat rejection, lowering discharge P *)
    matB[3, 6] := 0.0000;  (* Oil valve decoupling *)

    matB[4, 1] := 0.0480;  (* Comp 1 slide valve increases internal re-compression friction heat [deg C/%] *)
    matB[4, 2] := 0.0650;  (* Comp 1 speed increase generates shear friction heating [deg C/Hz] *)
    matB[4, 3] := 0.0420;  (* Comp 2 mechanical friction heating *)
    matB[4, 4] := -0.0550; (* Economizer intermediate vapor injection cools screw rotors and discharge gas *)
    matB[4, 5] := -0.0220; (* Condenser fan speed lowers overall condensing pressure & discharge temp *)
    matB[4, 6] := 0.0350;  (* Oil 3-way valve bypassing cooler increases injected oil & discharge temp *)

    matB[5, 1] := 0.0150;  (* Comp 1 loading increases oil friction heating *)
    matB[5, 2] := 0.0220;  (* Comp 1 speed increase heats oil *)
    matB[5, 3] := 0.0180;  (* Comp 2 loading heats oil *)
    matB[5, 4] := 0.0000;  (* Economizer decoupling *)
    matB[5, 5] := -0.0080; (* Cooler condenser liquid improves oil cooler thermosyphon delta-T *)
    matB[5, 6] := 0.0820;  (* Oil 3-way valve bypass directly regulates oil temperature [deg C/%] *)

    matB[6, 1] := 0.0050;  (* Comp 1 intermediate port pressure coupling *)
    matB[6, 2] := 0.0090;  (* Comp 1 speed intermediate port coupling *)
    matB[6, 3] := 0.0000;  (* Comp 2 port isolation *)
    matB[6, 4] := 0.0450;  (* Economizer EEV opening raises intermediate vessel pressure [bar/%] *)
    matB[6, 5] := -0.0120; (* Lower condensing pressure lowers economizer supply pressure *)
    matB[6, 6] := 0.0000;  (* Oil decoupling *)

    matB[7, 1] := 0.0080;  (* Comp 1 heat rejection to evaporative condenser *)
    matB[7, 2] := 0.0150;  (* Comp 1 speed heat rejection *)
    matB[7, 3] := 0.0100;  (* Comp 2 heat rejection *)
    matB[7, 4] := 0.0030;  (* Economizer heat rejection *)
    matB[7, 5] := -0.0650; (* EC fan bank speed forces evaporative mass transfer, cooling basin water *)
    matB[7, 6] := 0.0000;  (* Oil decoupling *)

    matB[8, 1] := -0.0120; (* Slide load draws more liquid droplets from surge drum, depressing superheat *)
    matB[8, 2] := -0.0200; (* VFD ramp draws wet suction gas *)
    matB[8, 3] := -0.0140; (* Comp 2 suction draw *)
    matB[8, 4] := 0.0000;  (* Economizer decoupling *)
    matB[8, 5] := 0.0000;  (* Condenser decoupling *)
    matB[8, 6] := 0.0000;  (* Oil decoupling *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* 0.3: EXOGENOUS DISTURBANCE MATRIX matEw (8x3)                                                                    *)
    (* Disturbances: w1=dTwb (wet-bulb), w2=dQ_load (thermal load), w3=dm_defrost (hot-gas diversion)                    *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    matEw[1, 1] := 0.0000; (* Wet-bulb does not directly affect suction header pressure *)
    matEw[1, 2] := 0.0085; (* Evaporator thermal load shock boils liquid ammonia, raising suction P [bar/kW] *)
    matEw[1, 3] := -0.0220; (* Hot-gas defrost diversion starves liquid feed, reducing suction return *)

    matEw[2, 1] := 0.0000;
    matEw[2, 2] := 0.0450; (* High room load increases evaporator superheat and suction vapor enthalpy *)
    matEw[2, 3] := -0.0350;

    matEw[3, 1] := 0.0320; (* Elevated ambient wet-bulb reduces evaporative heat rejection, raising discharge P *)
    matEw[3, 2] := 0.0180; (* Heavy thermal load increases heat rejection requirement at condenser *)
    matEw[3, 3] := -0.0450; (* Reverse hot-gas defrost diverts high-pressure gas, rapidly dropping discharge P *)

    matEw[4, 1] := 0.0250; (* Higher wet-bulb raises condensing temp, increasing discharge gas temp *)
    matEw[4, 2] := 0.0350; (* Heavy load increases compressor work, raising discharge temp *)
    matEw[4, 3] := -0.0150; (* Hot gas diversion mass relief cools discharge line *)

    matEw[5, 1] := 0.0120; (* High ambient wet-bulb warms oil cooling thermosyphon loop *)
    matEw[5, 2] := 0.0220; (* Sustained heavy load raises continuous oil heat dissipation *)
    matEw[5, 3] := 0.0000;

    matEw[6, 1] := 0.0150; (* High ambient wet-bulb raises intermediate vessel pressure *)
    matEw[6, 2] := 0.0080; (* Load expansion *)
    matEw[6, 3] := -0.0180; (* Hot gas bypass drains subcooler liquid line pressure *)

    matEw[7, 1] := 0.0850; (* Wet-bulb temperature drives evaporative condenser sump water equilibrium directly *)
    matEw[7, 2] := 0.0280; (* Thermal load increases total heat of condensation rejected to basin *)
    matEw[7, 3] := -0.0150; (* Hot gas defrost diverts heat into frozen coils, reducing basin rejection *)

    matEw[8, 1] := 0.0000;
    matEw[8, 2] := 0.0650; (* Room thermal load surge causes evaporator thermostatic expansion valve hunting *)
    matEw[8, 3] := -0.0400; (* Defrost cycle return liquid dumps into accumulator, lowering superheat *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* 0.4: MEASUREMENT OBSERVATION MATRIX matC (8x8) & FEEDTHROUGH MATRIX matD (8x6)                                   *)
    (* Direct observation of state vector variables with zero cross-coupling feedthrough                               *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 8 DO
        FOR idxCol := 1 TO 8 DO
            IF idxRow = idxCol THEN
                matC[idxRow, idxCol] := 1.0000;
            ELSE
                matC[idxRow, idxCol] := 0.0000;
            END_IF;
        END_FOR;
        FOR idxCol := 1 TO 6 DO
            matD[idxRow, idxCol] := 0.0000;
        END_FOR;
    END_FOR;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* 0.5: STEADY-STATE KALMAN OBSERVER INNOVATION GAIN MATRIX matK (8x8)                                              *)
    (* Optimal sensor noise covariance filtering vs process plant turbulence                                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 8 DO
        FOR idxCol := 1 TO 8 DO
            matK[idxRow, idxCol] := 0.0000;
        END_FOR;
    END_FOR;
    matK[1, 1] := 0.2850; (* Suction pressure innovation gain from PT-101 *)
    matK[1, 2] := 0.0120;
    matK[2, 2] := 0.2450; (* Suction enthalpy innovation gain *)
    matK[2, 8] := 0.0350;
    matK[3, 3] := 0.3100; (* Discharge pressure innovation gain from PT-601 *)
    matK[3, 4] := 0.0150;
    matK[4, 4] := 0.3400; (* Discharge temperature innovation gain from TT-201 *)
    matK[4, 5] := 0.0200;
    matK[5, 5] := 0.2200; (* Oil sump temperature innovation gain from TT-302 *)
    matK[6, 6] := 0.2900; (* Economizer pressure innovation gain from PT-501 *)
    matK[7, 7] := 0.1800; (* Condenser basin temperature innovation gain from TT-602 *)
    matK[8, 8] := 0.2600; (* Suction superheat innovation gain *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* 0.6: MPC QUADRATIC COST WEIGHTING MATRICES: matQ (8x8), matR (6x6), matS (6x6), matP (8x8)                       *)
    (* Penalty on suction pressure error, COP optimization, actuator hunting wear prevention                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 8 DO
        FOR idxCol := 1 TO 8 DO
            matQ[idxRow, idxCol] := 0.0000;
            matP[idxRow, idxCol] := 0.0000;
        END_FOR;
    END_FOR;
    FOR idxRow := 1 TO 6 DO
        FOR idxCol := 1 TO 6 DO
            matR[idxRow, idxCol] := 0.0000;
            matS[idxRow, idxCol] := 0.0000;
        END_FOR;
    END_FOR;

    (* State Error Weights Q: Heavily penalize suction pressure deviation to maintain cold storage temperature *)
    matQ[1, 1] := 185.0;  (* Suction pressure tracking penalty [(bar)^-2] *)
    matQ[2, 2] := 12.0;   (* Suction enthalpy penalty *)
    matQ[3, 3] := 45.0;   (* Discharge pressure penalty (floating head tracking) *)
    matQ[4, 4] := 35.0;   (* Discharge temperature penalty (prevent oil breakdown) *)
    matQ[5, 5] := 25.0;   (* Oil sump temperature penalty (maintain viscosity) *)
    matQ[6, 6] := 18.0;   (* Economizer pressure penalty *)
    matQ[7, 7] := 15.0;   (* Condenser sump temperature penalty *)
    matQ[8, 8] := 30.0;   (* Suction superheat penalty (prevent liquid carryover slugging) *)

    (* Control Effort Weights R: Minimize compressor electrical power consumption and excessive fan energy *)
    matR[1, 1] := 0.85;   (* Comp 1 slide-valve modulation cost *)
    matR[2, 2] := 1.45;   (* Comp 1 VFD frequency electrical power penalty [kW/Hz] *)
    matR[3, 3] := 1.10;   (* Comp 2 slide-valve modulation cost *)
    matR[4, 4] := 0.35;   (* Economizer EEV expansion modulation cost *)
    matR[5, 5] := 0.65;   (* Condenser EC fan electrical energy penalty *)
    matR[6, 6] := 0.25;   (* Oil cooler 3-way valve cycling cost *)

    (* Actuator Slew Rate Penalties S: Prevent rapid mechanical cycling, slide-valve cavitation & VFD stress *)
    matS[1, 1] := 4.50;   (* Comp 1 slide-valve slew rate penalty [(%/s)^-2] *)
    matS[2, 2] := 8.20;   (* Comp 1 VFD frequency acceleration slew penalty [(Hz/s)^-2] *)
    matS[3, 3] := 5.20;   (* Comp 2 slide-valve slew penalty *)
    matS[4, 4] := 1.80;   (* Economizer EEV stepper slew penalty *)
    matS[5, 5] := 3.20;   (* Condenser fan ramp rate slew penalty *)
    matS[6, 6] := 1.50;   (* Oil valve slew rate penalty *)

    (* Lyapunov Terminal State Matrix P: Riccati Equation steady-state solution for infinite horizon stability *)
    matP[1, 1] := 320.0;
    matP[2, 2] := 24.0;
    matP[3, 3] := 85.0;
    matP[4, 4] := 65.0;
    matP[5, 5] := 48.0;
    matP[6, 6] := 32.0;
    matP[7, 7] := 28.0;
    matP[8, 8] := 55.0;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* 0.7: PHYSICAL ACTUATOR HARDWARE BOX LIMITS & MAXIMUM PERMISSIBLE SLEW RATES                                      *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    vecU_min[1] := 15.0;   (* Comp 1 Minimum Slide Valve Unloaded Limit [15.0 %] *)
    vecU_max[1] := 100.0;  (* Comp 1 Maximum Slide Valve Fully Loaded [100.0 %] *)
    vecSlew_max[1] := 2.50; (* Comp 1 Slide Valve Max Rate of Change [2.50 %/s] -> 0.25 % per 100 ms *)

    vecU_min[2] := 30.0;   (* Comp 1 VFD Minimum Motor Operating Speed [30.0 Hz] *)
    vecU_max[2] := 60.0;   (* Comp 1 VFD Maximum Motor Operating Speed [60.0 Hz] *)
    vecSlew_max[2] := 2.00; (* Comp 1 VFD Speed Max Ramp Rate [2.00 Hz/s] -> 0.20 Hz per 100 ms *)

    vecU_min[3] := 0.0;    (* Comp 2 Minimum Slide Valve Position [0.0 %] *)
    vecU_max[3] := 100.0;  (* Comp 2 Maximum Slide Valve Position [100.0 %] *)
    vecSlew_max[3] := 2.50; (* Comp 2 Slide Valve Max Rate of Change [2.50 %/s] *)

    vecU_min[4] := 0.0;    (* Economizer Stepper EEV Minimum Opening [0.0 %] *)
    vecU_max[4] := 100.0;  (* Economizer Stepper EEV Maximum Opening [100.0 %] *)
    vecSlew_max[4] := 5.00; (* Economizer EEV Max Step Rate [5.00 %/s] *)

    vecU_min[5] := 15.0;   (* Condenser EC Fan Minimum Speed for Motor Bearing Air Flow [15.0 %] *)
    vecU_max[5] := 100.0;  (* Condenser EC Fan Full Air Flow Speed [100.0 %] *)
    vecSlew_max[5] := 4.00; (* Condenser Fan Max Acceleration Slew Rate [4.00 %/s] *)

    vecU_min[6] := 0.0;    (* Oil Cooler 3-Way Valve Full Bypass [0.0 %] *)
    vecU_max[6] := 100.0;  (* Oil Cooler 3-Way Valve Full Cooling Flow [100.0 %] *)
    vecSlew_max[6] := 3.00; (* Oil Valve Max Modulation Rate [3.00 %/s] *)

    (* Initialize State & Control Vectors *)
    FOR idxRow := 1 TO 8 DO
        vecX[idxRow] := 0.0;
        vecX_next[idxRow] := 0.0;
        vecX_hat[idxRow] := 0.0;
        vecR[idxRow] := 0.0;
        vecY_meas[idxRow] := 0.0;
        vecY_pred[idxRow] := 0.0;
        vecY_innov[idxRow] := 0.0;
    END_FOR;

    FOR idxRow := 1 TO 6 DO
        vecU[idxRow] := vecU_min[idxRow];
        vecU_prev[idxRow] := vecU_min[idxRow];
        vecDeltaU[idxRow] := 0.0;
        vecU_opt[idxRow] := vecU_min[idxRow];
        vecGradJ[idxRow] := 0.0;
    END_FOR;

    FOR idxRow := 1 TO 3 DO
        vecW[idxRow] := 0.0;
    END_FOR;

    bMatricesInitialized := TRUE;
END_IF;
"""
