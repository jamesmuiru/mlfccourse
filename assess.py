import pandas as pd
from typing import List, Tuple, Optional


class DataAssessment:
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

    def assess_poi_distribution(self, features: Optional[List[Tuple]] = None):
        if self.data_access.pois is None:
            self.data_access.access_pois()
        if features is None:
            features = self.default_features
            
        pois_df = pd.DataFrame(self.data_access.pois)
        pois_df['latitude'] = pois_df.apply(lambda row: row.geometry.centroid.y, axis=1)
        pois_df['longitude'] = pois_df.apply(lambda row: row.geometry.centroid.x, axis=1)
        
        poi_counts = {}
        for key, value in features:
            if key in pois_df.columns:
                if value:
                    poi_counts[f"{key}:{value}"] = (pois_df[key] == value).sum()
                else:
                    poi_counts[key] = pois_df[key].notnull().sum()
            else:
                poi_counts[f"{key}:{value}" if value else key] = 0
        
        results = pd.DataFrame(list(poi_counts.items()), columns=["POI Type", "Count"])
        print("POI Assessment Summary:")
        print(results)
        return results
