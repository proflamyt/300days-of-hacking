# Android Hacking

## Terms
**activities**: each screen is an activity

**resources** : any other that is not java code

**layout**: how a view should look, xml 

**Intent**: represent a way for one activity to another, what activity 

**AndroidManifest.xml** : configuration file that android can use to launch the file

**Broadcast and Receivers**:

**Services**: Backgroud Application


 **Content Providers**: Allows apps to share data and resources
 

 **META-INF/** : Android Certificates folder
 
 **assets/** : Stores images, icons, 
 
 **lib/**: Native libraries for the application



## Static Analysis

 ### TODO

### Understanding Dalvik,  ### TODO

The Java Code is compiled to dalvik bytecode by android runtime.

### Smali

Smali is the human readable version of dalvik bytecode , smali is like assembly language and dalvik just bytes


### Entrypoint of android (Launcher activity) 
the launcher activity is the first activity upon launch of an android app. 
Check the androidmanifest, the launcher activity will have the main and Launcher intent

### using jd-gui  ### TODO



# ADB

List Devices 

```
adb devices
```

Connect to a device 

```
adb connect devices
```
Install app

```
adb install apk

```

Upload to /data/local/tmp/ 

```
adb push something /data/local/tmp/ 
```

Run shell command

```
adb shell

adb shell getprop ro.product.cpu.abi # get device architecture
```
## Frida and Objection

Inject Frida into APK 

```
objection patchapk -s <apk>
```

Start Application and drop into frida shell

```
frida -U <appname>
```

### Uploading and running Frida Server on android

get architechture

```
adb shell getprop ro.product.cpu.abi
```

get release https://github.com/frida/frida/releases

```
adb push frida-server* /data/local/tmp
```

## Network Interception 


Android 14

```
# Create a separate temp directory, to hold the current certificates
# Otherwise, when we add the mount we can't read the current certs anymore.
mkdir -p -m 700 /data/local/tmp/tmp-ca-copy

# Copy out the existing certificates
cp /apex/com.android.conscrypt/cacerts/* /data/local/tmp/tmp-ca-copy/

# Create the in-memory mount on top of the system certs folder
mount -t tmpfs tmpfs /system/etc/security/cacerts

# Copy the existing certs back into the tmpfs, so we keep trusting them
mv /data/local/tmp/tmp-ca-copy/* /system/etc/security/cacerts/

# Copy our new cert in, so we trust that too
cp /data/misc/user/0/cacerts-added/* /system/etc/security/cacerts/

# Update the perms & selinux context labels
chown root:root /system/etc/security/cacerts/*
chmod 644 /system/etc/security/cacerts/*
chcon u:object_r:system_file:s0 /system/etc/security/cacerts/*

# Deal with the APEX overrides, which need injecting into each namespace:

# First we get the Zygote process(es), which launch each app
ZYGOTE_PID=$(pidof zygote || true)
ZYGOTE64_PID=$(pidof zygote64 || true)
# N.b. some devices appear to have both!

# Apps inherit the Zygote's mounts at startup, so we inject here to ensure
# all newly started apps will see these certs straight away:
for Z_PID in "$ZYGOTE_PID" "$ZYGOTE64_PID"; do
    if [ -n "$Z_PID" ]; then
        nsenter --mount=/proc/$Z_PID/ns/mnt -- \
            /bin/mount --bind /system/etc/security/cacerts /apex/com.android.conscrypt/cacerts
    fi
done

# Then we inject the mount into all already running apps, so they
# too see these CA certs immediately:

# Get the PID of every process whose parent is one of the Zygotes:
APP_PIDS=$(
    echo "$ZYGOTE_PID $ZYGOTE64_PID" | \
    xargs -n1 ps -o 'PID' -P | \
    grep -v PID
)

# Inject into the mount namespace of each of those apps:
for PID in $APP_PIDS; do
    nsenter --mount=/proc/$PID/ns/mnt -- \
        /bin/mount --bind /system/etc/security/cacerts /apex/com.android.conscrypt/cacerts &
done
wait # Launched in parallel - wait for completion here

echo "System certificate injected"
```

## Dynamic Analysis Using Frida

Modify or observe the behaviour of an application during runtime.



Install frida-client on your PC with

```
pip install frida-tools

```

Install Frida Server on mobile based on the architechture of the mobile device 


download server release here > "https://github.com/frida/frida/releases"

 ### Frida Trace
 trace function calls in application
 ```
frida-trace -U -j '<lassname>.*!*' <Application>
 ```

 ### Frida
 
 list all the installed applications in the device along with their process ID and identifier.
 
 ```
 frida-ps -Uai
 ```

attach frida to application by specifying the identifier

 ```
 frida -U -f  <application identifier>
 ```
 
 connect to application on device on default port 
 
 ```
 frida -U -f application -l script_to_run
 
 frida -H IP:Port # custom IP and Port
 ```
 
 
 ### FRIDA SCRIPTS

Javascript codes to change behavior of methods in runtime 
 ```js

Java.perform(function (){

// implementations here ..

})
 ```
 Enumerate Package Names 

 ```js
  Java.enumerateMethods('*!*')
 ```


change function implementation

```js
<classname>.<function>.implementation = function(){
    
}

```

overload function 

```js
<classname>.<function>.overload('int', 'int').implementation = function(a,b){ 
}
```


access value 

```js
<classname>.<function>.value 
```


```js

Java.performNow(function(){

Java.choose('com.<classname>.<function>.MainActivity', {

  onMatch: function(instance) {
   console.log("Instance found");
  },
  onComplete: function() {}

});

});

```


To hook native functions, we can use the Interceptor API. Now, let's see the template for this.

```js
Interceptor.attach(targetAddress, {
    onEnter: function (args) {
        console.log('Entering ' + functionName);
        // Modify or log arguments if needed
    },
    onLeave: function (retval) {
        console.log('Leaving ' + functionName);
        // Modify or log return value if needed
    }
});


```

Get Target Address

```js
Module.getBaseAddress("libraryname.so");

Module.enumerateExports("libraryname.so");

Module.enumerateImports("libfrida0x8.so");

Module.findExportByName("libc.so", "strcmp");

```

Calling Native function

```js

var native_adr = new NativePointer(<address_of_the_native_function>);
const native_function = new NativeFunction(native_adr, '<return type>', ['argument_data_type']);
native_function(<arguments>);
```




### Sending Intents 

```java
Intent intent1 = new Intent();
intent1.setClassName("<packagename>", "<pathname>");
intent1.setAction("<action>");
intent3.putExtra("reason", "next");
intent2.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_CLEAR_TOP);
intent.setData(Uri.parse("<url>"));
startActivity(intent1);

```


### Intent Filters 

Intent filters serve important role in the resolution of implicit intents by the android os .


### Broadcast Receiver

check AndroidManifest.xml  for tag

```
<receiver>
```

The other way is by dynamically registering a receiver class using 

```
registerReceiver().
```

#### AppWidgets

check 

```
 AppWidgetProvider 
```


https://github.com/DERE-ad2001/Frida-Labs/blob/main/Frida%200xA/Solution/Solution.md
