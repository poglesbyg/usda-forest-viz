"""
Example 4: Spatial Analysis and Statistics

This example demonstrates spatial analysis capabilities and statistical summaries.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from usda_forest_viz.utils import (
    load_shapefile,
    calculate_area,
    get_summary_statistics,
    filter_by_attribute,
    create_buffer
)
import pandas as pd
import matplotlib.pyplot as plt


def main():
    print("=" * 80)
    print("USDA Forest Service Spatial Analysis")
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
    
    # Example 1: Calculate areas
    print("\n" + "=" * 80)
    print("Example 1: Area Calculation")
    print("=" * 80)
    
    print("Calculating areas in acres...")
    gdf_with_area = calculate_area(gdf, unit="acres")
    
    print(f"\nTotal treated area: {gdf_with_area['area_acres'].sum():,.2f} acres")
    print(f"Average treatment size: {gdf_with_area['area_acres'].mean():,.2f} acres")
    print(f"Median treatment size: {gdf_with_area['area_acres'].median():,.2f} acres")
    print(f"Largest treatment: {gdf_with_area['area_acres'].max():,.2f} acres")
    print(f"Smallest treatment: {gdf_with_area['area_acres'].min():,.2f} acres")
    
    # Example 2: Summary statistics
    print("\n" + "=" * 80)
    print("Example 2: Summary Statistics")
    print("=" * 80)
    
    stats = get_summary_statistics(gdf_with_area)
    print("\nSummary statistics:")
    print(stats.to_string())
    
    # Example 3: Group by analysis
    print("\n" + "=" * 80)
    print("Example 3: Groupby Analysis")
    print("=" * 80)
    
    # Find categorical columns
    categorical_cols = gdf_with_area.select_dtypes(include=['object']).columns
    categorical_cols = [col for col in categorical_cols if col != 'geometry']
    
    if len(categorical_cols) > 0:
        group_col = categorical_cols[0]
        print(f"\nGrouping by: {group_col}")
        
        # Count by group
        counts = gdf_with_area[group_col].value_counts().head(10)
        print(f"\nTop 10 categories by count:")
        print(counts.to_string())
        
        # Area by group
        if 'area_acres' in gdf_with_area.columns:
            area_by_group = gdf_with_area.groupby(group_col)['area_acres'].agg([
                ('count', 'count'),
                ('total_acres', 'sum'),
                ('avg_acres', 'mean'),
                ('median_acres', 'median')
            ]).sort_values('total_acres', ascending=False).head(10)
            
            print(f"\nTop 10 categories by total area:")
            print(area_by_group.to_string())
    
    # Example 4: Temporal analysis (if date column exists)
    print("\n" + "=" * 80)
    print("Example 4: Temporal Analysis")
    print("=" * 80)
    
    # Find date columns
    date_cols = [col for col in gdf_with_area.columns 
                 if any(term in col.upper() for term in ['DATE', 'YEAR', 'TIME'])]
    
    if len(date_cols) > 0:
        date_col = date_cols[0]
        print(f"\nAnalyzing temporal patterns using: {date_col}")
        
        try:
            # Convert to datetime if not already
            gdf_with_area[f'{date_col}_parsed'] = pd.to_datetime(
                gdf_with_area[date_col], 
                errors='coerce'
            )
            
            # Extract year
            gdf_with_area['year'] = gdf_with_area[f'{date_col}_parsed'].dt.year
            
            # Treatments by year
            yearly_counts = gdf_with_area['year'].value_counts().sort_index()
            print(f"\nTreatments by year:")
            print(yearly_counts.tail(10).to_string())
            
            # Create bar chart
            if len(yearly_counts) > 0:
                plt.figure(figsize=(12, 6))
                yearly_counts.sort_index().plot(kind='bar')
                plt.title('Timber Harvest Activities by Year')
                plt.xlabel('Year')
                plt.ylabel('Number of Activities')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig('../outputs/05_temporal_analysis.png', dpi=300)
                plt.close()
                print("\n✓ Temporal analysis chart saved to outputs/05_temporal_analysis.png")
            
        except Exception as e:
            print(f"Could not parse dates: {e}")
    else:
        print("No date columns found for temporal analysis")
    
    # Example 5: Spatial filtering by state
    print("\n" + "=" * 80)
    print("Example 5: State-level Analysis")
    print("=" * 80)
    
    if 'STATE_ABBR' in gdf_with_area.columns:
        state_summary = gdf_with_area.groupby('STATE_ABBR').agg({
            'area_acres': ['count', 'sum', 'mean']
        }).round(2)
        state_summary.columns = ['Count', 'Total_Acres', 'Avg_Acres']
        state_summary = state_summary.sort_values('Total_Acres', ascending=False)
        
        print("\nSummary by state:")
        print(state_summary.head(15).to_string())
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        state_summary['Total_Acres'].head(15).plot(kind='barh')
        plt.title('Total Timber Harvest Area by State (Top 15)')
        plt.xlabel('Total Area (Acres)')
        plt.ylabel('State')
        plt.tight_layout()
        plt.savefig('../outputs/06_state_analysis.png', dpi=300)
        plt.close()
        print("\n✓ State analysis chart saved to outputs/06_state_analysis.png")
    
    # Example 6: Create buffer zones
    print("\n" + "=" * 80)
    print("Example 6: Buffer Analysis")
    print("=" * 80)
    
    print("Creating 1000-meter buffer zones around sample features...")
    sample = gdf_with_area.head(100)
    buffered = create_buffer(sample, distance=1000, unit="meters")
    
    print(f"Original features: {len(sample)}")
    print(f"Buffered features: {len(buffered)}")
    print(f"Original total area: {sample['area_acres'].sum():,.2f} acres")
    
    buffered_with_area = calculate_area(buffered, unit="acres")
    print(f"Buffered total area: {buffered_with_area['area_acres'].sum():,.2f} acres")
    
    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("Check the 'outputs' directory for generated charts.")
    print("=" * 80)


if __name__ == "__main__":
    main()

