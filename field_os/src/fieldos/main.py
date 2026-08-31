"""FIELD OS entry point (W1 stub).

Boot target: kiosk Chromium on cage showing the local app shell; this process
owns service wiring - hardware daemons, the ID loop, and the e-ink handoff.
Real services land per the week mapping in field_os/README.md.
"""


def main() -> None:
    print("FIELD OS 0.1.0 - SCOUT MK-1 bench build (W1 stub)")


if __name__ == "__main__":
    main()
