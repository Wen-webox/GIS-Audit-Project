# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: sqlite_manager.py

# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: core/sqlite_manager.py
# NEW_FEATURE: 實作 SQLite 離線防呆資料庫與資料隔離邏輯

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Tuple

class SQLiteManager:
    def __init__(self, db_name: str = "gis_audit_offline.sqlite3"):
        """
        初始化本地資料庫。
        遵循行動端封裝路徑鐵律：確保資料庫建立在可寫入的目錄。
        """
        # 判斷是否在 Android 環境，若是則指向可寫入的 user data 目錄
        if 'ANDROID_ARGUMENT' in os.environ:
            from android.storage import app_storage_path # type: ignore
            self.db_path = os.path.join(app_storage_path(), db_name)
        else:
            self.db_path = os.path.join(os.getcwd(), db_name)
            
        self._initialize_tables()

    def _get_connection(self) -> sqlite3.Connection:
        """取得資料庫連線"""
        return sqlite3.connect(self.db_path)

    def _initialize_tables(self):
        """建立防呆隔離資料表"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 1. 匯入批次表 (確保資料不污染)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batches (
                batch_id TEXT PRIMARY KEY,
                import_time TEXT,
                file_type TEXT,
                original_filename TEXT
            )
        ''')
        
        # 2. 軌跡點資料表 (GPS_History)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT,
                vehicle_id TEXT,
                record_date TEXT,
                timestamp TEXT,
                longitude REAL,
                latitude REAL,
                FOREIGN KEY(batch_id) REFERENCES batches(batch_id)
            )
        ''')
        
        # 3. 停頓點資料表 (GPS_Stoppoint)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stoppoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT,
                vehicle_id TEXT,
                record_date TEXT,
                start_time TEXT,
                end_time TEXT,
                duration_minutes REAL,
                longitude REAL,
                latitude REAL,
                location_name TEXT,
                FOREIGN KEY(batch_id) REFERENCES batches(batch_id)
            )
        ''')
        
        # 建立索引以優化查詢效能
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tracks_vehicle_date ON tracks(vehicle_id, record_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_stoppoints_vehicle_date ON stoppoints(vehicle_id, record_date)')
        
        conn.commit()
        conn.close()

    def register_batch(self, batch_id: str, file_type: str, filename: str):
        """註冊新的匯入批次"""
        conn = self._get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            'INSERT INTO batches (batch_id, import_time, file_type, original_filename) VALUES (?, ?, ?, ?)',
            (batch_id, now, file_type, filename)
        )
        conn.commit()
        conn.close()

    def insert_tracks(self, tracks_data: List[Tuple]):
        """批次寫入軌跡資料 (使用 executemany 提升效能)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.executemany(
            'INSERT INTO tracks (batch_id, vehicle_id, record_date, timestamp, longitude, latitude) VALUES (?, ?, ?, ?, ?, ?)',
            tracks_data
        )
        conn.commit()
        conn.close()

    def insert_stoppoints(self, stoppoints_data: List[Tuple]):
        """批次寫入停頓點資料"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.executemany(
            'INSERT INTO stoppoints (batch_id, vehicle_id, record_date, start_time, end_time, duration_minutes, longitude, latitude, location_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            stoppoints_data
        )
        conn.commit()
        conn.close()

    def get_available_vehicles(self) -> List[str]:
        """防呆機制：只列出資料庫中確實有資料的車號"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT vehicle_id FROM tracks 
            UNION 
            SELECT DISTINCT vehicle_id FROM stoppoints
        ''')
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results

    def get_available_dates_for_vehicle(self, vehicle_id: str) -> List[str]:
        """防呆機制：根據車號，只列出有軌跡或停頓點紀錄的日期"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT record_date FROM tracks WHERE vehicle_id = ?
            UNION
            SELECT DISTINCT record_date FROM stoppoints WHERE vehicle_id = ?
            ORDER BY record_date DESC
        ''', (vehicle_id, vehicle_id))
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results

    def fetch_gis_data(self, vehicle_id: str, record_date: str) -> Dict:
        """獲取指定車輛與日期的所有 GIS 渲染資料"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 獲取軌跡
        cursor.execute('SELECT timestamp, longitude, latitude FROM tracks WHERE vehicle_id = ? AND record_date = ? ORDER BY timestamp ASC', (vehicle_id, record_date))
        tracks = [{"timestamp": row[0], "lng": row[1], "lat": row[2]} for row in cursor.fetchall()]
        
        # 獲取停頓點
        cursor.execute('SELECT start_time, end_time, duration_minutes, longitude, latitude, location_name FROM stoppoints WHERE vehicle_id = ? AND record_date = ? ORDER BY start_time ASC', (vehicle_id, record_date))
        stoppoints = [{"start_time": row[0], "end_time": row[1], "duration": row[2], "lng": row[3], "lat": row[4], "name": row[5]} for row in cursor.fetchall()]
        
        conn.close()
        return {"tracks": tracks, "stoppoints": stoppoints}