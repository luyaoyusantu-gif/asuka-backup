import sys
import asyncio
from aiohttp import ClientSession

sys.path.insert(0, './skills/xiaomi-env/MiService')
from miservice import MiAccount, MiNAService

MI_USER = "2217835217"
MI_PASS = "recardo9441mlu"

async def main():
    async with ClientSession() as session:
        account = MiAccount(session, MI_USER, MI_PASS)
        mina = MiNAService(account)
        try:
            print("[*] Logging in with correct SID (micoapi)...")
            devices = await mina.device_list()
            if devices:
                print(f"[+] Success! Found {len(devices)} devices:")
                for d in devices:
                    print(f"  - {d.get('name')} (ID: {d.get('deviceID')})")
            else:
                print("[-] No devices found or login failed silently.")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())