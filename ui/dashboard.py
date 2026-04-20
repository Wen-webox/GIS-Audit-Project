# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: ui/dashboard.py
# NEW_FEATURE: 稽查人員主儀表板 (包含下拉防呆選單、播放控制列與地圖)

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
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager
        self.animator = Animator3D()
        
        # 建立主佈局
        self.layout = MDBoxLayout(orientation='vertical')
        
        # 1. 頂部導航列
        self.toolbar = MDTopAppBar(
            title="環保稽查 GIS 戰情圖台", 
            elevation=4,
            right_action_items=[
                ["folder-open", lambda x: self.go_to_file_control(), "匯入 KML 資料"],
                ["compass", lambda x: self.toggle_exploration(), "切換探索模式"]
            ]
        )
        self.layout.add_widget(self.toolbar)
        
        # 2. 防呆資料過濾列 (車號與日期)
        filter_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=10, spacing=10)
        
        # 車號選擇下拉選單
        self.vehicle_btn = MDRaisedButton(text="選擇車號", on_release=self.open_vehicle_menu)
        filter_layout.add_widget(self.vehicle_btn)
        
        # 日期選擇下拉選單
        self.date_btn = MDRaisedButton(text="選擇日期", on_release=self.open_date_menu)
        self.date_btn.disabled = True # 防呆：未選車號前鎖定
        filter_layout.add_widget(self.date_btn)
        
        self.load_data_btn = MDIconButton(icon="magnify", on_release=self.load_gis_data)
        filter_layout.add_widget(self.load_data_btn)
        
        self.layout.add_widget(filter_layout)
        
        # 3. WebView 地圖圖層
        self.map_view = MapWebView()
        self.layout.add_widget(self.map_view)
        
        # 4. 底部播放控制列
        control_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=70, padding=10, spacing=20)
        
        self.btn_prev = MDIconButton(icon="step-backward", on_release=lambda x: self.map_view.trigger_action('step_backward'))
        self.btn_play = MDIconButton(icon="play", icon_size="48sp", on_release=self.toggle_play)
        self.btn_next = MDIconButton(icon="step-forward", on_release=lambda x: self.map_view.trigger_action('step_forward'))
        self.btn_full = MDRaisedButton(text="一鍵全顯", on_release=lambda x: self.map_view.trigger_action('show_all'))
        
        # 置中對齊小技巧
        control_layout.add_widget(MDBoxLayout()) 
        control_layout.add_widget(self.btn_prev)
        control_layout.add_widget(self.btn_play)
        control_layout.add_widget(self.btn_next)
        control_layout.add_widget(self.btn_full)
        control_layout.add_widget(MDBoxLayout())
        
        self.layout.add_widget(control_layout)
        self.add_widget(self.layout)
        
        # 初始化選單變數
        self.vehicle_menu = None
        self.date_menu = None
        self.selected_vehicle = None
        self.selected_date = None

    def go_to_file_control(self):
        self.manager.current = 'file_control'

    def toggle_exploration(self):
        is_explore = self.animator.toggle_exploration_mode()
        status = "開啟" if is_explore else "關閉"
        print(f"探索模式已{status}")
        self.map_view.trigger_action('set_exploration_mode', {"enabled": is_explore})

    def open_vehicle_menu(self, instance):
        vehicles = self.db.get_available_vehicles()
        if not vehicles:
            vehicles = ["無資料，請先匯入"]
            
        menu_items = [
            {"text": v, "viewclass": "OneLineListItem", "on_release": lambda x=v: self.set_vehicle(x)}
            for v in vehicles
        ]
        self.vehicle_menu = MDDropdownMenu(caller=self.vehicle_btn, items=menu_items, width_mult=4)
        self.vehicle_menu.open()

    def set_vehicle(self, vehicle_id):
        self.selected_vehicle = vehicle_id
        self.vehicle_btn.text = vehicle_id
        self.vehicle_menu.dismiss()
        
        # 防呆機制連動：解鎖並更新日期清單
        if vehicle_id != "無資料，請先匯入":
            self.date_btn.disabled = False
            self.date_btn.text = "選擇日期"
            self.selected_date = None

    def open_date_menu(self, instance):
        if not self.selected_vehicle: return
        dates = self.db.get_available_dates_for_vehicle(self.selected_vehicle)
        
        menu_items = [
            {"text": d, "viewclass": "OneLineListItem", "on_release": lambda x=d: self.set_date(x)}
            for d in dates
        ]
        self.date_menu = MDDropdownMenu(caller=self.date_btn, items=menu_items, width_mult=4)
        self.date_menu.open()

    def set_date(self, date_str):
        self.selected_date = date_str
        self.date_btn.text = date_str
        self.date_menu.dismiss()

    def load_gis_data(self, instance):
        if not self.selected_vehicle or not self.selected_date:
            print("請先選擇車號與日期")
            return
            
        # 1. 查詢 SQLite 拿取隔離好的乾淨資料
        gis_data = self.db.fetch_gis_data(self.selected_vehicle, self.selected_date)
        
        # 2. 重置動畫狀態
        self.animator.load_trajectory(len(gis_data['tracks']))
        self.btn_play.icon = "play"
        
        # 3. 傳送到 WebView 的 JS 引擎進行渲染
        self.map_view.update_gis_data(gis_data)

    def toggle_play(self, instance):
        is_playing = self.animator.toggle_play_pause()
        self.btn_play.icon = "pause" if is_playing else "play"
        self.map_view.trigger_action('toggle_play', {"is_playing": is_playing})


# ----------------------------------------------------
# Kivy 應用程式實作 (GISAuditApp)
# ----------------------------------------------------
class GISAuditApp(MDApp):
    def __init__(self, db_manager, kml_parser, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager
        self.parser = kml_parser

    def build(self):
        # --- 【新增】解決中文亂碼/豆腐塊問題 ---
        # 暴力且最有效的解法：直接覆寫 Kivy 預設的 Roboto 字型
        
        # 判斷當前環境，給予對應的中文字型路徑
        if platform == 'win':
            # Windows 環境：直接吃系統內建的微軟正黑體
            font_path = "C:\\Windows\\Fonts\\msjh.ttc" 
        else:
            # Android 環境：未來打包成 APK 時，需要讀取專案內的字型檔
            # (稍後請在專案建立 assets/fonts 資料夾，放入 NotoSansTC.ttf)
            font_path = os.path.join(os.getcwd(), "assets", "fonts", "NotoSansTC-Regular.ttf")

        if os.path.exists(font_path):
            LabelBase.register(name="Roboto", fn_regular=font_path)
            # 若有粗體需求可加註：fn_bold=font_path
        else:
            print(f"⚠️ 找不到中文字型檔: {font_path}，介面將維持預設字型。")
        # ------------------------------------------

        self.theme_cls.primary_palette = "Teal" # 環保主題色
        self.theme_cls.theme_style = "Light"
        
        sm = ScreenManager()
        
        dashboard = DashboardScreen(name='dashboard', db_manager=self.db)
        file_control = FileControlScreen(name='file_control', db_manager=self.db, kml_parser=self.parser)
        
        sm.add_widget(dashboard)
        sm.add_widget(file_control)
        
        return sm