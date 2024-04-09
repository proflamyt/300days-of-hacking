# Tracking Mobile Phone From Personal Laptop

### Building Mobile Application


# permissions 

permission to get user accurate location.
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />

```

permission to access the user’s location while the app is running in the background

```xml
<uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />
```


to enable persistence i.e start app after boot

```xml
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
```


Shared Preferences

One of the ways android allows you to save app data is through shared preference, its a key value pair storage that is usually used to store user-specified configuration details, such as settings. In our own case we will be storing the Ip and port supplied by user , so that upon restart they wont have to input this over again
