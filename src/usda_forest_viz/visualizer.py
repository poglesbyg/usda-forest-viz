"""
Visualization tools for USDA Forest Service datasets.
"""

from pathlib import Path
from typing import Optional, Union, List
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import Normalize
import folium
from folium import plugins
import plotly.express as px
import plotly.graph_objects as go


class StaticMapVisualizer:
    """
    Create static map visualizations using matplotlib.
    """
    
    def __init__(self, style: str = "default"):
        """
        Initialize the static map visualizer.
        
        Args:
            style: Matplotlib style to use
        """
        if style != "default":
            plt.style.use(style)
    
    def plot_polygons(
        self,
        gdf: gpd.GeoDataFrame,
        column: Optional[str] = None,
        title: str = "USDA Forest Service Data",
        cmap: str = "viridis",
        figsize: tuple = (15, 10),
        legend: bool = True,
        alpha: float = 0.7,
        edgecolor: str = "black",
        linewidth: float = 0.5,
        output_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot polygon geometries.
        
        Args:
            gdf: GeoDataFrame to plot
            column: Column to use for coloring
            title: Plot title
            cmap: Colormap name
            figsize: Figure size (width, height)
            legend: Whether to show legend
            alpha: Transparency (0-1)
            edgecolor: Edge color
            linewidth: Edge line width
            output_path: Path to save figure (optional)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot the data
        gdf.plot(
            column=column,
            ax=ax,
            cmap=cmap,
            legend=legend,
            alpha=alpha,
            edgecolor=edgecolor,
            linewidth=linewidth
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel("Longitude", fontsize=12)
        ax.set_ylabel("Latitude", fontsize=12)
        
        # Remove axis spines for cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        
        if output_path:
            # Create directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {output_path}")
        
        return fig
    
    def plot_points(
        self,
        gdf: gpd.GeoDataFrame,
        column: Optional[str] = None,
        title: str = "USDA Forest Service Data",
        cmap: str = "viridis",
        figsize: tuple = (15, 10),
        markersize: float = 20,
        alpha: float = 0.6,
        output_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot point geometries.
        
        Args:
            gdf: GeoDataFrame to plot
            column: Column to use for coloring
            title: Plot title
            cmap: Colormap name
            figsize: Figure size
            markersize: Size of markers
            alpha: Transparency
            output_path: Path to save figure (optional)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        gdf.plot(
            column=column,
            ax=ax,
            cmap=cmap,
            legend=True,
            markersize=markersize,
            alpha=alpha
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel("Longitude", fontsize=12)
        ax.set_ylabel("Latitude", fontsize=12)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {output_path}")
        
        return fig
    
    def plot_choropleth(
        self,
        gdf: gpd.GeoDataFrame,
        value_column: str,
        title: str = "Choropleth Map",
        cmap: str = "YlOrRd",
        figsize: tuple = (15, 10),
        output_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create a choropleth map based on numeric values.
        
        Args:
            gdf: GeoDataFrame to plot
            value_column: Column with numeric values
            title: Plot title
            cmap: Colormap name
            figsize: Figure size
            output_path: Path to save figure (optional)
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        gdf.plot(
            column=value_column,
            ax=ax,
            cmap=cmap,
            legend=True,
            legend_kwds={'label': value_column, 'orientation': 'horizontal'}
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {output_path}")
        
        return fig
    
    def create_comparison_map(
        self,
        gdfs: List[gpd.GeoDataFrame],
        titles: List[str],
        figsize: tuple = (20, 10),
        output_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create side-by-side comparison of multiple datasets.
        
        Args:
            gdfs: List of GeoDataFrames to plot
            titles: List of titles for each subplot
            figsize: Figure size
            output_path: Path to save figure (optional)
            
        Returns:
            Matplotlib figure object
        """
        n_plots = len(gdfs)
        fig, axes = plt.subplots(1, n_plots, figsize=figsize)
        
        if n_plots == 1:
            axes = [axes]
        
        for i, (gdf, title) in enumerate(zip(gdfs, titles)):
            gdf.plot(ax=axes[i], alpha=0.7)
            axes[i].set_title(title, fontsize=14, fontweight='bold')
            axes[i].axis('off')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {output_path}")
        
        return fig


class InteractiveMapVisualizer:
    """
    Create interactive map visualizations using Folium.
    """
    
    def __init__(self):
        """Initialize the interactive map visualizer."""
        pass
    
    def create_map(
        self,
        gdf: gpd.GeoDataFrame,
        zoom_start: int = 6,
        tiles: str = "OpenStreetMap",
        style_column: Optional[str] = None,
        popup_fields: Optional[List[str]] = None,
        tooltip_fields: Optional[List[str]] = None,
        color: str = "blue",
        fill_opacity: float = 0.6
    ) -> folium.Map:
        """
        Create an interactive Folium map.
        
        Args:
            gdf: GeoDataFrame to plot
            zoom_start: Initial zoom level
            tiles: Base map tiles
            style_column: Column to use for styling
            popup_fields: Fields to show in popup
            tooltip_fields: Fields to show in tooltip
            color: Default color
            fill_opacity: Fill opacity
            
        Returns:
            Folium map object
        """
        # Ensure CRS is WGS84 for web mapping
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")
        
        # Calculate center
        center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
        
        # Create map
        m = folium.Map(
            location=center,
            zoom_start=zoom_start,
            tiles=tiles
        )
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Create feature group
        fg = folium.FeatureGroup(name="USDA Forest Service Data")
        
        # Add geometries
        for idx, row in gdf.iterrows():
            # Create popup content
            popup_html = "<div style='width: 200px'>"
            if popup_fields:
                for field in popup_fields:
                    if field in row:
                        popup_html += f"<b>{field}:</b> {row[field]}<br>"
            popup_html += "</div>"
            
            # Create tooltip content
            tooltip_html = None
            if tooltip_fields:
                tooltip_html = "<br>".join([f"<b>{field}:</b> {row[field]}" for field in tooltip_fields if field in row])
            
            # Determine color
            feature_color = color
            if style_column and style_column in row:
                # Simple color mapping - can be enhanced
                feature_color = self._get_color_for_value(row[style_column])
            
            # Add geometry based on type
            if row.geometry.geom_type == 'Point':
                folium.CircleMarker(
                    location=[row.geometry.y, row.geometry.x],
                    radius=5,
                    color=feature_color,
                    fill=True,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=tooltip_html
                ).add_to(fg)
            else:
                folium.GeoJson(
                    row.geometry.__geo_interface__,
                    style_function=lambda x, c=feature_color: {
                        'fillColor': c,
                        'color': 'black',
                        'weight': 1,
                        'fillOpacity': fill_opacity
                    },
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=tooltip_html
                ).add_to(fg)
        
        fg.add_to(m)
        
        # Add fullscreen button
        plugins.Fullscreen().add_to(m)
        
        # Add minimap
        plugins.MiniMap().add_to(m)
        
        return m
    
    def _get_color_for_value(self, value) -> str:
        """
        Get a color for a value (simple hash-based coloring).
        
        Args:
            value: Value to get color for
            
        Returns:
            Color hex code
        """
        colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']
        return colors[hash(str(value)) % len(colors)]
    
    def save_map(self, m: folium.Map, output_path: str):
        """
        Save a Folium map to HTML.
        
        Args:
            m: Folium map object
            output_path: Path to save HTML file
        """
        m.save(output_path)
        print(f"Interactive map saved to {output_path}")


class PlotlyVisualizer:
    """
    Create interactive visualizations using Plotly.
    """
    
    def __init__(self):
        """Initialize the Plotly visualizer."""
        pass
    
    def create_map(
        self,
        gdf: gpd.GeoDataFrame,
        color_column: Optional[str] = None,
        hover_data: Optional[List[str]] = None,
        title: str = "USDA Forest Service Data",
        mapbox_style: str = "open-street-map"
    ) -> go.Figure:
        """
        Create an interactive Plotly map.
        
        Args:
            gdf: GeoDataFrame to plot
            color_column: Column to use for coloring
            hover_data: Columns to show on hover
            title: Map title
            mapbox_style: Mapbox style
            
        Returns:
            Plotly figure object
        """
        # Ensure CRS is WGS84
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")
        
        fig = px.choropleth_mapbox(
            gdf,
            geojson=gdf.geometry.__geo_interface__,
            locations=gdf.index,
            color=color_column,
            hover_data=hover_data,
            mapbox_style=mapbox_style,
            center={"lat": gdf.geometry.centroid.y.mean(), 
                   "lon": gdf.geometry.centroid.x.mean()},
            zoom=6,
            title=title
        )
        
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
        
        return fig
    
    def create_time_series(
        self,
        gdf: gpd.GeoDataFrame,
        date_column: str,
        value_column: str,
        title: str = "Time Series Analysis",
        output_path: Optional[str] = None
    ) -> go.Figure:
        """
        Create a time series visualization.
        
        Args:
            gdf: GeoDataFrame with temporal data
            date_column: Column with dates
            value_column: Column with values to plot
            title: Plot title
            output_path: Path to save HTML (optional)
            
        Returns:
            Plotly figure object
        """
        # Aggregate by date
        df = gdf.groupby(date_column)[value_column].sum().reset_index()
        
        fig = px.line(
            df,
            x=date_column,
            y=value_column,
            title=title,
            markers=True
        )
        
        fig.update_layout(
            xaxis_title=date_column,
            yaxis_title=value_column,
            hovermode='x unified'
        )
        
        if output_path:
            fig.write_html(output_path)
            print(f"Time series saved to {output_path}")
        
        return fig

