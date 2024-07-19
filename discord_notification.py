import requests
import json

def send_discord_notification(name, url, message):
    webhook_url = 'https://discord.com/api/webhooks/1227777505889357955/t9hiPql2jrKAt01SfIldCqWHAbdyqXDoVoABvxxJcKaIVilQTOzSmplgnimHQgqKwRmL'
    data = {
    "embeds": [
        {
            "title": f"{name}",
            "url": f"{url}",
            "description": f"{message}",
            "color": 0x00ACED
        }
    ]
}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification. Status code:", response.status_code)