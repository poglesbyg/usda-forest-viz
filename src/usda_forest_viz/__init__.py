"""
USDA Forest Service Data Visualization

A Python package for downloading and visualizing geospatial datasets
from the USDA Forest Service Enterprise Data Warehouse.
"""

__version__ = "0.1.0"

from usda_forest_viz.downloader import DatasetDownloader
from usda_forest_viz.visualizer import StaticMapVisualizer, InteractiveMapVisualizer

__all__ = [
    "DatasetDownloader",
    "StaticMapVisualizer",
    "InteractiveMapVisualizer",
]


def main():
    """Main entry point for CLI."""
    print("USDA Forest Service Data Visualization Tools")
    print(f"Version: {__version__}")
    print("\nFor usage examples, see the examples/ directory")
    print("Documentation: https://github.com/yourusername/usda-forest-viz")
