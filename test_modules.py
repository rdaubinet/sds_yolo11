#!/usr/bin/env python3
"""Test custom module integration"""

try:
    from ultralytics.nn.modules import space_to_depth, CARAFE
    print("✅ Space-to-Depth:", space_to_depth)
    print("✅ CARAFE:", CARAFE)
    print("\n🔥 Custom modules successfully integrated!")
except ImportError as e:
    print("❌ Import failed:", e)
