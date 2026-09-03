# SCOUT MINI CAD - rev 2 (Sep 2 2026)
# Models the REAL assembly Jake will build - no custom shell:
#   Argon ONE V3 (NVMe model, 106x95x41mm, owned) held as a portrait brick:
#   - FRONT (case top face): 5.83" Waveshare e-Paper HAT off-board on a printed
#     bracket (panel 125.4x99.5, active 119.2x88.3, driver board 65x30.2),
#     GPIO ribbon disappearing under the magnetic cover.
#   - BACK (case bottom): Camera Module 3 Wide (25x24 PCB, FFC to the GPIO slot),
#     10,000mAh PD power bank (~104x52x26) + elastic straps, 30x70x17 speaker.
#   - TOP EDGE: adhesive printed pod with Sanwa OBSF-24 (CAPTURE) + 12mm LISTEN.
#   - LEFT EDGE: ReSpeaker Lite (86x35, USB) mic board, mics up.
#   - BOTTOM EDGE: case rear port strip (2xHDMI, 2xUSB-A, USB-C, RJ45, pwr btn).
#   - Brand badge decal on the bracket chin.
import bpy, math, os
D2R = math.pi/180.0
HERE = os.path.dirname(os.path.abspath(__file__))

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'
sc.unit_settings.scale_length = 0.001
sc.unit_settings.length_unit = 'MILLIMETERS'

def new_col(name):
    c = bpy.data.collections.new(name); sc.collection.children.link(c); return c
COL = {n: new_col(n) for n in ('CASE','EINK','CONTROLS','AUDIO','POWER','CAMERA','LABELS','STUDIO')}

def link_to(o, col):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o)

def srgb(r,g,b):
    f = lambda c: ((c+0.055)/1.055)**2.4 if c>0.04045 else c/12.92
    return (f(r),f(g),f(b),1.0)

def mat(name, base, rough=0.5, metal=0.0, emit=None, estr=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = base
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emit is not None:
        b.inputs['Emission Color'].default_value = emit
        b.inputs['Emission Strength'].default_value = estr
    return m

M = {}
M['alu']    = mat('Argon_Anodized', srgb(0.30,0.31,0.34), rough=0.35, metal=0.85)
M['alu2']   = mat('Argon_Cover', srgb(0.36,0.37,0.40), rough=0.4, metal=0.8)
M['abs']    = mat('Argon_ABS_Base', srgb(0.10,0.10,0.11), rough=0.6)
M['port']   = mat('Port_Dark', srgb(0.01,0.01,0.012), rough=0.6)
M['pcb']    = mat('PCB_Dark', srgb(0.02,0.03,0.07), rough=0.5)
M['petg']   = mat('Bracket_CharcoalPETG', srgb(0.09,0.09,0.10), rough=0.5)
M['petg2']  = mat('Pod_PETG', srgb(0.12,0.12,0.13), rough=0.55)
M['eink']   = mat('EInk_Glass', srgb(0.88,0.85,0.78), rough=0.55)
M['glass']  = mat('Lens_Glass', srgb(0.01,0.02,0.05), rough=0.08, metal=0.1)
M['sanwa']  = mat('Sanwa_Black', srgb(0.02,0.02,0.025), rough=0.25)
M['tpu']    = mat('Cap_TPU', srgb(0.10,0.10,0.11), rough=0.5)
M['bank']   = mat('PowerBank_Shell', srgb(0.22,0.22,0.24), rough=0.35)
M['strap']  = mat('Strap_Webbing', srgb(0.08,0.09,0.08), rough=0.9)
M['ribbon'] = mat('FFC_Amber', srgb(0.85,0.55,0.15), rough=0.4)
M['ribbonw']= mat('Ribbon_White', srgb(0.85,0.85,0.85), rough=0.6)
M['phos']   = mat('Engrave_Light', srgb(0.55,0.56,0.60), rough=0.5)
M['spk']    = mat('Speaker_Grille', srgb(0.04,0.04,0.045), rough=0.7)
M['mic']    = mat('Mic_Port', srgb(0.005,0.005,0.005), rough=0.4)

def apply_mod(o, name):
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    try: bpy.ops.object.modifier_apply(modifier=name)
    except Exception as e: print('MOD FAIL', name, e)
    o.select_set(False)

def rbox(name, w, h, d, loc, material, bevel=0.0, col=None):
    # w=x, h=z, d=y ; front face is -Y
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name
    o.dimensions = (w, d, h)
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

def img_plane(name, w, h, loc, rot, img_path, emit=0.55, col=None):
    img = bpy.data.images.load(img_path); img.pack()
    m = bpy.data.materials.new(name+'_Mat'); m.use_nodes = True
    nt = m.node_tree; nn = nt.nodes; ll = nt.links; nn.clear()
    out = nn.new('ShaderNodeOutputMaterial')
    bs = nn.new('ShaderNodeBsdfPrincipled')
    tex = nn.new('ShaderNodeTexImage'); tex.image = img
    ll.new(tex.outputs['Color'], bs.inputs['Base Color'])
    ll.new(tex.outputs['Color'], bs.inputs['Emission Color'])
    bs.inputs['Emission Strength'].default_value = emit
    bs.inputs['Roughness'].default_value = 0.4
    ll.new(bs.outputs['BSDF'], out.inputs['Surface'])
    mesh = bpy.data.meshes.new(name)
    hw, hh = w/2, h/2
    mesh.from_pydata([(-hw,0,-hh),(hw,0,-hh),(hw,0,hh),(-hw,0,hh)], [], [(0,1,2,3)])
    uv = mesh.uv_layers.new()
    for li, loop in enumerate(mesh.loops):
        uv.data[li].uv = [(0,0),(1,0),(1,1),(0,1)][loop.vertex_index]
    o = bpy.data.objects.new(name, mesh)
    (col or sc.collection).objects.link(o)
    o.location = loc; o.rotation_euler = rot
    o.data.materials.append(m)
    return o

def txt(name, body, size, loc, rot, material, extrude=0.25, col=None, align='CENTER'):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.data.body = body; o.data.align_x = align; o.data.align_y = 'CENTER'
    o.data.size = size; o.data.extrude = extrude
    if material: o.data.materials.append(material)
    if col: link_to(o, col)
    return o

# ================= ARGON ONE V3 CASE (106 x 95 x 41) =================
# world: width X=106, height Z=95, depth Y=41. Case center at origin.
# front face (case top, magnetic cover) faces -Y.
rbox('Argon_Body', 106, 95, 41, (0,0,0), M['alu'], bevel=3.5, col=COL['CASE'])
# ABS base strip (the M.2 expansion base, slightly different tone, bottom 12mm of depth)
rbox('Argon_Base', 104, 93, 12, (0, 15.0, 0), M['abs'], bevel=2.5, col=COL['CASE'])
# magnetic GPIO cover plate on the front face (top 36mm of the face)
rbox('GPIO_Cover', 98, 34, 1.2, (0, -20.8, 26), M['alu2'], bevel=1.5, col=COL['CASE'])
txt('Argon_Mark', 'ARGON ONE', 5.0, (-30, -21.6, 38), (90*D2R,0,0), M['port'], col=COL['LABELS'], align='LEFT')

# bottom edge port strip (case rear): 2xHDMI, 2xUSB-A, USB-C, RJ45, power button
rbox('Port_HDMI1', 16, 7, 1.5, (-34, 0, -47.6), M['port'], bevel=0.8, col=COL['CASE'])
rbox('Port_HDMI2', 16, 7, 1.5, (-15, 0, -47.6), M['port'], bevel=0.8, col=COL['CASE'])
rbox('Port_USBA1', 15, 6, 1.5, (4, 0, -47.6), M['port'], bevel=0.8, col=COL['CASE'])
rbox('Port_USBA2', 15, 6, 1.5, (22, 0, -47.6), M['port'], bevel=0.8, col=COL['CASE'])
rbox('Port_USBC', 9, 3.5, 1.5, (36, 0, -47.6), M['port'], bevel=1.2, col=COL['CASE'])
rbox('Port_RJ45', 16, 13, 1.5, (-34, 12, -47.6), M['port'], bevel=0.8, col=COL['CASE'])
cyl('Power_Btn', 4, 2.5, (46, -12, -47.5), M['sanwa'], rot=(90*D2R,0,0), col=COL['CASE'])

# ================= E-INK FRONT ASSEMBLY =================
# printed bracket (overhangs case ~10mm each side), panel sits proud on standoffs
rbox('EInk_Bracket', 130, 104, 4, (0, -22.5, 2), M['petg'], bevel=4, col=COL['EINK'])
# panel glass 125.4 x 99.5 x 1.2
rbox('EInk_Panel', 125.4, 99.5, 1.2, (0, -25.6, 2), M['eink'], bevel=0.8, col=COL['EINK'])
# active area content: dithered robin find card (119.2 x 88.3)
img_plane('EInk_Content', 119.2, 88.3, (0, -26.3, 2), (0,0,0),
          '/tmp/film/eink/ek_0100.png', emit=0.25, col=COL['EINK'])
# driver board peeking below the panel
rbox('EInk_Driver', 65, 30.2, 4, (0, -23.0, -30), M['pcb'], bevel=1.0, col=COL['EINK'])
# GPIO ribbon: from driver board along bracket bottom to under the magnetic cover
# bracket screws
for sx in (-58, 58):
    for sz in (-44, 48):
        cyl('Bracket_Screw', 1.6, 2, (sx, -26.2, sz), M['port'], rot=(90*D2R,0,0), col=COL['EINK'])
# brand badge decal on the bracket chin
img_plane('Mini_Badge', 16, 16, (-38, -24.7, -40), (0,0,0),
          os.path.join(HERE,'logo_badge_decal.png'), emit=0.4, col=COL['LABELS'])
txt('Mini_Name', 'SCOUT MINI', 4.5, (-26, -24.7, -40), (90*D2R,0,0), M['port'], col=COL['LABELS'], align='LEFT')

# ================= TOP EDGE: BUTTON POD =================
# rev 2: adhesive printed pod straddling the top edge. Shifted left to clear the
# x=+42 strap rail, deepened to 30mm so the 28mm OBSF-24 bezel is fully contained,
# buttons raised to sit ON the pod face (they were sunk inside the housing).
rbox('Button_Pod', 62, 18, 30, (6, 0, 50), M['petg2'], bevel=4.5, col=COL['CONTROLS'])
# CAPTURE: Sanwa OBSF-24 (24mm hole, 28mm bezel OD), plunger up, on the pod face (pod top z=59)
cyl('Capture_Bezel', 14, 6, (20, 0, 62), M['sanwa'], col=COL['CONTROLS'])
cyl('Capture_Button', 12, 7, (20, 0, 66.5), M['sanwa'], col=COL['CONTROLS'])
# LISTEN: 12mm tactile under printed TPU cap, on the pod face
cyl('Listen_Cap', 6, 6, (-2, 0, 62), M['tpu'], col=COL['CONTROLS'])
txt('Capture_Label', 'CAPTURE', 3.2, (20, -15.2, 50), (90*D2R,0,0), M['phos'], col=COL['LABELS'])
txt('Listen_Label', 'LISTEN', 3.2, (-2, -15.2, 50), (90*D2R,0,0), M['phos'], col=COL['LABELS'])

# ================= LEFT EDGE: RESPEAKER LITE =================
# board 86 long (z) x 35 (y) x 8 (x), mics on its top edge
rbox('ReSpeaker', 8, 86, 35, (-55.5, 0, 8), M['pcb'], bevel=1.5, col=COL['AUDIO'])
cyl('Mic1', 1.8, 2, (-55.5, -8, 52.5), M['mic'], col=COL['AUDIO'])
cyl('Mic2', 1.8, 2, (-55.5, 8, 52.5), M['mic'], col=COL['AUDIO'])
rbox('ReSpeaker_USBC', 4, 9, 4, (-55.5, 0, -36), M['port'], bevel=1.0, col=COL['AUDIO'])

# ================= BACK FACE: CAMERA / POWER BANK / SPEAKER =================
# Camera Module 3 Wide on a small printed bracket, top-right of the back face
rbox('Cam_Bracket', 30, 28, 3, (25, 21.6, 26), M['petg'], bevel=1.5, col=COL['CAMERA'])
rbox('Cam_PCB', 25, 24, 1.5, (25, 23.5, 26), M['pcb'], bevel=0.8, col=COL['CAMERA'])
cyl('Cam_Lens', 7, 9, (25, 27.5, 27), M['sanwa'], rot=(90*D2R,0,0), col=COL['CAMERA'])
cyl('Cam_Glass', 5.5, 1, (25, 32.2, 27), M['glass'], rot=(90*D2R,0,0), col=COL['CAMERA'])
# camera FFC from PCB down toward the GPIO slot
rbox('Cam_FFC', 12, 0.7, 40, (25, 21.2, 2), M['ribbon'], bevel=0.3, col=COL['CAMERA'])
# power bank on the back, held by two elastic straps
rbox('Power_Bank', 104, 52, 26, (0, 34, -14), M['bank'], bevel=6, col=COL['POWER'])
rbox('Bank_USBC', 9, 3.5, 2, (30, 34, -40.5), M['port'], bevel=1.0, col=COL['POWER'])
txt('Bank_Mark', '10K PD', 4.0, (0, 47.2, -14), (90*D2R,0,180*D2R), M['port'], col=COL['LABELS'])
for sx in (-42, 42):
    rbox('Strap_Back', 6, 96, 1.6, (sx, 47.9, 0), M['strap'], bevel=0.6, col=COL['POWER'])
    rbox('Strap_Top', 6, 1.6, 68, (sx, 13.5, 48.3), M['strap'], bevel=0.6, col=COL['POWER'])
    rbox('Strap_Bot', 6, 1.6, 68, (sx, 13.5, -48.3), M['strap'], bevel=0.6, col=COL['POWER'])
# speaker lower-left on the back
rbox('Speaker', 17, 70, 30, (54.5, 0, -12), M['spk'], bevel=3, col=COL['AUDIO'])

# ================= SAVE =================
out = os.path.join(HERE, 'scout-mini-assembly.blend')
bpy.ops.wm.save_as_mainfile(filepath=out)
print('MINI BUILD OK ->', out)
