import asyncio

from pyrogram import Client, idle
from pyrogram.errors import PeerIdInvalid
from pyrogram.session import Session

from config import API_HASH, API_ID, BOT_TOKEN, WORKERS
from database import db, save

# Inicializa o cliente.
client = Client(
    "bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    workers=WORKERS,
    plugins={"root": "plugins"},
)

# Desativa a mensagem do Pyrogram no início.
Session.notice_displayed = True


import asyncio

from pyrogram import Client, idle
from pyrogram.errors import PeerIdInvalid
from pyrogram.session import Session

from config import API_HASH, API_ID, BOT_TOKEN, WORKERS
from database import db, save

# Inicializa o cliente.
client = Client(
    "bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    workers=WORKERS,
    plugins={"root": "plugins"},
)

# Desativa a mensagem do Pyrogram no início.
Session.notice_displayed = True


async def main():
    try:
        await client.start()
    except PeerIdInvalid:
        print("Erro: ID de peer inválido.")
        return
    print("Bot iniciado com sucesso!")
    client.me = await client.get_me()

    while client.is_connected:
        await asyncio.sleep(0.1)

    await client.stop()
    save()
    db.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    print("Iniciando bot...")

    # Define a animação da barra de progresso
    animation = "|/-\\"
    idx = 0

    loop.run_until_complete(main())