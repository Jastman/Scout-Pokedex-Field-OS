"""The ID loop: SCAN (iNaturalist vision model, quantized TFLite/ONNX on CPU)
and LISTEN (BirdNET on the ReSpeaker mics) with confidence thresholds.

Every match passes the permanent danger layer: toxic/mushroom/dangerous taxa
render the "CANDIDATE ONLY - do not consume or handle" band (rev 24 rule 3).
Finds hand off to fieldos.data as atomic writes.
"""
