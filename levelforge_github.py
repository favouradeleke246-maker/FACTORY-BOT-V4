#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

print("TEST: Simple portfolio update")

portfolio_path = Path("portfolio.json")

# Load existing
entries = []
if portfolio_path.exists():
    try:
        entries = json.loads(portfolio_path.read_text())
        if not isinstance(entries, list):
            entries = []
    except:
        entries = []

# Add entry
entries.append({
    "date": datetime.now().isoformat(),
    "game": f"TEST_{datetime.now().strftime('%H%M%S')}",
    "status": "success"
})

# Save
portfolio_path.write_text(json.dumps(entries[-100:], indent=2))
print(f"✅ Saved! Total entries: {len(entries)}")

# Verify
print(f"✅ Verified: {portfolio_path.read_text()[:200]}")
