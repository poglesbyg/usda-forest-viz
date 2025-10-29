# Contributing to USDA Forest Service Visualization

Thank you for your interest in contributing! This document provides guidelines for adding new features, datasets, and improvements.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Install dependencies: `uv sync`
4. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

```bash
# Clone the repository
git clone <your-fork-url>
cd usda-forest-viz

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run tests
uv run python test_installation.py
```

## How to Contribute

### Adding New Datasets

To add support for a new USDA Forest Service dataset:

1. **Find the dataset** at https://data.fs.usda.gov/geodata/edw/datasets.php

2. **Get the download URLs** for both shapefile and geodatabase formats

3. **Add to `downloader.py`**:

```python
# In the DatasetDownloader.DATASETS dictionary
"YourDatasetName": {
    "shapefile": "edw_resources/shp/YourDataset.zip",
    "geodatabase": "edw_resources/fc/YourDataset.gdb.zip",
}
```

4. **Update documentation**:
   - Add dataset description to `DATASETS.md`
   - Update README.md if it's a commonly used dataset
   - Add usage example if needed

5. **Test the download**:
```python
downloader = DatasetDownloader()
downloader.download_dataset("YourDatasetName", format="shapefile")
```

### Adding New Visualization Types

To add a new visualization method:

1. **Add method to appropriate visualizer class** in `visualizer.py`:
   - `StaticMapVisualizer` for matplotlib-based plots
   - `InteractiveMapVisualizer` for Folium maps
   - `PlotlyVisualizer` for Plotly visualizations

2. **Follow existing method signatures**:
```python
def your_new_plot(
    self,
    gdf: gpd.GeoDataFrame,
    # ... other parameters
    output_path: Optional[str] = None
) -> Union[plt.Figure, folium.Map]:
    """
    Your visualization method.
    
    Args:
        gdf: GeoDataFrame to visualize
        output_path: Optional path to save output
        
    Returns:
        Figure or map object
    """
    # Your implementation
    pass
```

3. **Add example usage** in the `examples/` directory

### Adding Utility Functions

To add new utility functions to `utils.py`:

1. **Write the function** with proper type hints:
```python
def your_utility_function(
    gdf: gpd.GeoDataFrame,
    param: str
) -> gpd.GeoDataFrame:
    """
    Brief description.
    
    Args:
        gdf: Input GeoDataFrame
        param: Description of parameter
        
    Returns:
        Modified GeoDataFrame
    """
    # Implementation
    return result
```

2. **Add to exports** in `__init__.py` if it's a commonly used function

3. **Add example usage** in documentation

### Adding Examples

To add a new example script:

1. **Create file** in `examples/` directory: `05_your_example.py`

2. **Follow the template**:
```python
"""
Example X: Your Example Title

Brief description of what this example demonstrates.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from usda_forest_viz import DatasetDownloader

def main():
    print("=" * 80)
    print("Your Example Title")
    print("=" * 80)
    
    # Your example code
    
    print("\n" + "=" * 80)
    print("Example complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
```

3. **Update `examples/README.md`** with your new example

## Code Style

### Python Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write docstrings for all functions and classes
- Use meaningful variable names

### Docstring Format

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief one-line description.
    
    Longer description if needed, explaining what the function does,
    any important details, or usage notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Import Organization

```python
# Standard library imports
import os
from pathlib import Path
from typing import Optional, List

# Third-party imports
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

# Local imports
from usda_forest_viz.utils import load_shapefile
```

## Testing

Currently, the project uses a simple installation test. When adding new features:

1. **Manual testing**: Test your changes with real data
2. **Update test script**: Add tests to `test_installation.py` if adding core functionality
3. **Run existing tests**: `uv run python test_installation.py`

Future: We plan to add pytest-based unit tests and integration tests.

## Documentation

### Required Documentation Updates

When adding features, update:

1. **README.md**: If it's a major feature
2. **QUICKSTART.md**: If it simplifies common workflows
3. **DATASETS.md**: When adding new datasets
4. **Docstrings**: Always document your code
5. **Examples**: Add examples for new features

### Documentation Style

- Use clear, concise language
- Include code examples
- Add use cases when relevant
- Link to related documentation

## Pull Request Process

1. **Update documentation** for your changes
2. **Test your changes** thoroughly
3. **Run the installation test**: `uv run python test_installation.py`
4. **Create pull request** with:
   - Clear title describing the change
   - Description of what changed and why
   - Any breaking changes noted
   - Examples of new functionality

### PR Title Format

```
feat: Add support for Wilderness Area datasets
fix: Correct CRS handling in buffer function
docs: Update QUICKSTART with new examples
refactor: Simplify downloader error handling
```

## Feature Ideas

Looking for something to contribute? Here are some ideas:

### High Priority

- [ ] Add more commonly-used datasets
- [ ] Add automated tests (pytest)
- [ ] Add CLI interface for common operations
- [ ] Support for ArcGIS REST API map services
- [ ] Batch downloading of multiple datasets
- [ ] Progress bars for large downloads
- [ ] Caching for repeated downloads

### Visualization Enhancements

- [ ] 3D terrain visualizations
- [ ] Animation of temporal data
- [ ] Heatmap generation
- [ ] Custom color ramps and legends
- [ ] Better handling of large datasets (simplification)
- [ ] Export to various image formats (SVG, PDF)

### Analysis Features

- [ ] Proximity analysis
- [ ] Overlay analysis between datasets
- [ ] Time series analysis tools
- [ ] Statistical reporting
- [ ] Export to common formats (CSV, Excel)
- [ ] Integration with pandas for data analysis

### Data Management

- [ ] Dataset version tracking
- [ ] Automatic update checking
- [ ] Metadata parsing and display
- [ ] Data validation tools
- [ ] Conversion between formats

### Integration

- [ ] Jupyter notebook integration
- [ ] Integration with other GIS tools
- [ ] Export to QGIS/ArcGIS formats
- [ ] REST API for web applications
- [ ] Docker container for easy deployment

## Questions?

- Open an issue for questions about contributing
- Check existing issues for known problems
- Read the documentation thoroughly

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the best outcome for the community
- Assume good intentions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make USDA Forest Service data more accessible!

