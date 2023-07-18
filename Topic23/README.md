## ADB (Android Debug shell)

```
adb devices # list connected devices
# adb connect IP:port
adb shell
adb install "" # install apk
adb shell pm list packages

```




### PULL APP FROM PHONE

Determine the package name of the app

```
adb shell pm list packages
```

Get the full path name of the APK file for the desired package.

```
adb shell pm path com.example.someapp
```

Pull the APK file from the Android device to the development box.

```
adb pull /data/app/com.example.someapp-2.apk
```
