from flask import Flask, request, jsonify
import requests
import os

# Initialize Flask app
app = Flask(__name__)

# Get bot token from environment variable (set in Render dashboard)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise RuntimeError("❌ TELEGRAM_TOKEN environment variable is not set!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


@app.route('/')
def home():
    return "✅ Telegram bot is running! Webhook should be set to /webhook"


@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse incoming update from Telegram
    update = request.get_json()

    # Safety check: ensure it's a valid message
    if not update or 'message' not in update:
        return jsonify({'ok': False, 'error': 'No valid message'}), 400

    try:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')

        # Echo the message back
        reply_text = f"🔁 You said: {text}"

        # Send reply via Telegram Bot API
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={
                'chat_id': chat_id,
                'text': reply_text
            }
        )

        if response.status_code == 200:
            return jsonify({'ok': True})
        else:
            return jsonify({'ok': False, 'error': response.text}), 500

    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


# Only used for local testing (Render uses gunicorn, so this won't run in production)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
