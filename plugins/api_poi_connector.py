# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: plugins/api_poi_connector.py
# NEW_FEATURE: 停頓點周邊開源地標/工廠資料庫查詢引擎 (支援離線/在線雙模式)

import requests
import json
from typing import Dict, List

class POIConnector:
    def __init__(self):
        """地標與廠場資訊查詢引擎"""
        # 預留離線資料庫接口 (未來可讀取封裝在 APK 內的 SQLite 工商資料表)
        self.offline_mode = True
        
    def set_mode(self, offline: bool):
        """切換離線/在線模式"""
        self.offline_mode = offline

    def get_nearby_factories(self, lat: float, lng: float, radius_meters: int = 500) -> List[Dict]:
        """
        搜尋停頓點附近的可能廠家或地標。
        用於【探索模式】中漸進彈出的資訊圖卡。
        """
        if self.offline_mode:
            return self._query_offline_db(lat, lng, radius_meters)
        else:
            return self._query_online_api(lat, lng, radius_meters)

    def _query_offline_db(self, lat: float, lng: float, radius: int) -> List[Dict]:
        """
        離線資料庫查詢 (模擬邏輯)。
        實務上此處應向 SQLiteManager 請求比對空間座標(如 R-Tree 或簡單的經緯度範圍過濾)。
        """
        # 防呆與無網路環境的預設回傳值，確保不閃退
        return [
            {
                "name": "離線比對: 疑似未登記鐵皮屋",
                "type": "未知廠場",
                "distance": 120,
                "risk_level": "High"
            },
            {
                "name": "離線比對: 某某資源回收場",
                "type": "資源回收",
                "distance": 340,
                "risk_level": "Medium"
            }
        ]

    def _query_online_api(self, lat: float, lng: float, radius: int) -> List[Dict]:
        """
        在線模式：透過 4G 訊號呼叫 OpenStreetMap (Nominatim) API 進行反向地理編碼與地標查詢。
        """
        results = []
        try:
            # 呼叫 OSM Nominatim API (使用受限，建議實務上替換為政府開放資料 API 或 Google API)
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=18&addressdetails=1"
            headers = {'User-Agent': 'EnvironmentalAuditGISApp/1.0'}
            
            # 設定 Timeout 防止網路不良卡死 UI
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                address = data.get("address", {})
                
                # 嘗試提取有用的地標資訊
                poi_name = address.get("amenity") or address.get("shop") or address.get("industrial") or address.get("building")
                if not poi_name:
                    poi_name = data.get("display_name", "未知地點 (線上反查)")
                else:
                    poi_name = f"線上地標: {poi_name}"

                results.append({
                    "name": poi_name,
                    "type": "線上快查",
                    "distance": 0, # 反向地理編碼直接取該點
                    "risk_level": "Unknown",
                    "raw_address": data.get("display_name", "")
                })
        except requests.exceptions.RequestException as e:
            # 網路錯誤時自動退回離線資料，符合環保稽查野外環境特性
            print(f"API 請求失敗，切換為離線資料庫結果: {e}")
            return self._query_offline_db(lat, lng, radius)
            
        return results