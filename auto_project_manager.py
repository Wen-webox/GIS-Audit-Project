#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
終極自動化專案管理器 V14.0 (Kivy GIS 環保稽查特化版 & Android 跨平台專用優化版)
角色：Principal Mobile/GIS Python Architect
功能：自體繁殖、13大邏輯自動化工作流、AST 骨架萃取、智慧多檔補丁解析、Android 零 Bug 打包優化
更新：深度整合 Leaflet WebView、GPS插值運算、Batch_ID 資料隔離、熱區分析與探索模式架構
"""

import os
import sys
import subprocess
import shutil
import time
import ast
import json
import re
from datetime import datetime
from typing import List, Dict, Set

# ==========================================
# 核心初始化與自體繁殖 (Self-Bootstrap) 模板
# ==========================================

BASE_TASK_PY = """# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class BaseTask(ABC):
    def __init__(self, task_name: str):
        self.task_name = task_name

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
"""

MAIN_PY = """# -*- coding: utf-8 -*-
import os
import sys
import traceback
from datetime import datetime

# 全域致命錯誤捕捉器 (Anti-Silent Crash - Android 版)
def global_exception_handler(exc_type, exc_value, exc_traceback):
    traceback_details = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"CRITICAL CRASH:\\n{traceback_details}")
    
    # 嘗試寫入 Android 公開目錄或本地目錄
    log_paths = [
        "/sdcard/Download/app_crash_log.txt",  # Android 下載目錄
        os.path.join(os.path.expanduser("~"), "Downloads", "app_crash_log.txt"), # Windows/Linux 備用
        "app_crash_log.txt" # 本地備用
    ]
    
    for path in log_paths:
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FATAL ERROR:\\n")
                f.write(traceback_details)
                f.write("\\n" + "="*50 + "\\n")
            break # 成功寫入一個即可
        except Exception:
            continue

sys.excepthook = global_exception_handler

# 核心引擎與 UI 進入點 (Kivy App Placeholder)
def main():
    print("啟動跨平台環保稽查 GIS 核心引擎 (Kivy 環境)...")
    print("正在初始化 SQLite 本機資料庫與 KML 解析引擎...")
    print("UI 進入點已準備完畢，等待 Kivy 框架載入 WebView 與地圖圖層。")
    
    # 未來由 AI 實作 Kivy App 類別並在此處執行 run()
    # from ui.dashboard import GISAuditApp
    # GISAuditApp().run()

if __name__ == "__main__":
    main()
"""

# NEW_FEATURE: 預設 Leaflet WebView 模板，建立基礎圖台骨架
LEAFLET_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>GIS Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        body { padding: 0; margin: 0; }
        html, body, #map { height: 100%; width: 100%; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="map_logic.js"></script>
</body>
</html>
"""

# NEW_FEATURE: 更新專案 Meta 條件，納入高階 GIS 需求
PROJECT_META_JSON = {
    "project_type": "環保稽查 GIS 圖台 (Kivy + Leaflet)",
    "original_prompt": "使用 Kivy 開發 Android 平板單機版 GIS 稽查軟體",
    "constraints": [
        "跨平台相容", "SOLID 原則", "Clean Architecture", 
        "Kivy/KivyMD UI", "SQLite 離線防呆", "KML 批次解析",
        "GPS 軌跡插值與 Bearing 轉向", "Batch_ID 資料隔離", 
        "熱點圖分析", "離線 GeoJSON/連線 API 雙軌制"
    ]
}

GITIGNORE_TEMPLATE = """
.venv/
logs/
.git/
.buildozer/
__pycache__/
build/
dist/
.time_machine/
*.pyc
.env
*.sqlite3
"""

class AutoProjectManager:
    def __init__(self):
        # 1. 全域控管變數
        self.line_limit = 500
        self.method_limit = 10
        self.ignore_list = ['.venv', 'logs', '.git', '.buildozer', '__pycache__', 'build', 'dist', '.time_machine']
        self.root_dir = os.getcwd()
        
        # 2. 專案初始化器結構定義 (NEW_FEATURE: 擴展以支援插值、方位角與熱區分析模組)
        self.gis_structure = {
            "core": ["sqlite_manager.py", "kml_parser.py", "base_task.py", "geo_utils.py", "batch_manager.py", "__init__.py"],
            "plugins": ["api_poi_connector.py", "animator_3d.py", "data_interpolator.py", "heatmap_generator.py", "db_sync.py", "__init__.py"],
            "ui": ["dashboard.py", "file_control.py", "map_webview.py", "__init__.py"],
            "ui/components": ["vehicle_styles.py", "info_cards.py", "__init__.py"],
            "assets/icons/vehicles": [],
            "assets/kml_samples": [],
            "assets/www": ["leaflet_map.html", "map_logic.js", "style.css"],
            "config": ["project_meta.json"]
        }
        
    def bootstrap_system(self):
        """自體繁殖 (Self-Bootstrap) 建立目錄與核心檔案"""
        print(">>> 啟動自體繁殖與環境檢測...")
        directories = ['core', 'plugins', 'logs', 'config', 'assets', 'assets/www']
        
        for d in directories:
            dir_path = os.path.join(self.root_dir, d)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                if not d.startswith('assets') and d != 'logs' and d != 'config':
                    with open(os.path.join(dir_path, '__init__.py'), 'w', encoding='utf-8') as f:
                        f.write("# 初始化模組\n")
                print(f"  [+] 建立目錄: {d}/")
                
        files_to_create = {
            os.path.join('core', 'base_task.py'): BASE_TASK_PY,
            os.path.join('main.py'): MAIN_PY,
            os.path.join('config', 'project_meta.json'): json.dumps(PROJECT_META_JSON, indent=4, ensure_ascii=False)
        }
        
        for filepath, content in files_to_create.items():
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  [+] 建立核心檔案: {filepath}")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_menu(self):
        self.clear_screen()
        print("="*70)
        print(" 🚀 終極自動化專案管理器 V14.0 (Kivy GIS 環保稽查特化版)")
        print("="*70)
        print(" 【第一階段：專案初始化與環境設置】")
        print("  1. [環境與智慧領域建置]")
        print("  2. 🌍 [專案初始化器 (生成環保稽查圖台專屬結構與自動安裝 Kivy 依賴)]")
        print("  3. [套件管理] (匯出 requirements.txt)")
        print("-" * 70)
        print(" 【第二階段：代碼快照與智能協同】")
        print("  4. [專案狀態快照 (State Snapshot)]")
        print("  5. [時光回溯] (備份系統 .time_machine)")
        print("  6. [生成契約] (MASTER_PROMPT.md - 包含 GIS 開發鐵律)")
        print("  7. 🤖 [AI 智慧嚮導 (自然語言雙步工作流/補丁模式)]")
        print("  8. [記憶提取與 AST 精準防爆框萃取]")
        print("  9. [一鍵打包記憶] (執行 3 -> 6 -> 4 -> 5)")
        print("-" * 70)
        print(" 【第三階段：監控與發布】")
        print(" 10. [啟動雷達 (動態監控與 UX)]")
        print(" 11. 🌟 [一鍵完美無缺打包 APK (Android Kivy/WebView Zero-Bug Build)]")
        print("-" * 70)
        print(" 【系統操作】")
        print(" 12. 📖 [使用說明書 (新手引導)]")
        print(" 13. [離開]")
        print("="*70)

    # ==========================================
    # 選單 1：環境與智慧領域建置
    # ==========================================
    def menu_1_env_setup(self):
        print("\n--- 1. 環境與智慧領域建置 ---")
        print("💡 [引導] 此功能會為您建立隔離的虛擬環境 (.venv)，避免套件污染系統。")
        venv_path = os.path.join(self.root_dir, '.venv')
        if not os.path.exists(venv_path):
            print("正在建立虛擬環境 (.venv)...")
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
            print("虛擬環境建立完成。")
        else:
            print("虛擬環境 (.venv) 已存在。")

        gitignore_path = os.path.join(self.root_dir, '.gitignore')
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(GITIGNORE_TEMPLATE)
            print("建立 .gitignore 完成。")

        env_path = os.path.join(self.root_dir, '.env')
        if not os.path.exists(env_path):
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write("DEBUG=True\nAPI_KEY=\n")
            print("建立 .env 完成。")

        user_prompt = input("\n請輸入開發需求或 Prompt (直接按 Enter 則預設為 環保稽查 GIS): ")
        if not user_prompt.strip():
            domain = "⭐ [推薦] 環保稽查 GIS 專案 (Kivy + Leaflet WebView + Heatmap)"
            user_prompt = "預設環保稽查行動 GIS 專案"
        else:
            domain = "客製化跨平台專案"
            
        print(f"偵測領域：{domain}")
        
        meta_path = os.path.join(self.root_dir, 'config', 'project_meta.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            PROJECT_META_JSON["project_type"] = domain
            PROJECT_META_JSON["original_prompt"] = user_prompt
            json.dump(PROJECT_META_JSON, f, indent=4, ensure_ascii=False)
        
        print("\n\033[92m[重要] 請使用以下指令啟動虛擬環境以防套件污染：\033[0m")
        if os.name == 'nt':
            print("\033[92m  .venv\\Scripts\\activate\033[0m")
        else:
            print("\033[92m  source .venv/bin/activate\033[0m")
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 2：專案初始化器 (環保稽查圖台專用結構與套件安裝)
    # ==========================================
    def menu_2_initialize_gis_project(self):
        print("\n--- 2. 🌍 專案初始化器 (環保稽查圖台專用結構與套件安裝) ---")
        print("💡 [引導] 此功能將建立 Kivy GIS 開發專屬的目錄結構，並自動安裝所需套件。")
        print("🚀 開始建構環保稽查圖台開發環境...")
        
        for folder, files in self.gis_structure.items():
            folder_path = os.path.join(self.root_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            
            for file in files:
                file_path = os.path.join(folder_path, file)
                if not os.path.exists(file_path):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        if file.endswith(".py"):
                            f.write(f"# -*- coding: utf-8 -*-\n# Project: Environmental Audit GIS\n# Module: {file}\n\n")
                        elif file == "leaflet_map.html":
                            # NEW_FEATURE: 使用完整的 Leaflet 範本
                            f.write(LEAFLET_HTML_TEMPLATE)
                        elif file.endswith(".js"):
                            f.write("// Leaflet Map Logic Placeholder\n")
                    print(f"✅ 已生成: {os.path.relpath(file_path, self.root_dir)}")
        
        print("\n✨ 結構初始化完成！")

        print("\n📦 準備執行自動化依賴安裝 (Pip Install)...")
        req_path = os.path.join(self.root_dir, 'requirements.txt')
        
        if not os.path.exists(req_path) or True: # 強制更新依賴清單
            with open(req_path, 'w', encoding='utf-8') as f:
                f.write("kivy\nkivymd\nfastkml\nlxml\npandas\nrequests\n")
            print("✅ 建立 GIS 基礎 requirements.txt 完成 (包含 Kivy, fastkml, pandas 等)。")
        
        try:
            print(f">> 正在呼叫 {sys.executable} 安裝套件，請稍候 (初次安裝 Kivy 可能需要幾分鐘)...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)
            print("\n\033[92m🎉 套件自動安裝完成！環境已可正常運行。\033[0m")
        except Exception as e:
            print(f"\n\033[91m❌ 套件安裝發生錯誤: {e}\n建議手動啟動虛擬環境後執行 pip install -r requirements.txt\033[0m")

        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 3：套件管理
    # ==========================================
    def menu_3_package_manage(self):
        print("\n--- 3. 套件管理 ---")
        print("💡 [引導] 將目前環境中已安裝的套件版本固定並匯出至 requirements.txt。")
        try:
            req_path = os.path.join(self.root_dir, 'requirements.txt')
            result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, check=True)
            with open(req_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"已成功執行 pip freeze 並更新至 {req_path}。")
        except Exception as e:
            print(f"套件管理發生錯誤: {e}")
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 4：專案狀態快照
    # ==========================================
    def _generate_tree(self, directory: str, prefix: str = "") -> str:
        tree_str = ""
        try:
            items = os.listdir(directory)
        except PermissionError:
            return tree_str
            
        items.sort()
        items = [i for i in items if not i.startswith('.') and i not in self.ignore_list]
        
        for i, item in enumerate(items):
            path = os.path.join(directory, item)
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            tree_str += f"{prefix}{connector}{item}\n"
            if os.path.isdir(path):
                extension = "    " if is_last else "│   "
                tree_str += self._generate_tree(path, prefix + extension)
        return tree_str

    def menu_4_state_snapshot(self):
        print("\n--- 4. 專案狀態快照 ---")
        snapshot_path = os.path.join(self.root_dir, 'STATE_SNAPSHOT.md')
        
        content = "# 專案狀態快照\n\n## 1. 跨平台目錄樹\n```text\n"
        content += f"{os.path.basename(self.root_dir)}/\n"
        content += self._generate_tree(self.root_dir)
        content += "```\n\n## 2. 專案代碼骨架 (AST Skeleton)\n"
        
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in self.ignore_list]
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, self.root_dir)
                    content += f"\n### File: {rel_path}\n```python\n"
                    content += self._extract_ast_skeleton(filepath)
                    content += "\n```\n"
                    
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("狀態快照已匯出至 STATE_SNAPSHOT.md")
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 5：時光回溯 (專案備份)
    # ==========================================
    def menu_5_time_machine(self):
        print("\n--- 5. 時光回溯 (專案備份) ---")
        tm_dir = os.path.join(self.root_dir, '.time_machine')
        if not os.path.exists(tm_dir):
            os.makedirs(tm_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(tm_dir, f"backup_{timestamp}")
        
        print(f"正在備份專案至: {backup_path} ...")
        try:
            shutil.copytree(
                self.root_dir, 
                backup_path, 
                ignore=shutil.ignore_patterns(*self.ignore_list, '*.pyc', '*.sqlite3')
            )
            print("\033[92m備份成功！\033[0m")
        except Exception as e:
            print(f"備份發生錯誤: {e}")
            
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 6：生成契約 (MASTER_PROMPT.md)
    # ==========================================
    def menu_6_generate_master_prompt(self):
        print("\n--- 6. 生成契約 (MASTER_PROMPT.md) ---")
        # NEW_FEATURE: 全面擴充 E 區塊，納入 B 模組(New Requirements) 的架構設計細節
        prompt_content = f"""# 終極開發契約 MASTER_PROMPT (V14.0 Kivy GIS Edition)

## A. 主動告警與拆解防護
[系統強制規範] 若單一類別超過 {self.method_limit} 個方法，或者單一檔案超過 {self.line_limit} 行，AI 必須主動建議並執行拆解重構，絕不可繼續堆疊代碼。

## B. 14 點開發鐵律 (最高優先級，絕不可違背)
1. 嚴禁省略代碼：絕不可使用 `...` 或「其餘代碼保持不變」，必須提供可直接複製運行的全量代碼。
2. 需求完整保留：修改時必須保留所有既有的正確業務邏輯。
3. 介面一致：函數與類別簽名 (Signatures) 必須維持向下相容。
4. #NEW_FEATURE 註記：新增功能必須在註解加上 `#NEW_FEATURE` 標籤以便追蹤。
5. 支援配置檔過濾：環境變數與敏感資訊必須使用 `.env` 與 JSON 配置檔隔離。
6. 無限拓展：遵循 SOLID 原則中的開放封閉原則 (OCP)，保留擴充介面。
7. 3 次未解主動停損：若同一 Bug 修復 3 次仍失敗，AI 需停止嘗試，改為產出「問題分析報告與 3 個根本解決方案」。
8. 契約式除錯：除錯時必須印出進入函數與離開函數的狀態快照 (State Snapshot)。
9. 分離重構與修改：重構程式碼與新增功能不可在同一次 Commit/Prompt 中混用。
10. 拒絕假性修復：禁用 `try-except pass` 掩蓋錯誤，必須妥善處理 Exception。
11. 🌟 環保執法空間運算鐵律：GIS 運算需考慮 WGS84 轉換精度、KML 大檔案效能 (需使用 fastkml/lxml 分塊讀取)，以及 Android 平板設備的記憶體限制。
12. 動態專案約束：隨時參照 `config/project_meta.json` 內的約束條件進行開發。
13. 🌟 行動端封裝路徑鐵律：絕對禁止使用一般相對路徑！資源存取必須考慮 Android APK 解包後的路徑位置。
14. ⚠️ 嚴格 API 與引用防護：所有時間函數、路徑拼接、AST 操作，必須確認 Python 版本相容性。

## C. 程式碼修改思考流程
1. 現況分析：理解現有架構。
2. 衝擊評估：評估修改對 Windows 與 Android 環境差異的衝擊。
3. 最小化修改：精準定位修改點，確保為「補丁」性質。
4. 驗證邏輯：確保修改符合上述 14 點鐵律以及下方 E 區塊的框架防護鐵律。

## D. UI 與 UX 規範
介面設計必須對稽查人員友善：提供視覺化介面、專業圖台功能操作鍵、友善檔案管理、批次匯入/刪除功能。

## E. 🌟 環保稽查 GIS 專屬架構鐵律 (Kivy + SQLite + WebView)
**【核心模組實作規範】**
1. **防呆與資料隔離 (Batch_ID)**：必須實作 SQLite 本機資料庫。匯入 KML 時，必須自動分辨 `GPS_History.kml` 及 `GPS_Stoppoint.kml`，並賦予唯一 `Batch_ID` 防止污染。透過 SQL 動態生成下拉選單供選擇車號，確保使用者只能勾選到「有內容的日期」。
2. **圖台引擎 (Leaflet/Mapbox)**：使用 Android WebView 嵌入 HTML5/JS 引擎 (Leaflet.js)。Python 後端負責處理 KML 解析與運算，再透過 JS 傳遞給前端顯示，需支援 Google 混合圖層、空拍圖與街景連結。
3. **動態演示與 3D 動畫運算**：
   - **插值運算**：若 GPS 點位不夠密集，Python 需進行線性插值，確保車輛平滑移動。
   - **轉向控制 (Bearing)**：計算相鄰點的方位角 (Bearing)，動態更新 3D 車輛圖示的 Rotation 屬性，確保車頭朝向行駛方向。
4. **探索模式 UX (時間軸觸發器)**：預設為探索模式。隨軌跡播放，當到達特定時間點/停頓點，才觸發周邊 500 公尺內的「停頓點資訊卡」與地標資料漸進彈出。
5. **熱區分析與地標雙軌制**：
   - **熱點圖 (Heatmap)**：針對深夜頻繁停頓地點，生成熱點圖標示非法棄置疑點。
   - **離線/連線混合地標**：預先封裝離線 GeoJSON/SQLite 商號工廠庫，若有 4G 網路則透過 Python `requests` 異步呼叫 API 補強資訊。
"""
        prompt_path = os.path.join(self.root_dir, 'MASTER_PROMPT.md')
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        print("MASTER_PROMPT.md 已成功生成，包含最新 Kivy GIS (插值、方位角、熱區) 防護鐵律。")
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 7：AI 智慧嚮導 (雙步工作流/補丁模式)
    # ==========================================
    def menu_7_ai_guide(self):
        print("\n--- 7. 🤖 AI 智慧嚮導 (自然語言雙步工作流) ---")
        print("💡 [引導] 此功能讓您與 AI 協作開發。")
        print("⚠️ 【重要規範】請依序操作：必須先執行 Phase 1 讓 AI 規劃，再執行 Phase 2 合併代碼。\n")
        print("  1. [Phase 1] 生成規劃期 Prompt (規劃要改哪些檔案)")
        print("  2. [Phase 2] 🌟 執行多檔智能解析並打包 (需輸入 Phase 1 AI 給的回覆)")
        choice = input("\n請選擇 (1 或 2): ")
        
        if choice == '1':
            goal = input("\n請輸入您的開發目標 (例如: 實作 GPS 軌跡插值與 3D 動畫方位角計算): ")
            prompt = f"你現在是頂級架構規劃師。我的目標是：「{goal}」。\n請分析此需求，並回覆我需要『建立或修改』哪些檔案的「完整路徑」。\n注意：僅需列出路徑清單與簡略思路，**不要**開始寫程式碼。"
            with open('PHASE1_PROMPT.md', 'w', encoding='utf-8') as f:
                f.write(prompt)
            print("\n✅ 已產出 PHASE1_PROMPT.md！\n👉 請將其內容複製貼給 AI，並等待 AI 列出檔案清單。")
          
        elif choice == '2':
            confirm = input("\n⚠️ 【確認】您是否已經執行過 Phase 1，並拿到了 AI 回覆的檔案清單？ (y/n): ").lower()
            if confirm != 'y':
                print(">> 操作已取消。請先執行 [1. Phase 1] 功能！")
                time.sleep(1.5)
                return

            print("\n👉 請直接貼上 AI 在 Phase 1 回覆的完整內容。")
            print("(支援多行輸入，請在輸入完畢後，於新的一行輸入 'EOF' 並按 Enter)")
          
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == 'EOF':
                        break
                    lines.append(line)
                except EOFError:
                    break
                    
            text = "\n".join(lines)
            file_patterns = re.findall(r'([a-zA-Z0-9_\-\/\\]+\.(?:py|json|md|kml|kv|html|js|css))', text)
            unique_files = list(set([os.path.normpath(p.strip()) for p in file_patterns]))
          
            if not unique_files:
                print("\n❌ 無法從文本中解析出任何目標檔案路徑。請確認貼上的內容包含檔名。")
                input("\n按 Enter 鍵返回選單...")
                return
                
            print(f"\n✅ 成功解析到 {len(unique_files)} 個目標檔案：")
            for f in unique_files:
                print(f" - {f}")
                
            phase2_path = os.path.join(self.root_dir, 'PHASE2_PROMPT.md')
            with open(phase2_path, 'w', encoding='utf-8') as f:
                f.write("# 首席工程師多檔協同開發階段 (🔥 補丁與疊加模式 PATCH MODE)\n\n")
                f.write("請依照先前的規劃，為下列所有檔案撰寫完整的程式碼。\n")
                f.write("⚠️ 【嚴格補丁規範】：本次修改為「補丁」性質。你必須**完整保留**現有架構中的任何既有功能與邏輯，新需求必須是「疊加」或「優化」，絕對不可破壞、精簡或替換原有的核心系統！\n\n")
                f.write("⚠️ 【完整產出規範】：請遵守 MASTER_PROMPT 鐵律，產出完整的全量代碼，絕對禁止使用「...」或「原有程式碼保持不變」等佔位符。\n\n")
                
                for filepath in unique_files:
                    f.write(f"## 檔案: {filepath}\n```{'python' if filepath.endswith('.py') else 'javascript' if filepath.endswith('.js') else 'html' if filepath.endswith('.html') else 'text'}\n")
                    if os.path.exists(filepath):
                        with open(filepath, 'r', encoding='utf-8') as target_f:
                            f.write(target_f.read())
                    else:
                        dir_name = os.path.dirname(filepath)
                        if dir_name and not os.path.exists(dir_name):
                            os.makedirs(dir_name)
                        f.write(f"# 這是全新檔案，請生成完整代碼\n")
                    f.write("\n```\n\n")
                    
            print(f"\n🎉 已成功抓取現有代碼並產出 {phase2_path}。")
            print("👉 請將其內容交給 AI 首席工程師完成疊加開發！")
          
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 8：記憶提取與 AST 精準防爆框萃取
    # ==========================================
    def _extract_ast_skeleton(self, filepath: str) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source)
          
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        node.body = [ast.Expr(value=ast.Constant(value=docstring))]
                    else:
                        node.body = [ast.Pass()]
                        
            if hasattr(ast, 'unparse'):
                return ast.unparse(tree)
            else:
                skeleton_lines = []
                for line in source.split('\n'):
                    if line.strip().startswith('class ') or line.strip().startswith('def '):
                        skeleton_lines.append(line)
                return "\n".join(skeleton_lines) + "\n    # AST unparse unavailable, showing signatures only."
        except Exception as e:
            return f"# 骨架萃取失敗: {e}"

    def menu_8_memory_extraction(self):
        print("\n--- 8. 記憶提取與 AST 精準防爆框萃取 ---")
        targets_input = input("\n請輸入欲『完整提取修改』的檔案路徑 (多筆請用逗號分隔，留空則僅產出整體骨架): ")
        targets = [t.strip() for t in targets_input.split(',')] if targets_input else []
        
        rescue_path = os.path.join(self.root_dir, 'RESCUE_PROMPT.md')
        content = "# 系統記憶提取與救援 (RESCUE PROMPT)\n\n"
        
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in self.ignore_list]
            for file in files:
                if not file.endswith('.py'): continue
                
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, self.root_dir)
                norm_rel_path = rel_path.replace('\\', '/')
                target_matched = any(norm_rel_path == t.replace('\\', '/') for t in targets)
                
                if target_matched:
                    content += f"\n## <Modified> 目標修改檔案: {rel_path} \n```python\n"
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content += f.read()
                    content += "\n```\n"
                else:
                    content += f"\n## [參考骨架] {rel_path} \n```python\n"
                    content += self._extract_ast_skeleton(filepath)
                    content += "\n```\n"
                    
        with open(rescue_path, 'w', encoding='utf-8') as f:
            f.write(content)
          
        print(f"提取完成！已匯出至 {rescue_path}")
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 9：一鍵打包記憶
    # ==========================================
    def menu_9_one_click_memory(self):
        print("\n--- 9. 一鍵打包記憶 (依序執行 套件、契約、快照、備份) ---")
        self.menu_3_package_manage()
        self.menu_6_generate_master_prompt()
        self.menu_4_state_snapshot()
        self.menu_5_time_machine()
        print("\n\033[92m一鍵打包記憶流程全數完成！已可將生成物發送給 AI。\033[0m")
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 10：啟動雷達 (動態監控與 UX)
    # ==========================================
    def menu_10_launch_radar(self):
        print("\n--- 10. 啟動雷達 (代碼品質與膨脹監控) ---")
        print("啟動無限迴圈監控 (按 Ctrl+C 中止)...")
        try:
            while True:
                issues_found = False
                for root, dirs, files in os.walk(self.root_dir):
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in self.ignore_list]
                    for file in files:
                        if not file.endswith('.py'): continue
                        filepath = os.path.join(root, file)
                        
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                                line_count = len(lines)
                                
                            if line_count > self.line_limit:
                                print(f"[\033[91m警示\033[0m] {file} 行數超標: {line_count}/{self.line_limit}")
                                if os.name == 'nt': print('\a')
                                issues_found = True
                                
                            source = "".join(lines)
                            tree = ast.parse(source)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.ClassDef):
                                    methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                                    if len(methods) > self.method_limit:
                                        print(f"[\033[91m警示\033[0m] {file} 類別 {node.name} 方法數超標: {len(methods)}/{self.method_limit}")
                                        if os.name == 'nt': print('\a')
                                        issues_found = True
                        except Exception:
                            pass
                            
                if not issues_found:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n雷達監控已中止。")
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 11：一鍵完美無缺打包 APK
    # ==========================================
    def menu_11_android_build(self):
        print("\n--- 11. 🌟 一鍵完美無缺打包 APK (Kivy GIS 優化程序) ---")
        
        print("\n>> 步驟一：掃描 WebView 與靜態資源檔 (Assets)...")
        assets_extensions = ('.kml', '.json', '.png', '.jpg', '.kv', '.html', '.js', '.css')
        found_assets = set()
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in self.ignore_list]
            for file in files:
                if file.endswith(assets_extensions):
                    ext = file.split('.')[-1]
                    found_assets.add(ext)
        print(f"偵測到的資源副檔名: {', '.join(found_assets)}")

        print("\n>> 步驟二：Android GIS 與網路權限設定檢核...")
        permissions = "android.permissions = ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET"
        print(f"請確保 buildozer.spec 包含以下權限：\n\033[93m{permissions}\033[0m")
        if found_assets:
            ext_str = ",".join(found_assets)
            print(f"並確保 source.include_exts 包含: \033[93m{ext_str}\033[0m")

        print("\n>> 步驟三：靜默崩潰攔截器 (Anti-Silent Crash) 檢查...")
        main_path = os.path.join(self.root_dir, 'main.py')
        if os.path.exists(main_path):
            with open(main_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            if 'sys.excepthook = global_exception_handler' not in main_content:
                print("未偵測到全域崩潰攔截器，正在自動注入至 main.py ...")
                with open(main_path, 'w', encoding='utf-8') as f:
                    f.write("import sys\nimport traceback\nimport os\nfrom datetime import datetime\n\n")
                    f.write("def global_exception_handler(exc_type, exc_value, exc_traceback):\n")
                    f.write("    traceback_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))\n")
                    f.write("    try:\n")
                    f.write("        with open('/sdcard/Download/app_crash_log.txt', 'a', encoding='utf-8') as log_f:\n")
                    f.write("            log_f.write(f'\\n[{datetime.now()}] FATAL ERROR:\\n{traceback_details}')\n")
                    f.write("    except Exception:\n        pass\n")
                    f.write("    print('CRITICAL CRASH:\\n' + traceback_details)\n\n")
                    f.write("sys.excepthook = global_exception_handler\n\n")
                    f.write(main_content)
                print("注入成功！閃退將自動記錄至 Android Download 資料夾。")
            else:
                print("靜默崩潰攔截器已存在。")
        else:
            print("找不到 main.py，略過注入。")

        print("\n>> \033[92m打包優化準備完畢！\033[0m")
        print("請在 WSL2 或 Linux 終端機 (Terminal B) 執行以下指令進行 APK 編譯：")
        print("\033[92m  buildozer android debug deploy run\033[0m")
        input("\n按 Enter 鍵返回選單...")

    # ==========================================
    # 選單 12：使用說明書 (新手引導)
    # ==========================================
    def menu_12_user_manual(self):
        print("\n--- 12. 📖 使用說明書 (新手引導) ---")
        manual = """
==============================================================
【終極自動化專案管理器 - 系統導覽與操作步驟指南】
建議開啟雙終端機工作流：
Terminal A: 執行本腳本，負責架構管理、快照與 AI 協同溝通。
Terminal B: 進入 .venv 執行實際的 pip 安裝、Python 測試與打包編譯。

【第一階段：專案初始化與環境設置 (Setup)】
▶️ 功能 1 [環境與智慧領域建置]: 建立虛擬環境 (.venv) 及隱藏檔。
▶️ 功能 2 [專案初始化器 (GIS 結構與依賴)]: 建立 Kivy GIS 分層架構 (含 SQLite/WebView/Heatmap)，並自動安裝套件。
▶️ 功能 3 [套件管理]: 匯出 requirements.txt。

【第二階段：代碼快照與智能協同 (AI Collaboration)】
▶️ 功能 4 & 5 [快照與時光機]: 備份專案與產生代碼骨架。
▶️ 功能 6 [生成契約]: 產出 MASTER_PROMPT.md (包含 KML處理、插值運算、熱點圖與防呆鐵律)。
▶️ 功能 7 [AI 智慧嚮導 (Phase 1 & 2)]: 補丁模式智能開發工作流。
▶️ 功能 8 [記憶提取]: 重置 AI 對專案架構的記憶。

【第三階段：監控與發布 (Monitor & Build)】
▶️ 功能 10 [啟動雷達]: 背景掃描代碼品質。
▶️ 功能 11 [打包 APK 優化]: 自動掃描 GIS 資源並注入 Android 防閃退機制。
==============================================================
"""
        print(manual)
        input("按 Enter 鍵返回選單...")

    # ==========================================
    # 核心無限迴圈運行器
    # ==========================================
    def run(self):
        self.bootstrap_system()
        time.sleep(1) 
        
        while True:
            try:
                self.print_menu()
                choice = input("\n請輸入選項 (1-13): ").strip()
                
                if choice == '1':
                    self.menu_1_env_setup()
                elif choice == '2':
                    self.menu_2_initialize_gis_project()
                elif choice == '3':
                    self.menu_3_package_manage()
                elif choice == '4':
                    self.menu_4_state_snapshot()
                elif choice == '5':
                    self.menu_5_time_machine()
                elif choice == '6':
                    self.menu_6_generate_master_prompt()
                elif choice == '7':
                    self.menu_7_ai_guide()
                elif choice == '8':
                    self.menu_8_memory_extraction()
                elif choice == '9':
                    self.menu_9_one_click_memory()
                elif choice == '10':
                    self.menu_10_launch_radar()
                elif choice == '11':
                    self.menu_11_android_build()
                elif choice == '12':
                    self.menu_12_user_manual()
                elif choice == '13':
                    print("\n正在安全關閉專案管理器，再會！")
                    self.clear_screen()
                    break
                else:
                    print("無效的選項，請重新輸入。")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n\n偵測到 KeyboardInterrupt (Ctrl+C)。")
                print("正在安全清理資源並優雅退出系統...")
                time.sleep(1)
                self.clear_screen()
                sys.exit(0)
            except Exception as e:
                print(f"\n發生未預期錯誤: {e}")
                input("按 Enter 鍵繼續...")

if __name__ == "__main__":
    manager = AutoProjectManager()
    manager.run()