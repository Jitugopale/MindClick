[app]

# (str) Title of your application
title = MindClick

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,mp3,mp4

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow==10.0.1,pyttsx3==2.71,pygame==2.5.2

# (str) Application versioning
version = 0.1

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (list) The Android archs to build for
android.archs = armeabi-v7a, arm64-v8a

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Target Android API, should be as high as possible.
android.api = 31

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# (list) Java classes to add as activities to the manifest.
# android.add_activities = com.example.ExampleActivity

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
android.wakelock = False

# (list) Android application meta-data to set (key=value format)
# android.meta_data =

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

# Python for android (p4a) specific
p4a.branch = master

# (bool) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
