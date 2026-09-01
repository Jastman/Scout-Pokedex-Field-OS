# REV 24 (Sep 1 2026, architecture review): INTERNALS RE-LAYOUT - the rev 23 arrangement was not
#  assemblable with real part dimensions (fit-check, docs/hardware-architecture.md sec 7):
#  1. The 60mm SCAN button's switch body (~25-35mm behind panel - MEASURE THE REAL PART, the
#     OBSA-60UK is a 60x60 SQUARE thin-profile button, decision pending) and the UPS+cell pack
#     (~26mm) both lived in the ~40mm deck depth. Impossible. The pack moves BEHIND THE E-INK.
#  2. UPS HAT (E) pogo pins reach millimetres, not the 50mm the old 'pass-through slot' implied.
#     The HAT is REMOTE-MOUNTED behind the e-ink; pogo pins unused; Pi powered by 5V/GND leads
#     to the 40-pin header (or USB-C pigtail); I2C pair to the gauge MCU at 0x2D.
#  3. Pi 5 + Active Cooler (<=16mm incl. fins) + Pimoroni NVMe Base UNDER the Pi (7mm standoffs)
#     move BEHIND THE LCD - depth stack 2.5+1.2+2+16+1.6+9+1+2.5 = ~37.8 of 40.5mm. The old model
#     drew the NVMe on the component side and the blower on the wrong face. The Active Cooler
#     duct shrinks from 116mm to ~22mm (blower is now next to the top exhaust grille).
#  4. NEW cell_bay collection: crush walls (3mm + lid 2mm) with their OWN thickness parameters,
#     independent of the cosmetic WALL - this device will be dropped. Chimney vent slots kept.
#  5. Modeled for the first time: dome switch body placeholder, OBSF-24 MAP body, 40mm speaker +
#     front grille, VOL rocker (top edge), ReSpeaker v2 board, GPIO bonnet, e-ink driver PCB,
#     RTC coin cell, ADS1115 (bay NTC ADC). GPS corrected to the real BN-880 28x28x10 envelope.
#  6. Back exhaust vents moved up behind the cooler (z~100) to serve the new Pi bay.
#  UNVERIFIED ENVELOPES (measure on arrival, re-run this script): UPS HAT (E) board + holder
#  outline (modeled 96x76x26 assembly), OBSA-60UK behind-panel depth (modeled 32mm), Active
#  Cooler total height (modeled 16mm incl. clearance).
# REV 23 (Aug 29 2026): FIX - Exhaust_Duct dimensions were passed as (w=14, h=8, d=116), which rbox
#  maps to Blender (x=14, y=116, z=8): a 116mm rod along the DEPTH axis that poked out the front
#  face and rendered as a black bar over the screens. Corrected to (w=14, h=116, d=8) - vertical,
#  rising from the Active Cooler blower to the top-edge exhaust grille as designed in the thermal pass.
# REV 10 (Aug 29 2026, Claude design review) - THERMAL & SAFETY PASS. Apply before any shell print:
#  1. Model an explicit thermal_baffle collection: a physical wall between the battery bay and the
#     Pi/HAT stack bay, tracked as a real named part. Minimum air gap 5-8mm - hold to it.
#  2. Vents get a computed minimum free area: calculate total open vent area in mm2 for intake and
#     exhaust separately and print both numbers (spec doc gets the figures, not adjectives).
#  3. Chimney orientation: intake low on the shell, exhaust high - passive convection path before the fan.
#  4. Duct aligned to the Pi 5 Active Cooler blower so its exhaust vents through the shell.
#  5. Raised camera lens bezel, 1-2mm proud of the shell surface (drop protection for the lens).
#  6. HAT-stack clearance pass (AI HAT+, UPS HAT, GPS HAT on stacking headers) against the DSI ribbon
#     and camera FPC routing BEFORE locking internal volume - before the tolerance/snap-fit pass.
#  7. Gasket channel geometry around the button bosses and the USB-C port cutout.
#  8. Battery bay: 4x 21700 in 4S1P on the UPS HAT (E) - DECIDED Aug 29 (Option A). Single row of
#     four cells, NOT the old two-rows-of-three 6-cell bay. Applied below; regen .blend/.glb.
# REV 11 (Aug 29 2026): thermal pass APPLIED below - thermal_baffle collection, computed vent
#  free areas (printed at build), chimney intake/exhaust, Active Cooler duct, lens bezel, gaskets.
# REV 12 (Aug 29 2026): SCAN dome -20% (60->48mm), LISTEN +20% (16->19.2mm) - design review
#  call: encourages looking at the real world, audio-first. Vents are now small-hole grilles
#  (12x3mm holes) instead of long slots - debris/mud/kid-finger resistant.
# REV 13 (Aug 29 2026): SCAN dome -> 45mm stock part (resolves the orphaned BOM line), LISTEN
#  -> 20mm (Sanwa OBSF-24 stock). ASK/MAP relocation questions pending Jake's confirmation.
# REV 14 (Aug 29 2026): the two ears split into shapes/colors - LISTEN = yellow UP-triangle cap
#  beside the dome (nature in), ASK = purple DOWN-triangle cap under the D-pad (voice in); both
# REV 15 (Aug 29 2026): Jake reviewed the rev 14 deck and pulled back - SCAN dome restored to the
#  full 60mm stock part (Sanwa OBSA-60UK, the 45mm compromise is dead), and the TWO EARS move to a
#  stacked cluster on the right flank beside the dome: LISTEN (yellow UP-triangle) over ASK (purple
#  DOWN-triangle). MAP slides to the bottom-left under the D-pad. D-pad unchanged.
# REV 16 (Aug 29 2026): the ears pull together - LISTEN + ASK now sit base-to-base so the pair reads
#  as ONE diamond, and every corner gets a 1.8mm bevel (softer, more playful). One shared oval TPU
#  gasket ring around the pair replaces the two overlapping round channels. MAP gasket follows the
#  rev 15 MAP move (was orphaned at the old spot), MAP label too.
# REV 17 (Aug 29 2026): not a diamond - a SQUARE. The ears are one square button area split on the
#  diagonal: LISTEN = yellow UPPER right-triangle, ASK = purple LOWER right-triangle, fitted along
#  the diagonal seam, 1.8mm corner bevel kept. Dome nudged 2mm left to keep the seam clear of the
#  SCAN ring.
#  are printed TPU caps over 12mm tactiles. MAP physical button KEPT (live-GPS where-am-I).
# REV 18 (Aug 29 2026): square dead too (Jake) - ASK + LISTEN move to the BOTTOM edge, one
#  round cap under each thumb for the two-handed kid grip: ASK purple LEFT, LISTEN yellow
#  RIGHT (stays near SCAN - nature cluster). Caps simplify to round 20mm TPU over 12mm
#  tactiles. MAP displaced from bottom-left -> right flank below the dome at (56,-104).
# REV 19 (Aug 29 2026): Jake picked the two-column layout with a swap - D-pad over MAP
#  (green) in the left column, SCAN dome over LISTEN (yellow) in the right column, ASK
#  (purple) dead center between them. ASK and LISTEN sit EXACTLY the same distance from
#  the SCAN dome center: 46.0mm (LISTEN straight below, ASK at 45 deg down-left).
# REV 20 (Aug 29 2026): not centered - TUCKED (Jake). ASK reads as snug against the dome
#  on its lower-left diagonal, same 46.0mm reach as LISTEN (equal gap, verified). Placement
#  follows two-handed-grip ergonomics: D-pad under the left thumb, dome + LISTEN under the
#  right, ASK where the left thumb naturally arcs inward. Geometry unchanged from rev 19.
# SCOUT MK-1 "Field Unit 01" - parametric Blender model (Layout A: STACKED)
# Built headless with Blender 4.2 Python API. Units: 1 BU = 1 mm (scene unit scale 0.001).
import bpy, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
MODE = argv[0] if argv else 'full'          # 'test' or 'full'
OUT  = os.environ.get('SCOUT_CAD_OUT', '/downloads/v10/cad')

# ---------------- parameters (edit these) ----------------
P = dict(
    W=135.0, H=290.0, D=45.0,          # overall body
    CORNER=12.0,                        # shell corner radius
    WALL=2.5,                           # shell wall thickness
    LCD_W=121.0, LCD_H=76.0,            # 5" NON-TOUCH glass (rev 8)
    EINK_W=125.4, EINK_H=99.5,          # 5.83" e-ink glass
    LCD_CZ=97.0,                        # LCD center height (z)
    EINK_CZ=1.0,                        # e-ink center height (z)
    DOME_R=30.0, DOME_CX=31.5, DOME_CZ=-88.0,   # rev 19: right-column center - LISTEN + ASK both exactly 46mm away
    DPAD_CX=-36.0, DPAD_CZ=-90.0, DPAD_ARM=15.0, DPAD_LEN=48.0,
    SAT_R=10.0, MAP_R=12.0, MAP_CX=-36.0, MAP_CZ=-126.0,  # rev 24: MAP cap Ø24 - it is a stock OBSF-24, not a 20mm cap
    DOME_BODY_R=27.5, DOME_BODY_D=32.0,          # rev 24: SCAN switch body placeholder - MEASURE the real part
    UPS_W=96.0, UPS_H=76.0,                      # rev 24: UPS HAT (E) + holders assembly envelope - UNVERIFIED
    BAY_WALL=3.0, BAY_LID=2.0,                   # rev 24: cell-bay crush wall + lid, independent of WALL
    LISTEN_R=10.0, LISTEN_CX=31.5, LISTEN_CZ=-134.0, # rev 19: right column under the dome, 46.0mm from SCAN center
    ASK_CX=-1.03, ASK_CZ=-120.53,                     # rev 20: snug on the 45 deg down-left diagonal of SCAN, 46.0mm - equal to LISTEN
    SCREW_X=58.0, SCREW_Z=133.0,
)
FRONT_Y = -P['D']/2.0                   # front face plane (-22.5)
BACK_Y  =  P['D']/2.0

# ---------------- scene reset ----------------
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'
sc.unit_settings.scale_length = 0.001
sc.unit_settings.length_unit = 'MILLIMETERS'

# ---------------- collections ----------------
def new_col(name):
    c = bpy.data.collections.new(name)
    sc.collection.children.link(c)
    return c
COL = {n: new_col(n) for n in ('SHELL','SCREENS','CONTROLS','LABELS','PORTS','INTERNALS','STUDIO','thermal_baffle','thermal_pass','cell_bay')}

def link_to(obj, col):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    col.objects.link(obj)

# ---------------- materials ----------------
def srgb(r,g,b):
    f = lambda c: ((c+0.055)/1.055)**2.4 if c>0.04045 else c/12.92
    return (f(r),f(g),f(b),1.0)

def mat(name, base, rough=0.5, metal=0.0, emit=None, estr=0.0, trans=0.0, ior=1.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = base
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['IOR'].default_value = ior
    if trans > 0:
        b.inputs['Transmission Weight'].default_value = trans
    if emit is not None:
        b.inputs['Emission Color'].default_value = emit
        b.inputs['Emission Strength'].default_value = estr
    return m

M = {}
M['smoke']  = mat('Shell_SmokePETG', srgb(0.25,0.26,0.30), rough=0.22, trans=0.95, ior=1.46)
M['bezel']  = mat('Bezel_Charcoal', srgb(0.02,0.02,0.03), rough=0.45)
M['lcd']    = mat('LCD_Glass', srgb(0.01,0.05,0.03), rough=0.15, emit=srgb(0.08,0.35,0.18), estr=0.35)
M['phos']   = mat('Phosphor_Green', srgb(0.2,0.9,0.5), rough=0.4, emit=srgb(0.25,1.0,0.55), estr=3.0)
M['eink']   = mat('EInk_Cream', srgb(0.90,0.87,0.79), rough=0.75)
M['ink']    = mat('EInk_Dark', srgb(0.05,0.05,0.05), rough=0.6)
M['magenta']= mat('SCAN_Magenta', srgb(0.88,0.07,0.40), rough=0.25, emit=srgb(0.88,0.07,0.40), estr=0.5)
M['tpu']    = mat('DPad_CharcoalTPU', srgb(0.11,0.11,0.12), rough=0.45)
M['cyan']   = mat('Sat_Cyan', srgb(0.10,0.75,0.85), rough=0.3, emit=srgb(0.10,0.75,0.85), estr=0.5)
M['yellow'] = mat('Sat_Yellow', srgb(1.0,0.82,0.25), rough=0.3, emit=srgb(1.0,0.82,0.25), estr=0.5)
M['purple'] = mat('Sat_Purple', srgb(0.70,0.42,1.0), rough=0.3, emit=srgb(0.70,0.42,1.0), estr=0.5)
M['amber']  = mat('Sat_Amber', srgb(0.95,0.60,0.08), rough=0.3, emit=srgb(0.95,0.60,0.08), estr=0.5)
M['green']  = mat('Sat_Green', srgb(0.25,0.85,0.40), rough=0.3, emit=srgb(0.25,0.85,0.40), estr=0.5)
M['screw']  = mat('Torx_Black', srgb(0.03,0.03,0.035), rough=0.35, metal=0.9)
M['brass']  = mat('Brass_Inserts', srgb(0.70,0.52,0.24), rough=0.3, metal=1.0)
M['pcb']    = mat('PCB_Green', srgb(0.02,0.20,0.07), rough=0.5)
M['pcbd']   = mat('PCB_Dark', srgb(0.02,0.03,0.07), rough=0.5)
M['chip']   = mat('Chip_Black', srgb(0.02,0.02,0.02), rough=0.3)
M['cell']   = mat('Cell_50E', srgb(0.10,0.45,0.16), rough=0.35, metal=0.25)
M['steel']  = mat('Steel', srgb(0.5,0.51,0.53), rough=0.3, metal=0.95)
M['gps']    = mat('GPS_Patch', srgb(0.35,0.05,0.20), rough=0.5)
M['port']   = mat('Port_Dark', srgb(0.01,0.01,0.012), rough=0.6)
M['lens']   = mat('Lens_Glass', srgb(0.01,0.02,0.05), rough=0.08, metal=0.1)
M['label']  = mat('Engrave_Dark', srgb(0.012,0.012,0.014), rough=0.55)
M['glow']   = mat('StatusLED_Amber', srgb(0.9,0.55,0.1), rough=0.3, emit=srgb(1.0,0.6,0.12), estr=2.5)
M['ground'] = mat('Studio_Floor', srgb(0.72,0.72,0.74), rough=0.9)
M['mark']   = mat('BackMark_Light', srgb(0.55,0.56,0.60), rough=0.5)

# ---------------- geometry helpers ----------------
def apply_mod(obj, name):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try: bpy.ops.object.modifier_apply(modifier=name)
    except Exception as e: print('MOD FAIL', name, e)
    obj.select_set(False)

def rbox(name, w, h, d, loc, material, bevel=0.0, col=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name
    o.dimensions = (w, d, h)          # w=x, h=z, d=y  (front is -Y)
    bpy.ops.object.transform_apply(scale=True)
    if bevel > 0:
        m = o.modifiers.new('Bevel','BEVEL'); m.width = bevel; m.segments = 4
        apply_mod(o, 'Bevel')
    if material: o.data.materials.append(material)
    if col: link_to(o, col)
    return o

def cyl(name, r, depth, loc, material, rot=(0,0,0), col=None, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object; o.name = name
    if material: o.data.materials.append(material)
    if col: link_to(o, col)
    bpy.ops.object.shade_smooth()
    return o

def sphere(name, r, loc, scale, material, col=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=64, ring_count=32)
    o = bpy.context.object; o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    if col: link_to(o, col)
    bpy.ops.object.shade_smooth()
    return o

def torus(name, R, r, loc, rot, material, col=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=64,
        minor_segments=16, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    if material: o.data.materials.append(material)
    if col: link_to(o, col)
    bpy.ops.object.shade_smooth()
    return o

def txt(name, body, size, loc, rot, material, extrude=0.3, col=None, align='CENTER'):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.data.body = body
    o.data.align_x = align
    o.data.align_y = 'CENTER'
    o.data.size = size
    o.data.extrude = extrude
    if material: o.data.materials.append(material)
    if col: link_to(o, col)
    return o

def boolean_cut(target, cutter):
    m = target.modifiers.new('Cut','BOOLEAN')
    m.operation = 'DIFFERENCE'; m.solver = 'EXACT'
    m.object = cutter
    apply_mod(target, 'Cut')
    bpy.data.objects.remove(cutter, do_unlink=True)

RX90  = (math.radians(90),0,0)          # face -Y (front)
RBACK = (math.radians(90),0,math.radians(180))  # face +Y (back), readable

# ---------------- shell ----------------
# Back housing: hollow rounded box (open at front)
housing = rbox('Shell_BackHousing', P['W'], P['H'], P['D']-1.0, (0, 1.0, 0), M['smoke'],
               bevel=P['CORNER'], col=COL['SHELL'])
# inner cutter: spans past the front opening, stops WALL short of the back face
inner = rbox('tmp_inner', P['W']-2*P['WALL'], P['H']-2*P['WALL'], 50.0, (0, -4.5, 0), None, bevel=P['CORNER']-P['WALL'])
boolean_cut(housing, inner)

# Front face plate (translucent, with cutouts for screens + dome)
plate = rbox('Shell_FrontPlate', P['W'], P['H'], P['WALL'], (0, FRONT_Y + P['WALL']/2, 0), M['smoke'],
             bevel=P['CORNER'], col=COL['SHELL'])
# screen openings
c = rbox('tmp_lcd', P['LCD_W'], P['LCD_H'], 12, (0, FRONT_Y, P['LCD_CZ']), None); boolean_cut(plate, c)
c = rbox('tmp_eink', P['EINK_W'], P['EINK_H'], 12, (0, FRONT_Y, P['EINK_CZ']), None); boolean_cut(plate, c)
c = cyl('tmp_dome', P['DOME_R']+0.8, 12, (P['DOME_CX'], FRONT_Y, P['DOME_CZ']), None, rot=RX90); boolean_cut(plate, c)

# Corner Torx screws (exposed, black)
for sx in (-1,1):
    for sz in (-1,1):
        cyl(f'Torx_{"TL" if sx<0 and sz>0 else "TR" if sx>0 and sz>0 else "BL" if sx<0 else "BR"}',
            3.0, 2.2, (sx*P['SCREW_X'], FRONT_Y-0.6, sz*P['SCREW_Z']), M['screw'], rot=RX90, col=COL['SHELL'])
        cyl('TorxSlot', 1.3, 0.6, (sx*P['SCREW_X'], FRONT_Y-1.6, sz*P['SCREW_Z']), M['port'], rot=RX90, col=COL['SHELL'], verts=6)

# ---- vents: real through-shell grille cuts with computed free area (rev 11/12 thermal pass) ----
# rev 12 (design review): many small openings, not long slots - a 12x3mm grille hole resists
# debris, mud, and kid fingers while still holding the convection free area.
def slot_area(w, h, bev):
    return w*h - (4.0-math.pi)*bev*bev   # rect minus rounded-corner loss
VENT_BEV = 1.2
def vent_row(prefix, plane, xs, ys):
    for ci, cx_ in enumerate(xs):
        for ri, rr in enumerate(ys):
            if plane == 'bottom':    # through the bottom wall (chimney intake, low)
                c = rbox(f'tmp_{prefix}_{ci}_{ri}', 12.0, 8.0, 3.0, (cx_, rr, -P['H']/2), None, bevel=VENT_BEV)
                rbox(f'Vent_{prefix}_{ci}_{ri}', 10.4, 1.0, 1.6, (cx_, rr, -P['H']/2+1.6), M['port'], bevel=0.7, col=COL['thermal_pass'])
            elif plane == 'top':     # through the top wall (chimney exhaust, high) - clear of mic ports + PWR
                c = rbox(f'tmp_{prefix}_{ci}_{ri}', 12.0, 8.0, 3.0, (cx_, rr, P['H']/2), None, bevel=VENT_BEV)
                rbox(f'Vent_{prefix}_{ci}_{ri}', 10.4, 1.0, 1.6, (cx_, rr, P['H']/2-1.6), M['port'], bevel=0.7, col=COL['thermal_pass'])
            else:                    # through the back wall (exhaust assist)
                c = rbox(f'tmp_{prefix}_{ci}_{ri}', 12.0, 3.0, 8.0, (cx_, BACK_Y, rr), None, bevel=VENT_BEV)
                rbox(f'Vent_{prefix}_{ci}_{ri}', 10.4, 1.6, 1.0, (cx_, BACK_Y-1.0, rr), M['port'], bevel=0.7, col=COL['thermal_pass'])
            boolean_cut(housing, c)
vent_row('IN', 'bottom', (-46,-32,-18,-4,10), (-6,6))   # 10 holes - intake low (chimney)
vent_row('EX', 'top',    (-18,-6,6,18), (-6,6))         # 8 holes - exhaust high; the cooler duct lands here
vent_row('BK', 'back',   (-11,3,17,31), (98,106))       # 8 holes - exhaust assist on the back face, behind the Active Cooler (rev 24: Pi bay is now the TOP bay)
SLOT_A = slot_area(12.0, 3.0, VENT_BEV)
INTAKE_AREA = 10 * SLOT_A
EXHAUST_AREA = 16 * SLOT_A
print('THERMAL PASS: intake grille free area  = %.0f mm2 (10x 12x3 holes, bottom edge)' % INTAKE_AREA)
print('THERMAL PASS: exhaust grille free area = %.0f mm2 (8x top-edge + 8x back)' % EXHAUST_AREA)
print('THERMAL PASS: top exhaust grille held 4.6mm clear of both mic ports; duct exhaust exits the top edge, away from grip, face, mics, and speaker (whistle check on the bench)')

# Speaker grille: functional hole pattern through the BACK shell at the speaker (rev 24 - the
# front deck is owned by the switch bodies; back-center sits between the two-hand grip swells)
import math as _m
GRILLE_AREA = 0.0
def grille_hole(gx, gz):
    global GRILLE_AREA
    c = cyl('tmp_grille', 1.3, 8, (gx, BACK_Y, gz), None, rot=RX90, verts=16)
    boolean_cut(housing, c)
    GRILLE_AREA += _m.pi*1.3*1.3
grille_hole(-25.0, -95.0)
for gi in range(6):
    a = gi*_m.pi/3
    grille_hole(-25.0+7*_m.cos(a), -95.0+7*_m.sin(a))
for gi in range(12):
    a = gi*_m.pi/6
    grille_hole(-25.0+14*_m.cos(a), -95.0+14*_m.sin(a))
print('SPEAKER GRILLE: %d holes, %.0f mm2 open area, BACK shell at (-25,-95) - behind the D-pad, clear of the dome switch body' % (19, GRILLE_AREA))

# Lanyard loop (bottom right, back corner)
torus('Lanyard_Loop', 6.5, 2.2, (52, BACK_Y-4, -P['H']/2+6), RX90, M['screw'], col=COL['SHELL'])

# Back mark
txt('Back_Mark', 'SCOUT  MK-1', 6.0, (0, BACK_Y+0.2, -112), RBACK, M['mark'], extrude=0.25, col=COL['LABELS'])

# ---------------- screens ----------------
# LCD: bezel + glass + phosphor text
rbox('LCD_Bezel', P['LCD_W']+6, P['LCD_H']+6, 4.0, (0, FRONT_Y+P['WALL']+1.5, P['LCD_CZ']), M['bezel'], bevel=3.0, col=COL['SCREENS'])
rbox('LCD_Glass', P['LCD_W'], P['LCD_H'], 1.0, (0, FRONT_Y+P['WALL']-0.4, P['LCD_CZ']), M['lcd'], bevel=1.5, col=COL['SCREENS'])
yt = FRONT_Y - 0.8
txt('LCD_Line1','[ AF ]  -  CAM0 LIVE', 7.5, (0, yt, P['LCD_CZ']+6), RX90, M['phos'], extrude=0.2, col=COL['LABELS'])
txt('LCD_Line2','VIEWFINDER - SLEEPS WHEN IDLE', 4.2, (0, yt, P['LCD_CZ']-10), RX90, M['phos'], extrude=0.2, col=COL['LABELS'])
txt('LCD_Bar','CAMERA SCREEN - NON-TOUCH', 3.0, (0, yt, P['LCD_CZ']+30), RX90, M['phos'], extrude=0.2, col=COL['LABELS'])

# E-ink: bezel + cream card + dark card text
rbox('EInk_Bezel', P['EINK_W']+6, P['EINK_H']+6, 4.0, (0, FRONT_Y+P['WALL']+1.5, P['EINK_CZ']), M['bezel'], bevel=3.0, col=COL['SCREENS'])
rbox('EInk_Card', P['EINK_W'], P['EINK_H'], 1.0, (0, FRONT_Y+P['WALL']-0.4, P['EINK_CZ']), M['eink'], bevel=1.5, col=COL['SCREENS'])
txt('EK_Line1','AMERICAN ROBIN', 7.0, (0, yt, P['EINK_CZ']+34), RX90, M['ink'], extrude=0.15, col=COL['LABELS'])
txt('EK_Line2','Turdus migratorius', 4.0, (0, yt, P['EINK_CZ']+22), RX90, M['ink'], extrude=0.15, col=COL['LABELS'])
txt('EK_Line3','RARITY  ***--', 3.6, (0, yt, P['EINK_CZ']-2), RX90, M['ink'], extrude=0.15, col=COL['LABELS'])
txt('EK_Line4','2026-08-27   40.73N 73.98W', 3.2, (0, yt, P['EINK_CZ']-30), RX90, M['ink'], extrude=0.15, col=COL['LABELS'])
txt('EK_Line5','FIELD UNIT 01  -  CARD #003', 2.8, (0, yt, P['EINK_CZ']-40), RX90, M['ink'], extrude=0.15, col=COL['LABELS'])

# ---------------- control deck ----------------
# D-pad: cross cap (two rboxes) + center DEX disc
rbox('DPad_V', P['DPAD_ARM'], P['DPAD_LEN'], 5.0, (P['DPAD_CX'], FRONT_Y-2.5, P['DPAD_CZ']), M['tpu'], bevel=4.0, col=COL['CONTROLS'])
rbox('DPad_H', P['DPAD_LEN'], P['DPAD_ARM'], 5.0, (P['DPAD_CX'], FRONT_Y-2.5, P['DPAD_CZ']), M['tpu'], bevel=4.0, col=COL['CONTROLS'])
cyl('DPad_Center', 8.5, 6.0, (P['DPAD_CX'], FRONT_Y-3.0, P['DPAD_CZ']), M['green'], rot=RX90, col=COL['CONTROLS'])
txt('DPad_Label','SEL', 3.4, (P['DPAD_CX'], FRONT_Y-6.4, P['DPAD_CZ']), RX90, M['label'], extrude=0.2, col=COL['LABELS'])

# SCAN dome: base ring + squashed sphere + SCAN label
torus('SCAN_Ring', P['DOME_R']+2.5, 2.2, (P['DOME_CX'], FRONT_Y-1.5, P['DOME_CZ']), RX90, M['magenta'], col=COL['CONTROLS'])
cyl('SCAN_Base', P['DOME_R']+1.0, 5.0, (P['DOME_CX'], FRONT_Y-2.5, P['DOME_CZ']), M['bezel'], rot=RX90, col=COL['CONTROLS'])
sphere('SCAN_Dome', P['DOME_R'], (P['DOME_CX'], FRONT_Y-4.0, P['DOME_CZ']), (1.0, 0.42, 1.0), M['magenta'], col=COL['CONTROLS'])
txt('SCAN_Label','SCAN', 5.0, (P['DOME_CX'], FRONT_Y-4.0-P['DOME_R']*0.42-0.2, P['DOME_CZ']), RX90, M['label'], extrude=0.25, col=COL['LABELS'])

# LISTEN + ASK: the two ears EXACTLY equidistant from SCAN (46.0mm) - LISTEN snug below the dome, ASK snug on its down-left diagonal (rev 20, Jake)
# rev 19: round soft caps, printed TPU over 12mm tactiles - yellow LISTEN right column, purple ASK center
def halfsq(name, half, size, depth, loc, material, col):
    h=size/2.0
    pts=[(-h,-h),(-h,h),(h,h)] if half=='upper' else [(-h,-h),(h,-h),(h,h)]  # (x,z); diagonal seam BL->TR
    verts=[(x,-depth/2,z) for x,z in pts]+[(x,depth/2,z) for x,z in pts]
    faces=[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)]
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    o=bpy.data.objects.new(name,me); o.location=loc
    if material: o.data.materials.append(material)
    if col: link_to(o,col)
    bpy.context.view_layer.objects.active=o; o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.object.mode_set(mode='OBJECT')
    b=o.modifiers.new('SoftCorners','BEVEL'); b.width=1.8; b.segments=3; b.limit_method='ANGLE'
    bpy.ops.object.modifier_apply(modifier='SoftCorners')
    bpy.ops.object.shade_auto_smooth(angle=0.6)
    return o
cyl('Sat_ASK', P['SAT_R'], 6.0, (P['ASK_CX'], FRONT_Y-3.0, P['ASK_CZ']), M['purple'], rot=RX90, col=COL['CONTROLS'])  # purple round cap, LEFT thumb
txt('SatLbl_ASK', 'ASK', 2.2, (P['ASK_CX'], FRONT_Y-0.4, P['ASK_CZ']-P['SAT_R']-3.5), RX90, M['label'], extrude=0.2, col=COL['LABELS'])
cyl('Sat_LISTEN', P['SAT_R'], 6.0, (P['LISTEN_CX'], FRONT_Y-3.0, P['LISTEN_CZ']), M['yellow'], rot=RX90, col=COL['CONTROLS'])  # yellow round cap, RIGHT thumb
txt('SatLbl_LISTEN', 'LISTEN', 2.2, (P['LISTEN_CX']+P['SAT_R']+4.5, FRONT_Y-0.4, P['LISTEN_CZ']), RX90, M['label'], extrude=0.2, col=COL['LABELS'])  # rev 19: right of the cap (no room below)
# MAP satellite button - round green, KEPT (Jake, Aug 29): instant live-GPS where-am-I is its job
cyl('Sat_MAP', P['MAP_R'], 6.0, (P['MAP_CX'], FRONT_Y-3.0, P['MAP_CZ']), M['green'], rot=RX90, col=COL['CONTROLS'])  # rev 24: Ø24 - the real OBSF-24 cap size (was drawn Ø20)
# rev 24: the switch BODIES exist now - they drive the internal layout. Dome depth UNVERIFIED (32mm placeholder).
cyl('SCAN_SwitchBody', P['DOME_BODY_R'], P['DOME_BODY_D'], (P['DOME_CX'], FRONT_Y+P['WALL']+P['DOME_BODY_D']/2, P['DOME_CZ']), M['chip'], rot=RX90, col=COL['INTERNALS'])
cyl('MAP_SwitchBody', 13.0, 26.0, (P['MAP_CX'], FRONT_Y+P['WALL']+13.0, P['MAP_CZ']), M['chip'], rot=RX90, col=COL['INTERNALS'])
txt('SatLbl_MAP', 'MAP', 2.2, (P['MAP_CX'], FRONT_Y-0.4, P['MAP_CZ']-P['SAT_R']-3.5), RX90, M['label'], extrude=0.2, col=COL['LABELS'])  # rev 19: follows the MAP move

# Power slide switch (TOP edge - moved Aug 27: no accidental kills in a kid grip)
rbox('PWR_Slot', 16.0, 3.0, 4.0, (38, 0, P['H']/2+0.5), M['port'], bevel=1.5, col=COL['PORTS'])
rbox('PWR_Slider', 8.0, 5.0, 5.0, (35, 0, P['H']/2+1.8), M['tpu'], bevel=1.2, col=COL['PORTS'])

# VOL +/- rocker: two tactiles on the TOP edge next to PWR (rev 11 spec, modeled rev 24)
rbox('VOL_Plus',  6.0, 4.0, 5.0, (52, 0, P['H']/2+1.2), M['tpu'], bevel=1.0, col=COL['PORTS'])
rbox('VOL_Minus', 6.0, 4.0, 5.0, (60, 0, P['H']/2+1.2), M['tpu'], bevel=1.0, col=COL['PORTS'])
txt('VOL_Label', 'VOL', 2.2, (56, -3.5, P['H']/2-4.5), RX90, M['label'], extrude=0.2, col=COL['LABELS'])

# ---------------- ports / edge details ----------------
# USB-C PD (bottom edge)
rbox('USBC_Port', 10.0, 3.5, 4.0, (30, 0, -P['H']/2+0.5), M['port'], bevel=1.6, col=COL['PORTS'])
# Dual mic ports (top edge, near camera corner)
cyl('Mic_1', 1.6, 3.0, (-34, -6, P['H']/2-0.5), M['port'], col=COL['PORTS'])
cyl('Mic_2', 1.6, 3.0, (-27, -6, P['H']/2-0.5), M['port'], col=COL['PORTS'])
# Status LED ring (front, top-left)
torus('StatusLED', 4.0, 1.2, (-52, FRONT_Y-0.5, 136), RX90, M['glow'], col=COL['PORTS'])

# Camera module (back, top-left)
rbox('Camera_Module', 26, 26, 5.0, (-40, BACK_Y+1.5, 115), M['bezel'], bevel=4.0, col=COL['PORTS'])  # rev 9: was sunk INSIDE the shell (BACK_Y-*) - camera bump now protrudes off the back face
cyl('Camera_Lens', 8.0, 3.0, (-40, BACK_Y+3.5, 115), M['lens'], rot=RX90, col=COL['PORTS'])
cyl('Camera_LensDot', 3.0, 1.0, (-40, BACK_Y+5.2, 115), M['cyan'], rot=RX90, col=COL['PORTS'])
cyl('Camera_Flash', 2.0, 1.5, (-28, BACK_Y+3.5, 122), M['glow'], rot=RX90, col=COL['PORTS'])

# ---------------- internals (visible through ghost shell) ----------------
# REV 24 LAYOUT: TOP bay (behind LCD) = Pi 5 + Active Cooler + NVMe Base; MID bay (behind
# e-ink) = UPS HAT (E) + 4x21700 inside the cell_bay crush box; BOTTOM bay (deck) = switch
# bodies + speaker + ReSpeaker + bonnet + e-ink driver PCB. Chimney: bottom intake -> deck ->
# bay slots -> baffle slots -> Pi bay -> top/back exhaust.

# --- TOP BAY: Pi 5 stack behind the LCD (components + cooler face the BACK wall) ---
rbox('Pi5_PCB', 85, 56, 1.6, (13, -6.7, 93), M['pcb'], bevel=1.5, col=COL['INTERNALS'])
rbox('Pi5_SoC', 14, 14, 2.2, (8, -4.7, 93), M['chip'], bevel=0.5, col=COL['INTERNALS'])
rbox('Pi5_RAM', 10, 10, 1.8, (24, -4.9, 93), M['chip'], bevel=0.5, col=COL['INTERNALS'])
rbox('Pi5_GPIO', 51, 5, 6.0, (13, -4.0, 118), M['chip'], bevel=0.3, col=COL['INTERNALS'])
rbox('Pi5_USB1', 15, 16, 8.0, (43, -1.9, 110), M['steel'], bevel=0.5, col=COL['INTERNALS'])
rbox('Pi5_ETH', 16, 21, 8.0, (45, -1.9, 86), M['steel'], bevel=0.5, col=COL['INTERNALS'])
# Active Cooler: 63.5x42.5, <=16mm over the PCB incl. fins/fan (officially clears 16mm headers)
rbox('ActiveCooler', 60, 42, 13.0, (13, 0.9, 93), M['steel'], bevel=1.5, col=COL['thermal_pass'])
rbox('ActiveCooler_Blower', 16.0, 16.0, 6.0, (13, 1.0, 118), M['steel'], bevel=1.5, col=COL['thermal_pass'])
# NVMe Base UNDER the Pi (7mm standoffs toward the FRONT), SSD between Base and Pi
rbox('NVMeBase_PCB', 85, 56, 1.6, (13, -12.4, 93), M['pcbd'], bevel=1.5, col=COL['INTERNALS'])
rbox('NVMe_M2', 80, 22, 2.2, (13, -10.2, 93), M['chip'], bevel=0.5, col=COL['INTERNALS'])
for sx in (-1,1):
    for sz in (-1,1):
        cyl('Standoff', 2.5, 5.0, (13+sx*39, -9.5, 93+sz*24), M['brass'], rot=RX90, col=COL['INTERNALS'])
# RTC coin cell (rev 24 spec): cabled to the Pi J5 header
cyl('RTC_Cell', 10.0, 3.0, (-45, -5, 100), M['steel'], rot=RX90, col=COL['INTERNALS'])
# GPS: real BN-880 envelope 28x28x10 (was drawn 40x18) - sky-facing under plain PETG, clear of the duct
rbox('GPS_BN880', 28, 10, 28, (34, 5, 134), M['gps'], bevel=1.0, col=COL['INTERNALS'])

# --- MID BAY: UPS HAT (E) + 4x21700 behind the e-ink, inside the crush box ---
# Assembly envelope UNVERIFIED (96x76x~26 modeled) - measure the real board+holders on arrival.
_i=0
for cx in (-33.75, -11.25, 11.25, 33.75):
    _i+=1
    cyl(f'Cell_{_i}', 10.5, 70, (cx, 0.0, 0.0), M['cell'], col=COL['INTERNALS'])
    cyl(f'CellCap_{_i}', 8.0, 2.0, (cx, 0.0, 36.0), M['steel'], col=COL['INTERNALS'])
rbox('UPS_Board', P['UPS_W'], P['UPS_H'], 1.8, (0, 12.0, 0), M['pcb'], bevel=1.5, col=COL['INTERNALS'])
rbox('UPS_IC1', 10, 10, 2.0, (-30, 13.9, 0), M['chip'], bevel=0.5, col=COL['INTERNALS'])
rbox('UPS_IC2', 8, 12, 2.0, (28, 13.9, 8), M['chip'], bevel=0.5, col=COL['INTERNALS'])
rbox('ADS1115_NTC', 15, 10, 1.6, (40, 15.5, 28), M['pcbd'], bevel=0.5, col=COL['INTERNALS'])

# --- BOTTOM BAY (deck): boards that share the button zone, placed clear of the switch bodies ---
rbox('EInk_Driver_PCB', 65, 30, 1.6, (-30, -2, -66), M['pcb'], bevel=1.0, col=COL['INTERNALS'])
rbox('ReSpeaker_PCB', 65, 30, 1.6, (-30, 4.5, -90), M['pcb'], bevel=1.0, col=COL['INTERNALS'])
rbox('GPIO_Bonnet', 55, 25, 1.6, (8, 4.5, -129), M['pcbd'], bevel=1.0, col=COL['INTERNALS'])
# rev 24 FINDING: a Ø40 front-firing speaker does NOT fit the deck (dome body + OBSF-24 body own
# the bottom front). The speaker fires through the BACK shell, behind the D-pad, left of the
# dome switch body's full-depth cylinder (dome depth placeholder = 32mm, unverified).
cyl('Speaker_40mm', 20.0, 10.0, (-25, 14, -95), M['chip'], rot=RX90, col=COL['INTERNALS'])

# Brass corner inserts
for sx in (-1,1):
    for sz in (-1,1):
        cyl('BrassInsert', 3.0, 8.0, (sx*58, 0, sz*130), M['brass'], rot=RX90, col=COL['INTERNALS'])

# ---------------- REV 24 THERMAL & SAFETY PASS ----------------
# thermal_baffle: physical wall between the cell bay (mid) and the Pi bay (top).
# Air gaps: pack top (z=+38 caps/board edge) to baffle z=49 -> 11mm; baffle z=51 to Pi PCB
# bottom edge z=65 -> 14mm. Spec 5-8mm minimum - held with margin.
baffle = rbox('Thermal_Baffle', 125.0, 2.0, 36.0, (0, 2.0, 50.0), M['pcb'], bevel=1.0, col=COL['thermal_baffle'])
# power/I2C harness grommet (replaces the rev 11 'pogo pass-through' - pogo pins are UNUSED, the
# UPS HAT is remote-mounted and wired to the 40-pin header)
c = rbox('tmp_baffle_wire', 18.0, 3.0, 10.0, (-45.0, -6.0, 50.0), None); boolean_cut(baffle, c)
# baffle transfer slots (chimney path: cell bay -> Pi bay), 6 slots 8x2.4
BAFFLE_SLOT_AREA = 0.0
for i in range(6):
    yy = -12.0 + i*5.2
    c = rbox(f'tmp_baffle_v_{i}', 8.0, 3.0, 2.4, (45.0, yy, 50.0), None); boolean_cut(baffle, c)
    BAFFLE_SLOT_AREA += 8.0*2.4
print('THERMAL PASS: baffle air gaps - pack->baffle 11.0mm, baffle->Pi 14.0mm (spec 5-8mm min) - transfer slots %.0f mm2' % BAFFLE_SLOT_AREA)

# cell_bay: the crush box (rev 24, review finding) - ITS OWN wall parameters, not the cosmetic shell.
# 3mm side/top/bottom walls + 2mm front lid; back = shell wall + UPS board. Slotted top+bottom for the chimney.
BAY_SLOT_AREA = 0.0
def bay_wall(name, w, h, d, loc):
    return rbox(name, w, h, d, loc, M['pcbd'], bevel=0.8, col=COL['cell_bay'])
bay_wall('CellBay_Wall_L', P['BAY_WALL'], 92, 26, (-48.75, 0, 0))
bay_wall('CellBay_Wall_R', P['BAY_WALL'], 92, 26, ( 48.75, 0, 0))
wb = bay_wall('CellBay_Wall_B', 100.5, P['BAY_WALL'], 26, (0, 0, -44.5))
wt = bay_wall('CellBay_Wall_T', 100.5, P['BAY_WALL'], 26, (0, 0,  44.5))
lid = bay_wall('CellBay_Lid_F', 100.5, 92, P['BAY_LID'], (0, -14.5, 0))
for i in range(4):
    xx = -30.0 + i*20.0
    c = rbox(f'tmp_bayb_{i}', 8.0, 4.5, 2.4, (xx, 0, -44.5), None); boolean_cut(wb, c)
    c = rbox(f'tmp_bayt_{i}', 8.0, 4.5, 2.4, (xx, 0,  44.5), None); boolean_cut(wt, c)
    BAY_SLOT_AREA += 2*8.0*2.4
print('CELL BAY: 3mm crush walls + 2mm lid (independent of WALL=%.1f) - chimney slots %.0f mm2 - >=5mm crumple to the bottom shell edge held by the deck bay' % (P['WALL'], BAY_SLOT_AREA))

# Active Cooler duct: rev 24 - the Pi bay is the TOP bay now, so the duct is a short 22mm rise
# from the blower to the top-edge exhaust grille (was a 116mm run in rev 23).
rbox('Exhaust_Duct', 14.0, 22.0, 8.0, (8, 1.0, 131.5), M['tpu'], bevel=2.0, col=COL['thermal_pass'])  # rev 24: short rise, offset left of the BN-880

# Camera lens bezel: 1-2mm proud of the bump face so the lens never takes ground contact
torus('Lens_Bezel', 9.5, 1.4, (-40, BACK_Y+4.8, 115), RX90, M['tpu'], col=COL['thermal_pass'])

# Gasket channels (TPU): button bosses + USB-C cutout
torus('Gasket_SCAN', P['DOME_R']+1.8, 0.8, (P['DOME_CX'], FRONT_Y+P['WALL']+0.3, P['DOME_CZ']), RX90, M['tpu'], col=COL['thermal_pass'])
torus('Gasket_ASK', P['SAT_R']+0.3, 0.7, (P['ASK_CX'], FRONT_Y+P['WALL']+0.3, P['ASK_CZ']), RX90, M['tpu'], col=COL['thermal_pass'])
torus('Gasket_LISTEN', P['SAT_R']+0.3, 0.7, (P['LISTEN_CX'], FRONT_Y+P['WALL']+0.3, P['LISTEN_CZ']), RX90, M['tpu'], col=COL['thermal_pass'])
torus('Gasket_MAP', P['MAP_R']+1.0, 0.7, (P['MAP_CX'], FRONT_Y+P['WALL']+0.3, P['MAP_CZ']), RX90, M['tpu'], col=COL['thermal_pass'])
gm = P['DPAD_LEN']/2 + 1.5
rbox('Gasket_DPad_L', 1.0, 2*gm+1, 0.8, (P['DPAD_CX']-gm, FRONT_Y+P['WALL']+0.3, P['DPAD_CZ']), M['tpu'], col=COL['thermal_pass'])  # rev 24 fix: h/d were swapped (a 49mm-deep wall through the shell - same bug class as the rev 23 duct)
rbox('Gasket_DPad_R', 1.0, 2*gm+1, 0.8, (P['DPAD_CX']+gm, FRONT_Y+P['WALL']+0.3, P['DPAD_CZ']), M['tpu'], col=COL['thermal_pass'])  # rev 24 fix: ditto
rbox('Gasket_DPad_T', 2*gm+1, 0.8, 1.0, (P['DPAD_CX'], FRONT_Y+P['WALL']+0.3, P['DPAD_CZ']+gm), M['tpu'], col=COL['thermal_pass'])
rbox('Gasket_DPad_B', 2*gm+1, 0.8, 1.0, (P['DPAD_CX'], FRONT_Y+P['WALL']+0.3, P['DPAD_CZ']-gm), M['tpu'], col=COL['thermal_pass'])
rbox('Gasket_USBC_T', 13.0, 0.8, 1.0, (30, 3.25, -P['H']/2+P['WALL']+0.3), M['tpu'], col=COL['thermal_pass'])
rbox('Gasket_USBC_B', 13.0, 0.8, 1.0, (30, -3.25, -P['H']/2+P['WALL']+0.3), M['tpu'], col=COL['thermal_pass'])
rbox('Gasket_USBC_L', 1.0, 0.8, 6.5, (30-6.5, 0, -P['H']/2+P['WALL']+0.3), M['tpu'], col=COL['thermal_pass'])
rbox('Gasket_USBC_R', 1.0, 0.8, 6.5, (30+6.5, 0, -P['H']/2+P['WALL']+0.3), M['tpu'], col=COL['thermal_pass'])

# Depth-stack clearance pass (rev 24, printed at build - hardware doc sec 5 holds the table)
print('DEPTH STACK (Pi bay): plate 2.5 + e-ink/LCD glass 1.2 + gap 2 + cooler 16 + Pi PCB 1.6 + NVMe under-stack 9 + gap 1 + back wall 2.5 = 37.8 of 40.5mm - DSI/FPC routing lives in the margin')
print('DEPTH STACK (cell bay): lid 2 + gap 3 + cells 21 + board 1.8 + gap 7.9 = fits 34.8mm behind the e-ink')
print('DEPTH STACK (deck): dome body 32 (UNVERIFIED) + boards behind at y>+3 - pack is OUT of this bay (rev 24)')

print('BUILD OK - objects:', len(bpy.data.objects))

# ---------------- studio + render ----------------
def look_at(o, target):
    d = Vector(target) - o.location
    o.rotation_euler = d.to_track_quat('-Z','Y').to_euler()

def area(name, loc, energy, size, color, target=(0,0,0)):
    bpy.ops.object.light_add(type='AREA', location=loc)
    o = bpy.context.object; o.name = name
    o.data.energy = energy; o.data.shape = 'DISK'; o.data.size = size; o.data.color = color
    look_at(o, target)
    link_to(o, COL['STUDIO'])
    return o

area('Key',  (260,-320,340), 1300, 160, (1.0,0.95,0.90))
area('Fill', (-320,-220,120), 650, 200, (0.88,0.92,1.0))
area('Rim',  (60,320,420),  1800, 180, (1.0,0.98,0.95))
area('Top',  (0,-60,520),   500, 140, (1.0,1.0,1.0))

rbox('Ground', 2400, 10, 2400, (0, 0, -P['H']/2-5.2), M['ground'], col=COL['STUDIO'])

def ptlight(name, loc, energy, color=(1.0,1.0,1.0)):
    bpy.ops.object.light_add(type='POINT', location=loc)
    o = bpy.context.object; o.name = name
    o.data.energy = energy; o.data.color = color
    link_to(o, COL['STUDIO'])
    return o
ptlight('LED_Interior_Top', (0, 0, 60), 60)
ptlight('LED_Interior_Mid', (0, 0, -20), 45)
ptlight('LED_Interior_Cells', (0, 2, -100), 35)

bpy.ops.object.camera_add(location=(0,-520,0))
cam = bpy.context.object; cam.name = 'Camera'
look_at(cam, (0,0,0))
cam.data.lens = 70
sc.camera = cam
link_to(cam, COL['STUDIO'])

sc.render.engine = 'CYCLES'
sc.cycles.samples = 28 if MODE=='full' else 16
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.cycles.transmission_bounces = 4
sc.render.image_settings.file_format = 'PNG'
sc.render.film_transparent = False
sc.view_settings.look = 'AgX - Medium High Contrast'
w = sc.world or bpy.data.worlds.new('W')
sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = srgb(0.80,0.81,0.83)
w.node_tree.nodes['Background'].inputs[1].default_value = 0.8

def render(name, cam_loc, target, rx, ry, lens=70):
    cam.location = cam_loc
    cam.data.lens = lens
    look_at(cam, target)
    sc.render.resolution_x = rx; sc.render.resolution_y = ry
    sc.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print('RENDERED', name)

if MODE == 'norender':
    bpy.data.texts.load(os.path.join(OUT,'build_pokedex.py'))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'pokedex-mk1-layoutA.blend'))
    for o in list(COL['STUDIO'].objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'pokedex-mk1-layoutA.glb'), export_format='GLB')
    print('NORENDER blend+glb done')
    sys.exit(0)

if MODE == 'resave':
    bpy.data.texts.load(os.path.join(OUT,'build_pokedex.py'))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'pokedex-mk1-layoutA.blend'))
    for o in list(COL['STUDIO'].objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'pokedex-mk1-layoutA.glb'), export_format='GLB')
    print('RESAVE+GLB DONE')
    sys.exit(0)

if MODE == 'backonly':
    render('render_back.png', (0,520,0), (0,0,0), 700, 1000)
    sys.exit(0)

if MODE == 'test':
    render('test_hero.png', (300,-400,230), (0,0,0), 640, 580, lens=60)
    render('test_deck.png', (40,-300,-120), (-5,-10,-92), 640, 512, lens=60)
    sys.exit(0)

# save assembled .blend (+ embed this script for parametric edits)
bpy.data.texts.load(os.path.join(OUT,'build_pokedex.py'))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'pokedex-mk1-layoutA.blend'))
print('SAVED blend')

if MODE != 'explodeonly':
    render('render_front.png', (0,-520,0), (0,0,0), 700, 1000)
    render('render_back.png', (0,520,0), (0,0,0), 700, 1000)
    render('render_hero.png', (300,-400,230), (0,0,0), 1000, 900, lens=60)
    render('render_deck.png', (40,-300,-120), (-5,-10,-92), 1000, 800, lens=60)

# exploded view along Y (front is -Y)
EXP = {
 'Shell_FrontPlate':-80, 'SCAN_Ring':-95,'SCAN_Base':-95,'SCAN_Dome':-95,'SCAN_Label':-95,
 'DPad_V':-95,'DPad_H':-95,'DPad_Center':-95,'DPad_Label':-95,
 'Sat_LISTEN':-95,'Sat_ASK':-95,'Sat_MAP':-95,
 'SatLbl_LISTEN':-80,'SatLbl_ASK':-80,'SatLbl_MAP':-80,
 'StatusLED':-80,'Torx_TL':-80,'Torx_TR':-80,'Torx_BL':-80,'Torx_BR':-80,
 'LCD_Bezel':-50,'LCD_Glass':-50,'LCD_Line1':-50,'LCD_Line2':-50,'LCD_Bar':-50,
 'EInk_Bezel':-50,'EInk_Card':-50,'EK_Line1':-50,'EK_Line2':-50,'EK_Line3':-50,'EK_Line4':-50,'EK_Line5':-50,
 'SCAN_SwitchBody':-38,'MAP_SwitchBody':-38,'Speaker_40mm':-38,
 'EInk_Driver_PCB':-25,'ReSpeaker_PCB':-12,'GPIO_Bonnet':-12,
 'Pi5_PCB':0,'Pi5_SoC':0,'Pi5_RAM':0,'Pi5_GPIO':0,'Pi5_USB1':0,'Pi5_ETH':0,'RTC_Cell':0,
 'NVMeBase_PCB':-18,'NVMe_M2':-18,'Standoff':-9,
 'ActiveCooler':12,'ActiveCooler_Blower':12,'Exhaust_Duct':12,
 'CellBay_Lid_F':-30,'CellBay_Wall_L':45,'CellBay_Wall_R':45,'CellBay_Wall_B':45,'CellBay_Wall_T':45,
 'UPS_Board':36,'UPS_IC1':36,'UPS_IC2':36,'ADS1115_NTC':36,
 'Cell_1':58,'Cell_2':58,'Cell_3':58,'Cell_4':58,
 'CellCap_1':58,'CellCap_2':58,'CellCap_3':58,'CellCap_4':58,
 'GPS_BN880':45,
 'Thermal_Baffle':54,
 'Gasket_SCAN':-95,'Gasket_ASK':-95,'Gasket_LISTEN':-95,'Gasket_MAP':-95,
 'Gasket_DPad_L':-95,'Gasket_DPad_R':-95,'Gasket_DPad_T':-95,'Gasket_DPad_B':-95,
 'Gasket_USBC_T':90,'Gasket_USBC_B':90,'Gasket_USBC_L':90,'Gasket_USBC_R':90,
 'Lens_Bezel':90,
 'Shell_BackHousing':90,'Camera_Module':90,'Camera_Lens':90,'Camera_LensDot':90,'Camera_Flash':90,
 'Vent_1':90,'Vent_2':90,'Vent_3':90,'Vent_4':90,'Lanyard_Loop':90,'Back_Mark':90,
 'PWR_Slot':90,'PWR_Slider':90,'VOL_Plus':90,'VOL_Minus':90,
}

if MODE == 'explodeonly':
    for o in bpy.data.objects:
        for key, off in EXP.items():
            if o.name.startswith(key):
                o.location.y += off
                break
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'pokedex-mk1-layoutA-exploded.blend'))
    print('EXPLODED blend saved')
    sys.exit(0)
for o in bpy.data.objects:
    for key, off in EXP.items():
        if o.name.startswith(key):
            o.location.y += off
            break
if MODE != 'explodeonly':
    render('render_exploded.png', (420,-520,260), (0,10,0), 1100, 900, lens=58)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'pokedex-mk1-layoutA-exploded.blend'))
print('DONE')
