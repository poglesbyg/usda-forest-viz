#!/usr/bin/env python3
"""
Quick test to verify the output directory auto-creation fix works.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from usda_forest_viz import StaticMapVisualizer
from usda_forest_viz.utils import load_shapefile

print("Testing visualizer directory auto-creation fix...")
print("=" * 80)

# Load data from parent directory
data_path = Path("../data/shapefiles/Actv_TimberHarvest")

if not data_path.exists():
    print(f"✗ Data not found at {data_path}")
    print("\nPlease download data first:")
    print("  cd usda-forest-viz")
    print("  uv run python examples/01_download_data.py")
    sys.exit(1)

print("✓ Found data")
print(f"Loading from: {data_path}")

# Load a small subset
gdf = load_shapefile(data_path)
sample = gdf.head(100)

print(f"✓ Loaded {len(sample)} features")

# Test that output directory is created automatically
viz = StaticMapVisualizer()

# This should create ./outputs/ automatically now
output_path = "./outputs/test_auto_creation.png"
print(f"\nTesting automatic directory creation for: {output_path}")

try:
    fig = viz.plot_polygons(
        sample,
        title="Test: Auto Directory Creation",
        figsize=(10, 8),
        output_path=output_path
    )
    print("✓ SUCCESS! Directory was created automatically")
    print(f"✓ File saved to: {output_path}")
    
    # Clean up
    import matplotlib.pyplot as plt
    plt.close(fig)
    
except FileNotFoundError as e:
    print(f"✗ FAILED: {e}")
    print("The auto-creation fix didn't work")
    sys.exit(1)

print("\n" + "=" * 80)
print("✓ Fix verified! The visualizer now creates output directories automatically.")
print("=" * 80)

