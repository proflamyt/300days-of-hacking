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

## Dynamic Analysis

 ### Frida
 
 list all the installed applications in the device along with their process 
 
 ```
 frida-ps -Uai
 ```
 
 connect to application on device on default port 
 
 ```
 frida -U -f application -l script_to_run
 
 frida -H IP:Port # custom IP and Port
 ```
 
 
 ### TODO
