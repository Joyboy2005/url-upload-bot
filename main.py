import os
import requests
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

def upload(update, context):
    if not context.args:
        update.message.reply_text("❌ Use: /upload <url>")
        return

    url = context.args[0]
    fname = "downloaded_file"

    update.message.reply_text("📥 Downloading…")
    resp = requests.get(url, stream=True)
    with open(fname, "wb") as f:
        for chunk in resp.iter_content(1024 * 1024):
            f.write(chunk)

    update.message.reply_text("📤 Uploading…")
    with open(fname, "rb") as f:
        context.bot.send_document(CHANNEL_ID, document=f, caption="✅ Done")

    update.message.reply_text("✅ Uploaded!")
    os.remove(fname)

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("upload", upload))
updater.start_polling()
updater.idle()
