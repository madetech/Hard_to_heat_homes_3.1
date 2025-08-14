import geopandas as gpd
import pandas as pd
import contextily as cx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
from src.council_data_utils import get_formatted_bbox_for_council_code
from data.coucil_code_to_council_name import council_code_to_council_name

def load_consumption_data(bbox):
    data_frame = gpd.read_parquet(
        "s3://weave.energy/smart-meter",
        bbox=bbox,
        columns=[
            "geometry",
            "data_collection_log_timestamp",
            "total_consumption_active_import",
            "secondary_substation_unique_id"
        ],
        filters=[
            ("data_collection_log_timestamp", "=", pd.Timestamp("2024-07-14 20:00Z"))
        ]
    )
    return data_frame

def aggregate_substation_data(gdf):
    substations = gdf.groupby(
        ["secondary_substation_unique_id", "geometry"],
        as_index=False
    ).sum("total_consumption_active_import").set_geometry("geometry")

    substations = substations[substations["total_consumption_active_import"] < 20000] # remove outliers
    substations["total_consumption_active_import"] /= 1000  # Convert to kWh
    return substations

def plot_heatmap(substations, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    substations.plot(
        ax=ax,
        column="total_consumption_active_import",
        markersize=5,
        legend=True,
        legend_kwds={"label": "Total consumption per substation (active import kWh)"}
    )
    ax.set_title(title)
    ax.set_axis_off()
    ax.set_facecolor("#1B2526")
    cx.add_basemap(ax, crs=4326, source=cx.providers.CartoDB.Positron, attribution=False)
    return fig

def generate_base64_image(fig):
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    img_buffer.seek(0)
    encoded_img = base64.b64encode(img_buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_img}"

def generate_heat_map(council_code):
    bbox = get_formatted_bbox_for_council_code(council_code)
    gdf = load_consumption_data(bbox)
    substations = aggregate_substation_data(gdf)
    council_name = council_code_to_council_name[council_code]
    fig = plot_heatmap(substations, f"{council_name}'s Energy Consumption at 7pm on 14th July 2024")
    return generate_base64_image(fig)
