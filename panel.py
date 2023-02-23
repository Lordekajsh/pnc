from typing import Union

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMINS
from database import cur, save


# Definindo função para exibir um painel de administração do bot quando o comando /painel é enviado ou quando um botão do painel é pressionado
@Client.on_message(filters.command("painel") & filters.user(ADMINS))
@Client.on_callback_query(filters.regex("^painel$") & filters.user(ADMINS))
async def panel(c: Client, m: Union[Message, CallbackQuery]):
    # Definindo a estrutura do painel com botões que os administradores podem selecionar
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("🚦 Status do bot", callback_data="bot_status"),
                InlineKeyboardButton("🏦 Lara", callback_data="change_lara"),
            ],
            [
                InlineKeyboardButton("💵 Preços", callback_data="change_prices"),
                InlineKeyboardButton("🔃 Gates", callback_data="select_gate"),
            ],
            [
                InlineKeyboardButton("💠 Pix auto", callback_data="auto_pay"),
                InlineKeyboardButton("💳 Estoque", callback_data="stock cards"),
            ],
            [
                InlineKeyboardButton("👤 Usuários", switch_inline_query_current_chat="search_user "),
            ],
            [
               InlineKeyboardButton("♻ Config trocas", callback_data="settings")
            ],
        ]
    )

    # Determinando se a mensagem que ativou a função é uma mensagem de callback
    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text

    # Exibindo a mensagem do painel com a estrutura definida acima
    await send(
        """<b>🛂 Painel de administração da store</b>
<i>- Selecione abaixo o que você deseja visualizar ou modificar.</i>""",
        reply_markup=kb,
    )


# Definindo função para exibir configurações quando o comando /settings é enviado ou quando um botão de configuração é pressionado
@Client.on_message(
    filters.command(["settings", "set", "config", "setting"]) & filters.user(ADMINS)
)
@Client.on_callback_query(filters.regex("^settings") & filters.user(ADMINS))
async def settings(c: Client, m: Union[CallbackQuery, Message]):
    # Definindo função para determinar se a mensagem recebida é uma mensagem de callback ou não
    m = m.reply_text if isinstance(m, Message) else m.message.edit_text
    exhance_is = cur.execute("SELECT exchange_is FROM bot_config").fetchone()[0]
    msg, calb = (
        ("⭕️ Desabilitar", "exchange_0")
        if exhance_is == 1
        else ("✅ Habilitar", "exchange_1")
    )
    # Estrutura do painel de configurações
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🕐 Tempo de troca", callback_data="set time")],
            [InlineKeyboardButton(text=msg, callback_data=f"set {calb}")],
            [InlineKeyboardButton(text="🔙 Voltar", callback_data="painel")],
        ]
    )

    if action == "time":
        await m.message.delete()
        new_time = await m.message.ask(
            "Digite o tempo de troca",
            filters=filters.regex(r"^\d+"),
            reply_markup=ForceReply(),
        )
        cur.execute("UPDATE bot_config SET time_exchange=?", [int(new_time.text)])
        save()
        return await m.message.reply_text(
            f"Tempo de troca alterado com sucesso. Novo tempo {new_time.text}m",
            reply_markup=kb,
        )
    st = action.split("_")[1]
    is_exch = "habilitadas" if st == 1 else "Desabilitadas"
    cur.execute("UPDATE bot_config SET exchange_is=?", [int(st)])
    save()
    return await m.edit_message_text(
        f"<b>Trocas {is_exch} com sucesso.</b>", reply_markup=kb
    )