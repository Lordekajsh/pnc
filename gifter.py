import random
import string
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from config import ADMIN_CHAT, ADMINS, GIFTERS
from database import cur, save


def gift_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choices(chars, k=size))


GIFT_MSG = """<b>🟢 GIFT GERADO</b>
<b>🏷 GIFT: </b><code>/resgatar {gift}</code>
<b>VALOR: R$ {value}</b>
<b>RESGATE: @{bot_username}</b>
<b>CANAL: @HECSTECH</b>
<b>⚠️ | Copia o /resgatar e manda pro bot pra resgatar o gift!!</b>"""


@Client.on_message(filters.regex("^/gift (?P<value>-?\d+)") & filters.create(lambda _, __, msg: msg.from_user.id in set(ADMINS) | set(GIFTERS)))
async def create_gift(c: Client, m: Message):
    value = int(m.matches[0]["value"])
    gift = gift_generator()
    cur.execute("INSERT INTO gifts(token, value) VALUES(?, ?)", [gift, value])
    save()
    await m.reply_text(GIFT_MSG.format(value=value, gift=gift, bot_username=c.me.username))
    text = f"🎁 {m.from_user.first_name} criou um gift card de <b>R${value}</b>\n- Gift card: <code>{gift}</code>"
    await c.send_message(ADMIN_CHAT, text)


@Client.on_inline_query(filters.regex(r"^gift (?P<value>-?\d+)") & filters.user(set(ADMINS).union(GIFTERS)))
async def create_gift_inline(c: Client, m: InlineQuery):
    value = int(m.matches[0]["value"])
    gift = gift_generator()
    cur.execute("INSERT INTO gifts(token, value) VALUES(?, ?)", [gift, value])
    save()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("👽 Resgatar", callback_data="resgatar " + gift)]
        ]
    )
    results = [
        InlineQueryResultArticle(
            title=f"Gift de R$ {value} criado",
            description="Clique para enviar o gift no chat.",
            input_message_content=InputTextMessageContent(
                GIFT_MSG.format(value=value, gift=gift, bot_username=c.me.username)
            ),
            reply_markup=kb,
        )
    ]
    await m.answer(results, cache_time=0, is_personal=True)
    text = f"🎁 {m.from_user.first_name} criou um gift card de <b>R${value}</b>\n- Gift card: <code>{gift}</code>"
    await c.send_message(ADMIN_CHAT, text)