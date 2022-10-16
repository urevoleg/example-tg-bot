import logging
import os
import datetime as dt

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dotenv import load_dotenv
load_dotenv()


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def processed_voice(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"It's a voice message! Processing.....")

    voice_obj = update.message.voice

    audio = voice_obj.get_file().download_as_bytearray()
    audio_path = f'src/audio-{dt.datetime.now()}.wav'
    with open(audio_path, 'wb') as f:
        f.write(audio)

    if voice_obj.duration < 10:
        update.message.reply_text(f"Duration is too short, try again for 10+ seconds!")
    else:
        import soundfile as sf
        import pyloudnorm as pyln

        data, rate = sf.read(os.path.abspath(audio_path), stop=250 * 1024)  # load audio
        meter1 = pyln.Meter(rate)

        update.message.reply_text(f"Duration is : {voice_obj.duration}")
        loudness = meter1.integrated_loudness(data)
        if loudness < -28:
            update.message.reply_text(f"Loudness is : {loudness:.1f}. Your voice is quite!")
        else:
            update.message.reply_text(f"Loudness is : {loudness:.1f}. Your voice is good!")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv('TG_TOKEN'))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # voice msg
    dispatcher.add_handler(MessageHandler(Filters.voice, processed_voice))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()