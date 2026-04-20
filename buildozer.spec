[app]

# (str) Title of your application
title = 環保稽查GIS圖台

# (str) Package name
package.name = gisaudit

# (str) Package domain (needed for android/ios packaging)
package.domain = org.epa.audit

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
# 🌟 關鍵修改 1：確保所有地圖資源與字型都被打包
source.include_exts = py,png,jpg,kv,atlas,ttf,html,js,css,json,kml

# (str) Application versioning
version = 1.0

# (list) Application requirements
# 🌟 關鍵修改 2：補齊所有 Python 套件依賴
requirements = python3,kivy,kivymd,fastkml,lxml,pandas,requests,pyjnius

# (str) Custom source folders for requirements
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
# 平板應用程式，預設設定為橫向 (landscape) 或全向 (all)
orientation = landscape

# (list) Permissions
# 🌟 關鍵修改 3：開放 GPS 定位、網路與檔案讀寫權限
android.permissions = ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
# android.api = 33

# (int) Minimum API your APK / AAB will support.
# android.minapi = 21

# (str) Android NDK version to use
# android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid network timeouts or system updates
# android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
# android.whitelist =

# (str) Path to a custom whitelist file
# android.whitelist_src =

# (str) Path to a custom blacklist file
# android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes.
# android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
# android.add_src =

# (list) Android AAR archives to add
# android.add_aars =

# (list) Put these files or directories in the apk assets directory.
# android.add_assets =

# (list) Gradle dependencies to add
# android.gradle_dependencies =

# (bool) Enable AndroidX support.
android.enable_androidx = True

# (list) add java compile options
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add
# android.gradle_repositories =

# (list) packaging options to add
# android.packaging_options =

# (list) Java classes to add as activities to the manifest.
# android.add_activities =

# (str) OUYA Console category. Should be one of GAME or APP
# android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
# android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
# android.manifest.intent_filters =

# (list) Copy these files to src/main/res/xml/ (used for example with intent-filters)
# android.res_xml =

# (str) launchMode to set for the main activity
# android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android/*.so
# android.add_libs_armeabi_v7a = libs/android-v7a/*.so
# android.add_libs_arm64_v8a = libs/android-v8a/*.so
# android.add_libs_x86 = libs/android-x86/*.so
# android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# android.wakelock = False

# (list) Android application meta-data to set
# android.meta_data =

# (list) Android library project to add
# android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
# android.uses_library =

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (bool) Android logcat only display log for activity's pid
# android.logcat_pid_only = False

# (str) Android additional adb arguments
# android.adb_args = -H host.docker.internal

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides check that android.ndk == android.ndk_api
# android.ndk_api = 21

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk or aar).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
# android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin