[app]

# (str) Title of your application
title = 環保稽查GIS圖台

# (str) Package name
package.name = gisaudit

# (str) Package domain (needed for android/ios packaging)
package.domain = org.epa.audit

# (str) Source code where the main.py live
source.dir = .

# (list) 包含所有地圖資源與副檔名
source.include_exts = py,png,jpg,kv,atlas,ttf,html,js,css,json,kml

# (str) Application versioning
version = 1.0

# (list) 🌟 輕量化核心套件 (已徹底移除 pandas, numpy, lxml, fastkml 這些會導致編譯失敗的重型套件)
requirements = python3,kivy,kivymd,requests,pyjnius

# (list) 平板應用程式，固定為橫向
orientation = landscape

# (list) 開放定位、網路與檔案讀寫權限
android.permissions = ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Android API 級別
android.api = 31
android.minapi = 21

# (bool) 自動接受 SDK 授權
android.accept_sdk_license = True

# (bool) 啟用 AndroidX 支援 (KivyMD 必備)
android.enable_androidx = True

# (list) 支援的架構 (目前主流平板皆為 64位元)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log 等級 (2 代表詳細偵錯訊息)
log_level = 2

# (int) 若以 root 執行顯示警告
warn_on_root = 1
