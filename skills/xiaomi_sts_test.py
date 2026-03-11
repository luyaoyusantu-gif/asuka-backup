import urllib.request
import urllib.parse
import json
import http.cookiejar

url = "https://api2.mina.mi.com/sts?d=wb_689811bf-b638-4bc5-84c8-e3edaa7b92ca&ticket=0&pwd=0&p_ts=1772905637770&fid=0&p_lm=1&p_ur=CN&auth=fCP3lLPjST3no%2BS9GcEVdhnvC7P%2Bwa1%2BOwR%2BAsKBvsciq8vlhVSjCoaPYNjKmhMZox2kiXJzRaagg1406rn1%2FliaKmPnKFAsVQGLxiTqaMC0w3Wd2nDzH9Y8DHxYytaDjkefJCxhhdLjDV4%2F5EQJBmB6krlNQUmWgdds2keXl1U%3D&m=5&_group=DEFAULT&tsl=1&p_ca=0&p_idc=China&nonce=qfkz8pAnJjYBwt%2Ba&_ssign=V2iU%2Bqkfd2TteQFMFsYqIPe0SUM%3D"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Step 1: Get Service Token
print("Getting service token...")
req = urllib.request.Request(url)
try:
    resp = opener.open(req)
    print("STS response:", resp.getcode())
except Exception as e:
    print("STS error:", e)

cookies = {cookie.name: cookie.value for cookie in cj}
print("Cookies:", cookies)

# Step 2: Get Device List
userId = "2217835217"
device_list_url = f"https://api2.mina.mi.com/admin/v2/device_list?master=0&requestId=app_ios_12345"

req2 = urllib.request.Request(device_list_url)
# Add required cookies
cookie_header = f"userId={userId}; serviceToken={cookies.get('serviceToken', '')}"
req2.add_header("Cookie", cookie_header)
# Mina API usually requires a User-Agent from a mobile app
req2.add_header("User-Agent", "APP/com.xiaomi.mico APPV/2.1.17 iosStandInside/true os_version/14.4 system/Darwin builder/20210218160000")

try:
    resp2 = opener.open(req2)
    data = resp2.read().decode('utf-8')
    print("Device List Response:", data)
except Exception as e:
    print("Device List error:", e)