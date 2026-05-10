#!/usr/bin/env python3
"""
TEST - Only portfolio.json update
"""

import json
from datetime import datetime
from pathlib import Path

print("=" * 60)
print("TEST: Portfolio.json Update Test")
print("=" * 60)

# ============ SIMPLE PORTFOLIO UPDATE ============
print("\n📁 UPDATING PORTFOLIO.JSON...")

portfolio_path = Path("portfolio.json")

# Load existing
entries = []
if portfolio_path.exists():
    try:
        content = portfolio_path.read_text()
        if content.strip():
            entries = json.loads(content)
            if not isinstance(entries, list):
                entries = []
        print(f"   Loaded {len(entries)} existing games")
    except Exception as e:
        print(f"   Error loading: {e}")
        entries = []

# Add test entry
new_entry = {
    "date": datetime.now().isoformat(),
    "game": f"TEST_GAME_{datetime.now().strftime('%H%M%S')}",
    "genre": "test",
    "mechanic": "test",
    "description": "This is a test entry",
    "status": "test_success"
}

entries.append(new_entry)
entries = entries[-100:]

# Save
try:
    portfolio_path.write_text(json.dumps(entries, indent=2))
    print(f"   ✅ Portfolio saved! Total: {len(entries)}")
    print(f"   ✅ Added: {new_entry['game']}")
except Exception as e:
    print(f"   ❌ Save failed: {e}")

# Verify
try:
    verify = portfolio_path.read_text()
    if new_entry['game'] in verify:
        print(f"   ✅ VERIFIED: Entry found!")
    else:
        print(f"   ❌ VERIFICATION FAILED!")
except Exception as e:
    print(f"   ❌ Cannot verify: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
