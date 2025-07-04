from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from notion_client import Client

# API KEYS (अपनी API यहां डालना)
TELEGRAM_TOKEN = "8167946456:AAHpV_RWfEEHt8cNalHRRhNMkaNbHIKKlWU"
NOTION_TOKEN = "ntn_n73717790436lqIfNVx0lzTlrYwAUgMcriczCdOJd0Z4Y2"
DATABASE_ID = "2261b7646be38090b9e5efa6e223fe30"


# Notion Client Setup
notion = Client(auth=NOTION_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Jarwis Online ✅\n\nSend me your note in this format:\nFolderName: Your Note"
    )

async def save_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if ":" not in text:
        await update.message.reply_text("⚠️ Format should be:\nFolderName: Your Note")
        return
    folder, content = text.split(":", 1)
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Folder": {"select": {"name": folder.strip()}},
            "Title": {"title": [{"text": {"content": content.strip()}}]}
        },
    )
    await update.message.reply_text(f"✅ Saved to {folder.strip()} folder in Notion!")

# Telegram Bot Setup
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), save_note))
app.run_polling()
