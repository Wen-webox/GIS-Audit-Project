# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: core/kml_parser.py
# NEW_FEATURE: KML 批次解析引擎，自動分辨格式並轉換為 SQLite 相容格式

import os
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from core.sqlite_manager import SQLiteManager

class KMLParser:
    def __init__(self, db_manager: SQLiteManager):
        self.db = db_manager
        # KML 標準命名空間
        self.ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    def process_file(self, filepath: str, vehicle_id: str) -> bool:
        """
        處理單一 KML 檔案。
        自動偵測是軌跡檔還是停頓點檔，並寫入資料庫。
        """
        if not os.path.exists(filepath):
            print(f"錯誤：找不到檔案 {filepath}")
            return False

        filename = os.path.basename(filepath).lower()
        batch_id = str(uuid.uuid4()) # 產生唯一批次碼，防資料污染

        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            if "history" in filename or "track" in filename:
                self._parse_history(root, batch_id, vehicle_id, filepath)
                return True
            elif "stoppoint" in filename or "stop" in filename:
                self._parse_stoppoint(root, batch_id, vehicle_id, filepath)
                return True
            else:
                # 嘗試動態特徵辨識
                if root.findall('.//kml:LineString', self.ns):
                    self._parse_history(root, batch_id, vehicle_id, filepath)
                    return True
                else:
                    self._parse_stoppoint(root, batch_id, vehicle_id, filepath)
                    return True

        except Exception as e:
            print(f"KML 解析失敗 ({filepath}): {str(e)}")
            return False

    def _parse_history(self, root: ET.Element, batch_id: str, vehicle_id: str, filepath: str):
        """解析軌跡線檔案"""
        self.db.register_batch(batch_id, "History", os.path.basename(filepath))
        tracks_to_insert = []
        
        # 尋找所有的 Placemark 包含 LineString 或 gx:Track
        for placemark in root.findall('.//kml:Placemark', self.ns):
            # 針對標準 LineString 提取
            linestring = placemark.find('.//kml:LineString/kml:coordinates', self.ns)
            if linestring is not None and linestring.text:
                coords = linestring.text.strip().split()
                # 假設軌跡檔的名稱或描述帶有日期，這裡我們使用當天日期作為防呆紀錄
                # 實務上可依據 KML 內 <TimeSpan> 或 <TimeStamp> 取出
                record_date = datetime.now().strftime('%Y-%m-%d') 
                
                for index, coord in enumerate(coords):
                    parts = coord.split(',')
                    if len(parts) >= 2:
                        lng, lat = float(parts[0]), float(parts[1])
                        # 模擬時間戳 (實務上需解析 gx:coord 或 description 內的真實時間)
                        sim_time = f"{record_date} {str(index % 24).zfill(2)}:{str(index % 60).zfill(2)}:00"
                        tracks_to_insert.append((batch_id, vehicle_id, record_date, sim_time, lng, lat))
                        
        if tracks_to_insert:
            self.db.insert_tracks(tracks_to_insert)

    def _parse_stoppoint(self, root: ET.Element, batch_id: str, vehicle_id: str, filepath: str):
        """解析停頓點檔案"""
        self.db.register_batch(batch_id, "Stoppoint", os.path.basename(filepath))
        stoppoints_to_insert = []

        for placemark in root.findall('.//kml:Placemark', self.ns):
            name_node = placemark.find('kml:name', self.ns)
            location_name = name_node.text if name_node is not None else "未知停頓點"
            
            point = placemark.find('.//kml:Point/kml:coordinates', self.ns)
            if point is not None and point.text:
                parts = point.text.strip().split(',')
                if len(parts) >= 2:
                    lng, lat = float(parts[0]), float(parts[1])
                    record_date = datetime.now().strftime('%Y-%m-%d')
                    start_time = f"{record_date} 00:00:00" # 需從 description 提取
                    end_time = f"{record_date} 01:00:00"   # 需從 description 提取
                    duration = 60.0
                    
                    stoppoints_to_insert.append((
                        batch_id, vehicle_id, record_date, 
                        start_time, end_time, duration, lng, lat, location_name
                    ))

        if stoppoints_to_insert:
            self.db.insert_stoppoints(stoppoints_to_insert)