import io
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def handle_open_for_read(uri):
    str = str(uri).replace("/+++/", "/").split('?')[0]
    open_for_read = web_view.get_resource_api().open_for_read(uri.parse(str), True)
    if is_crypt_files(str):
        with open_for_read.input_stream as input_stream:
            content = input_stream.read().decode()
        
        decode = base64.b64decode(content)
        print("decrypt:", str)
        
        try:
            secret_key = CRYPT_KEY.encode('utf-8')
            iv = CRYPT_IV.encode('utf-8')
            cipher = AES.new(secret_key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(decode), AES.block_size)
            byte_stream = io.BytesIO(decrypted_data)
        except Exception as e:
            print(e)
            byte_stream = None
        
        return (open_for_read.uri, byte_stream, open_for_read.mimeType, open_for_read.length, open_for_read.assetFd)
    
    return open_for_read

def remap_uri(uri):
    uri2 = uri
    if "/+++/".encode() in uri.encode():
        uri2 = to_plugin_uri(uri) # Assuming the to_plugin_uri() method is defined elsewhere
    return uri2
