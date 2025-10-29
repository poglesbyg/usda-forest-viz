# Quick Start Guide

Get started with USDA Forest Service data visualization in 5 minutes!

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

```bash
# Clone or download the project
cd usda-forest-viz

# Install dependencies (uv will create a virtual environment)
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

## Your First Visualization in 3 Steps

### Step 1: Download Data

Create a file `quick_demo.py`:

```python
from usda_forest_viz import DatasetDownloader

# Download timber harvest data
downloader = DatasetDownloader(data_dir="data")
downloader.download_dataset("Actv_TimberHarvest", format="shapefile")
```

Run it:
```bash
python quick_demo.py
```

### Step 2: Create a Map

Add to `quick_demo.py`:

```python
from usda_forest_viz import StaticMapVisualizer
from usda_forest_viz.utils import load_shapefile

# Load the data
gdf = load_shapefile("data/shapefiles/Actv_TimberHarvest")

# Create visualizer and plot
viz = StaticMapVisualizer()
viz.plot_polygons(
    gdf.head(1000),  # First 1000 features
    title="USDA Timber Harvests",
    output_path="my_first_map.png"
)

print("✓ Map saved as my_first_map.png")
```

Run it:
```bash
python quick_demo.py
```

### Step 3: Create an Interactive Map

Add to `quick_demo.py`:

```python
from usda_forest_viz import InteractiveMapVisualizer

# Create interactive map
viz_interactive = InteractiveMapVisualizer()
m = viz_interactive.create_map(
    gdf.head(500),
    popup_fields=["ACTIVITY", "DATE_COMPLETED"],
    zoom_start=6
)

# Save to HTML
viz_interactive.save_map(m, "interactive_map.html")
print("✓ Interactive map saved as interactive_map.html")
print("  Open it in your web browser!")
```

Run it:
```bash
python quick_demo.py
```

Open `interactive_map.html` in your browser to explore!

## What's Next?

### Explore More Datasets

```python
# List all available datasets
downloader = DatasetDownloader()
print(downloader.list_available_datasets())

# Try hazardous fuel treatments
downloader.download_dataset("Actv_HazFuelTrt_PL", format="shapefile")

# Or silviculture reforestation
downloader.download_dataset("Actv_SilvReforest", format="shapefile")
```

### Perform Analysis

```python
from usda_forest_viz.utils import calculate_area, get_summary_statistics

# Calculate areas
gdf_with_area = calculate_area(gdf, unit="acres")
print(f"Total area: {gdf_with_area['area_acres'].sum():,.0f} acres")

# Get statistics
stats = get_summary_statistics(gdf_with_area)
print(stats)
```

### Filter Data

```python
from usda_forest_viz.utils import filter_by_attribute, filter_by_bounds

# Filter by state (if column exists)
california_data = filter_by_attribute(gdf, "STATE_ABBR", "CA")

# Filter by bounding box (minx, miny, maxx, maxy)
west_coast = filter_by_bounds(gdf, (-125, 32, -114, 42))
```

### Customize Visualizations

```python
# Change colors and styles
viz.plot_polygons(
    gdf.head(1000),
    column="ACTIVITY",  # Color by this column
    title="Timber Harvests by Activity Type",
    cmap="tab20",       # Color scheme
    figsize=(20, 15),   # Larger figure
    alpha=0.8,          # More opaque
    output_path="custom_map.png"
)
```

## Example Scripts

Check out the `examples/` directory for comprehensive examples:

- `01_download_data.py` - Download multiple datasets
- `02_static_maps.py` - Create publication-quality maps
- `03_interactive_maps.py` - Build web maps with Folium
- `04_analysis.py` - Perform spatial analysis

## Common Use Cases

### 1. Track Wildfire Management

```python
# Download hazardous fuel treatment data
downloader.download_dataset("Actv_HazFuelTrt_PL", format="shapefile")
gdf = load_shapefile("data/shapefiles/Actv_HazFuelTrt_PL")

# Calculate total area treated
gdf_area = calculate_area(gdf, unit="acres")
print(f"Total fuel reduction area: {gdf_area['area_acres'].sum():,.0f} acres")
```

### 2. Monitor Reforestation Efforts

```python
# Download reforestation data
downloader.download_dataset("Actv_SilvReforest", format="shapefile")
gdf = load_shapefile("data/shapefiles/Actv_SilvReforest")

# Analyze by year (if date column exists)
# Filter and visualize recent plantings
```

### 3. Compare Multiple Activities

```python
from usda_forest_viz import StaticMapVisualizer

# Load multiple datasets
harvest = load_shapefile("data/shapefiles/Actv_TimberHarvest")
reforest = load_shapefile("data/shapefiles/Actv_SilvReforest")

# Create side-by-side comparison
viz = StaticMapVisualizer()
viz.create_comparison_map(
    [harvest.head(500), reforest.head(500)],
    titles=["Timber Harvest", "Reforestation"],
    output_path="comparison.png"
)
```

## Tips

1. **Start Small**: Use `.head(n)` to work with subsets of large datasets
2. **Check CRS**: The tools automatically handle coordinate transformations
3. **Save Memory**: Download in shapefile format for smaller datasets, geodatabase for complex ones
4. **Explore Metadata**: Each dataset has metadata at the USDA website
5. **Use Filters**: Apply spatial and attribute filters before visualization for better performance

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review [examples/](examples/) for complete use cases
- Visit [USDA Forest Service Data Portal](https://data.fs.usda.gov/geodata/edw/datasets.php) for dataset information

## Troubleshooting

**"Module not found" error?**
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate
```

**Download fails?**
- Check your internet connection
- Some datasets are very large (500+ MB)
- Try a smaller dataset first

**Out of memory?**
- Use `.head(n)` to work with fewer features
- Try a different dataset with fewer features
- Close other applications

Happy mapping! 🗺️

