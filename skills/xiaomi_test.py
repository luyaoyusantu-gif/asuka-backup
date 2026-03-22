import sys
import asyncio
from aiohttp import ClientSession

# Inject the cloned MiService path
sys.path.insert(0, './skills/xiaomi-env/MiService')
from miservice import MiAccount, MiNAService

MI_USER = "2217835217"
MI_PASS = "recardo9441mlu"

async def list_devices():
    print("[*] Connecting to Xiaomi Cloud...")
    async with ClientSession() as session:
        account = MiAccount(session, MI_USER, MI_PASS)
        try:
            await account.login('mina')
            mina = MiNAService(account)
            
            print("[+] Login successful! Fetching MiAI devices...")
            devices = await mina.device_list()
            
            print(f"\n[*] Found {len(devices)} device(s):")
            for idx, dev in enumerate(devices):
                name = dev.get('name', 'Unknown')
                did = dev.get('deviceID', 'Unknown')
                mac = dev.get('mac', 'Unknown')
                print(f"  {idx+1}. Name: {name} | DeviceID: {did} | MAC: {mac}")
                
            return devices
            
        except Exception as e:
            print(f"[!] Login or fetch failed: {e}")
            return None

if __name__ == '__main__':
    asyncio.run(list_devices())
