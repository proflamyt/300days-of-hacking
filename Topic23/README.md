---
title: "Android Debug Shell (ADB)"
topic: "android-debug-shell"
tags: [adb, android, debugging, mobile, apk, logcat]
difficulty: intermediate
day: 23
layout: default
parent: Topics
nav_order: 23
---

# Android Debug Shell (ADB)

## What You Will Learn
- What ADB is and how to use it to interact with Android devices
- How to install, pull, and inspect APKs using ADB
- How to view logs from a running application
- How to merge and sign split APKs

## What Is It?

**ADB (Android Debug Bridge)** is a command-line tool that lets you communicate with a connected Android device. It is part of the Android SDK and is essential for Android security research and mobile penetration testing.

ADB allows you to:
- Install and remove apps
- Run shell commands on the device
- Transfer files to and from the device
- View application logs
- Pull APKs for static analysis

## Hands-On

### Basic ADB Commands

```bash
adb devices             # list connected devices
adb connect <IP>:<port> # connect to a device over Wi-Fi
adb shell               # open an interactive shell on the device
adb install <path.apk>  # install an APK on the device
adb shell pm list packages              # list all installed packages
adb shell pm list packages -3           # list only third-party packages
```

### Inspect an App's Package

```bash
# Get detailed information about a package (permissions, activities)
adb shell dumpsys package <package_name>

# Start an activity
adb shell am start <package_name>/<activity_name>
```

### Pull an APK from the Device

Determine the package name of the app:

```bash
adb shell pm list packages
```

List only third-party packages:

```bash
adb shell pm list packages -3
```

Get the full path of the APK file:

```bash
adb shell pm path com.example.someapp
```

Pull the APK file from the device to your machine:

```bash
adb pull /data/app/com.example.someapp-2.apk
```

### View Application Logs

```bash
adb logcat "MainActivity:V *:S" -v brief
```

This filters logcat output to only show verbose logs from `MainActivity` and silences everything else.

### Merge Split APKs

Modern apps are often distributed as split APKs (multiple `.apk` files). To merge them into a single APK:

```bash
java -jar APKEditor-1.4.5.jar m -i <directory>
```

### Re-sign an APK

After modifying an APK, it must be re-signed before installation:

```bash
java -jar uber-apk-signer-1.2.1.jar --allowResign -a <modified.apk>
```

## Resources

- [Official ADB Documentation](https://developer.android.com/studio/command-line/adb)
- [APKEditor GitHub](https://github.com/REAndroid/APKEditor)
- [uber-apk-signer GitHub](https://github.com/patrickfav/uber-apk-signer)
- [TryHackMe — Android Hacking](https://tryhackme.com/module/android-hacking)
