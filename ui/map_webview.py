# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: ui/map_webview.py
# NEW_FEATURE: 跨平台 WebView 容器 (Windows 模擬開發 + Android 原生渲染)

import os
import json
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class MapWebView(Widget):
    """
    地圖容器：在 Android 設備上使用原生 WebView 渲染 Leaflet，
    在 Windows 開發環境下則提供視覺化的模擬佔位符。
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_path = os.path.join(os.getcwd(), 'assets', 'www', 'leaflet_map.html')
        self.webview = None
        
        # 繪製背景
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        if platform == 'android':
            self._init_android_webview()
        else:
            self._init_windows_mock()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        if hasattr(self, 'mock_label'):
            self.mock_label.pos = self.pos
            self.mock_label.size = self.size

    def _init_windows_mock(self):
        """Windows 開發環境下的模擬視圖 (防呆與除錯用)"""
        self.mock_label = Label(
            text="[Windows 開發模式]\nLeaflet 地圖引擎將於 Android 平板原生渲染\n(WebView API)",
            color=(0.3, 0.3, 0.3, 1),
            halign="center"
        )
        self.add_widget(self.mock_label)

    def _init_android_webview(self):
        """Android 原生 WebView 初始化 (透過 Pyjnius 呼叫 Java API)"""
        from jnius import autoclass
        from android.runnable import run_on_ui_thread # type: ignore
        
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity

        @run_on_ui_thread
        def create_webview():
            self.webview = WebView(activity)
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.getSettings().setDomStorageEnabled(True)
            self.webview.getSettings().setAllowFileAccess(True) # 允許讀取本地 HTML
            self.webview.setWebViewClient(WebViewClient())
            
            # 將 HTML 載入 WebView
            file_url = f"file://{self.html_path}"
            self.webview.loadUrl(file_url)
            
            # 將 WebView 加入到 Android Activity 的視圖中
            activity.setContentView(self.webview)

        create_webview()

    @mainthread
    def evaluate_javascript(self, js_code: str):
        """從 Python 傳送資料到 Leaflet JavaScript 引擎"""
        if platform == 'android' and self.webview:
            from android.runnable import run_on_ui_thread # type: ignore
            from jnius import autoclass
            ValueCallback = autoclass('android.webkit.ValueCallback')
            
            @run_on_ui_thread
            def run_js():
                # Android 4.4+ 支援 evaluateJavascript
                self.webview.evaluateJavascript(js_code, None)
            run_js()
        else:
            print(f"[Windows 模擬] 傳送 JS 指令: {js_code[:100]}...")

    def update_gis_data(self, gis_data: dict):
        """將 SQLite 取得的軌跡與停頓點傳入前端"""
        json_data = json.dumps(gis_data)
        js_code = f"window.receiveGISData({json_data});"
        self.evaluate_javascript(js_code)
        
    def trigger_action(self, action: str, payload: dict = {}):
        """觸發地圖前端動畫或狀態改變 (例如：播放、暫停、下一步)"""
        json_payload = json.dumps(payload)
        js_code = f"window.triggerAction('{action}', {json_payload});"
        self.evaluate_javascript(js_code)