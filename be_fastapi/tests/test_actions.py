import os
import sys

from bot.utils.time_converter import parse_duration
from bot.actions.command_registry import COMMAND_MAP

# 1. Setup path to find src/bot/actions.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_map_integrity():
    print("--- Testing Command Map ---")
    required_keys = ['SEND_MESSAGE', 'REPLY_MESSAGE', 'BAN_USER', 'TIMEOUT_USER']

    # Check if keys exist in the imported MAP
    current_keys = list(COMMAND_MAP.keys())
    print(f"Found Actions: {current_keys}")

    missing = [key for key in required_keys if key not in current_keys]

    if not missing:
        print("✅ SUCCESS: All required actions are mapped.")
    else:
        print(f"❌ FAILED: Missing actions: {missing}")


def test_time_parser():
    print("\n--- Testing Time Parser ---")
    # Test 10 minutes
    t1 = parse_duration("10m")
    print(f"Input '10m' -> {t1} (Expected: 0:10:00)")

    # Test 1 hour
    t2 = parse_duration("1h")
    print(f"Input '1h'  -> {t2} (Expected: 1:00:00)")

    if t1.total_seconds() == 600 and t2.total_seconds() == 3600:
        print("✅ SUCCESS: Time parser works correctly.")
    else:
        print("❌ FAILED: Time parser calculation is wrong.")


if __name__ == "__main__":
    test_map_integrity()
    test_time_parser()
