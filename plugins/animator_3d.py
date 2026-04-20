# -*- coding: utf-8 -*-
# Project: Environmental Audit GIS
# Module: plugins/animator_3d.py
# NEW_FEATURE: 時間軸與軌跡動畫狀態控制器

class Animator3D:
    def __init__(self):
        """
        動畫控制器：管理圖台上 3D 車輛演示的狀態機。
        這將與 Kivy 的 Clock schedule 以及 WebView 的 JavaScript 溝通。
        """
        self.is_playing = False
        self.current_index = 0
        self.total_frames = 0
        self.playback_speed = 1.0 # 播放倍速
        self.exploration_mode = True # 預設為探索模式 (會自動暫停並彈出資訊卡)

    def load_trajectory(self, total_points: int):
        """載入軌跡總長度並重置狀態"""
        self.total_frames = total_points
        self.current_index = 0
        self.is_playing = False

    def toggle_play_pause(self) -> bool:
        """切換播放與暫停。回傳當前是否為播放狀態"""
        if self.current_index >= self.total_frames - 1:
            # 若已到終點則重頭開始
            self.current_index = 0
            
        self.is_playing = not self.is_playing
        return self.is_playing

    def step_forward(self) -> int:
        """單步前進 (下一步)"""
        self.is_playing = False
        if self.current_index < self.total_frames - 1:
            self.current_index += 1
        return self.current_index

    def step_backward(self) -> int:
        """單步後退 (上一步)"""
        self.is_playing = False
        if self.current_index > 0:
            self.current_index -= 1
        return self.current_index

    def set_speed(self, speed_multiplier: float):
        """調整播放速度"""
        self.playback_speed = max(0.5, min(speed_multiplier, 5.0))

    def toggle_exploration_mode(self) -> bool:
        """切換探索模式 (漸進顯示) 或 一鍵全顯模式"""
        self.exploration_mode = not self.exploration_mode
        return self.exploration_mode

    def advance_frame(self) -> int:
        """
        給 Kivy 定時器 (Clock) 呼叫用的前進邏輯。
        回傳下一個 index。若到達終點則回傳 -1 表示停止。
        """
        if not self.is_playing:
            return self.current_index
            
        if self.current_index < self.total_frames - 1:
            self.current_index += 1
            return self.current_index
        else:
            self.is_playing = False
            return -1
            
    def get_progress_percentage(self) -> float:
        """取得播放進度百分比 (供 UI 進度條使用)"""
        if self.total_frames <= 1:
            return 0.0
        return (self.current_index / (self.total_frames - 1)) * 100.0