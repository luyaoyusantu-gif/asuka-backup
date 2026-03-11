import urllib.request
import ssl
import json

TARGET = "192.168.31.1"
URLS = [
    f"http://{TARGET}/",
    f"http://{TARGET}:8080/",
    f"https://{TARGET}/"
]

print(f"[*] Starting 'Asuka Banner-Grabber' against {TARGET}...\n")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for url in URLS:
    print(f"[-] Probing {url} ...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Asuka/1.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=3) as response:
            server = response.getheader('Server')
            auth = response.getheader('WWW-Authenticate')
            html = response.read().decode('utf-8', errors='ignore')
            
            # Simple title extraction
            title = "Unknown"
            if "<title>" in html.lower():
                start = html.lower().find("<title>") + 7
                end = html.lower().find("</title>")
                title = html[start:end].strip()
                
            print(f"    [+] Status: {response.status}")
            print(f"    [+] Server Header: {server}")
            if auth: print(f"    [+] Auth Header: {auth}")
            print(f"    [+] Page Title: {title}\n")
            
    except urllib.error.HTTPError as e:
        server = e.headers.get('Server')
        auth = e.headers.get('WWW-Authenticate')
        print(f"    [!] HTTP Error: {e.code} {e.reason}")
        print(f"    [+] Server Header: {server}")
        if auth: print(f"    [+] Auth Header: {auth}\n")
    except Exception as e:
        print(f"    [x] Failed: {type(e).__name__} - {str(e)}\n")
