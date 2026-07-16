---
title: "Android Hacking"
topic: "android-hacking"
tags: [android, frida, adb, mobile-security, static-analysis, dynamic-analysis, apk]
difficulty: intermediate
day: 30
layout: default
parent: Topics
nav_order: 30
---

# Android Hacking

## What You Will Learn
- The key components of an Android app and what they do
- How to perform static analysis on an APK
- How to use Frida for dynamic instrumentation and runtime hooking
- How to intercept network traffic from Android apps
- How to install and manage CA certificates for HTTPS interception

## Terms

| Term | Description |
|------|-------------|
| **Activity** | Each screen in an Android app is an Activity. |
| **Resources** | Anything that is not Java code (layouts, images, strings). |
| **Layout** | Defines how a view should look — written in XML. |
| **Intent** | A messaging object that represents a request to start an Activity or pass data between components. |
| **AndroidManifest.xml** | The configuration file Android uses to understand and launch the app. Declares all components and permissions. |
| **Broadcast Receivers** | Components that respond to system-wide broadcast events. |
| **Services** | Background operations that run without a user interface. |
| **Content Providers** | Allow apps to share data and resources with other apps. |
| **META-INF/** | Folder containing Android certificate and signing information. |
| **assets/** | Stores images, icons, and other raw files. |
| **lib/** | Native libraries (`.so` files) for the application. |

## Static Analysis

Static analysis examines an APK without running it. The goal is to understand the app's structure, identify hardcoded secrets, and find potentially vulnerable components.

```bash
# Decompile an APK using apktool (get Smali + resources)
apktool d app.apk -o output_dir

# Decompile to Java using jadx
jadx -d output_dir app.apk

# Or use the jadx GUI
jadx-gui app.apk
```

### Understanding Dalvik Bytecode

Android Java code is compiled to **Dalvik bytecode**, stored in `.dex` files inside the APK. The Android Runtime (ART) executes this bytecode.

### Smali

**Smali** is the human-readable representation of Dalvik bytecode. It looks like assembly language. When you decompile with apktool, you get Smali code that you can modify and recompile.

```smali
.method public onCreate(Landroid/os/Bundle;)V
    .registers 2
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    return-void
.end method
```


### Enumerate other apps (v11+)

```java
<queries>
    <package android:name="com.whatsapp"/>
</queries>
```


```java
PackageManager pm = getPackageManager();

try {
    pm.getPackageInfo("com.whatsapp", 0);
    // App is installed
} catch (PackageManager.NameNotFoundException e) {
    // App is not installed
}
```

### Entry Point (Launcher Activity)

The launcher activity is the first activity launched when an Android app starts. Check `AndroidManifest.xml` — the launcher activity will have:

```xml
<intent-filter>
    <action android:name="android.intent.action.MAIN" />
    <category android:name="android.intent.category.LAUNCHER" />
</intent-filter>
```

## ADB

```bash
adb devices                           # list connected devices
adb connect <IP>:<port>               # connect to device over Wi-Fi
adb install <apk>                     # install APK
adb shell                             # open shell on device
adb shell getprop ro.product.cpu.abi  # get device architecture
adb push something /data/local/tmp/   # upload a file to device
```

## Frida and Objection

**Frida** is a dynamic instrumentation toolkit that lets you inject JavaScript snippets into running processes and hook functions at runtime.

```bash
# Inject Frida into an APK (Objection patches the APK)
objection patchapk -s <apk>

# Start application and drop into Frida shell
frida -U <appname>
```

### Upload and Run Frida Server on Android

```bash
# Get device architecture
adb shell getprop ro.product.cpu.abi

# Download the right Frida server from https://github.com/frida/frida/releases
# Upload it to the device
adb push frida-server* /data/local/tmp

# Make it executable and run it
adb shell chmod +x /data/local/tmp/frida-server
adb shell /data/local/tmp/frida-server &
```

### Frida Commands

```bash
# List all installed applications with PID and identifier
frida-ps -Uai

# Attach to an application by package name
frida -U -f <application.identifier>

# Attach and run a script
frida -U -f <application.identifier> -l script.js

# Connect to a specific IP and port
frida -H <IP>:<Port>

# Trace function calls
frida-trace -U -j '<classname>.*!*' <Application>
```

### Frida Scripts

Frida scripts are JavaScript code that modify the behavior of methods at runtime:

```js
Java.perform(function () {
    // All instrumentation goes here
});
```

**Enumerate methods in a class:**

```js
Java.enumerateMethods('*!*')
```

**Override a function implementation:**

```js
var ClassName = Java.use('com.example.ClassName');
ClassName.methodName.implementation = function () {
    console.log('Method called!');
    return this.methodName();  // call original
};
```

**Overload a function:**

```js
ClassName.methodName.overload('int', 'int').implementation = function (a, b) {
    console.log('Args: ' + a + ', ' + b);
    return this.methodName(a, b);
};
```

**Find instances of a class at runtime:**

```js
Java.performNow(function () {
    Java.choose('com.example.MainActivity', {
        onMatch: function (instance) {
            console.log("Instance found: " + instance);
        },
        onComplete: function () {}
    });
});
```

**Hook a native function:**

```js
Interceptor.attach(Module.findExportByName("libc.so", "strcmp"), {
    onEnter: function (args) {
        console.log('strcmp called with: ' + Memory.readUtf8String(args[0]));
    },
    onLeave: function (retval) {
        console.log('strcmp returned: ' + retval);
    }
});
```

**Get native function addresses:**

```js
Module.getBaseAddress("libraryname.so");
Module.enumerateExports("libraryname.so");
Module.findExportByName("libc.so", "strcmp");
```

## Network Interception

To intercept HTTPS traffic from an Android app, you need to install a custom CA certificate as a system-trusted certificate (required for Android 7+).

### Install Split APK

```bash
adb shell pm path com.app | sed 's/^package://g' | xargs -L1 adb pull
adb install-multiple *.apk
```

### Install CA Certificate (Android 14)

```bash
mkdir -p -m 700 /data/local/tmp/tmp-ca-copy
cp /apex/com.android.conscrypt/cacerts/* /data/local/tmp/tmp-ca-copy/
mount -t tmpfs tmpfs /system/etc/security/cacerts
mv /data/local/tmp/tmp-ca-copy/* /system/etc/security/cacerts/
cp /data/misc/user/0/cacerts-added/* /system/etc/security/cacerts/
chown root:root /system/etc/security/cacerts/*
chmod 644 /system/etc/security/cacerts/*
chcon u:object_r:system_file:s0 /system/etc/security/cacerts/*

ZYGOTE_PID=$(pidof zygote || true)
ZYGOTE64_PID=$(pidof zygote64 || true)

for Z_PID in "$ZYGOTE_PID" "$ZYGOTE64_PID"; do
    if [ -n "$Z_PID" ]; then
        nsenter --mount=/proc/$Z_PID/ns/mnt -- \
            /bin/mount --bind /system/etc/security/cacerts /apex/com.android.conscrypt/cacerts
    fi
done

APP_PIDS=$(echo "$ZYGOTE_PID $ZYGOTE64_PID" | xargs -n1 ps -o 'PID' -P | grep -v PID)

for PID in $APP_PIDS; do
    nsenter --mount=/proc/$PID/ns/mnt -- \
        /bin/mount --bind /system/etc/security/cacerts /apex/com.android.conscrypt/cacerts &
done
wait

echo "System certificate injected"
```

## Dynamic Analysis Using Frida

Dynamic analysis involves modifying or observing the behavior of an application during runtime.

```bash
# Install Frida client on your PC
pip install frida-tools
```

## Sending Intents

```java
Intent intent1 = new Intent();
intent1.setClassName("<packagename>", "<pathname>");
intent1.setAction("<action>");
intent1.putExtra("reason", "next");
intent1.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_CLEAR_TOP);
intent1.setData(Uri.parse("<url>"));
startActivity(intent1);
```

### Intent Filters

Intent filters serve an important role in the resolution of implicit intents by the Android OS.

### Broadcast Receivers

Check `AndroidManifest.xml` for the `<receiver>` tag:

```xml
<receiver android:name=".MyReceiver">
    <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED" />
    </intent-filter>
</receiver>
```

Or dynamically register a receiver class using:

```java
registerReceiver(myReceiver, intentFilter);
```

check 

```
onReceive()
```

## Resources

- [Frida Labs Solutions](https://github.com/DERE-ad2001/Frida-Labs/blob/main/Frida%200xA/Solution/Solution.md)
- [Frida Official Documentation](https://frida.re/docs/)
- [Objection — Runtime Mobile Exploration](https://github.com/sensepost/objection)
- [MobSF — Mobile Security Framework](https://github.com/MobSF/Mobile-Security-Framework-MobSF)
- [TryHackMe — Android Hacking](https://tryhackme.com/module/android-hacking)
