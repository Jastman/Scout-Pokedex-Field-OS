# SCOUT MK-1 bench tests

Run over SSH from the Mac against the bench Pi (`scout.local`). Each script prints an
explicit PASS/FAIL against the threshold documented in
`docs/software-architecture.md` §7 and `docs/hardware-architecture.md` §2.4/§7.

| Script | What it proves | Gate |
|---|---|---|
| `pcie_storage_soak.sh` | The chosen storage/accelerator topology enumerates on every cold boot and survives sustained concurrent I/O + inference | **before any part goes in the shell** |
| `concurrent_soak.sh` | Spec §10.1 thermal soak: all four AI engines at once, 30 min, SoC/PMIC/bay logging | **before the shell print** (open bench), **before field use** (closed shell + sun) |
| `ask_latency.sh` | ASK round trip: release → first spoken audio, per-stage timing, tiny/base + 3/4-thread A/Bs | **W3 exit** |
| `read_bay_ntc.sh` | Helper: prints battery-bay temperature in °C (ADS1115 + 10k NTC divider) | used by the soaks |
| `loops/vision_once.py`, `loops/birdnet_once.py` | Single-inference helpers the soak loops call — wire these to the real W2 models when they land | |

Order of operations: `pcie_storage_soak.sh` (bench, W1) → `ask_latency.sh` (W3) →
`concurrent_soak.sh` open-bench (W5) → closed-shell + sun (W6, before the park trip).

The `loops/` helpers and `read_bay_ntc.sh` are stubs until the W2/W5 hardware exists —
each exits with a clear NOT-WIRED message rather than a fake number.
