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
        self._update_event = None  # 防抖動計時器
        
        # 繪製 Kivy 背景
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
        # 綁定尺寸變更，但觸發的是「防抖動」機制，而非直接呼叫 Android
        self.bind(size=self._trigger_update, pos=self._trigger_update)

        if platform == 'android':
            # 【根本解法 1】：延遲 1.5 秒初始化。等 Kivy 畫面完全排版完、平靜下來後再叫出 WebView，避開開機風暴
            Clock.schedule_once(lambda dt: self._init_android_webview(), 1.5)
        else:
            self._init_windows_mock()

    def _trigger_update(self, *args):
        """Kivy 尺寸變更時觸發 (每秒可能觸發數十次)"""
        self.rect.pos = self.pos
        self.rect.size = self.size
        
        if platform != 'android' or not self.webview:
            return
            
        # 【根本解法 2】：防抖動 (Debounce) 機制
        # 如果 0.2 秒內有新的變更，就取消舊的傳送，只傳送「最後一次」穩定的座標給 Java
        if self._update_event:
            self._update_event.cancel()
        self._update_event = Clock.schedule_once(self._do_update_geometry, 0.2)

    def _do_update_geometry(self, dt):
        """將最終穩定的座標傳送給 Android 原生層"""
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
                
                # 使用 FrameLayout 的 LayoutParams 進行精準的絕對座標定位
                LayoutParams = autoclass('android.widget.FrameLayout$LayoutParams')
                params = LayoutParams(kivy_w, kivy_h)
                params.leftMargin = kivy_x
                params.topMargin = android_y
                
                self.webview.setLayoutParams(params)
            except Exception as e:
                print(f"Geometry Update Error: {e}")
        
        update_params()

    def _init_windows_mock(self):
        self.mock_label = Label(text="[Windows 模擬模式]\n地圖區域將在此渲染", color=(1,1,1,1))
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
                
                # 【根本解法 3】：使用 FrameLayout 作為安全容器
                FrameLayout = autoclass('android.widget.FrameLayout')
                ViewGroupParams = autoclass('android.view.ViewGroup$LayoutParams')
                
                self.webview = WebView(activity)
                settings = self.webview.getSettings()
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True)
                settings.setAllowFileAccess(True)
                settings.setAllowFileAccessFromFileURLs(True)
                settings.setAllowUniversalAccessFromFileURLs(True)
                
                self.webview.setWebViewClient(WebViewClient())
                
                # 建立透明的安全容器
                layout = FrameLayout(activity)
                layout.addView(self.webview)
                
                # 將容器蓋在 Kivy 畫面上
                activity.addContentView(layout, ViewGroupParams(ViewGroupParams.MATCH_PARENT, ViewGroupParams.MATCH_PARENT))
                
                file_url = f"file://{self.html_path}"
                self.webview.loadUrl(file_url)
                
            except Exception as e:
                print(f"WebView Creation Error: {e}")

        create_webview()
        # 初始化後，觸發第一次座標定位
        Clock.schedule_once(lambda dt: self._trigger_update(), 0.5)

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
