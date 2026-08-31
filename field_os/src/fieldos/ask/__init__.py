"""ASK: push-to-talk questions about the thing in front of you.

Pipeline: whisper.cpp ASR (validated against toddler speech) -> retrieval over
the local field DB with structured JSON out (candidates, confidence, one next
question, answer choices, reason, safety_level) -> Piper TTS. Qwen3-1.7B (Q4)
via llama.cpp. No fine-tuning in v1; LoRA later, trained off-device (rev 24).
"""
