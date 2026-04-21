# -*- coding: utf-8 -*-
import os
import json
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock, mainthread
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class MapWebView(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_path = os.path.join(os.getcwd(), 'assets', 'www', 'leaflet_map.html')
        self.webview = None
        
        # 繪製 Kivy 背景 (除錯用)
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_native_view_geometry, pos=self._update_native_view_geometry)

        if platform == 'android':
            # 延遲一點點時間執行，確保 Kivy 視圖已經穩定
            Clock.schedule_once(lambda dt: self._init_android_webview(), 1)
        else:
            self._init_windows_mock()

    def _update_native_view_geometry(self, *args):
        """同步 Kivy 元件的位置到 Android 原生 WebView"""
        self.rect.pos = self.pos
        self.rect.size = self.size
        
        if platform == 'android' and self.webview:
            from jnius import autoclass
            from android.runnable import run_on_ui_thread # type: ignore
            
            # Kivy 的 (0,0) 在左下，Android 的 (0,0) 在左上，需要轉換
            window = autoclass('org.kivy.android.PythonActivity').mActivity.getWindow().getDecorView()
            win_height = window.getHeight()
            
            # 計算在 Android 座標系中的位置
            x = int(self.x)
            y = int(win_height - (self.y + self.height)) # 座標系翻轉
            w = int(self.width)
            h = int(self.height)

            @run_on_ui_thread
            def update_params():
                LayoutParams = autoclass('android.widget.FrameLayout$LayoutParams')
                params = LayoutParams(w, h)
                params.leftMargin = x
                params.topMargin = y
                self.webview.setLayoutParams(params)
            
            update_params()

    def _init_windows_mock(self):
        self.mock_label = Label(text="[Windows 模擬模式]\n地圖區域", color=(1,1,1,1))
        self.add_widget(self.mock_label)
        self.bind(pos=lambda x,y: setattr(self.mock_label, 'pos', self.pos),
                  size=lambda x,y: setattr(self.mock_label, 'size', self.size))

    def _init_android_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread # type: ignore
        
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        FrameLayout = autoclass('android.widget.FrameLayout')

        @run_on_ui_thread
        def create_webview():
            self.webview = WebView(activity)
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.getSettings().setDomStorageEnabled(True)
            self.webview.getSettings().setAllowFileAccess(True)
            self.webview.setWebViewClient(WebViewClient())
            
            # 載入地圖
            file_url = f"file://{self.html_path}"
            self.webview.loadUrl(file_url)
            
            # 【關鍵修復】：不要使用 setContentView，而是 addView
            # 取得 Android 的最底層佈局，然後把 WebView 疊加在 Kivy 指定的位置上
            parent = activity.findViewById(16908290) # android.R.id.content
            parent.addView(self.webview)
            
            # 立即更新一次位置
            self._update_native_view_geometry()

        create_webview()

    @mainthread
    def evaluate_javascript(self, js_code: str):
        if platform == 'android' and self.webview:
            from android.runnable import run_on_ui_thread # type: ignore
            @run_on_ui_thread
            def run_js():
                self.webview.evaluateJavascript(js_code, None)
            run_js()

    def update_gis_data(self, gis_data: dict):
        json_data = json.dumps(gis_data)
        js_code = f"window.receiveGISData({json_data});"
        self.evaluate_javascript(js_code)
        
    def trigger_action(self, action: str, payload: dict = {}):
        json_payload = json.dumps(payload)
        js_code = f"window.triggerAction('{action}', {json_payload});"
        self.evaluate_javascript(js_code)
