# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: ui/file_control.py
# BUG_FIX: 移除無效的 color 屬性，改用深色背景容器凸顯白色文字

import os
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.dialog import MDDialog
from kivy.graphics import Color, Rectangle # 新增繪圖模組

class FileControlScreen(MDScreen):
    def __init__(self, db_manager, kml_parser, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager
        self.parser = kml_parser
        self.dialog = None
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 標題 (黑色)
        title = MDLabel(
            text="KML 軌跡與停頓點批次匯入中心", 
            font_style="H5", 
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None, 
            height=60
        )
        layout.add_widget(title)
        
        # 建立一個有深色背景的容器來放置 FileChooser (用來襯托預設的白色文字)
        fc_container = MDBoxLayout(orientation='vertical')
        with fc_container.canvas.before:
            Color(0.2, 0.2, 0.2, 1) # 深灰色背景
            self.bg_rect = Rectangle(size=fc_container.size, pos=fc_container.pos)
        fc_container.bind(size=self._update_rect, pos=self._update_rect)
        
        start_path = "/sdcard/Download" if 'ANDROID_ARGUMENT' in os.environ else os.getcwd()
        
        # 檔案選取器 (移除了錯誤的 color 屬性)
        self.file_chooser = FileChooserListView(
            path=start_path,
            filters=['*.kml', '*.KML']
        )
        fc_container.add_widget(self.file_chooser)
        layout.add_widget(fc_container)
        
        # 下方按鈕區
        btn_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        import_btn = MDRaisedButton(
            text="匯入所選 KML",
            on_release=self.process_import
        )
        
        back_btn = MDRaisedButton(
            text="返回圖台",
            md_bg_color=(0.5, 0.5, 0.5, 1),
            on_release=self.go_back
        )
        
        btn_layout.add_widget(import_btn)
        btn_layout.add_widget(back_btn)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        """動態更新背景色塊的大小"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def process_import(self, instance):
        selection = self.file_chooser.selection
        if not selection:
            self.show_dialog("提示", "請先選擇至少一個 KML 檔案！")
            return
            
        success_count = 0
        for filepath in selection:
            filename = os.path.basename(filepath)
            vehicle_id = filename.split('_')[0] if '_' in filename else "未知車輛"
            if self.parser.process_file(filepath, vehicle_id):
                success_count += 1
                
        self.show_dialog("匯入完成", f"成功處理 {success_count} 個 KML 檔案。\n現在可以返回圖台進行演示。")

    def show_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(text="確定", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

    def go_back(self, instance):
        self.manager.current = 'dashboard'