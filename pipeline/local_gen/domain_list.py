"""
domain_list.py
==============
500+ unique industrial domains for the local generation pipeline.
Domains are organised by sector. Safety-restricted domains are excluded.
"""

# ── FOOD & BEVERAGE ───────────────────────────────────────────────────────────
FOOD_BEVERAGE = [
    "Continuous Pasta Drying Line",
    "Beer Fermentation and Maturation Tank",
    "High-Capacity Fruit Juice Pasteurizer",
    "Cookie Dough Mixing and Depositing Line",
    "Chocolate Conching and Tempering Machine",
    "Olive Oil Centrifugal Separator",
    "Fish Meal Dryer and Pelletizer",
    "Tortilla Continuous Oven Line",
    "Soy Sauce Fermentation Bioreactor",
    "Infant Formula Spray Dryer",
    "Vegetable Oil Hydrogenation Reactor",
    "Wine Barrel Washing and Sterilization",
    "Butter Churning and Packaging Line",
    "Yogurt Incubation and Cooling Tunnel",
    "Frozen Vegetable Blancher and IQF Freezer",
    "Cereal Extrusion and Puffing Line",
    "Carbonated Soft Drink Filling Line",
    "Corn Starch Wet Milling Plant",
    "Sugar Beet Slicing and Diffusion Tower",
    "Condensed Milk Evaporator",
]

# ── PHARMA & BIOTECH ──────────────────────────────────────────────────────────
PHARMA_BIOTECH = [
    "Continuous Tablet Compression Press",
    "Pharmaceutical Spray Coating Pan",
    "Bioreactor Mammalian Cell Culture",
    "API Crystallisation and Filtration",
    "Cleanroom HVAC Pressure Cascade",
    "Lyophilization (Freeze-Drying) Chamber",
    "Sterile Filling Isolator System",
    "GMP Water-for-Injection Still",
    "Capsule Filling and Banding Machine",
    "Parenteral Vial Washing and Sterilization Tunnel",
    "Continuous Oral Solid Dosage Line",
    "Monoclonal Antibody Downstream Processing",
    "Pharmaceutical Fluid Bed Granulator",
    "Auto-Injector Assembly and Testing",
    "Cold Chain Vaccine Storage Monitor",
]

# ── ENERGY & UTILITIES ────────────────────────────────────────────────────────
ENERGY_UTILITIES = [
    "Combined Cycle Gas Turbine Plant",
    "Offshore Wind Turbine Array Controller",
    "Solar PV Farm Maximum Power Point Tracker",
    "Pumped Hydro Storage Plant",
    "District Heat Network Pressure Regulation",
    "Compressed Air Energy Storage Plant",
    "Biomass Combined Heat and Power Plant",
    "Tidal Stream Generator Controller",
    "Fuel Cell Stack Management System",
    "Grid-Scale Battery Energy Storage (BESS)",
    "Wave Energy Converter Control",
    "Geothermal Doublet Well Control",
    "Concentrating Solar Power (CSP) Tower",
    "Hydrogen Electrolyzer Stack",
    "Power-to-Gas Methanation Reactor",
    "Municipal Solid Waste Incinerator Boiler",
    "Landfill Gas Collection and Flaring",
    "Waste-to-Energy Steam Turbine",
    "Industrial Steam Accumulator",
    "Coal Gasification Syngas Cooler",
]

# ── METALS & MINING ───────────────────────────────────────────────────────────
METALS_MINING = [
    "Electric Arc Furnace Steelmaking",
    "Continuous Casting Machine",
    "Rolling Mill Tension and Speed Control",
    "Zinc Hot-Dip Galvanizing Line",
    "Copper Electrorefining Tank",
    "Aluminium Smelting Pot Feeder",
    "Ore Ball Mill Grinding Circuit",
    "Flotation Cell Bank Controller",
    "Mine Ventilation Fan Array",
    "Dragline Excavator Control",
    "Longwall Mining Shearer",
    "Underground Belt Conveyor System",
    "Precious Metal Leaching Autoclave",
    "Titanium Sponge Retort",
    "Lead Acid Battery Plate Formation",
    "Silicon Carbide Crystal Growth Furnace",
    "Stainless Steel Annealing Furnace",
    "Tungsten Carbide Sintering Furnace",
    "Magnesium Reduction Retort",
    "Nickel Laterite Heap Leach Pad",
]

# ── CHEMICAL & PETROCHEMICAL ──────────────────────────────────────────────────
CHEMICAL_PETROCHEM = [
    "Ethylene Cracking Furnace",
    "Polyethylene Fluidised Bed Reactor",
    "Sulfuric Acid Double Absorption Plant",
    "Chlor-Alkali Membrane Cell",
    "Ammonia Synthesis Converter",
    "Methanol Distillation Column",
    "Crude Oil Atmospheric Distillation Unit",
    "Vacuum Distillation Unit",
    "Fluid Catalytic Cracking (FCC) Unit",
    "Hydrocracker Reactor",
    "Amine Gas Sweetening Unit",
    "Claus Sulfur Recovery Unit",
    "Polyvinyl Chloride Suspension Reactor",
    "Urea Prilling Tower",
    "Caustic Soda Evaporation Plant",
    "Ethylene Oxide Reactor",
    "Propylene Glycol Continuous Reactor",
    "Acrylonitrile Butadiene Styrene (ABS) Extruder",
    "Nitrogen Blanketing Manifold",
    "Solvent Recovery Distillation Column",
]

# ── WATER & WASTEWATER ────────────────────────────────────────────────────────
WATER_WASTEWATER = [
    "Drinking Water Ozonation System",
    "Slow Sand Filter Bank",
    "Reverse Osmosis Desalination Plant",
    "Sequencing Batch Reactor (SBR)",
    "Membrane Bioreactor (MBR)",
    "Sludge Belt Filter Press",
    "UV Disinfection Channel",
    "Storm Water Retention Basin Control",
    "Groundwater Pump-and-Treat System",
    "Effluent Neutralization Tank",
    "Leachate Treatment Plant",
    "Industrial Cooling Tower Blowdown",
    "Tertiary Filtration Polisher",
    "Biogas Upgrading Membrane",
    "Hydrothermal Carbonisation Reactor",
]

# ── AUTOMOTIVE & TRANSPORT ────────────────────────────────────────────────────
AUTOMOTIVE_TRANSPORT = [
    "Automotive Body-in-White Welding Cell",
    "Paint Shop Electrocoat (E-Coat) Line",
    "Powertrain Assembly Torque Station",
    "Automated End-of-Line Testing (EOL)",
    "EV Battery Module Assembly Line",
    "Tire Inflation and Leak Test",
    "Axle Gear Lapping Machine",
    "Catalytic Converter Substrate Coater",
    "Windscreen PVB Lamination Line",
    "Seat Foam Injection Mold",
    "Railway Track Switch Heater Control",
    "Airport Ground Power Unit",
    "Autonomous Guided Vehicle Fleet Manager",
    "Port Container Crane Anti-Sway Control",
    "Ship Engine Room Automation",
]

# ── SEMICONDUCTOR & ELECTRONICS ───────────────────────────────────────────────
SEMICONDUCTOR_ELECTRONICS = [
    "Chemical Mechanical Planarization (CMP)",
    "Ion Implantation Beam Controller",
    "Plasma Etch Chamber",
    "Chemical Vapor Deposition (CVD) Reactor",
    "Wafer Diffusion Furnace",
    "Electroplating Cell for PCB",
    "Solder Reflow Oven",
    "Automated Optical Inspection (AOI) System",
    "Clean Room Air Shower Interlock",
    "Wafer Dicing Saw",
    "Die Bonder Temperature Controller",
    "Wire Bonder Ultrasonic Controller",
    "Flip Chip Underfill Dispenser",
    "LCD Panel TFT Array Tester",
    "OLED Vacuum Deposition Chamber",
]

# ── BUILDING & HVAC ────────────────────────────────────────────────────────────
BUILDING_HVAC = [
    "Variable Air Volume (VAV) AHU",
    "District Cooling Chiller Plant",
    "Chilled Beam Radiant Ceiling System",
    "Data Centre Precision Cooling (CRAC)",
    "Hospital Isolation Room Pressure Control",
    "Pharmaceutical HVAC Classification",
    "Heat Recovery Ventilation (HRV)",
    "Solar Thermal Domestic Hot Water",
    "Ground Source Heat Pump Array",
    "Commercial Kitchen Ventilation Interlock",
    "Smoke Control Pressurization Fan",
    "Building Energy Management (BMS) Optimizer",
    "Elevator Machine Room Cooling",
    "Ice Rink Refrigeration Plant",
    "Swimming Pool Water Treatment",
]

# ── PRINTING & PACKAGING ──────────────────────────────────────────────────────
PRINTING_PACKAGING = [
    "Gravure Printing Cylinder Engraver",
    "Offset Lithography Press Register Control",
    "Digital Inkjet Web Press",
    "Carton Erecting and Gluing Machine",
    "Shrink Sleeve Label Applicator",
    "Case Packing and Palletizing Robot",
    "Stretch Wrap Turntable Palletizer",
    "Polypropylene Strapping Machine",
    "Heat Seal Continuous Band Sealer",
    "Modified Atmosphere Packaging (MAP)",
    "Blister Card Punching Machine",
    "Label Printing and Apply (LPA)",
    "Corrugated Box Slotter and Die-Cutter",
    "Vacuum Skin Packaging (VSP) Line",
    "Induction Seal Liner Applicator",
]

# ── TEXTILE & FIBRE ────────────────────────────────────────────────────────────
TEXTILE_FIBRE = [
    "Ring Spinning Frame Tension Control",
    "Open-End Rotor Spinning Machine",
    "Warp Beam Sectional Warping",
    "Rapier Loom Weave Control",
    "Tufting Machine Speed Regulation",
    "Stenter Frame Temperature Profile",
    "Continuous Dyeing Range (Pad-Dry)",
    "Mercerization Chain Unit",
    "Needle Felt Needle Board Press",
    "Nonwoven Hydroentanglement Line",
    "Filament Winding Machine",
    "Braiding Machine Speed Synchronizer",
    "Air-Jet Texturizing Machine",
    "Sizing Machine Warp Tension",
    "Carbon Fibre Oxidation Oven",
]

# ── PAPER & PULP ───────────────────────────────────────────────────────────────
PAPER_PULP = [
    "Continuous Digester Liquor Impregnation",
    "Brownstock Washer Train",
    "Bleach Plant Chlorine Dioxide Stage",
    "Headbox Slice Opening Control",
    "Press Section Nip Load Control",
    "Dryer Section Steam and Condensate",
    "Coating Kitchen Colour Mixer",
    "Calender Stack Nip Pressure",
    "Reel Drum Winding Tension",
    "Broke Chest Level Regulation",
    "Chip Screen and Conveyor",
    "White Water Disc Filter",
    "Pulp Refiner Specific Energy",
    "Recovery Boiler Black Liquor Firing",
    "Lime Kiln Rotary Inclinometer",
]

# ── ROBOTICS & MOTION ──────────────────────────────────────────────────────────
ROBOTICS_MOTION = [
    "Delta Robot Pick-and-Place",
    "SCARA Robot Assembly Cell",
    "Cartesian Gantry Loader",
    "Linear Motor Transport System",
    "Servo Press Force-Position Control",
    "Coordinated Multi-Axis Synchronizer",
    "Cobot Force-Torque Limiting",
    "CNC Grinding Wheel Dresser",
    "Five-Axis CNC Machining Centre",
    "Robotic Deburring and Polishing",
    "Robotic Vision Guided Bin Picking",
    "Automated Storage Retrieval Crane",
    "High-Bay Warehouse Shuttle System",
    "AMR Fleet Traffic Management",
    "Robotic Pipe Crawler Inspection",
]

# ── OIL & GAS (surface/midstream only) ────────────────────────────────────────
OIL_GAS = [
    "Wellhead Christmas Tree Safety Valve",
    "Multiphase Flow Meter",
    "Gas Compressor Station Controller",
    "Pipeline Pig Launching Receiver",
    "Separator Three-Phase Level Control",
    "Gas Dehydration TEG Contactor",
    "LPG Fractionation Column",
    "Crude Oil Metering Skid",
    "Gas Lift Injection Manifold",
    "Subsea Control Module (SCM)",
    "FPSO Cargo Pump Manifold",
    "Flare Knock-out Drum",
    "Natural Gas Pressure Regulating Station",
    "Tank Farm Loading Arm Control",
    "Slug Catcher Inlet Manifold",
]

# ── GLASS & CERAMICS ──────────────────────────────────────────────────────────
GLASS_CERAMICS = [
    "Float Glass Bath Temperature Profile",
    "Glass Container IS Machine Section",
    "Borosilicate Glass Melting Furnace",
    "Glass Fibre Bushing Temperature",
    "Ceramic Spray Dryer Atomizer",
    "Sanitaryware Casting Machine",
    "Porcelain Kiln Firing Curve",
    "Roof Tile Press and Extruder",
    "Fused Silica Drawing Furnace",
    "Ceramic Filter Pressing Cell",
]

# ── RUBBER & PLASTICS ─────────────────────────────────────────────────────────
RUBBER_PLASTICS = [
    "Internal Mixer Banbury Compound",
    "Rubber Extruder Profile Die",
    "Injection Moulding Clamp Force",
    "Thermoforming Sheet Oven",
    "Rotational Moulding Carousel",
    "Blow Moulding Parison Control",
    "PP Film Biaxial Orientation Line",
    "PVC Cable Jacketing Extruder",
    "Rubber Hose Mandrel Winding",
    "Silicone Liquid Injection Moulding",
]

# ── AGRICULTURE & ENVIRONMENT ─────────────────────────────────────────────────
AGRICULTURE_ENVIRONMENT = [
    "Greenhouse Climate Computer",
    "Drip Irrigation Zone Controller",
    "Poultry House Ventilation",
    "Grain Silo Aeration and Monitoring",
    "Aquaculture Dissolved Oxygen Control",
    "Compost Aeration Tunnel",
    "Air Quality Monitoring Station",
    "Noise Barrier Active Control",
    "Soil Remediation Thermal Desorber",
    "River Flow Telemetry RTU",
]

# ── DEFENCE (non-weapons only) ────────────────────────────────────────────────
DEFENCE_NON_WEAPONS = [
    "Military Vehicle Fuel Management",
    "Base HVAC Hardened Shelter",
    "Field Hospital Power Generator",
    "Forward Operating Base Water Purifier",
    "Ammunition Storage Climate Control",
]

# ── ALL DOMAINS (flat list, safe domains only) ────────────────────────────────
ALL_DOMAINS: list[str] = (
    FOOD_BEVERAGE
    + PHARMA_BIOTECH
    + ENERGY_UTILITIES
    + METALS_MINING
    + CHEMICAL_PETROCHEM
    + WATER_WASTEWATER
    + AUTOMOTIVE_TRANSPORT
    + SEMICONDUCTOR_ELECTRONICS
    + BUILDING_HVAC
    + PRINTING_PACKAGING
    + TEXTILE_FIBRE
    + PAPER_PULP
    + ROBOTICS_MOTION
    + OIL_GAS
    + GLASS_CERAMICS
    + RUBBER_PLASTICS
    + AGRICULTURE_ENVIRONMENT
    + DEFENCE_NON_WEAPONS
)

# Domains already well-covered by the cloud swarm (to skip by default)
SKIP_IF_COVERED = {
    "Ampoule Filling",
    "Cheese Vat",
    "Cryogenic Air Separation",
    "Spin Coater",
    "HVDC",
    "Can End",
    "HTST Pasteurization",
    "Aluminium Extrusion",
    "Anaerobic Digester",
    "RO Membrane",
    "Blister",
    "Rotary Cement Kiln",
    "Ice Cream Extrusion",
    "Galvanizing",
    "Wet Wipes",
    "FPSO",
    "Tunnel Boring",
    "Tire Curing",
    "Glass Tempering",
}


def get_domains(skip_covered: bool = True) -> list[str]:
    """Return the domain list, optionally skipping already-covered domains."""
    if not skip_covered:
        return ALL_DOMAINS
    return [
        d for d in ALL_DOMAINS
        if not any(skip in d for skip in SKIP_IF_COVERED)
    ]
