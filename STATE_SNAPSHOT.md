# 專案狀態快照

## 1. 跨平台目錄樹
```text
試-安卓平板自動化專案管理器2.0/
├── MASTER_PROMPT.md
├── PHASE1_PROMPT.md
├── PHASE2_PROMPT.md
├── STATE_SNAPSHOT.md
├── assets
│   ├── fonts
│   │   └── NotoSansTC-VariableFont_wght.ttf
│   ├── icons
│   │   └── vehicles
│   ├── kml_samples
│   └── www
│       ├── leaflet_map.html
│       ├── map_logic.js
│       └── style.css
├── auto_project_manager.py
├── config
│   └── project_meta.json
├── core
│   ├── __init__.py
│   ├── base_task.py
│   ├── kml_parser.py
│   └── sqlite_manager.py
├── gis_audit_offline.sqlite3
├── main.py
├── plugins
│   ├── __init__.py
│   ├── animator_3d.py
│   ├── api_poi_connector.py
│   └── data_interpolator.py
├── requirements.txt
├── ui
│   ├── __init__.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── info_cards.py
│   │   └── vehicle_styles.py
│   ├── dashboard.py
│   ├── file_control.py
│   └── map_webview.py
├── 原生prompt.docx
└── 新增 Microsoft Word 文件.docx
```

## 2. 專案代碼骨架 (AST Skeleton)

### File: auto_project_manager.py
```python
"""
終極自動化專案管理器 V13.0 (Kivy GIS 環保稽查特化版 & Android 跨平台專用優化版)
角色：Principal Mobile/GIS Python Architect
功能：自體繁殖、13大邏輯自動化工作流、AST 骨架萃取、智慧多檔補丁解析、Android 零 Bug 打包優化
更新：導入 Kivy+Leaflet 架構、KML/SQLite 目錄結構、GIS專屬開發鐵律、補丁模式強化
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
BASE_TASK_PY = '# -*- coding: utf-8 -*-\nfrom abc import ABC, abstractmethod\n\nclass BaseTask(ABC):\n    def __init__(self, task_name: str):\n        self.task_name = task_name\n\n    @abstractmethod\n    def execute(self, *args, **kwargs):\n        pass\n'
MAIN_PY = '# -*- coding: utf-8 -*-\nimport os\nimport sys\nimport traceback\nfrom datetime import datetime\n\n# 全域致命錯誤捕捉器 (Anti-Silent Crash - Android 版)\ndef global_exception_handler(exc_type, exc_value, exc_traceback):\n    traceback_details = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))\n    print(f"CRITICAL CRASH:\\n{traceback_details}")\n    \n    # 嘗試寫入 Android 公開目錄或本地目錄\n    log_paths = [\n        "/sdcard/Download/app_crash_log.txt",  # Android 下載目錄\n        os.path.join(os.path.expanduser("~"), "Downloads", "app_crash_log.txt"), # Windows/Linux 備用\n        "app_crash_log.txt" # 本地備用\n    ]\n    \n    for path in log_paths:\n        try:\n            with open(path, "a", encoding="utf-8") as f:\n                f.write(f"\\n[{datetime.now().strftime(\'%Y-%m-%d %H:%M:%S\')}] FATAL ERROR:\\n")\n                f.write(traceback_details)\n                f.write("\\n" + "="*50 + "\\n")\n            break # 成功寫入一個即可\n        except Exception:\n            continue\n\nsys.excepthook = global_exception_handler\n\n# 核心引擎與 UI 進入點 (Kivy App Placeholder)\ndef main():\n    print("啟動跨平台環保稽查 GIS 核心引擎 (Kivy 環境)...")\n    print("正在初始化 SQLite 本機資料庫與 KML 解析引擎...")\n    print("UI 進入點已準備完畢，等待 Kivy 框架載入 WebView 與地圖圖層。")\n    \n    # 未來由 AI 實作 Kivy App 類別並在此處執行 run()\n    # from ui.dashboard import GISAuditApp\n    # GISAuditApp().run()\n\nif __name__ == "__main__":\n    main()\n'
PROJECT_META_JSON = {'project_type': '環保稽查 GIS 圖台 (Kivy + Leaflet)', 'original_prompt': '使用 Kivy 開發 Android 平板單機版 GIS 稽查軟體', 'constraints': ['跨平台相容', 'SOLID 原則', 'Clean Architecture', 'Kivy/KivyMD UI', 'SQLite 離線防呆', 'KML 批次解析']}
GITIGNORE_TEMPLATE = '\n.venv/\nlogs/\n.git/\n.buildozer/\n__pycache__/\nbuild/\ndist/\n.time_machine/\n*.pyc\n.env\n*.sqlite3\n'

class AutoProjectManager:
    pass
if __name__ == '__main__':
    manager = AutoProjectManager()
    manager.run()
```

### File: main.py
```python
import os
import sys
import traceback
from datetime import datetime
from core.sqlite_manager import SQLiteManager
from core.kml_parser import KMLParser

def global_exception_handler(exc_type, exc_value, exc_traceback):
    pass
sys.excepthook = global_exception_handler

class GISEngineBootstrap:
    pass

def main():
    pass
if __name__ == '__main__':
    main()
```

### File: core\base_task.py
```python
from abc import ABC, abstractmethod

class BaseTask(ABC):
    pass
```

### File: core\kml_parser.py
```python
import os
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from core.sqlite_manager import SQLiteManager

class KMLParser:
    pass
```

### File: core\sqlite_manager.py
```python
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Tuple

class SQLiteManager:
    pass
```

### File: core\__init__.py
```python

```

### File: plugins\animator_3d.py
```python
class Animator3D:
    pass
```

### File: plugins\api_poi_connector.py
```python
import requests
import json
from typing import Dict, List

class POIConnector:
    pass
```

### File: plugins\data_interpolator.py
```python
import math
from typing import List, Dict

class DataInterpolator:
    pass
```

### File: plugins\__init__.py
```python

```

### File: ui\dashboard.py
```python
import os
from kivy.utils import platform
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from ui.map_webview import MapWebView
from ui.file_control import FileControlScreen
from plugins.animator_3d import Animator3D

class DashboardScreen(MDScreen):
    pass

class GISAuditApp(MDApp):
    pass
```

### File: ui\file_control.py
```python
import os
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.dialog import MDDialog
from kivy.graphics import Color, Rectangle

class FileControlScreen(MDScreen):
    pass
```

### File: ui\map_webview.py
```python
import os
import json
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class MapWebView(Widget):
    """地圖容器：在 Android 設備上使用原生 WebView 渲染 Leaflet，
在 Windows 開發環境下則提供視覺化的模擬佔位符。"""
```

### File: ui\__init__.py
```python

```

### File: ui\components\info_cards.py
```python

```

### File: ui\components\vehicle_styles.py
```python

```

### File: ui\components\__init__.py
```python

```
