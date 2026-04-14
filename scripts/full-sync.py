#!/usr/bin/env python3
"""
Integrated XYO + 250GHz RFID/WiFi System
Complete container synchronization with terahertz localization
"""

import subprocess
import sys

def run_xyo_sync():
    """Run XYO Three Invariants synchronization"""
    print("\n" + "═" * 70)
    print("PHASE 1: XYO Three Invariants Synchronization")
    print("═" * 70)
    result = subprocess.run([sys.executable, "engine_core/xyo_invariants.py"])
    return result.returncode == 0

def run_thz_interlock():
    """Run 250GHz RFID/WiFi interlock"""
    print("\n" + "═" * 70)
    print("PHASE 2: 250GHz RFID/WiFi Terahertz Interlock")
    print("═" * 70)
    result = subprocess.run([sys.executable, "engine_core/thz_rfid_interlock.py"])
    return result.returncode == 0

def main():
    """Complete ENGINE container synchronization"""
    
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  ENGINE - Complete Container Synchronization System".center(68) + "║")
    print("║" + "  XYO Three Invariants + 250GHz RFID/WiFi Interlock".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    xyo_ok = run_xyo_sync()
    thz_ok = run_thz_interlock()
    
    print("\n" + "═" * 70)
    print("SYNCHRONIZATION SUMMARY")
    print("═" * 70)
    print()
    print(f"XYO Three Invariants (位置 時間 身分): {'✓ PASSED' if xyo_ok else '✗ FAILED'}")
    print(f"250GHz RFID/WiFi Interlock:         {'✓ PASSED' if thz_ok else '✗ FAILED'}")
    print()
    
    if xyo_ok and thz_ok:
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  ALL SYSTEMS SYNCHRONIZED                           ✓      ║")
        print("║  Containers: Healthy & Localized                    ✓      ║")
        print("║  THz Interlock: Active                              ✓      ║")
        print("╚════════════════════════════════════════════════════════════╝")
        return 0
    else:
        print("✗ Synchronization failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
