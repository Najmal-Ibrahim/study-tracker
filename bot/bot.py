import json
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# -----------------------------------
# CONFIGURATION
# -----------------------------------
load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")

# -----------------------------------
# LOGGING SETUP
# -----------------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# -----------------------------------
# /start COMMAND
# -----------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Study Tracker Bot Active ✅\n\n"
        "Example:\n"
        "/log scratch 2"
    )

# -----------------------------------
# /log COMMAND
# -----------------------------------

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        # Example:
        # /log scratch 2

        args = context.args

        # Validate command format
        if len(args) != 2:

            await update.message.reply_text(
                "Usage:\n/log <topic> <pomodoros>"
            )
            return

        # Extract values
        topic = args[0].lower()
        pomodoros = int(args[1])

        # Open stats.json
        with open("data/stats.json", "r") as file:
            stats = json.load(file)

        # Add topic if not exists
        if topic not in stats:
            stats[topic] = 0

        # Update value
        stats[topic] += pomodoros

        # Save updated JSON
        with open("data/stats.json", "w") as file:
            json.dump(stats, file, indent=2)

        # Reply to user
        await update.message.reply_text(
            f"✅ Logged {pomodoros} pomodoros for {topic}\n"
            f"Total: {stats[topic]}"
        )

    except ValueError:

        await update.message.reply_text(
            "Pomodoros must be a number."
        )

    except Exception as e:

        logging.exception("Error occurred")

        await update.message.reply_text(
            f"Error: {str(e)}"
        )

# -----------------------------------
# MAIN FUNCTION
# -----------------------------------

def main():

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("log", log))

    print("Bot is running...")

    # Start bot
    app.run_polling()

# -----------------------------------
# RUN APPLICATION
# -----------------------------------

if __name__ == "__main__":
    main()