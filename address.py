import matplotlib.pyplot as plt
import osmnx as ox
from typing import List, Tuple, Optional


class DataSolution:
    def __init__(self, data_access):
        self.data_access = data_access
        self.default_features = [
            ("building", None),
            ("amenity", None),
            ("amenity", "school"),
            ("amenity", "hospital"),
            ("amenity", "restaurant"),
            ("amenity", "cafe"),
            ("shop", None),
            ("tourism", None),
            ("tourism", "hotel"),
            ("tourism", "museum"),
            ("leisure", None),
            ("leisure", "park"),
            ("historic", None),
            ("amenity", "place_of_worship"),
        ]

    def address_visualization(self, figsize: Tuple[int, int] = (6, 6)):
        if any(data is None for data in [self.data_access.area, self.data_access.buildings, 
                                       self.data_access.edges, self.data_access.nodes, self.data_access.pois]):
            self.data_access.access_all_data()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if self.data_access.area is not None:
            self.data_access.area.plot(ax=ax, color="tan", alpha=0.5)
        if self.data_access.buildings is not None:
            self.data_access.buildings.plot(ax=ax, facecolor="gray", edgecolor="gray")
        if self.data_access.edges is not None:
            self.data_access.edges.plot(ax=ax, linewidth=1, edgecolor="black", alpha=0.3)
        if self.data_access.nodes is not None:
            self.data_access.nodes.plot(ax=ax, color="black", markersize=1, alpha=0.3)
        if self.data_access.pois is not None:
            self.data_access.pois.plot(ax=ax, color="green", markersize=5, alpha=1)
        
        ax.set_xlim(self.data_access.west, self.data_access.east)
        ax.set_ylim(self.data_access.south, self.data_access.north)
        ax.set_title(self.data_access.place_name, fontsize=14)
        plt.show()
        return fig
    
    def address_feature_extraction(self, latitude: float, longitude: float, 
                                 box_size_km: float = 2, features: Optional[List[Tuple]] = None):
        if features is None:
            features = self.default_features
        
        box_deg = box_size_km / 111
        north = latitude + box_deg / 2
        south = latitude - box_deg / 2
        east = longitude + box_deg / 2
        west = longitude - box_deg / 2
        bbox = (west, south, east, north)
        
        keys = {k for k, _ in features}
        tags = {k: True for k in keys}
        
        try:
            pois = ox.features_from_bbox(bbox, tags=tags)
        except:
            return {f"{key}:{value}" if value else key: 0 for key, value in features}
        
        counts = {}
        for key, value in features:
            if key in pois.columns:
                if value:
                    counts[f"{key}:{value}"] = (pois[key] == value).sum()
                else:
                    counts[key] = pois[key].notnull().sum()
            else:
                counts[f"{key}:{value}" if value else key] = 0
        
        return counts
