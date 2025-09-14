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

Once I did that, the app started failing all its HTTP requests, suggesting the interception by my proxy now works. Checking the error logs, I saw connection failures caused by certificate errors. This pointed to SSL pinning: the app was validating the server’s certificate itself, and since Burp’s certificate wasn’t in its trusted list, the connection was refused.

At this point, I had three possible approaches:

1. Decompile the app, inject the Burp certificate, and recompile.

2. Decompile the app, modify the function handling certificate validation, and recompile.

3. Inject code at runtime to manipulate the function handling certificate validation.

Because of the complexity and issues with recompiling the app, I decided to go with solution 3. My next step was to find the function handling the certificate check and make it accept my proxy—all while the app was running.

### Looking For the culprit function

While researching online, I found out that Flutter apps use Google’s `BoringSSL` library for TLS connections. More importantly, they rely on the [`SSL_verify_cert_chain`](https://github.com/google/boringssl/blob/main/ssl/ssl_x509.cc#L201) function for verifying the SSL certificate chain.


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

```

This function returns a boolean indicating whether a certificate is valid or not, which makes it a perfect target for bypassing SSL pinning.
```c
static bool ssl_crypto_x509_session_verify_cert_chain(SSL_SESSION *session,
                                                      SSL_HANDSHAKE *hs,
                                                      uint8_t *out_alert)
```

So the next line of action is to hook this function during runtime and make it return true (valid certificate) everytime it is called. Remember the library is compiled in flutter engine (libflutter.so). 

### Decompiler to the rescue

I initially thought it would be as simple as loading libflutter.so into a decompiler and checking the function’s address in the binary. Unfortunately, that approach didn’t work because the binary had been stripped of all symbols.
However, since we have access to the original source code of the SSL library, we can try tracing the function by looking for unique strings used within it. Hopefully, these strings aren’t used in many other functions, which would help us narrow down the exact function in the decompiled library.

<img width="886" height="138" alt="image" src="https://github.com/user-attachments/assets/1735f361-19b4-47a7-a88d-b77f840ce928" />

I found two strings used inside the function in the original source code: "ssl_client" and "ssl_server". Searching for "ssl_client" in the decompiled library showed two functions referencing it.

<img width="732" height="141" alt="image" src="https://github.com/user-attachments/assets/ea469391-7942-409d-94c4-48e61ce80e22" />


Looking at the first one, it only had a single argument and clearly wasn’t handling certificate verification. Our target function, ssl_crypto_x509_session_verify_cert_chain, has three arguments, so I ruled it out.
<img width="618" height="380" alt="image" src="https://github.com/user-attachments/assets/8f2ccef5-c8a5-45fc-ac00-b9f8fc7765f5" />

The second function, however, has three arguments, and after scanning through it, I could see that its structure closely matches our target function.


<img width="685" height="494" alt="image" src="https://github.com/user-attachments/assets/aef524b9-2814-4007-9b16-edf510ff6277" />

Now that we have identified the function in the decompiled binary, our next step was to hook ssl_crypto_x509_session_verify_cert_chain and make it return true every time. However, because of ASLR (Address Space Layout Randomization), we couldn’t just use the address from the binary directly.

To work around this, I copied the first couple of lines from the function’s byte pattern and searched for it in the read-and-executable sections of the application code at runtime.

<img width="1511" height="361" alt="image" src="https://github.com/user-attachments/assets/d3b2d135-95f9-4c5f-8462-946e366bd9ea" />


**FUNCTION BYTE PATTERN**
```
"55 41 57 41 56 41 55 41 54 53 48 83 EC ?? C6 02 ?? 48 8B AF A0"
```

### Frida – Our DynaFriend

My goal was to scan the memory of `libflutter.so` at runtime, look through its `r-x (read-and-executable)` section, and search for the byte pattern I had copied. However, none of the loaded modules showed `libflutter.so`.

```
Process.enumerateModules().forEach(function(m) {
    console.log(m.name + ' | ' + m.base + ' | ' + m.size);
});
```


So, I decided to scan through every **modules’ read-and-executable sections** to look for my function’s byte pattern:

```
ranges = Process.enumerateRanges({protection: 'r-x'})
```

```
ranges.forEach(function(range) {
    console.log('[*] Scanning RX range: ' + range.base + ' - ' + range.base.add(range.size));

    Memory.scan(range.base, range.size, pattern, {
        onMatch: function(address, size) {
            console.log('[+] Found pattern at: ' + address);
            var funcAddress = address;
            var symbol = DebugSymbol.fromAddress(address);
            console.log('    Symbol: ' + symbol.name + ' | Module: ' + symbol.moduleName);
        },
        onError: function(reason) {
            console.log('[-] Scan error: ' + reason);
        },
        onComplete: function() {
            // console.log('Scan complete for this range');
        }
    });
    });
```

<img width="888" height="331" alt="image" src="https://github.com/user-attachments/assets/549a45d2-98f0-4a5c-9d2f-9773ad567241" />

Luckily, I found it! By comparing the last three bytes with the function address we had identified earlier, I could confirm that this is indeed our target function.

The next step is to hook this address and make it return true every time:

```
Interceptor.attach(funcAddress, {
    onEnter: function(args) {
        console.log('[*] Function called');
    },
    onLeave: function(retval) {
        retval.replace(1);
        console.log('[*] Function return forced to TRUE');
    }
});
```


And just like that—voilà! The app’s traffic starts flowing through the proxy.
