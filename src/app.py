# pip install python-telegram-bot 

import logging
import os

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, ApplicationBuilder

from dbModule import *
from parseUpdateToJson import *
from updateDiff import updateDiff
from getProgression import getProgression

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Global db conn
# TODO: add secret reference from file
mongoUser = os.getenv("MONGO_USER")
mongoPassword = os.getenv("MONGO_PASSWORD")
dbConn = getDbConnection(mongoUser, mongoPassword)

# ============================================================================================================================

# Command handlers
async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"""Hi {user.mention_html()}!\nSend me the ALL TIME stats to continue""",
    )

# ============================================================================================================================

async def helpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me the ALL TIME stats, or export the ALL TIME stats to this bot to continue")

# ============================================================================================================================

jsonUpdate = {}

async def processUpdate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_id = update.message.chat.id
    jsonUpdate = parseUpdateToJson(update.message.text)
    if jsonUpdate['time_span'] != "all_time":
        await update.message.reply_text("Send me the <b>ALL TIME</b> profile update instead.", parse_mode="HTML")
        return ConversationHandler.END

    agentName = update.message.text.split("\n")[1].split(" ")[2] # a bit hacky
    await update.message.reply_text("Welcome back, agent {}".format(agentName))
    print("Received update from agent {}".format(agentName))
    
    lastUpdate = getlastUpdate(dbConn, user_id)

    if lastUpdate is not None and not firstDTIsBeforeEqualsSecondDT(jsonUpdate, lastUpdate):
        # TODO: exception handling
        await update.message.reply_text(updateDiff(lastUpdate, jsonUpdate), parse_mode="HTML")

    try:    
        insertUpdate(dbConn, user_id, jsonUpdate)
    except Exception as e:
        await update.message.reply_text(str(e))

    ""
    await update.message.reply_text(getProgression(jsonUpdate), parse_mode="HTML")
    return ConversationHandler.END


# ============================================================================================================================

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    # TODO: secret reference from file
    telebotToken = os.getenv("ISTATTRACKER_BOT_TOKEN")
    app = Application.builder().token(telebotToken).build()

    # Command handlers
    app.add_handler(CommandHandler("start", startCommand))
    app.add_handler(CommandHandler("help", helpCommand))


    # on non command i.e message - echo the message on Telegram
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processUpdate))

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
