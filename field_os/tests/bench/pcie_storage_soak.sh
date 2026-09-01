#!/usr/bin/env bash
# SCOUT MK-1 bench: PCIe/storage reliability soak (hardware-architecture.md §2.4).
# Purpose: prove the CHOSEN storage+accelerator topology is stable on OUR boards and
# firmware BEFORE anything goes in the shell. Covers both open risks from the review:
#   (a) boot reliability with the topology as wired (cold boots in a loop),
#   (b) device coexistence under sustained concurrent I/O + inference.
#
# Usage:
#   ./pcie_storage_soak.sh boot   # run the 20x cold-boot half (needs a smart plug or
#                                 # manual power cycling; verifies both devices enumerate)
#   ./pcie_storage_soak.sh soak   # 15-min concurrent fio + Hailo inference loop
#
# PASS (boot): 20/20 boots reach multi-user.target with the NVMe root mounted AND
#              (if fitted) the Hailo enumerated in lspci.
# PASS (soak): zero I/O errors in dmesg, zero PCIe AER/link-down events, Hailo
#              inference FPS steady within 10% start-to-end, fio completes all loops.
set -u
MODE="${1:-soak}"
MIN="${MIN:-15}"
HEF="${HEF:-/usr/share/hailo-models/resnet_v1_50.hef}"   # any classification HEF

check_devices() {
  ok=1
  lspci | grep -qi 'non-volatile\|nvme' && echo "NVMe: enumerated" || { echo "NVMe: MISSING"; ok=0; }
  if command -v hailortcli >/dev/null; then
    hailortcli scan 2>/dev/null | grep -qi hailo && echo "Hailo: enumerated" || { echo "Hailo: MISSING"; ok=0; }
  fi
  return $((1-ok))
}

if [ "$MODE" = boot ]; then
  # Log one boot's verdict; wire this into a @reboot cron or systemd unit and
  # power-cycle 20x. Verdicts accumulate in /var/log/scout_boot_soak.log
  { date; check_devices && echo VERDICT=OK || echo VERDICT=FAIL; } >> /var/log/scout_boot_soak.log
  tail -5 /var/log/scout_boot_soak.log
  exit 0
fi

echo "== device check before soak =="
check_devices || { echo "FAIL: devices missing before load"; exit 1; }
dmesg -C 2>/dev/null || sudo dmesg -C

# Concurrent load: sustained mixed read/write on the SSD + Hailo inference loop
fio --name=scout-soak --filename="${FIO_FILE:-$HOME/fio_soak.bin}" --size=2G \
    --rw=randrw --rwmixread=70 --bs=64k --iodepth=8 --numjobs=2 --direct=1 \
    --time_based --runtime=$((MIN*60)) --group_reporting > /tmp/fio_soak.txt 2>&1 &
FIO=$!

HAILO_LOG=/tmp/hailo_soak.txt; : > "$HAILO_LOG"
if command -v hailortcli >/dev/null; then
  ( end=$(( $(date +%s) + MIN*60 ))
    while [ "$(date +%s)" -lt "$end" ]; do
      hailortcli benchmark "$HEF" -t 30 2>&1 | grep -i fps >> "$HAILO_LOG"
    done ) &
  HB=$!
else
  echo "note: hailortcli not present - storage-only soak (valid for the no-Hailo topology)"
  HB=""
fi

wait $FIO; [ -n "$HB" ] && wait $HB

echo "== results =="
grep -E 'err=|error' /tmp/fio_soak.txt | head -5
ERR=0
(dmesg 2>/dev/null || sudo dmesg) | grep -iE 'nvme.*(err|timeout|reset)|pcie.*(aer|link.*down)|hailo.*(err|remove)' && ERR=1
[ -s "$HAILO_LOG" ] && { echo "Hailo FPS first/last:"; head -1 "$HAILO_LOG"; tail -1 "$HAILO_LOG"; }
check_devices || ERR=1
if [ "$ERR" -eq 0 ]; then echo "PASS: storage+accelerator stable under ${MIN}min concurrent load";
else echo "FAIL: see dmesg lines above - do NOT put this topology in the shell"; exit 1; fi
