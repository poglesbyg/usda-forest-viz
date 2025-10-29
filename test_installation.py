#!/usr/bin/env python3
"""
Test script to verify that the USDA Forest Service visualization tools are installed correctly.
"""

import sys


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import geopandas
        print("  ✓ geopandas")
    except ImportError as e:
        print(f"  ✗ geopandas: {e}")
        return False
    
    try:
        import matplotlib
        print("  ✓ matplotlib")
    except ImportError as e:
        print(f"  ✗ matplotlib: {e}")
        return False
    
    try:
        import plotly
        print("  ✓ plotly")
    except ImportError as e:
        print(f"  ✗ plotly: {e}")
        return False
    
    try:
        import folium
        print("  ✓ folium")
    except ImportError as e:
        print(f"  ✗ folium: {e}")
        return False
    
    try:
        import requests
        print("  ✓ requests")
    except ImportError as e:
        print(f"  ✗ requests: {e}")
        return False
    
    try:
        from usda_forest_viz import DatasetDownloader, StaticMapVisualizer, InteractiveMapVisualizer
        print("  ✓ usda_forest_viz")
    except ImportError as e:
        print(f"  ✗ usda_forest_viz: {e}")
        return False
    
    return True


def test_downloader():
    """Test that the downloader can be initialized."""
    print("\nTesting DatasetDownloader...")
    
    try:
        from usda_forest_viz import DatasetDownloader
        downloader = DatasetDownloader(data_dir="test_data")
        
        # Test listing datasets
        datasets = downloader.list_available_datasets()
        if len(datasets) > 0:
            print(f"  ✓ Found {len(datasets)} available datasets")
        else:
            print("  ✗ No datasets found")
            return False
        
        # Test getting dataset info
        info = downloader.get_dataset_info("Actv_TimberHarvest")
        if info and 'name' in info:
            print(f"  ✓ Can retrieve dataset information")
        else:
            print("  ✗ Cannot retrieve dataset information")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_visualizers():
    """Test that visualizers can be initialized."""
    print("\nTesting Visualizers...")
    
    try:
        from usda_forest_viz import StaticMapVisualizer, InteractiveMapVisualizer
        
        static_viz = StaticMapVisualizer()
        print("  ✓ StaticMapVisualizer initialized")
        
        interactive_viz = InteractiveMapVisualizer()
        print("  ✓ InteractiveMapVisualizer initialized")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    try:
        from usda_forest_viz import utils
        
        # Check that key functions exist
        required_functions = [
            'load_shapefile',
            'load_geodatabase',
            'filter_by_bounds',
            'filter_by_attribute',
            'calculate_area',
            'get_summary_statistics'
        ]
        
        for func_name in required_functions:
            if hasattr(utils, func_name):
                print(f"  ✓ {func_name} available")
            else:
                print(f"  ✗ {func_name} not found")
                return False
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("USDA Forest Service Visualization Tools - Installation Test")
    print("=" * 80)
    
    all_passed = True
    
    # Run tests
    if not test_imports():
        all_passed = False
    
    if not test_downloader():
        all_passed = False
    
    if not test_visualizers():
        all_passed = False
    
    if not test_utils():
        all_passed = False
    
    # Print summary
    print("\n" + "=" * 80)
    if all_passed:
        print("✓ All tests passed!")
        print("\nYour installation is working correctly.")
        print("\nNext steps:")
        print("  1. Check out QUICKSTART.md for a 5-minute tutorial")
        print("  2. Run the examples in the examples/ directory")
        print("  3. Read DATASETS.md to learn about available datasets")
    else:
        print("✗ Some tests failed")
        print("\nPlease ensure all dependencies are installed:")
        print("  uv sync")
        print("\nAnd that you're in the virtual environment:")
        print("  source .venv/bin/activate")
    print("=" * 80)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

