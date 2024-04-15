import requests
import json

def send_discord_notification(message):
    webhook_url = 'https://discord.com/api/webhooks/1229498628100587752/rDK_NY9tVuZisJSRwh5uDI1vfroe2KUEo0YsWZBeDfI1V2zYBWq5Byxw0vsWZbI2aeob'
    payload = {'content': message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification. Status code:", response.status_code)