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
            
            kivy_x = int(self.x)
            kivy_y = int(self.y)
            kivy_w = int(self.width)
            kivy_h = int(self.height)

            @run_on_ui_thread
            def update_params():
                try:
                    activity = autoclass('org.kivy.android.PythonActivity').mActivity
                    window = activity.getWindow().getDecorView()
                    win_height = window.getHeight()
                    
                    android_y = int(win_height - (kivy_y + kivy_h))
                    
                    # 【根本解法 1】：放棄 LayoutParams 邊距，改用系統底層絕對座標
                    # 這完全避開了 Kivy 與 Android 佈局類別不合導致的 ClassCastException 秒退
                    self.webview.setX(float(kivy_x))
                    self.webview.setY(float(android_y))
                    
                    # 僅單純更新寬高
                    params = self.webview.getLayoutParams()
                    if params:
                        params.width = kivy_w
                        params.height = kivy_h
                        self.webview.setLayoutParams(params)
                        
                except Exception as e:
                    print(f"Geometry Update Error: {e}")
            
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
                settings = self.webview.getSettings()
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True)
                
                # 【根本解法 2】：暴力解鎖 Android 11+ 的 WebView 跨網域與本地讀取限制
                settings.setAllowFileAccess(True)
                settings.setAllowFileAccessFromFileURLs(True)
                settings.setAllowUniversalAccessFromFileURLs(True)
                
                self.webview.setWebViewClient(WebViewClient())
                
                # 用最基礎的 0,0 大小初始化，等 Kivy 計算好位置後再放大，避免畫面閃爍崩潰
                LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
                activity.addContentView(self.webview, LayoutParams(0, 0))
                
                file_url = f"file://{self.html_path}"
                self.webview.loadUrl(file_url)
                
                self._update_native_view_geometry()
            except Exception as e:
                print(f"WebView Creation Error: {e}")

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
