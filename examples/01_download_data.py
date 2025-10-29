"""
Example 1: Downloading USDA Forest Service Datasets

This example demonstrates how to download datasets from the USDA Forest Service
Enterprise Data Warehouse.
"""

from usda_forest_viz import DatasetDownloader


def main():
    # Initialize the downloader
    downloader = DatasetDownloader(data_dir="../data")
    
    print("=" * 80)
    print("USDA Forest Service Dataset Downloader")
    print("=" * 80)
    
    # List all available datasets
    print("\nAvailable datasets:")
    datasets = downloader.list_available_datasets()
    for i, dataset in enumerate(datasets, 1):
        print(f"{i}. {dataset}")
    
    print("\n" + "=" * 80)
    
    # Example 1: Download Timber Harvest data as shapefile
    print("\nExample 1: Downloading Timber Harvest data (Shapefile)...")
    try:
        path = downloader.download_dataset(
            name="Actv_TimberHarvest",
            format="shapefile"
        )
        print(f"✓ Downloaded to: {path}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 80)
    
    # Example 2: Download Hazardous Fuel Treatment data as geodatabase
    print("\nExample 2: Downloading Hazardous Fuel Treatment data (Geodatabase)...")
    try:
        path = downloader.download_dataset(
            name="Actv_HazFuelTrt_PL",
            format="geodatabase"
        )
        print(f"✓ Downloaded to: {path}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 80)
    
    # Example 3: Get dataset information
    print("\nExample 3: Getting dataset information...")
    info = downloader.get_dataset_info("Actv_SilvReforest")
    print(f"Dataset: {info['name']}")
    print(f"Available formats: {', '.join(info['available_formats'])}")
    print(f"Metadata URL: {info['metadata_url']}")
    
    print("\n" + "=" * 80)
    
    # Example 4: Download multiple datasets
    print("\nExample 4: Downloading multiple datasets...")
    datasets_to_download = [
        ("Actv_SilvReforest", "shapefile"),
        ("Actv_RngVegImprove", "shapefile"),
    ]
    
    for dataset_name, format_type in datasets_to_download:
        try:
            print(f"\n  Downloading {dataset_name}...")
            path = downloader.download_dataset(
                name=dataset_name,
                format=format_type
            )
            print(f"  ✓ Downloaded to: {path}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "=" * 80)
    print("Download complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()

