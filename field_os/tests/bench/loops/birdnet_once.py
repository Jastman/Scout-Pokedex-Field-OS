#!/usr/bin/env python3
"""One BirdNET analysis pass on a canned clip (soak-loop helper).

Wire this to the real W2 BirdNET TFLite (3 s window, num_threads=3). Until then it
exits NOT-WIRED instead of faking load.
"""
import sys, pathlib

MODEL = pathlib.Path.home() / "scout/models/birdnet.tflite"

if not MODEL.exists():
    sys.exit(f"NOT-WIRED: {MODEL} missing (W2). Soak runs without the BirdNET lane.")

# Minimal stand-in for the idloop LISTEN path: load 3 s @ 48 kHz mono, run once.
import numpy as np
import soundfile as sf
try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    from tensorflow.lite import Interpreter

audio, sr = sf.read(sys.argv[1], dtype="float32")
if audio.ndim > 1:
    audio = audio.mean(axis=1)
window = audio[: 3 * sr]
interp = Interpreter(model_path=str(MODEL), num_threads=3)
interp.allocate_tensors()
inp = interp.get_input_details()[0]
buf = np.zeros(inp["shape"][-1], dtype=np.float32)
buf[: len(window)] = window[: len(buf)]
interp.set_tensor(inp["index"], buf[None])
interp.invoke()
