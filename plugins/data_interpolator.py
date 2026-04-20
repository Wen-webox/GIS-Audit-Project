# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: plugins/data_interpolator.py
# NEW_FEATURE: 實作 WGS84 座標系的方位角 (Bearing) 計算與軌跡插值補點

import math
from typing import List, Dict

class DataInterpolator:
    def __init__(self):
        """空間邏輯運算引擎：負責處理軌跡平滑化與 3D 轉向角度"""
        # 地球半徑 (公尺)
        self.R = 6371000

    def calculate_bearing(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        計算兩點之間的初始方位角 (Bearing)。
        用於讓 3D 車輛圖示的車頭永遠朝向行進方向。
        回傳值: 0 ~ 360 度 (正北為 0，順時針)
        """
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        diff_lng = math.radians(lng2 - lng1)

        x = math.sin(diff_lng) * math.cos(lat2_rad)
        y = math.cos(lat1_rad) * math.sin(lat2_rad) - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(diff_lng))

        initial_bearing = math.atan2(x, y)
        
        # 將弧度轉為度數，並標準化至 0-360
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        
        return compass_bearing

    def interpolate_tracks(self, tracks: List[Dict], max_distance_meters: float = 50.0) -> List[Dict]:
        """
        線性插值：若兩個 GPS 點位距離過遠，導致動畫跳躍，則在中間自動補點。
        tracks 格式要求: [{"lat": float, "lng": float, "timestamp": str}, ...]
        """
        if not tracks or len(tracks) < 2:
            return tracks

        smoothed_tracks = [tracks[0]]
        
        for i in range(1, len(tracks)):
            p1 = tracks[i-1]
            p2 = tracks[i]
            
            dist = self._haversine_distance(p1['lat'], p1['lng'], p2['lat'], p2['lng'])
            
            # 若距離超過閾值，進行插值
            if dist > max_distance_meters:
                num_points_to_add = int(dist // max_distance_meters)
                for j in range(1, num_points_to_add + 1):
                    fraction = j / (num_points_to_add + 1)
                    interp_lat = p1['lat'] + (p2['lat'] - p1['lat']) * fraction
                    interp_lng = p1['lng'] + (p2['lng'] - p1['lng']) * fraction
                    
                    # 補點的時間戳以 p1 代替，或者標記為補點
                    smoothed_tracks.append({
                        "lat": interp_lat,
                        "lng": interp_lng,
                        "timestamp": p1['timestamp'],
                        "is_interpolated": True
                    })
            
            # 加入原始點位並計算方位角
            bearing = self.calculate_bearing(p1['lat'], p1['lng'], p2['lat'], p2['lng'])
            p2_copy = dict(p2)
            p2_copy['bearing'] = bearing
            smoothed_tracks.append(p2_copy)
            
        return smoothed_tracks

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """計算兩座標點的球面距離(公尺)"""
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)

        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1_rad) * math.cos(lat2_rad)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return self.R * c