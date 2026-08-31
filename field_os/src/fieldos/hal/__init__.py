"""Hardware abstraction layer.

Buttons arrive as key events from the gpio-keys daemon (SCAN dome, D-pad with
center SELECT, LISTEN, ASK, MAP, VOL+/-, PWR-as-soft-shutdown). Displays: DSI
LCD is the kiosk's screen; the 5.83" e-ink is driven by its own daemon with
5s full / 0.3s partial refresh policy. Camera via libcamera (rpicam). GPS via
gpsd over GPIO UART (BN-880, serial login shell OFF). UPS HAT (E) fuel gauge +
battery-bay NTC thermistor over I2C - the software-owned thermal cutoff lives
here (spec rev 24 rule 4).
"""
