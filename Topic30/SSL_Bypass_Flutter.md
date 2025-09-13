# Flutter SSL Pinning Bypass Using Frida

I was pentesting a Flutter application with the goal of intercepting its HTTPS communications. Along the way, I ran into a few roadblocks while trying to intercept the requests. After figuring it out, I decided to put together this write-up to show how I did it. 

### Quick Background On Flutter

Flutter is a software development kit (SDK) by Google, widely known for its cross-platform application development. Its most attractive feature is the ability to create mobile, web, and desktop apps from a single Dart codebase.

Developers can write just one codebase and cross-compile it for multiple platforms. This means a single application code can serve all your users, reducing development costs, speeding up rollouts, and eliminating the overhead of maintaining multiple platform-specific codebases.

Flutter achieves this by combining Dart and C/C++. Dart code is compiled into native ARM or x86 machine code. The framework uses Dart for the UI and C/C++ for the underlying engine. Developers write their UI in Dart, which the engine then executes. On Android, the engine interacts with Java/Kotlin to run the application. Besides the UI, the developer’s business logic is also embedded into the core app.

When you build a Flutter app for Android, your APK/Bundle typically contains 4 major :

1. App Dart Code (your business logic & UI widgets) -> libapp.so
    - Your app’s compiled Dart code
    - Dart code is AOT compiled into native machine code.

2. Flutter Engine compiled into a shared native library (C++ library, shipped with the app) -> libflutter.so .
     - Renders UI using Skia (2D graphics engine).
     - Handles text, animations, gestures, etc.

3. Java/Kotlin Bootstrap -> /classes.dex.
    - extends FlutterActivity
    - load libflutter.so via JNI and point it to libapp.so (release) or snapshots (debug).
    
4. Assets (images, fonts, etc.).

### How flutter runs your code

To simply put, when you start a Flutter app on Android, the system first launches a small Java `MainActivity`. This activity loads `libflutter.so` (the Flutter engine) via JNI. The engine then loads your Dart code (libapp.so in release or snapshot blobs in debug), runs its main() function, and executes your Dart instructions inside its runtime. Using the Skia graphics engine, it draws the UI onto a surface that Android simply displays

<img width="807" height="183" alt="image" src="https://github.com/user-attachments/assets/501024a9-8085-482c-8c78-2e8dc2f68fcb" />

### Intercepting HTTPS requests in android

Android applications use the system CA store by default, unless the app explicitly specifies otherwise. When I test Android applications, I usually combine dynamic and static analysis to get a complete picture during a pentest.

As always i set up my rooted emulator, configure the system CA to include my Burp certificate, and install the target mobile app. However, I noticed that the app ignored my proxy settings and continued sending and receiving HTTPS requests.

My next step was to use a VPN ( [Rethink](https://github.com/celzero/rethink-app]) ) to route the app’s raw TCP traffic through my Burp proxy.

Once I did that, the app started failing all its HTTP requests, suggesting my proxy the interception now works. Checking the error logs, I saw connection failures caused by certificate errors. This pointed to SSL pinning: the app was validating the server’s certificate itself, and since Burp’s certificate wasn’t in its trusted list, the connection was refused.

At this point, I had three possible approaches:

1. Decompile the app, inject the Burp certificate, and recompile.

2. Decompile the app, modify the function handling certificate validation, and recompile.

3. Inject code at runtime to manipulate the function handling certificate validation.

Because of the complexity and issues with recompiling the app, I decided to go with solution 3. My next step was to find the function handling the certificate check and make it accept my proxy—all while the app was running.

### Looking For the culprit function

While researching online, I found out that Flutter apps use Google’s BoringSSL library for TLS connections. More importantly, they rely on the [`SSL_verify_cert_chain`](https://github.com/google/boringssl/blob/main/ssl/ssl_x509.cc#L201) function for verifying the SSL certificate chain.


```
Flutter Dart code
       |
       v
HttpClient -> Flutter Engine (C/C++)
       |
       v
BoringSSL TLS handshake
       |
       +---> Receives server certificate chain
       |
       +---> session_verify_cert_chain()
                |
                +---> Build X509_STORE_CTX
                |       - Peer chain (leaf + intermediates)
                |       - Trust store = Android system CA / Custom trust Store
                |
                +---> Verify chain to a trusted root CA
                |
                +---> Check hostname, constraints, expiry
                |
                +---> Set session->verify_result
       |
       +---> TLS handshake continues or aborts
       |
       v
Flutter Dart code receives result

