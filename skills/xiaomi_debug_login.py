import asyncio
from aiohttp import ClientSession
import json

MI_USER = "2217835217"
MI_PASS = "recardo9441mlu"

async def test_login():
    async with ClientSession() as sess:
        url1 = "https://account.xiaomi.com/pass/serviceLogin?sid=micoapi&_json=true"
        headers = {'User-Agent': 'APP/com.xiaomi.mihome APPV/6.0.103 iosPassportSDK/3.9.0 iOS/14.4 miHSTS'}
        cookies = {'sdkVersion': '3.9', 'deviceId': 'ASUKA_DEVICE_1234'}
        
        async with sess.get(url1, headers=headers, cookies=cookies) as r:
            raw = await r.read()
            resp = json.loads(raw[11:])
            print("[+] Step 1 Response:", json.dumps(resp, indent=2))
            
        if resp['code'] != 0:
            import hashlib
            hash_pw = hashlib.md5(MI_PASS.encode()).hexdigest().upper()
            data = {
                '_json': 'true',
                'qs': resp.get('qs', ''),
                'sid': resp.get('sid', 'micoapi'),
                '_sign': resp.get('_sign', ''),
                'callback': resp.get('callback', ''),
                'user': MI_USER,
                'hash': hash_pw
            }
            url2 = "https://account.xiaomi.com/pass/serviceLoginAuth2"
            async with sess.post(url2, data=data, headers=headers, cookies=cookies) as r2:
                raw2 = await r2.read()
                resp2 = json.loads(raw2[11:])
                print("[+] Step 2 Response:", json.dumps(resp2, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_login())
