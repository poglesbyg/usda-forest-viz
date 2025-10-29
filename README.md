# USDA Forest Service Data Visualization

A Python project for downloading and visualizing geospatial datasets from the USDA Forest Service Enterprise Data Warehouse (EDW).

## Overview

This project provides tools to work with datasets from the [USDA Forest Service Geodata Clearinghouse](https://data.fs.usda.gov/geodata/edw/datasets.php), including:

- **Activity datasets**: Timber harvests, silviculture, hazardous fuel treatments, range vegetation improvements
- **Boundaries**: National forests, ranger districts, wilderness areas
- **Environmental data**: Fire perimeters, wildlife habitats, watersheds
- **Infrastructure**: Roads, trails, recreation sites

## Features

- 📥 Download datasets in multiple formats (Shapefile, GeoJSON, ESRI Geodatabase)
- 🗺️ Create static and interactive maps
- 📊 Generate statistical visualizations
- 🔍 Query and filter geospatial data
- 🎨 Customizable map styling

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management.

```bash
# Clone the repository
git clone <repository-url>
cd usda-forest-viz

# Install dependencies (uv will create a virtual environment automatically)
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

## Quick Start

### 1. Download a Dataset

```python
from usda_forest_viz.downloader import DatasetDownloader

# Initialize downloader
downloader = DatasetDownloader(data_dir="data")

# Download timber harvest data (shapefile format)
downloader.download_dataset(
    name="Actv_TimberHarvest",
    format="shapefile"
)
```

### 2. Create a Static Map

```python
from usda_forest_viz.visualizer import StaticMapVisualizer
import geopandas as gpd

# Load the data
gdf = gpd.read_file("data/shapefiles/Actv_TimberHarvest.shp")

# Create visualizer
viz = StaticMapVisualizer()

# Plot timber harvest areas
viz.plot_polygons(
    gdf,
    column="TREATMENT_TYPE",
    title="USDA Forest Service Timber Harvests",
    cmap="viridis",
    figsize=(15, 10)
)
```

### 3. Create an Interactive Map

```python
from usda_forest_viz.visualizer import InteractiveMapVisualizer

# Create interactive map
viz = InteractiveMapVisualizer()
m = viz.create_map(
    gdf,
    style_column="TREATMENT_TYPE",
    popup_fields=["ACTIVITY_NAME", "ACTIVITY_QUANTITY", "DATE_COMPLETED"]
)

# Save to HTML
m.save("timber_harvests_map.html")
```

## Available Datasets

The USDA Forest Service provides numerous datasets categorized by:

- **Biota** (23 datasets): Wildlife habitats, vegetation surveys
- **Boundaries** (62 datasets): Administrative boundaries, land ownership
- **Environment** (106 datasets): Fire history, watersheds, climate data
- **Geoscientific** (8 datasets): Geology, soils
- **Imagery & Basemaps** (1 dataset)
- **Inland Waters** (23 datasets): Rivers, lakes, wetlands
- **Planning Cadastre** (12 datasets): Land use planning
- **Structure** (7 datasets): Buildings, facilities
- **Transportation** (4 datasets): Roads, trails

Popular datasets include:
- `Actv_TimberHarvest`: Timber harvest activities
- `Actv_HazFuelTrt_PL`: Hazardous fuel treatment areas
- `Actv_SilvReforest`: Silviculture reforestation activities
- National forest boundaries
- Wilderness areas
- Fire perimeters

## Project Structure

```
usda-forest-viz/
├── src/
│   └── usda_forest_viz/
│       ├── __init__.py
│       ├── downloader.py      # Dataset downloading utilities
│       ├── visualizer.py      # Visualization tools
│       └── utils.py           # Helper functions
├── examples/
│   ├── 01_download_data.py
│   ├── 02_static_maps.py
│   ├── 03_interactive_maps.py
│   └── 04_analysis.py
├── data/                      # Downloaded datasets (not in git)
│   ├── shapefiles/
│   ├── geodatabases/
│   └── geojson/
├── outputs/                   # Generated visualizations
├── pyproject.toml
└── README.md
```

## Data Formats

The USDA Forest Service provides data in multiple formats:

1. **Shapefiles** (`.shp`): Traditional GIS format (being phased out for large datasets)
2. **ESRI File Geodatabase** (`.gdb`): Recommended format for complex datasets
3. **GeoJSON**: Web-friendly format
4. **Map Services**: ArcGIS REST API endpoints

**Note**: Shapefiles are being retired for datasets that exceed technical limitations. Use ESRI File Geodatabase or GeoJSON for best results.

## Examples

See the `examples/` directory for detailed usage examples:

- **01_download_data.py**: Download multiple datasets
- **02_static_maps.py**: Create publication-quality static maps
- **03_interactive_maps.py**: Build interactive web maps with Folium
- **04_analysis.py**: Perform spatial analysis and generate statistics

## Data Sources

All data is sourced from:
- **Main Portal**: https://data.fs.usda.gov/geodata/edw/datasets.php
- **Geospatial Discovery Tool**: https://data-usfs.hub.arcgis.com/
- **Map Services**: https://apps.fs.usda.gov/arcx/rest/services/

## License

This project is licensed under the MIT License. The USDA Forest Service datasets are public domain.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Data provided by the USDA Forest Service, Field Services and Innovation Center, Geospatial Office (FSIC-GO).

For questions about the data, contact: [SM.FS.data@usda.gov](mailto:SM.FS.data@usda.gov)

