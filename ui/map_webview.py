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
        
        # 繪製 Kivy 背景 (除錯用底色)
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_native_view_geometry, pos=self._update_native_view_geometry)

        if platform == 'android':
            Clock.schedule_once(lambda dt: self._init_android_webview(), 1)
        else:
            self._init_windows_mock()

    def _update_native_view_geometry(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
        if platform == 'android' and self.webview:
            from jnius import autoclass
            from android.runnable import run_on_ui_thread # type: ignore
            
            # 【關鍵修復】：在 Python 執行緒先取得尺寸數值
            kivy_x = int(self.x)
            kivy_y = int(self.y)
            kivy_w = int(self.width)
            kivy_h = int(self.height)

            @run_on_ui_thread
            def update_params():
                try:
                    # 【關鍵修復】：所有牽涉到 Android 原生 UI 的操作，必須在 UI Thread 內執行
                    activity = autoclass('org.kivy.android.PythonActivity').mActivity
                    window = activity.getWindow().getDecorView()
                    win_height = window.getHeight()
                    
                    # 座標系翻轉
                    android_y = int(win_height - (kivy_y + kivy_h))
                    
                    LayoutParams = autoclass('android.widget.FrameLayout$LayoutParams')
                    params = LayoutParams(kivy_w, kivy_h)
                    params.leftMargin = kivy_x
                    params.topMargin = android_y
                    
                    self.webview.setLayoutParams(params)
                except Exception as e:
                    print(f"WebView 尺寸更新失敗: {e}")
            
            update_params()

    def _init_windows_mock(self):
        self.mock_label = Label(text="[Windows 模擬模式]\n地圖區域", color=(1,1,1,1))
        self.add_widget(self.mock_label)
        self.bind(pos=lambda x,y: setattr(self.mock_label, 'pos', self.pos),
                  size=lambda x,y: setattr(self.mock_label, 'size', self.size))

    def _init_android_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread # type: ignore

        @run_on_ui_thread
        def create_webview():
            try:
                WebView = autoclass('android.webkit.WebView')
                WebViewClient = autoclass('android.webkit.WebViewClient')
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                
                self.webview = WebView(activity)
                self.webview.getSettings().setJavaScriptEnabled(True)
                self.webview.getSettings().setDomStorageEnabled(True)
                self.webview.getSettings().setAllowFileAccess(True)
                self.webview.setWebViewClient(WebViewClient())
                
                file_url = f"file://{self.html_path}"
                self.webview.loadUrl(file_url)
                
                # 【關鍵修復】：使用更安全的 addContentView，避免覆蓋 Kivy 主畫面
                LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
                activity.addContentView(self.webview, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
                
                self._update_native_view_geometry()
            except Exception as e:
                print(f"WebView 建立失敗: {e}")

        create_webview()

    @mainthread
    def evaluate_javascript(self, js_code: str):
        if platform == 'android' and self.webview:
            from android.runnable import run_on_ui_thread # type: ignore
            @run_on_ui_thread
            def run_js():
                try:
                    self.webview.evaluateJavascript(js_code, None)
                except Exception:
                    pass
            run_js()

    def update_gis_data(self, gis_data: dict):
        json_data = json.dumps(gis_data)
        js_code = f"window.receiveGISData({json_data});"
        self.evaluate_javascript(js_code)
        
    def trigger_action(self, action: str, payload: dict = {}):
        json_payload = json.dumps(payload)
        js_code = f"window.triggerAction('{action}', {json_payload});"
        self.evaluate_javascript(js_code)
