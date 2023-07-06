package com.tkyaji.cordova;

import android.net.Uri;
import android.util.Base64;
import barcodescanner.xservices.p005nl.barcodescanner.BuildConfig;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.regex.Pattern;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import org.apache.cordova.CordovaPlugin;
import org.apache.cordova.CordovaResourceApi;
import org.apache.cordova.LOG;

/* loaded from: classes-dex2jar.jar:com/tkyaji/cordova/DecryptResource.class */
public class DecryptResource extends CordovaPlugin {
    private static final String CRYPT_IV = "lwwO02t2uF0UT65J";
    private static final String CRYPT_KEY = "ErKWC88KOPv7W9ocecm6QHN0yU3R/6z8";
    private static final String TAG = "DecryptResource";
    private static final String[] INCLUDE_FILES = {"\\.(htm|html|js|css)$"};
    private static final String[] EXCLUDE_FILES = new String[0];

    private boolean hasMatch(String str, String[] strArr) {
        for (String str2 : strArr) {
            if (Pattern.compile(str2).matcher(str).find()) {
                return true;
            }
        }
        return false;
    }

    private boolean isCryptFiles(String str) {
        String replace = str.replace("file:///android_asset/www/", BuildConfig.FLAVOR);
        return hasMatch(replace, INCLUDE_FILES) && !hasMatch(replace, EXCLUDE_FILES);
    }

    @Override // org.apache.cordova.CordovaPlugin
    public CordovaResourceApi.OpenForReadResult handleOpenForRead(Uri uri) throws IOException {
        ByteArrayInputStream byteArrayInputStream;
        String str = fromPluginUri(uri).toString().replace("/+++/", "/").split("\\?")[0];
        CordovaResourceApi.OpenForReadResult openForRead = this.webView.getResourceApi().openForRead(Uri.parse(str), true);
        if (isCryptFiles(str)) {
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(openForRead.inputStream));
            StringBuilder sb = new StringBuilder();
            while (true) {
                String readLine = bufferedReader.readLine();
                if (readLine == null) {
                    break;
                }
                sb.append(readLine);
            }
            bufferedReader.close();
            byte[] decode = Base64.decode(sb.toString(), 0);
            LOG.m15d(TAG, "decrypt: " + str);
            try {
                SecretKeySpec secretKeySpec = new SecretKeySpec(CRYPT_KEY.getBytes("UTF-8"), "AES");
                Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
                cipher.init(2, secretKeySpec, new IvParameterSpec(CRYPT_IV.getBytes("UTF-8")));
                ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                byteArrayOutputStream.write(cipher.doFinal(decode));
                byteArrayInputStream = new ByteArrayInputStream(byteArrayOutputStream.toByteArray());
            } catch (Exception e) {
                LOG.m12e(TAG, e.getMessage());
                byteArrayInputStream = null;
            }
            return new CordovaResourceApi.OpenForReadResult(openForRead.uri, byteArrayInputStream, openForRead.mimeType, openForRead.length, openForRead.assetFd);
        }
        return openForRead;
    }

    @Override // org.apache.cordova.CordovaPlugin
    public Uri remapUri(Uri uri) {
        Uri uri2 = uri;
        if (uri.toString().indexOf("/+++/") > -1) {
            uri2 = toPluginUri(uri);
        }
        return uri2;
    }
}