# Examples

This directory contains example scripts demonstrating how to use the USDA Forest Service data visualization tools.

## Running the Examples

Make sure you've installed the package and activated the virtual environment:

```bash
cd /path/to/usda-forest-viz
source .venv/bin/activate  # On Unix/macOS
```

Then run the examples in order:

### 1. Download Data

```bash
cd examples
python 01_download_data.py
```

This script downloads sample datasets from the USDA Forest Service. The data will be saved to the `data/` directory.

**Note:** Some datasets are large (100+ MB). The download may take several minutes depending on your internet connection.

### 2. Create Static Maps

```bash
python 02_static_maps.py
```

Creates publication-quality static maps using matplotlib. Output files are saved to `outputs/`.

### 3. Create Interactive Maps

```bash
python 03_interactive_maps.py
```

Generates interactive HTML maps using Folium. Open the generated HTML files in a web browser to explore the data.

### 4. Perform Analysis

```bash
python 04_analysis.py
```

Demonstrates spatial analysis capabilities including area calculations, summary statistics, temporal analysis, and more.

## Example Output

After running all examples, you should have:

- **Downloaded data** in `data/shapefiles/` and `data/geodatabases/`
- **Static maps** (PNG) in `outputs/`:
  - Basic polygon maps
  - Choropleth maps
  - Filtered visualizations
  - Statistical charts
- **Interactive maps** (HTML) in `outputs/`:
  - Basic interactive map
  - Satellite imagery base
  - Styled by attributes
  - Filtered datasets

## Customization

Each example script is well-commented and can be easily modified to:
- Download different datasets
- Change visualization styles and colors
- Filter data by different criteria
- Analyze different attributes
- Create custom analyses

## Troubleshooting

### "Data not found" Error

If you get an error about missing data, make sure you've run `01_download_data.py` first.

### Memory Issues

If you encounter memory errors with large datasets, reduce the number of features being visualized by using `.head(n)` to select a subset.

### Missing Dependencies

If you get import errors, make sure all dependencies are installed:

```bash
uv sync
```

### CRS Warnings

Coordinate Reference System (CRS) warnings are normal when reprojecting data. The scripts handle CRS transformations automatically.

