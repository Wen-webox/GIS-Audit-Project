# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: main.py
# NEW_FEATURE: 結合 Kivy 引擎、防閃退機制與 SQLite 資料庫初始化的系統進入點

import os
import sys
import traceback
from datetime import datetime

# 導入我們剛建立的核心模組
from core.sqlite_manager import SQLiteManager
from core.kml_parser import KMLParser

# 全域致命錯誤捕捉器 (Anti-Silent Crash - Android 版)
def global_exception_handler(exc_type, exc_value, exc_traceback):
    traceback_details = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"CRITICAL CRASH:\n{traceback_details}")
    
    # 嘗試寫入 Android 公開目錄或本地目錄
    log_paths = [
        "/sdcard/Download/app_crash_log.txt",  
        os.path.join(os.path.expanduser("~"), "Downloads", "app_crash_log.txt"), 
        "app_crash_log.txt" 
    ]
    
    for path in log_paths:
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FATAL ERROR:\n")
                f.write(traceback_details)
                f.write("\n" + "="*50 + "\n")
            break
        except Exception:
            continue

sys.excepthook = global_exception_handler

class GISEngineBootstrap:
    def __init__(self):
        print("啟動跨平台環保稽查 GIS 核心引擎...")
        # 1. 初始化資料庫防呆模組
        self.db = SQLiteManager()
        print("✅ SQLite 本機隔離資料庫連線成功。")
        
        # 2. 初始化 KML 解析引擎
        self.parser = KMLParser(self.db)
        print("✅ KML 批次解析引擎載入完成。")

    def run_ui(self):
        """載入 Kivy UI (保留供下一階段 UI 模組掛載)"""
        print("等待 Kivy 框架載入 WebView 與地圖圖層...")
        
        # 在此處我們確保 Kivy 不會在無頭環境崩潰，若 ui.dashboard 尚未建立，提供安全防護
        try:
            from ui.dashboard import GISAuditApp
            app = GISAuditApp(self.db, self.parser)
            app.run()
            print("🚀 UI 介面尚未實作，核心系統測試正常結束。請接續開發 UI 層！")
        except ImportError as e:
            print(f"⚠️ UI 載入暫停，等待下一階段開發: {e}")

def main():
    engine = GISEngineBootstrap()
    engine.run_ui()

if __name__ == "__main__":
    main()