"""
Utility functions for working with USDA Forest Service datasets.
"""

from pathlib import Path
from typing import Optional, Tuple
import geopandas as gpd
import pandas as pd


def load_shapefile(directory: Path, name: Optional[str] = None) -> gpd.GeoDataFrame:
    """
    Load a shapefile from a directory.
    
    Args:
        directory: Directory containing shapefile
        name: Specific shapefile name (without .shp extension). If None, loads first .shp found
        
    Returns:
        GeoDataFrame
        
    Raises:
        FileNotFoundError: If no shapefile found
    """
    directory = Path(directory)
    
    if name:
        shp_path = directory / f"{name}.shp"
    else:
        # Find first .shp file
        shp_files = list(directory.glob("*.shp"))
        if not shp_files:
            raise FileNotFoundError(f"No shapefile found in {directory}")
        shp_path = shp_files[0]
    
    if not shp_path.exists():
        raise FileNotFoundError(f"Shapefile not found: {shp_path}")
    
    print(f"Loading {shp_path}...")
    gdf = gpd.read_file(shp_path)
    print(f"Loaded {len(gdf)} features")
    
    return gdf


def load_geodatabase(directory: Path, layer: Optional[str] = None) -> gpd.GeoDataFrame:
    """
    Load a layer from an ESRI File Geodatabase.
    
    Args:
        directory: Directory containing .gdb folder
        layer: Specific layer name. If None, loads first layer
        
    Returns:
        GeoDataFrame
        
    Raises:
        FileNotFoundError: If no geodatabase found
    """
    directory = Path(directory)
    
    # Find .gdb directory
    gdb_dirs = list(directory.glob("*.gdb"))
    if not gdb_dirs:
        raise FileNotFoundError(f"No geodatabase found in {directory}")
    
    gdb_path = gdb_dirs[0]
    
    # List available layers
    import fiona
    layers = fiona.listlayers(gdb_path)
    
    if not layers:
        raise ValueError(f"No layers found in {gdb_path}")
    
    if layer:
        if layer not in layers:
            raise ValueError(f"Layer '{layer}' not found. Available layers: {', '.join(layers)}")
        layer_name = layer
    else:
        layer_name = layers[0]
    
    print(f"Loading layer '{layer_name}' from {gdb_path}...")
    gdf = gpd.read_file(gdb_path, layer=layer_name)
    print(f"Loaded {len(gdf)} features")
    
    return gdf


def filter_by_bounds(
    gdf: gpd.GeoDataFrame,
    bounds: Tuple[float, float, float, float]
) -> gpd.GeoDataFrame:
    """
    Filter GeoDataFrame by bounding box.
    
    Args:
        gdf: GeoDataFrame to filter
        bounds: Bounding box (minx, miny, maxx, maxy)
        
    Returns:
        Filtered GeoDataFrame
    """
    minx, miny, maxx, maxy = bounds
    
    # Create bounding box
    from shapely.geometry import box
    bbox = box(minx, miny, maxx, maxy)
    
    # Filter features that intersect the bounding box
    filtered = gdf[gdf.geometry.intersects(bbox)]
    
    print(f"Filtered from {len(gdf)} to {len(filtered)} features")
    
    return filtered


def filter_by_attribute(
    gdf: gpd.GeoDataFrame,
    column: str,
    value
) -> gpd.GeoDataFrame:
    """
    Filter GeoDataFrame by attribute value.
    
    Args:
        gdf: GeoDataFrame to filter
        column: Column name
        value: Value to filter by (can be single value or list)
        
    Returns:
        Filtered GeoDataFrame
    """
    if isinstance(value, (list, tuple)):
        filtered = gdf[gdf[column].isin(value)]
    else:
        filtered = gdf[gdf[column] == value]
    
    print(f"Filtered from {len(gdf)} to {len(filtered)} features")
    
    return filtered


def calculate_area(gdf: gpd.GeoDataFrame, unit: str = "acres") -> gpd.GeoDataFrame:
    """
    Calculate area for polygon features.
    
    Args:
        gdf: GeoDataFrame with polygon geometries
        unit: Unit for area calculation ('acres', 'hectares', 'sqm', 'sqkm')
        
    Returns:
        GeoDataFrame with added 'area' column
    """
    # Reproject to equal-area projection for accurate area calculation
    # Using Albers Equal Area for US
    gdf_proj = gdf.to_crs("EPSG:5070")
    
    # Calculate area in square meters
    area_sqm = gdf_proj.geometry.area
    
    # Convert to desired unit
    conversions = {
        "sqm": 1,
        "sqkm": 1e-6,
        "acres": 0.000247105,
        "hectares": 0.0001
    }
    
    if unit not in conversions:
        raise ValueError(f"Unit must be one of: {', '.join(conversions.keys())}")
    
    gdf = gdf.copy()
    gdf[f"area_{unit}"] = area_sqm * conversions[unit]
    
    return gdf


def get_summary_statistics(gdf: gpd.GeoDataFrame, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Get summary statistics for numeric columns.
    
    Args:
        gdf: GeoDataFrame
        columns: Specific columns to summarize (if None, summarizes all numeric columns)
        
    Returns:
        DataFrame with summary statistics
    """
    if columns:
        df = gdf[columns]
    else:
        df = gdf.select_dtypes(include=['number'])
    
    return df.describe()


def export_to_geojson(gdf: gpd.GeoDataFrame, output_path: str):
    """
    Export GeoDataFrame to GeoJSON format.
    
    Args:
        gdf: GeoDataFrame to export
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    gdf.to_file(output_path, driver="GeoJSON")
    print(f"Exported to {output_path}")


def merge_datasets(
    gdfs: list[gpd.GeoDataFrame],
    how: str = "union"
) -> gpd.GeoDataFrame:
    """
    Merge multiple GeoDataFrames.
    
    Args:
        gdfs: List of GeoDataFrames to merge
        how: How to merge ('union' or 'intersection')
        
    Returns:
        Merged GeoDataFrame
    """
    if not gdfs:
        raise ValueError("No GeoDataFrames provided")
    
    if len(gdfs) == 1:
        return gdfs[0]
    
    # Ensure all have same CRS
    crs = gdfs[0].crs
    gdfs = [gdf.to_crs(crs) for gdf in gdfs]
    
    # Concatenate
    merged = pd.concat(gdfs, ignore_index=True)
    
    return merged


def create_buffer(
    gdf: gpd.GeoDataFrame,
    distance: float,
    unit: str = "meters"
) -> gpd.GeoDataFrame:
    """
    Create buffer around geometries.
    
    Args:
        gdf: GeoDataFrame
        distance: Buffer distance
        unit: Distance unit ('meters', 'kilometers', 'miles', 'feet')
        
    Returns:
        GeoDataFrame with buffered geometries
    """
    # Convert to projected CRS for accurate buffering
    gdf_proj = gdf.to_crs("EPSG:5070")
    
    # Convert distance to meters
    conversions = {
        "meters": 1,
        "kilometers": 1000,
        "miles": 1609.34,
        "feet": 0.3048
    }
    
    if unit not in conversions:
        raise ValueError(f"Unit must be one of: {', '.join(conversions.keys())}")
    
    distance_m = distance * conversions[unit]
    
    # Create buffer
    buffered = gdf_proj.copy()
    buffered.geometry = gdf_proj.geometry.buffer(distance_m)
    
    # Convert back to original CRS
    return buffered.to_crs(gdf.crs)


def spatial_join(
    gdf1: gpd.GeoDataFrame,
    gdf2: gpd.GeoDataFrame,
    how: str = "inner",
    predicate: str = "intersects"
) -> gpd.GeoDataFrame:
    """
    Perform spatial join between two GeoDataFrames.
    
    Args:
        gdf1: First GeoDataFrame
        gdf2: Second GeoDataFrame
        how: Type of join ('inner', 'left', 'right')
        predicate: Spatial relationship ('intersects', 'contains', 'within')
        
    Returns:
        Joined GeoDataFrame
    """
    # Ensure same CRS
    if gdf1.crs != gdf2.crs:
        gdf2 = gdf2.to_crs(gdf1.crs)
    
    return gpd.sjoin(gdf1, gdf2, how=how, predicate=predicate)

