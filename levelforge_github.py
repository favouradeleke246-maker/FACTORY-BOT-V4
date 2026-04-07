import os
import requests
from datetime import datetime

print("=" * 50)
print("BOT STARTING - DEBUG MODE")
print("=" * 50)

# Check what secrets we have
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

print(f"\n1. TELEGRAM_BOT_TOKEN: {'FOUND' if telegram_token else 'MISSING'}")
print(f"   First 10 chars: {telegram_token[:10] if telegram_token else 'None'}...")
print(f"\n2. TELEGRAM_CHAT_ID: {'FOUND' if telegram_chat_id else 'MISSING'}")
print(f"   Value: {telegram_chat_id if telegram_chat_id else 'None'}")

# Try to send message
if telegram_token and telegram_chat_id:
    print("\n3. Attempting to send Telegram message...")
    
    message = f"""
🎮 *TEST MESSAGE* 🎮

Your GitHub Actions bot is running!

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: Working!

If you see this, your Telegram is configured correctly!
"""
    
    try:
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        data = {
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        print(f"   Sending to: {url[:50]}...")
        response = requests.post(url, json=data, timeout=10)
        
        print(f"   Response status: {response.status_code}")
        print(f"   Response body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! Message sent to Telegram!")
        else:
            print(f"\n❌ Failed! Error: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
else:
    print("\n❌ Missing Telegram credentials!")
    print("   Cannot send message.")

print("\n" + "=" * 50)
print("BOT FINISHED")
print("=" * 50)
