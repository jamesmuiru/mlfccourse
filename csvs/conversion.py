# conversion.py
import geopandas as gpd
import os

# Input shapefile path (update if needed)
input_shapefile = r"C:\Users\Administrator\Downloads\mlfccourse\csvs\shapefile\county_with_raster_means.shp"

# Output GeoPackage path
output_gpkg = r"C:\Users\Administrator\Downloads\mlfccourse\csvs\county_with_raster_means.gpkg"

# Ensure the input file exists
if not os.path.exists(input_shapefile):
    raise FileNotFoundError(f"Shapefile not found: {input_shapefile}")

# Load the shapefile
gdf = gpd.read_file(input_shapefile)

# Save as GeoPackage
gdf.to_file(output_gpkg, driver="GPKG")

print(f"✅ Successfully converted shapefile to GeoPackage:\n{output_gpkg}")
