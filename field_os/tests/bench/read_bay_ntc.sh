#!/usr/bin/env bash
# Prints the battery-bay temperature in C from the 10k NTC via an I2C ADC (ADS1115),
# or "NA" until the W5 hardware exists. The Pi GPIO is digital-only: a bare NTC +
# divider on a GPIO pin cannot be read - the ADC breakout is REQUIRED, not optional
# (see hardware-architecture.md §5, I2C map: ADS1115 at 0x48).
set -u
if ! command -v python3 >/dev/null || ! i2cdetect -y 1 2>/dev/null | grep -q 48; then
  echo NA; exit 0
fi
python3 - <<'EOF'
# 10k NTC (B=3950) + 10k divider from 3.3V, NTC on the low side, ADS1115 A0.
import math
try:
    import board, busio
    from adafruit_ads1x15.ads1115 import ADS1115, P0
    from adafruit_ads1x15.analog_in import AnalogIn
    ch = AnalogIn(ADS1115(busio.I2C(board.SCL, board.SDA)), P0)
    v = ch.voltage
    r_ntc = 10000.0 * v / (3.3 - v)
    t = 1.0 / (1.0/298.15 + math.log(r_ntc/10000.0)/3950.0) - 273.15
    print(f"{t:.1f}")
except Exception:
    print("NA")
EOF
