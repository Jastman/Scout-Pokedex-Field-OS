#!/usr/bin/env python3
"""One vision-model inference on a still (soak-loop helper).

Wire this to the real W2 model (quantized iNat vision export, TFLite int8,
num_threads=3). Until then it exits NOT-WIRED instead of faking load.
"""
import sys, pathlib

MODEL = pathlib.Path.home() / "scout/models/inat_vision_int8.tflite"

if not MODEL.exists():
    sys.exit(f"NOT-WIRED: {MODEL} missing (W2). Soak runs without the vision lane.")

import numpy as np
from PIL import Image
try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    from tensorflow.lite import Interpreter  # bench fallback

interp = Interpreter(model_path=str(MODEL), num_threads=3)
interp.allocate_tensors()
inp = interp.get_input_details()[0]
_, h, w, _ = inp["shape"]
img = np.asarray(Image.open(sys.argv[1]).convert("RGB").resize((w, h)))
interp.set_tensor(inp["index"], img[None].astype(inp["dtype"]))
interp.invoke()
