import json, os, glob

subagents = [
    ('Agent #01', '66a11ac4-6929-4384-a6e0-fd23e50bf4d1', 'E-Axle Gear Hobbing & EGB Spindle Sync', 'eaxle_gearhobbing_builder'),
    ('Agent #02', '6d03b401-3d33-4364-b17b-6232bd59d239', 'BIW Cathodic Electrodeposition E-Coat Dip Tank', 'ecoat_dip_tank_builder'),
    ('Agent #03', '25664167-8a80-4bb5-81be-8679ccbb9aba', 'EOL 4WD Chassis Dyno & ADAS Calibration', 'dyno_builder'),
    ('Agent #04', 'ab1db654-41e2-4295-85d6-d41a39879073', 'BIW Roof Laser Brazing & Seam Tracking', 'biw_roof_laser_brazing_builder'),
    ('Agent #05', 'f3001271-04f5-49d9-b829-886f72fc7589', 'Hot Stamping & Press Hardening', 'hot_stamping_builder'),
    ('Agent #06', '8cadb750-0fc6-4e9c-95b0-1b191cecbe7e', 'Radial Tire Curing & Steam Bladder', 'tire_vulcanization_builder'),
    ('Agent #07', 'f503fcba-9b17-410e-8c53-44197a2941cf', 'Acoustic Windshield Autoclave Lamination', 'windshield_autoclave_builder'),
    ('Agent #08', '88dc5eb8-e6b5-4f5c-aff0-271daffc8da6', 'LPDC Engine Block Casting & Riser Control', 'lpdc_casting_builder'),
    ('Agent #09', '14e2016c-fa22-42bd-9880-04f21492b63c', 'EV Battery Wire Bonding & Piezo Horn', 'ev_wirebond_builder'),
    ('Agent #10', '7e2788e6-9550-426a-b166-2120ac2a21fb', 'Seat Foam Reaction Injection Molding (RIM)', 'seat_foam_rim_builder'),
    ('Agent #11', '3a7d2e03-c656-442e-a9fc-5c21eef23cb3', 'Exhaust CNC Tube Bending & Robotic MIG', 'exhaust_tube_weld_builder'),
    ('Agent #12', '98baff0d-de99-475a-8132-7415bbf1bf26', 'Brake Rotor Casting & CNC Dynamic Balancing', 'brake_rotor_builder'),
    ('Agent #13', '77bf504a-cc77-4df6-b279-ae2ba5d946b3', 'Automotive Inverter 800V EOL Burn-In Dyno', 'inverter_dyno_builder'),
    ('Agent #14', '5f51e9e0-45e0-4733-bb2a-402bfbf42d1b', 'EV Battery Pack Laser Busbar & TIM Dispensing', 'ev_battery_pack_builder'),
    ('Agent #15', '45b74f94-bf6e-4997-b9d7-bb090c83ad38', 'Paint Clearcoat Bell Atomizer & Electrostatic', 'clearcoat_bell_builder'),
    ('Agent #16', 'e5130eb6-b3d7-413a-b6d0-b924467f0cac', 'e-Axle Planetary Shimming & Backlash Gauging', 'eaxle_shimming_builder'),
    ('Agent #17', '1588f6e7-db56-4e84-81b5-f05552d593ab', 'Transmission Valve Body EOL Test & Solenoid', 'valve_body_builder'),
    ('Agent #18', 'fc141af3-3d24-4ede-8637-161681d22592', 'Automotive Glazing Robotic Polyurethane Cell', 'glazing_dispense_builder'),
    ('Agent #19', '25aa126c-df91-48f1-bf45-b98d07727b03', 'Cylinder Head Multi-Spindle CNC Machining', 'cylinder_head_machining_builder'),
    ('Agent #20', '89b9db1c-206d-4ca7-a6de-a5ff38b1746d', 'Robotic Roller Hemming for BIW Closures', 'roller_hemming_builder'),
    ('Agent #21', 'ed280149-dfc9-43cc-9b9b-95422b7d1afb', 'Chassis Subframe Multi-Robot MIG Welding', 'subframe_mig_builder'),
    ('Agent #22', '10d9e3f7-75fc-415f-8b5d-9d5b3208c94a', 'EV Stator Needle Winding & Slot Insulation', 'stator_winding_builder'),
    ('Agent #23', '460da361-1700-411a-834a-00afe32f0395', 'Engine Block HP Waterjet Deburring Cell', 'waterjet_deburr_builder'),
    ('Agent #24', '04d7ef7a-77f1-4028-8151-74069580ca90', 'TWB Dissimilar Laser Welding & Leveling', 'twb_laser_leveler_builder'),
    ('Agent #25', '7ebd85db-c672-43f0-af13-d9de5aa87a60', 'BIW Structural Crash Adhesive Dispense', 'biw_adhesive_builder'),
    ('Agent #26', 'd78dc530-8095-4eea-974d-d3ee33965b01', 'Wheel Hub 5-Spindle Robotic Nutrunner Cell', 'wheel_hub_nutrunner_builder'),
    ('Agent #27', '44ebfa48-dec3-402e-ad61-56782fa8f51d', 'Crankshaft CNC Orbital Pin Grinding Cell', 'crankshaft_grinding_builder'),
    ('Agent #28', '4af4bfc6-e1ad-4508-9013-e6c9ce4f27b8', 'Robotic FIPFG Foam Gasket Dispense Cell', 'fipfg_gasketing_builder'),
    ('Agent #29', '7922b439-1c39-44b8-9520-4a7845fce846', 'Fuel Tank 6-Layer Blow Molding & Parison', 'fuel_tank_blowmolding_builder'),
    ('Agent #30', '3e97725d-c921-44d7-8de8-74812f6b3637', 'Brake Pad Thermal Scorching & Induction', 'brakepad_scorching_builder'),
    ('Agent #31', '6f4429bd-9cdf-48cb-bedd-5aaaa1d8bb7e', 'Dashboard PU Spray Skin & Thermoforming', 'dashboard_spray_builder'),
    ('Agent #32', 'fbddd40e-2e20-4d77-b94a-848e24d15b3e', 'Underbody Robotic PVC Spray Sealing Cell', 'underbody_pvc_builder')
]

for tag, cid, domain, bdir in subagents:
    transcript_path = f'C:/Users/majip/.gemini/antigravity/brain/{cid}/.system_generated/logs/transcript.jsonl'
    status = 'SPAWNED'
    last_action = ''
    total_chars = 0
    if os.path.exists(transcript_path):
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if 'tool_calls' in data and data['tool_calls']:
                        tc = data['tool_calls'][-1]
                        cmd = tc.get('args', {}).get('CommandLine', '')
                        path = tc.get('args', {}).get('Path', '')
                        last_action = f"{tc.get('name')}: {cmd[:30] if cmd else path[-30:]}"
                        status = 'SYNTHESIZING'
                    if 'content' in data and data['content']:
                        if 'EVOLUTION COMPLETE' in data['content']:
                            status = 'SAVED'
                except:
                    pass
    
    if bdir and os.path.exists(bdir):
        for root, dirs, files in os.walk(bdir):
            for file in files:
                total_chars += os.path.getsize(os.path.join(root, file))

    print(f'{tag} | {cid[:8]} | {status:12} | {total_chars:7d} B built | {last_action[:40]:40} | {domain}')
