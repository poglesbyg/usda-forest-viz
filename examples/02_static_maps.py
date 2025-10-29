"""
Example 2: Creating Static Maps

This example demonstrates how to create static visualizations using matplotlib.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from usda_forest_viz import StaticMapVisualizer
from usda_forest_viz.utils import load_shapefile, filter_by_attribute, calculate_area
import matplotlib.pyplot as plt


def main():
    print("=" * 80)
    print("USDA Forest Service Static Map Visualization")
    print("=" * 80)
    
    # Check if data exists
    data_path = Path("../data/shapefiles/Actv_TimberHarvest")
    if not data_path.exists():
        print(f"\n✗ Data not found at {data_path}")
        print("Please run 01_download_data.py first to download the datasets.")
        return
    
    # Load the timber harvest data
    print("\nLoading timber harvest data...")
    gdf = load_shapefile(data_path)
    
    # Display basic information
    print(f"\nDataset information:")
    print(f"  - Total features: {len(gdf)}")
    print(f"  - CRS: {gdf.crs}")
    print(f"  - Columns: {', '.join(gdf.columns[:10])}...")
    
    # Initialize visualizer
    viz = StaticMapVisualizer()
    
    # Example 1: Basic polygon map
    print("\n" + "=" * 80)
    print("Example 1: Basic Polygon Map")
    print("=" * 80)
    
    fig = viz.plot_polygons(
        gdf.head(1000),  # Plot first 1000 features for speed
        title="USDA Forest Service Timber Harvests",
        figsize=(15, 10),
        alpha=0.6,
        output_path="../outputs/01_basic_map.png"
    )
    plt.close(fig)
    
    # Example 2: Colored by attribute
    print("\n" + "=" * 80)
    print("Example 2: Map Colored by Activity Type")
    print("=" * 80)
    
    # Find a good column for coloring
    if 'ACTIVITY' in gdf.columns:
        color_col = 'ACTIVITY'
    elif 'TYPE_NAME' in gdf.columns:
        color_col = 'TYPE_NAME'
    elif 'METHOD' in gdf.columns:
        color_col = 'METHOD'
    else:
        # Use first non-geometry column
        color_col = [col for col in gdf.columns if col != 'geometry'][0]
    
    print(f"Coloring by: {color_col}")
    
    fig = viz.plot_polygons(
        gdf.head(1000),
        column=color_col,
        title=f"Timber Harvests by {color_col}",
        cmap="tab20",
        figsize=(15, 10),
        output_path="../outputs/02_colored_map.png"
    )
    plt.close(fig)
    
    # Example 3: Calculate and visualize areas
    print("\n" + "=" * 80)
    print("Example 3: Choropleth Map of Treatment Areas")
    print("=" * 80)
    
    # Calculate areas
    gdf_with_area = calculate_area(gdf.head(1000), unit="acres")
    
    fig = viz.plot_choropleth(
        gdf_with_area,
        value_column="area_acres",
        title="Treatment Area (Acres)",
        cmap="YlOrRd",
        figsize=(15, 10),
        output_path="../outputs/03_area_choropleth.png"
    )
    plt.close(fig)
    
    # Example 4: Filter and visualize specific region
    print("\n" + "=" * 80)
    print("Example 4: Filtered Dataset")
    print("=" * 80)
    
    # Get unique values for filtering
    if 'STATE_ABBR' in gdf.columns:
        filter_col = 'STATE_ABBR'
        # Get most common state
        filter_value = gdf[filter_col].value_counts().index[0]
    elif 'REGION' in gdf.columns:
        filter_col = 'REGION'
        filter_value = gdf[filter_col].value_counts().index[0]
    else:
        filter_col = color_col
        filter_value = gdf[color_col].value_counts().index[0]
    
    print(f"Filtering by {filter_col} = {filter_value}")
    
    gdf_filtered = filter_by_attribute(gdf, filter_col, filter_value)
    
    if len(gdf_filtered) > 0:
        fig = viz.plot_polygons(
            gdf_filtered.head(500),
            title=f"Timber Harvests - {filter_col}: {filter_value}",
            figsize=(12, 10),
            color='forestgreen',
            output_path="../outputs/04_filtered_map.png"
        )
        plt.close(fig)
    
    print("\n" + "=" * 80)
    print("Static maps created successfully!")
    print("Check the 'outputs' directory for generated maps.")
    print("=" * 80)


if __name__ == "__main__":
    main()

