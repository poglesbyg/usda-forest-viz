"""
Example 3: Creating Interactive Maps

This example demonstrates how to create interactive web maps using Folium.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from usda_forest_viz import InteractiveMapVisualizer
from usda_forest_viz.utils import load_shapefile, filter_by_attribute


def main():
    print("=" * 80)
    print("USDA Forest Service Interactive Map Visualization")
    print("=" * 80)
    
    # Check if data exists
    data_path = Path("../data/shapefiles/Actv_TimberHarvest")
    if not data_path.exists():
        print(f"\n✗ Data not found at {data_path}")
        print("Please run 01_download_data.py first to download the datasets.")
        return
    
    # Load the data
    print("\nLoading timber harvest data...")
    gdf = load_shapefile(data_path)
    
    # For interactive maps, we'll use a subset to keep file size reasonable
    print(f"Using subset of {min(500, len(gdf))} features for interactive map...")
    gdf_subset = gdf.head(500)
    
    # Initialize visualizer
    viz = InteractiveMapVisualizer()
    
    # Example 1: Basic interactive map
    print("\n" + "=" * 80)
    print("Example 1: Basic Interactive Map")
    print("=" * 80)
    
    # Determine popup fields (use first few non-geometry columns)
    popup_fields = [col for col in gdf_subset.columns if col != 'geometry'][:5]
    print(f"Popup fields: {', '.join(popup_fields)}")
    
    m = viz.create_map(
        gdf_subset,
        popup_fields=popup_fields,
        tooltip_fields=popup_fields[:2],
        zoom_start=6,
        tiles="OpenStreetMap"
    )
    
    output_path = "../outputs/01_interactive_basic.html"
    viz.save_map(m, output_path)
    print(f"✓ Saved to {output_path}")
    
    # Example 2: Map with different basemap
    print("\n" + "=" * 80)
    print("Example 2: Map with Satellite Imagery")
    print("=" * 80)
    
    m = viz.create_map(
        gdf_subset,
        popup_fields=popup_fields,
        zoom_start=6,
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        color="yellow",
        fill_opacity=0.5
    )
    
    output_path = "../outputs/02_interactive_satellite.html"
    viz.save_map(m, output_path)
    print(f"✓ Saved to {output_path}")
    
    # Example 3: Styled by attribute
    print("\n" + "=" * 80)
    print("Example 3: Styled by Attribute")
    print("=" * 80)
    
    # Find a good column for styling
    if 'ACTIVITY' in gdf_subset.columns:
        style_col = 'ACTIVITY'
    elif 'TYPE_NAME' in gdf_subset.columns:
        style_col = 'TYPE_NAME'
    elif 'METHOD' in gdf_subset.columns:
        style_col = 'METHOD'
    else:
        style_col = [col for col in gdf_subset.columns if col != 'geometry'][0]
    
    print(f"Styling by: {style_col}")
    
    m = viz.create_map(
        gdf_subset,
        style_column=style_col,
        popup_fields=popup_fields,
        tooltip_fields=[style_col],
        zoom_start=6
    )
    
    output_path = "../outputs/03_interactive_styled.html"
    viz.save_map(m, output_path)
    print(f"✓ Saved to {output_path}")
    
    # Example 4: Filtered dataset
    print("\n" + "=" * 80)
    print("Example 4: Filtered Interactive Map")
    print("=" * 80)
    
    # Filter by most common value
    if 'STATE_ABBR' in gdf.columns:
        filter_col = 'STATE_ABBR'
        filter_value = gdf[filter_col].value_counts().index[0]
    elif style_col in gdf.columns:
        filter_col = style_col
        filter_value = gdf[filter_col].value_counts().index[0]
    else:
        print("Skipping filtered example (no suitable column)")
        return
    
    print(f"Filtering by {filter_col} = {filter_value}")
    gdf_filtered = filter_by_attribute(gdf, filter_col, filter_value)
    gdf_filtered = gdf_filtered.head(500)
    
    if len(gdf_filtered) > 0:
        m = viz.create_map(
            gdf_filtered,
            popup_fields=popup_fields,
            tooltip_fields=[filter_col],
            zoom_start=7,
            color="red"
        )
        
        output_path = "../outputs/04_interactive_filtered.html"
        viz.save_map(m, output_path)
        print(f"✓ Saved to {output_path}")
    
    print("\n" + "=" * 80)
    print("Interactive maps created successfully!")
    print("Open the HTML files in 'outputs' directory with a web browser.")
    print("=" * 80)


if __name__ == "__main__":
    main()

