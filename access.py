import osmnx as ox
import warnings
from typing import Dict, Optional, Tuple
import geopandas as gpd

warnings.filterwarnings("ignore", category=FutureWarning, module='osmnx')


class DataAccess:
    def __init__(self, place_name: str, latitude: float, longitude: float, 
                 box_width: float = 0.1, box_height: float = 0.1):
        self.place_name = place_name
        self.latitude = latitude
        self.longitude = longitude
        self.box_width = box_width
        self.box_height = box_height
        
        self.north = latitude + box_height/2
        self.south = latitude - box_height/2
        self.west = longitude - box_width/2
        self.east = longitude + box_width/2
        self.bbox = (self.west, self.south, self.east, self.north)
        
        self.default_tags = {
            "amenity": True,
            "building": True,
            "historic": True,
            "leisure": True,
            "shop": True,
            "tourism": True,
            "religion": True,
            "memorial": True
        }
        
        self.pois = None
        self.graph = None
        self.area = None
        self.nodes = None
        self.edges = None
        self.buildings = None

    def access_pois(self, tags: Optional[Dict] = None):
        if tags is None:
            tags = self.default_tags
        self.pois = ox.features_from_bbox(self.bbox, tags)
        print(f"Retrieved {len(self.pois)} POIs")
        return self.pois
    
    def access_road_network(self):
        self.graph = ox.graph_from_bbox(self.bbox)
        self.nodes, self.edges = ox.graph_to_gdfs(self.graph)
        return self.nodes, self.edges
    
    def access_area_boundary(self):
        self.area = ox.geocode_to_gdf(self.place_name)
        return self.area
    
    def access_buildings(self):
        self.buildings = ox.features_from_bbox(self.bbox, tags={"building": True})
        return self.buildings
    
    def access_all_data(self):
        self.access_pois()
        self.access_area_boundary()
        self.access_buildings()
        try:
            self.access_road_network()
        except:
            pass
