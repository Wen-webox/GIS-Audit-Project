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
        
        # 繪製 Kivy 背景
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
            
            window = autoclass('org.kivy.android.PythonActivity').mActivity.getWindow().getDecorView()
            win_height = window.getHeight()
            
            x = int(self.x)
            y = int(win_height - (self.y + self.height))
            w = int(self.width)
            h = int(self.height)

            @run_on_ui_thread
            def update_params():
                LayoutParams = autoclass('android.widget.FrameLayout$LayoutParams')
                params = LayoutParams(w, h)
                params.leftMargin = x
                params.topMargin = y
                self.webview.setLayoutParams(params)
                # 【關鍵修改 1】：每次更新尺寸時，強制把地圖提到最上層，避免被 Kivy 蓋住
                self.webview.bringToFront()
            
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

        @run_on_ui_thread
        def create_webview():
            self.webview = WebView(activity)
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.getSettings().setDomStorageEnabled(True)
            self.webview.getSettings().setAllowFileAccess(True)
            self.webview.setWebViewClient(WebViewClient())
            
            file_url = f"file://{self.html_path}"
            self.webview.loadUrl(file_url)
            
            parent = activity.findViewById(16908290)
            parent.addView(self.webview)
            
            # 【關鍵修改 2】：剛建立好地圖時，強制提到最上層
            self.webview.bringToFront()
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
