"""
Dataset downloading utilities for USDA Forest Service data.
"""

import os
from pathlib import Path
from typing import Literal, Optional
import requests
from urllib.parse import urljoin
import zipfile
import io


class DatasetDownloader:
    """
    Download and manage USDA Forest Service datasets.
    
    Attributes:
        base_url: Base URL for the USDA Forest Service data clearinghouse
        data_dir: Local directory to store downloaded datasets
    """
    
    BASE_URL = "https://data.fs.usda.gov/geodata/edw/"
    
    # Common dataset names and their download URLs
    DATASETS = {
        "Actv_TimberHarvest": {
            "shapefile": "edw_resources/shp/Actv_TimberHarvest.zip",
            "geodatabase": "edw_resources/fc/Actv_TimberHarvest.gdb.zip",
        },
        "Actv_HazFuelTrt_PL": {
            "shapefile": "edw_resources/shp/Actv_HazFuelTrt_PL.zip",
            "geodatabase": "edw_resources/fc/Actv_HazFuelTrt_PL.gdb.zip",
        },
        "Actv_HazFuelTrt_LN": {
            "shapefile": "edw_resources/shp/Actv_HazFuelTrt_LN.zip",
            "geodatabase": "edw_resources/fc/Actv_HazFuelTrt_LN.gdb.zip",
        },
        "Actv_SilvReforest": {
            "shapefile": "edw_resources/shp/Actv_SilvReforest.zip",
            "geodatabase": "edw_resources/fc/Actv_SilvReforest.gdb.zip",
        },
        "Actv_SilvTSI": {
            "shapefile": "edw_resources/shp/Actv_SilvTSI.zip",
            "geodatabase": "edw_resources/fc/Actv_SilvTSI.gdb.zip",
        },
        "Actv_RngVegImprove": {
            "shapefile": "edw_resources/shp/Actv_RngVegImprove.zip",
            "geodatabase": "edw_resources/fc/Actv_RngVegImprove.gdb.zip",
        },
    }
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the downloader.
        
        Args:
            data_dir: Directory to store downloaded datasets
        """
        self.data_dir = Path(data_dir)
        self.base_url = self.BASE_URL
        
        # Create directory structure
        self.shapefile_dir = self.data_dir / "shapefiles"
        self.geodatabase_dir = self.data_dir / "geodatabases"
        
        self.shapefile_dir.mkdir(parents=True, exist_ok=True)
        self.geodatabase_dir.mkdir(parents=True, exist_ok=True)
    
    def list_available_datasets(self) -> list[str]:
        """
        List all available dataset names.
        
        Returns:
            List of dataset names
        """
        return list(self.DATASETS.keys())
    
    def download_dataset(
        self,
        name: str,
        format: Literal["shapefile", "geodatabase"] = "shapefile",
        force: bool = False
    ) -> Path:
        """
        Download a dataset from the USDA Forest Service.
        
        Args:
            name: Dataset name (e.g., 'Actv_TimberHarvest')
            format: File format ('shapefile' or 'geodatabase')
            force: If True, re-download even if file exists
            
        Returns:
            Path to the downloaded dataset
            
        Raises:
            ValueError: If dataset name or format is invalid
            requests.RequestException: If download fails
        """
        if name not in self.DATASETS:
            raise ValueError(
                f"Dataset '{name}' not found. "
                f"Available datasets: {', '.join(self.list_available_datasets())}"
            )
        
        if format not in ["shapefile", "geodatabase"]:
            raise ValueError("Format must be 'shapefile' or 'geodatabase'")
        
        # Get the download URL
        relative_url = self.DATASETS[name].get(format)
        if not relative_url:
            raise ValueError(f"Format '{format}' not available for dataset '{name}'")
        
        url = urljoin(self.base_url, relative_url)
        
        # Determine output directory and path
        if format == "shapefile":
            output_dir = self.shapefile_dir / name
        else:
            output_dir = self.geodatabase_dir / name
        
        # Check if already downloaded
        if output_dir.exists() and not force:
            print(f"Dataset '{name}' already exists at {output_dir}")
            return output_dir
        
        print(f"Downloading {name} ({format}) from USDA Forest Service...")
        print(f"URL: {url}")
        
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get total file size
        total_size = int(response.headers.get('content-length', 0))
        
        # Download and extract
        print(f"Downloading {total_size / (1024*1024):.1f} MB...")
        
        # Read the zip file from memory
        zip_data = io.BytesIO()
        downloaded = 0
        
        for chunk in response.iter_content(chunk_size=8192):
            zip_data.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"\rProgress: {percent:.1f}%", end="", flush=True)
        
        print("\nExtracting...")
        
        # Extract the zip file
        with zipfile.ZipFile(zip_data) as zip_ref:
            output_dir.mkdir(parents=True, exist_ok=True)
            zip_ref.extractall(output_dir)
        
        print(f"Successfully downloaded and extracted to {output_dir}")
        return output_dir
    
    def get_dataset_info(self, name: str) -> dict:
        """
        Get information about a dataset.
        
        Args:
            name: Dataset name
            
        Returns:
            Dictionary with dataset information
        """
        if name not in self.DATASETS:
            raise ValueError(f"Dataset '{name}' not found")
        
        return {
            "name": name,
            "available_formats": list(self.DATASETS[name].keys()),
            "metadata_url": f"{self.base_url}edw_resources/meta/{name}.xml",
        }
    
    def download_custom_dataset(
        self,
        url: str,
        output_name: str,
        format: Literal["shapefile", "geodatabase"] = "shapefile"
    ) -> Path:
        """
        Download a custom dataset from a direct URL.
        
        Args:
            url: Direct URL to the dataset zip file
            output_name: Name to save the dataset as
            format: File format for organization
            
        Returns:
            Path to the downloaded dataset
        """
        if format == "shapefile":
            output_dir = self.shapefile_dir / output_name
        else:
            output_dir = self.geodatabase_dir / output_name
        
        print(f"Downloading custom dataset from {url}...")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        zip_data = io.BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            zip_data.write(chunk)
        
        print("Extracting...")
        with zipfile.ZipFile(zip_data) as zip_ref:
            output_dir.mkdir(parents=True, exist_ok=True)
            zip_ref.extractall(output_dir)
        
        print(f"Successfully downloaded to {output_dir}")
        return output_dir

