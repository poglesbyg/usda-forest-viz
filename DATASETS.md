# Available USDA Forest Service Datasets

This document provides information about the datasets available through this visualization tool.

## Data Source

All datasets are from the **USDA Forest Service Enterprise Data Warehouse (EDW)**:
- **Main Portal**: https://data.fs.usda.gov/geodata/edw/datasets.php
- **Discovery Tool**: https://data-usfs.hub.arcgis.com/
- **Contact**: SM.FS.data@usda.gov

## Currently Supported Datasets

### 1. Timber Harvest Activities (`Actv_TimberHarvest`)

**Description**: Areas where timber harvest activities have been completed, including commercial thinning, clearcut, shelterwood, seed tree, and other harvest methods.

**Features**: Polygons representing harvest units  
**Update Frequency**: Updated regularly from FACTS database  
**Last Update**: Check metadata for current date  

**Use Cases**:
- Track timber harvest operations
- Analyze harvest methods and patterns
- Monitor sustainable forestry practices
- Calculate harvested areas by region/year

**Download**:
```python
downloader.download_dataset("Actv_TimberHarvest", format="shapefile")
```

---

### 2. Hazardous Fuel Treatment - Polygon (`Actv_HazFuelTrt_PL`)

**Description**: Polygon features representing areas treated to reduce hazardous fuels. Includes burning, mechanical treatments, and other methods to reduce wildfire risk.

**Features**: Polygons of treated areas  
**Size**: Large dataset (600+ MB)  
**Update Frequency**: Regular updates

**Use Cases**:
- Wildfire risk management analysis
- Track fuel reduction efforts
- Monitor fire prevention activities
- Calculate treated acres by state/forest

**Download**:
```python
downloader.download_dataset("Actv_HazFuelTrt_PL", format="shapefile")
```

---

### 3. Hazardous Fuel Treatment - Line (`Actv_HazFuelTrt_LN`)

**Description**: Linear fuel treatment features such as fuel breaks and defensible space along roads.

**Features**: Line features  
**Size**: Small dataset

**Use Cases**:
- Map fuel breaks and fire lines
- Analyze linear fuel treatment patterns
- Track roadside fuel management

**Download**:
```python
downloader.download_dataset("Actv_HazFuelTrt_LN", format="shapefile")
```

---

### 4. Silviculture Reforestation (`Actv_SilvReforest`)

**Description**: Areas where reforestation activities have occurred, including planting, seeding, site preparation, and natural regeneration certification.

**Features**: Polygons of reforested areas  
**Size**: Large dataset (500+ MB)

**Use Cases**:
- Track reforestation efforts
- Monitor post-harvest regeneration
- Analyze planting vs. natural regeneration
- Calculate reforested acres

**Download**:
```python
downloader.download_dataset("Actv_SilvReforest", format="shapefile")
```

---

### 5. Timber Stand Improvement (`Actv_SilvTSI`)

**Description**: Areas treated for timber stand improvement including precommercial thinning, pruning, release, weeding, cleaning, and fertilization.

**Features**: Polygons of treatment areas  
**Size**: Large dataset (400+ MB)

**Use Cases**:
- Track forest health improvements
- Monitor stand management activities
- Analyze treatment methods
- Calculate improvement areas

**Download**:
```python
downloader.download_dataset("Actv_SilvTSI", format="shapefile")
```

---

### 6. Range Vegetation Improvement (`Actv_RngVegImprove`)

**Description**: Areas treated for range vegetation improvement to enhance grazing lands and wildlife habitat.

**Features**: Polygons of treatment areas  
**Size**: Medium dataset (80+ MB)

**Use Cases**:
- Monitor rangeland management
- Track vegetation improvement projects
- Analyze grazing land treatments
- Calculate improved acreage

**Download**:
```python
downloader.download_dataset("Actv_RngVegImprove", format="shapefile")
```

---

## Common Data Fields

Most activity datasets share common attribute fields:

- **ACTIVITY_NAME**: Name/description of the activity
- **ACTIVITY_CODE**: Numeric code for activity type
- **DATE_COMPLETED**: Date the activity was completed
- **DATE_AWARDED**: Date the activity was initiated
- **ACTIVITY_QUANTITY**: Quantity (usually acres) treated
- **ACTIVITY_UOM**: Unit of measure
- **STATE_ABBR**: State abbreviation
- **REGION**: Forest Service region
- **FOREST_NAME**: National Forest name
- **DISTRICT**: Ranger District
- **METHOD**: Treatment method used

*Note: Actual field names may vary by dataset. Check the metadata for specific information.*

## Data Formats

### Shapefile
- Traditional GIS format
- Widely compatible
- Limited to 2GB file size
- Being phased out for large datasets

### ESRI File Geodatabase (.gdb)
- Recommended format
- No file size limitations
- Better attribute support
- Can contain multiple layers

### Accessing Other Datasets

This tool currently supports 6 pre-configured datasets. To access other USDA Forest Service datasets:

1. **Browse the catalog**: https://data.fs.usda.gov/geodata/edw/datasets.php
2. **Find the download URL** for your dataset
3. **Use custom download**:

```python
downloader = DatasetDownloader()
downloader.download_custom_dataset(
    url="https://data.fs.usda.gov/geodata/edw/edw_resources/shp/YourDataset.zip",
    output_name="YourDataset",
    format="shapefile"
)
```

## Dataset Categories

The USDA Forest Service organizes datasets into these categories:

### Biota (23 datasets)
Wildlife habitats, vegetation surveys, species observations

### Boundaries (62 datasets)
- National Forest boundaries
- Ranger District boundaries
- Wilderness areas
- Land ownership
- Administrative units

### Environment (106 datasets)
- Fire perimeters and history
- Watersheds and hydrology
- Air quality monitoring
- Climate data
- Soil surveys

### Geoscientific (8 datasets)
Geology, mineral resources, geological hazards

### Imagery & Basemaps (1 dataset)
Topographic and reference imagery

### Inland Waters (23 datasets)
Rivers, streams, lakes, wetlands

### Planning Cadastre (12 datasets)
Land use planning, cadastral surveys

### Structure (7 datasets)
Buildings, facilities, infrastructure

### Transportation (4 datasets)
Roads, trails, recreation routes

## Data Quality and Updates

- **Source**: Data is self-reported by Forest Service units through the FACTS (Forest Activity Tracking System) database
- **Updates**: Most datasets are updated regularly (weekly to monthly)
- **Completeness**: Spatial data reporting is not 100% complete; coverage improves over time
- **Accuracy**: Positional accuracy varies by dataset and reporting unit
- **Validation**: Check metadata files for data quality information

## Metadata

Each dataset includes metadata in XML format:

```python
# Get metadata URL
info = downloader.get_dataset_info("Actv_TimberHarvest")
print(info['metadata_url'])
# https://data.fs.usda.gov/geodata/edw/edw_resources/meta/Actv_TimberHarvest.xml
```

Metadata includes:
- Abstract and purpose
- Geographic extent
- Attribute descriptions
- Data quality information
- Contact information
- Update frequency
- Use constraints

## Performance Tips

1. **Start with small datasets** for testing
2. **Use shapefiles for smaller datasets** (< 100 MB)
3. **Use geodatabases for large datasets** (> 100 MB)
4. **Download during off-peak hours** for large files
5. **Filter data immediately** after loading to reduce memory usage
6. **Use spatial indexing** for faster queries with large datasets

## Legal and Usage

- **Public Domain**: USDA Forest Service data is in the public domain
- **No restrictions**: Free to use for any purpose
- **Attribution**: Attribution appreciated but not required
- **No warranty**: Data is provided "as-is" without warranty

## Getting Help

For questions about:
- **This tool**: Create an issue on GitHub
- **The datasets**: Contact SM.FS.data@usda.gov
- **Data access**: https://data.fs.usda.gov/geodata/help.php

## Additional Resources

- **USDA Forest Service Geospatial Data Discovery**: https://data-usfs.hub.arcgis.com/
- **Data.gov Forest Service Data**: https://catalog.data.gov/organization/fs
- **Map Services**: https://apps.fs.usda.gov/arcx/rest/services/
- **FSGeodata Clearinghouse**: https://data.fs.usda.gov/geodata/

