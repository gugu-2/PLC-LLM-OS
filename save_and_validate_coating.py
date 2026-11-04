# save_and_validate_coating.py
import os
import sys
import json
import uuid
import build_coating_dataset
import validate_iec

def main():
    agent_uuid = uuid.uuid4().hex[:8]
    output_filename = f"agent_{agent_uuid}.json"
    output_path = os.path.join(os.getcwd(), "data", "swarm_raw", output_filename)
    
    # 1. Generate IEC 61131-3 ST Code
    st_code = build_coating_dataset.build_iec_code()
    lines_count = len(st_code.splitlines())
    char_count = len(st_code)
    
    print("=" * 80)
    print("LUMINA CYBER-PHYSICAL DATASET SYNTHESIS - AGENT WORKER")
    print("=" * 80)
    print(f"Generated IEC 61131-3 ST Code:")
    print(f"  Target File: {output_filename}")
    print(f"  Lines:       {lines_count}")
    print(f"  Characters:  {char_count}")
    
    # 2. Check AST Delimiter Parity directly
    errs = validate_iec.validate_iec_st(st_code)
    if errs:
        print("\n[ERROR] Direct ST Code Validation Failed:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
        
    print("\n[PASS] Direct ST Code Syntax and Parity 100% OK!")
    
    # 3. Formulate Prompt
    instruction_prompt = """Design and implement a mathematically rigorous, deterministic IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_Finishing_ElectrostaticPowderCoating_Curing for a continuous industrial surface pretreatment and electrostatic powder coating complex in the automotive component manufacturing sector.

SYSTEM SPECIFICATION & ENGINEERING TOPOLOGY:
1. 7-Stage Spray/Immersion Chemical Pretreatment Tunnel:
   - Stage 1: Alkaline Degrease & Heavy Oil Saponification (55.0 to 65.0 deg C, 1.8 to 2.5 bar, 4000 to 8000 uS/cm toroidal conductivity).
   - Stage 2: City Water Immersion & Cascade Counter-Flow Rinse (Ambient, 1.5 bar, < 800 uS/cm).
   - Stage 3: Acid Pickling & Micro-Etch Descaling (40.0 to 50.0 deg C, pH 2.0 to 3.2, 15000 to 25000 uS/cm).
   - Stage 4: Secondary DI Pre-Rinse (Ambient, 1.5 bar, < 500 uS/cm).
   - Stage 5: Nanocrystalline Iron/Zinc Phosphating Conversion Bath (45.0 to 55.0 deg C, pH 4.2 to 5.2, 3500 to 6000 uS/cm).
   - Stage 6: Demineralized (DI) Water Ultra-Pure Rinse (Ambient, 1.2 bar, < 20 uS/cm).
   - Stage 7: Silane Nanotechnology Zirconium/Polymer Sealant Passivation (25.0 to 35.0 deg C, pH 4.0 to 5.0, 1500 to 2500 uS/cm) with closed-loop stoichiometric chemical dosing.
2. Multi-Axis Servo Reciprocator Electrostatic Powder Coating Booth:
   - 16 Corona / Tribo Electrostatic Spray Guns (8 Left / 8 Right).
   - -100 kV High-Voltage Cascade Generator (-30.0 to -100.0 kV DC, 10 to 100 uA current limiter with sub-5ms crowbar trip).
   - Fluidized Powder Hopper Bed with Continuous Ultrasonic Conditioning Sieve (140 mesh / 105 um).
   - Dynamic Powder Mass Flow Delivery (50.0 to 450.0 g/min per injector, atomizing air 0.8 to 2.5 bar).
   - Multi-Axis Servo Vertical Reciprocators (Stroke 800 to 2400 mm, speed 0.1 to 0.8 m/s sinusoidal tracking).
3. 40-Meter Continuous Gas-Fired Convection Tunnel Curing Oven:
   - Zone 1 Preheat & Gelation: 150.0 to 180.0 deg C (350 kW modulating natural gas burner).
   - Zone 2 Crosslinking Curing: 190.0 to 215.0 deg C (450 kW modulating natural gas burner).
   - Zone 3 Thermal Dwell / Soak: 200.0 to 220.0 deg C (300 kW modulating natural gas burner).
   - Guaranteed Part Metal Temperature (PMT): 190.0 to 204.0 deg C maintained for minimum 12.0 min (20.0 min total tunnel dwell).
   - Exhaust Solvent / VOC Flammability Monitor: Triplicated Catalytic/NDIR LEL Sensors (Warning: 15% LEL, Critical Trip: 25% LEL).
4. Continuous Power-and-Free Overhead Monorail Conveyor:
   - Nominal Chain Speed: 3.0 m/min (Range 1.0 to 5.0 m/min).
   - Carrier Tracking: Continuous RFID Transponder Carrier Collation & Carrier Drop-Section Hoist Safety Interlocks.

CYBER-PHYSICAL MATHEMATICAL RIGOR:
- Full 8-state Discrete State-Space Model (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) capturing pretreatment tank temperatures, spray header pressures, bath conductivities, silane pH, high-voltage electrostatic field charge, powder coating film thickness, oven curing thermal kinetics, and conveyor line velocity.
- Receding-Horizon Model Predictive Control (MPC) quadratic cost approximation penalizing dry film thickness (DFT) deviation (Q), powder feed pump adjustments (R), and burner fuel gas consumption (P).
- 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on 16 triplicated field transmitter sets.
- ISA-18.2 multi-tiered alarm hierarchy (Critical Conveyor Jam / Ground Fault HH, Oven Over-Temperature HH, Exhaust LEL Flammability HH, Warning H/L, Diagnostic, Priority Escalation).
- 12-Stage Finite State Machine (CASE nFSM_State OF ... END_CASE) covering bath circulation pre-heat, chemical concentration dosing, booth exhaust ventilation start, high-voltage electrostatic prime, conveyor carrier entry sync, automatic reciprocating spray coating, inter-booth powder recovery cyclone, oven curing dwell, cool-down, carrier unload hoist transfer, daily rinse cleanout, and emergency ground-fault trip.

Strict Syntax Parity: Ensure all IF, CASE, FOR, and FUNCTION_BLOCK statements have matching END delimiters. Provide full mathematical implementations with zero placeholders or omissions."""

    formatted_output = f"```iec-st\n{st_code}\n```"
    
    # 4. Construct JSON Record with dual schema compatibility
    record = {
        "id": f"synthetic_v3_{agent_uuid}",
        "instruction": instruction_prompt,
        "input": "",
        "output": formatted_output,
        "messages": [
            {"role": "user", "content": instruction_prompt},
            {"role": "assistant", "content": formatted_output}
        ],
        "metadata": {
            "domain": "Surface Finishing & Automotive Component Coating",
            "function_block": "FB_Finishing_ElectrostaticPowderCoating_Curing",
            "version": "v3_cyberphysical_max",
            "lines": lines_count,
            "characters": len(formatted_output),
            "validated": True
        }
    }
    
    # 5. Write to isolated JSON file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"\nSuccessfully written dataset to: {output_path}")
    print(f"File size on disk: {os.path.getsize(output_path)} bytes")
    
    # 6. Execute validate_iec.py on the saved JSON file
    file_errs = validate_iec.validate_json_file(output_path)
    if file_errs:
        print("\n[ERROR] JSON File Validation Failed:")
        for e in file_errs:
            print(" -", e)
        sys.exit(1)
        
    print("\n[PASS] validate_json_file checks passed with 100% precision!")
    print("=" * 80)
    print(f"EVOLUTION COMPLETE: Surface Finishing & Automotive Component Coating")
    print(f"File:       {output_filename}")
    print(f"Characters: {len(formatted_output)}")
    print(f"Lines:      {lines_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()
