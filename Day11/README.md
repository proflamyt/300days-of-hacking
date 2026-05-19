---
title: "Tracking Mobile Phone From Personal Laptop"
topic: "tracking-mobile-phone"
tags: [android, mobile, location, gps, tracking, java, permissions]
difficulty: intermediate
day: 11
layout: default
parent: Topics
nav_order: 11
---

# Tracking Mobile Phone From Personal Laptop

## What You Will Learn
- How Android location permissions work
- How to build a simple Android app that reports its GPS location
- How to receive that location on a laptop over a network
- Why understanding this is important for mobile security assessments

## What Is It?

This is a hands-on project: build a simple Android application that tracks GPS location and sends coordinates to a laptop on the same network. This simulates what spyware and stalkerware do — understanding how it works helps you identify and protect against it.

## Why It Matters

Mobile tracking is used in parental controls, fleet management, and — maliciously — in stalkerware. As a security professional, you need to understand:

- What permissions a malicious app would request
- How location data is transmitted
- How to detect such apps on a device

## Key Concepts

### Android Permissions

Android requires apps to explicitly declare the permissions they need in `AndroidManifest.xml`. Location is a **dangerous permission** — the user must grant it at runtime.

## Hands-On

### Building the Android Application

#### Required Permissions

Permission to get the user's precise GPS location:

```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

Permission to access the user's location while the app is running in the background:

```xml
<uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />
```

To enable persistence — start the app after device reboot:

```xml
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
```

Permission to access the internet (needed to send location data to your laptop):

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### Storing Server Configuration (Shared Preferences)

One of the ways Android allows you to save app data is through **Shared Preferences** — a key-value pair storage that is usually used to store user-specified configuration details such as settings. In our case, we store the IP and port supplied by the user so that upon restart they won't have to input them again.

```java
SharedPreferences prefs = getSharedPreferences("config", MODE_PRIVATE);
SharedPreferences.Editor editor = prefs.edit();
editor.putString("server_ip", ipAddress);
editor.putInt("server_port", port);
editor.apply();
```

### Reading Location Using FusedLocationProviderClient

```java
FusedLocationProviderClient fusedClient =
    LocationServices.getFusedLocationProviderClient(this);

fusedClient.getLastLocation().addOnSuccessListener(location -> {
    if (location != null) {
        double lat = location.getLatitude();
        double lon = location.getLongitude();
        sendToServer(lat, lon);
    }
});
```

### Receiving on Laptop (Python)

On your laptop, run a simple TCP listener to receive coordinates:

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen(1)
print("[*] Listening for connections...")

conn, addr = server.accept()
print(f"[*] Connection from {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"[Location] {data.decode()}")

conn.close()
```

## Security Implications

Real-world stalkerware often:
- Hides its icon after installation
- Requests `RECEIVE_BOOT_COMPLETED` to survive reboots
- Uses background services to continuously report location
- Requests `ACCESS_BACKGROUND_LOCATION` to track even when the screen is off

### How to Detect Tracking Apps on Android

1. Go to **Settings → Apps** and look for apps without icons or names.
2. Check **Settings → Privacy → Permission Manager → Location** to see which apps have location access.
3. Review **Settings → Battery → Battery Usage** — background tracking apps consume unusual battery.

## Resources

- [Android Location Documentation](https://developer.android.com/training/location)
- [Android Permissions Guide](https://developer.android.com/guide/topics/permissions/overview)
- [TryHackMe — Android Hacking](https://tryhackme.com/module/android-hacking)
