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

## Dynamic Analysis Using Frida

Modify or observe the behaviour of an application during runtime.



Install frida-client on your PC with

```
pip install frida-tools

```

Install Frida Server on mobile based on the architechture of the mobile device 


download server release here > "https://github.com/frida/frida/releases"


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




https://github.com/DERE-ad2001/Frida-Labs/blob/main/Frida%200xA/Solution/Solution.md
