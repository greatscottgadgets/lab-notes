import pcbnew

ORIGIN = (125, 125)
CUTTER_DIAMETER = 1.5
CUTTER_RADIUS = CUTTER_DIAMETER/2

CUT_FEED_RATE = 300.0

Z_CLEARANCE = 10.0
Z_CUT = 0.0

# X offsets from the footprint centre
START_OFFSET = 12
END_OFFSET = 1.575 - CUTTER_RADIUS

pcb = pcbnew.LoadBoard('swg_test_kicad/swg_test.kicad_pcb')

# Lookup coordinates for each set of footprints
# errata: this should've been flipped since we're milling from the back
refs_left = ["J1", "J5", "J6", "J8", "J10", "J12"]
refs_right = ["J2", "J7", "J9", "J11", "J13"]

coords_left = []
for ref in refs_left:
    f = pcb.FindFootprintByReference(ref)
    coords_left.append((f.GetX()/1e6, f.GetY()/1e6))

coords_right = []
for ref in refs_right:
    f = pcb.FindFootprintByReference(ref)
    coords_right.append((f.GetX()/1e6, f.GetY()/1e6))


# Print G-Code preamble
print("G90 G94 G17")
print("G21")
print()
print("S5000 M3")
print("G54")

# Generate G-Code for each slot
for c in coords_left:
    x = c[0] - ORIGIN[0] # swap x direction
    y = ORIGIN[1] - c[1]
    print(f"G00 Z{Z_CLEARANCE}")
    print(f"G00 X{x - START_OFFSET} Y{y}")
    print(f"G01 Z{Z_CUT} F{CUT_FEED_RATE}")
    print(f"G01 X{x + END_OFFSET} F{CUT_FEED_RATE}")
    print(f"G01 Z{Z_CLEARANCE} F{CUT_FEED_RATE}")
    print()
    
# Generate G-Code for each slot
for c in coords_right:
    x = c[0] - ORIGIN[0] # swap x direction
    y = ORIGIN[1] - c[1]
    print(f"G00 Z{Z_CLEARANCE}")
    print(f"G00 X{x + START_OFFSET} Y{y}")
    print(f"G01 Z{Z_CUT} F{CUT_FEED_RATE}")
    print(f"G01 X{x - END_OFFSET} F{CUT_FEED_RATE}")
    print(f"G01 Z{Z_CLEARANCE} F{CUT_FEED_RATE}")
    print()


print("M30")
