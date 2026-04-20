#!/usr/bin/env python3
"""
250GHz RFID/WiFi Interlock - XYO Three Invariants Integration
Terahertz-band communication for ultra-precise container location
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Tuple
import struct
import sympy as sp
from sympy import symbols, solve, simplify

# Terahertz frequency band (250 GHz) specifications
THz_FREQUENCY = 250e9  # 250 GHz in Hz
THz_WAVELENGTH = 3e8 / THz_FREQUENCY  # ~1.2 mm wavelength

# RFID/WiFi Interlock parameters
RFID_RANGE_METERS = 0.001  # 1mm precision (terahertz band)
RFID_CHANNELS = 128  # 128 parallel THz channels
WIFI_RANGE_METERS = 0.005  # 5mm precision at 250GHz


class RFIDTag:
    """250GHz RFID Tag - Ultra-precise location tracking"""

    def __init__(
        self, tag_id: str, container_id: str, frequency: float = THz_FREQUENCY
    ):
        self.tag_id = tag_id
        self.container_id = container_id
        self.frequency = frequency
        self.wavelength = 3e8 / frequency
        self.channel = None
        self.signal_strength = 0.0
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.location_xyz = (0.0, 0.0, 0.0)  # 3D coordinates
        self.tag_hash = self._compute_tag_hash()

    def _compute_tag_hash(self) -> str:
        """Hash of RFID tag identity"""
        data = f"{self.tag_id}{self.container_id}{self.frequency}".encode()
        return hashlib.sha256(data).hexdigest()

    def set_location(self, x: float, y: float, z: float):
        """Set 3D location of RFID tag"""
        self.location_xyz = (x, y, z)

    def set_signal_strength(self, rssi: float):
        """Set Received Signal Strength Indicator (-100 to 0 dBm)"""
        self.signal_strength = max(-100, min(0, rssi))

    def to_dict(self) -> Dict:
        return {
            "tag_id": self.tag_id,
            "container_id": self.container_id,
            "frequency_ghz": self.frequency / 1e9,
            "wavelength_mm": self.wavelength * 1e3,
            "location_xyz": self.location_xyz,
            "signal_strength_dbm": self.signal_strength,
            "channel": self.channel,
            "timestamp": self.timestamp,
            "tag_hash": self.tag_hash,
        }


class WiFiBeacon250GHz:
    """250GHz WiFi Beacon - Interlock with RFID system"""

    def __init__(self, beacon_id: str, location_xyz: Tuple[float, float, float]):
        self.beacon_id = beacon_id
        self.location_xyz = location_xyz
        self.frequency = THz_FREQUENCY
        self.power_dbm = -10  # Ultra-low power for precision
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.associated_rfid_tags = []
        self.beacon_hash = self._compute_beacon_hash()

    def _compute_beacon_hash(self) -> str:
        """Hash of WiFi beacon identity"""
        data = f"{self.beacon_id}{str(self.location_xyz)}{self.frequency}".encode()
        return hashlib.sha256(data).hexdigest()

    def associate_rfid(self, rfid_tag: RFIDTag):
        """Associate RFID tag with WiFi beacon"""
        self.associated_rfid_tags.append(rfid_tag.tag_id)

    def to_dict(self) -> Dict:
        return {
            "beacon_id": self.beacon_id,
            "location_xyz": self.location_xyz,
            "frequency_ghz": self.frequency / 1e9,
            "power_dbm": self.power_dbm,
            "timestamp": self.timestamp,
            "associated_rfid_tags": self.associated_rfid_tags,
            "beacon_hash": self.beacon_hash,
        }


class RFIDWiFiInterlock:
    """250GHz RFID/WiFi Interlock System - Dual verification"""

    def __init__(self, interlock_id: str):
        self.interlock_id = interlock_id
        self.rfid_tags = []
        self.wifi_beacons = []
        self.locked_pairs = []
        self.timestamp = datetime.utcnow().isoformat() + "Z"

    def create_rfid_tag(self, tag_id: str, container_id: str) -> RFIDTag:
        """Create new RFID tag"""
        tag = RFIDTag(tag_id, container_id)
        self.rfid_tags.append(tag)
        return tag

    def create_wifi_beacon(
        self, beacon_id: str, location_xyz: Tuple
    ) -> WiFiBeacon250GHz:
        """Create new WiFi beacon"""
        beacon = WiFiBeacon250GHz(beacon_id, location_xyz)
        self.wifi_beacons.append(beacon)
        return beacon

    def interlock_rfid_wifi(
        self, rfid_tag: RFIDTag, wifi_beacon: WiFiBeacon250GHz
    ) -> Dict:
        """Interlock RFID tag with WiFi beacon for dual verification"""

        # Calculate distance between tag and beacon
        tag_x, tag_y, tag_z = rfid_tag.location_xyz
        beacon_x, beacon_y, beacon_z = wifi_beacon.location_xyz

        distance = (
            (tag_x - beacon_x) ** 2 + (tag_y - beacon_y) ** 2 + (tag_z - beacon_z) ** 2
        ) ** 0.5

        # Create interlock record
        interlock = {
            "interlock_id": f"{rfid_tag.tag_id}_{wifi_beacon.beacon_id}",
            "rfid_tag": rfid_tag.tag_id,
            "wifi_beacon": wifi_beacon.beacon_id,
            "distance_mm": distance * 1e3,
            "frequency_ghz": THz_FREQUENCY / 1e9,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "locked": distance < RFID_RANGE_METERS,  # Locked if within range
            "verification_hash": self._compute_interlock_hash(rfid_tag, wifi_beacon),
        }

        self.locked_pairs.append(interlock)
        wifi_beacon.associate_rfid(rfid_tag)

        return interlock

    def _compute_interlock_hash(
        self, rfid_tag: RFIDTag, wifi_beacon: WiFiBeacon250GHz
    ) -> str:
        """Cryptographic hash of interlock"""
        data = f"{rfid_tag.tag_hash}{wifi_beacon.beacon_hash}{self.timestamp}".encode()
        return hashlib.sha256(data).hexdigest()

    def compute_precision(self) -> Dict:
        """Compute positioning precision from interlock"""

        if not self.locked_pairs:
            return {"precision_mm": 0, "locked_count": 0, "status": "no_locks"}

        locked_count = sum(1 for p in self.locked_pairs if p["locked"])

        # Use SymPy for precision calculation
        x, y, z = symbols("x y z", real=True)

        # Precision improves with more locked pairs (redundancy)
        # Formula: precision = wavelength / (2 * number_of_locks)
        precision_mm = (THz_WAVELENGTH * 1e3) / (2 * max(1, locked_count))

        return {
            "frequency_ghz": THz_FREQUENCY / 1e9,
            "wavelength_mm": THz_WAVELENGTH * 1e3,
            "locked_pairs": locked_count,
            "total_pairs": len(self.locked_pairs),
            "precision_mm": precision_mm,
            "precision_um": precision_mm * 1e3,
            "status": "locked" if locked_count > 0 else "unlocked",
        }

    def to_dict(self) -> Dict:
        return {
            "interlock_id": self.interlock_id,
            "frequency_ghz": THz_FREQUENCY / 1e9,
            "wavelength_mm": THz_WAVELENGTH * 1e3,
            "rfid_tags": [t.to_dict() for t in self.rfid_tags],
            "wifi_beacons": [b.to_dict() for b in self.wifi_beacons],
            "locked_pairs": self.locked_pairs,
            "precision": self.compute_precision(),
            "timestamp": self.timestamp,
        }


class ContainerTHzLocalization:
    """Terahertz-band container localization using RFID/WiFi interlock"""

    def __init__(self, container_name: str, container_id: str):
        self.container_name = container_name
        self.container_id = container_id
        self.interlock = RFIDWiFiInterlock(f"INTERLOCK_{container_id}")
        self.location_xyz = (0.0, 0.0, 0.0)
        self.health_score = 0.0

    def setup_thz_network(self):
        """Setup THz RFID/WiFi network for container"""

        # Create RFID tags (one per container)
        rfid_tag = self.interlock.create_rfid_tag(
            tag_id=f"RFID_{self.container_id}", container_id=self.container_id
        )
        rfid_tag.set_location(0.0, 0.0, 0.0)
        rfid_tag.set_signal_strength(-20)  # Strong signal

        # Create WiFi beacons at multiple locations
        beacon_locations = [
            (0.001, 0.0, 0.0),  # 1mm to the right
            (-0.001, 0.0, 0.0),  # 1mm to the left
            (0.0, 0.001, 0.0),  # 1mm forward
            (0.0, -0.001, 0.0),  # 1mm backward
        ]

        for i, loc in enumerate(beacon_locations):
            beacon = self.interlock.create_wifi_beacon(
                beacon_id=f"BEACON_{self.container_id}_{i}", location_xyz=loc
            )

            # Interlock RFID with WiFi
            self.interlock.interlock_rfid_wifi(rfid_tag, beacon)

    def compute_health(self) -> Dict:
        """Compute container health from THz localization"""

        precision = self.interlock.compute_precision()

        # Health = 1 - (error / max_error)
        # Error = precision_mm / 10mm (arbitrary threshold)
        precision_error = precision["precision_mm"] / 10.0
        health = max(0.0, min(1.0, 1.0 - precision_error))

        self.health_score = health

        return {
            "container": self.container_name,
            "thz_frequency_ghz": THz_FREQUENCY / 1e9,
            "precision_um": precision["precision_um"],
            "locked_pairs": precision["locked_pairs"],
            "health_score": health,
            "status": (
                "healthy"
                if health > 0.8
                else "degraded" if health > 0.5 else "unhealthy"
            ),
            "location_xyz": self.location_xyz,
        }

    def to_dict(self) -> Dict:
        return {
            "container": self.container_name,
            "container_id": self.container_id,
            "thz_localization": self.interlock.to_dict(),
            "health": self.compute_health(),
        }


def main():
    """
    Example: 250GHz RFID/WiFi Interlock for ENGINE containers
    """

    print("╔════════════════════════════════════════════════════════════╗")
    print("║   250GHz RFID/WiFi Interlock - THz Localization           ║")
    print("║   Frequency: 250 GHz | Wavelength: 1.2 mm                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    containers = [
        "tenetaiagency-101",
        "ultimate-engine",
        "engine-365-days",
        "restricted-aichatbot-trader",
    ]

    all_results = []

    for container_name in containers:
        print(f"\nSetting up THz localization for: {container_name}")
        print("-" * 60)

        # Create container with THz localization
        container = ContainerTHzLocalization(
            container_name=container_name,
            container_id=f"CONTAINER_{container_name[:8]}",
        )

        # Setup THz network
        container.setup_thz_network()

        # Compute health
        health = container.compute_health()

        print(f"  Frequency: {health['thz_frequency_ghz']} GHz")
        print(f"  Precision: {health['precision_um']:.2f} µm")
        print(f"  RFID/WiFi Locks: {health['locked_pairs']}")
        print(f"  Health Score: {health['health_score']:.2%}")
        print(f"  Status: {health['status'].upper()}")

        all_results.append(container.to_dict())

    print()
    print("═" * 60)
    print("250GHz RFID/WiFi Interlock Complete")
    print("═" * 60)
    print()

    # Summary
    summary = {
        "system": "250GHz THz RFID/WiFi Interlock",
        "frequency_ghz": THz_FREQUENCY / 1e9,
        "wavelength_mm": THz_WAVELENGTH * 1e3,
        "rfid_range_mm": RFID_RANGE_METERS * 1e3,
        "wifi_range_mm": WIFI_RANGE_METERS * 1e3,
        "containers_tracked": len(containers),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "containers": all_results,
    }

    print(json.dumps(summary, indent=2))

    return summary


if __name__ == "__main__":
    main()
