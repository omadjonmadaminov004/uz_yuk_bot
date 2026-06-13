from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler

TOKEN = "8860401698:AAFxqKwHV1c22skiqa0X_bDxlbqTJeAH9-4"
ADMIN = "Madaminov_421"
ADMIN_ID = None
yuklar = []
yuk_id = [1]
ROLE, QAYERDAN, QAYERGA, OGIRLIK, NARX, TEL = range(6)

async def start(update, context):
    global ADMIN_ID
    if update.effective_user.username == ADMIN:
        ADMIN_ID = update.effective_chat.id
    kb = [
        [InlineKeyboardButton("Yuk yuboruvchi", callback_data="sender")],
        [InlineKeyboardButton("Haydovchi", callback_data="driver")]
    ]
    await update.message.reply_text(
        "UzYuk ga xush kelibsiz!\n\nSiz kimsiz?",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    return ROLE

async def role(update, context):
    q = update.callback_query
    await q.answer()
    if q.data == "sender":
        await q.edit_message_text("Yukingiz qayerdan jonatiladi?")
        return QAYERDAN
    text = "Mavjud yuklar:\n\n"
    if not yuklar:
        text += "Hozircha yuk yoq."
    else:
        for y in yuklar:
            text += f"#{y['id']} {y['dan']} - {y['ga']}\nOgirligi: {y['og']}\nNarxi: {y['narx']}\nTel: {y['tel']}\n\n"
    await q.edit_message_text(text)
    return ConversationHandler.END

async def qayerdan(update, context):
    context.user_data['dan'] = update.message.text
    await update.message.reply_text("Qayerga yetkaziladi?")
    return QAYERGA

async def qayerga(update, context):
    context.user_data['ga'] = update.message.text
    await update.message.reply_text("Ogirligi qancha?")
    return OGIRLIK

async def ogirlik(update, context):
    context.user_data['og'] = update.message.text
    await update.message.reply_text("Narxi qancha?")
    return NARX

async def narx(update, context):
    context.user_data['narx'] = update.message.text
    await update.message.reply_text("Telefon raqamingiz?")
    return TEL

async def tel(update, context):
    d = context.user_data
    y = {
        'id': yuk_id[0],
        'dan': d['dan'],
        'ga': d['ga'],
        'og': d['og'],
        'narx': d['narx'],
        'tel': update.message.text
    }
    yuklar.append(y)
    yuk_id[0] += 1
    await update.message.reply_text(
        f"Qabul qilindi!\n{y['dan']} - {y['ga']}\n{y['og']}\n{y['narx']}\nHaydovchilar boglanadi!"
    )
    if ADMIN_ID:
        await context.bot.send_message(
            ADMIN_ID,
            f"Yangi yuk #{y['id']}\n{y['dan']}-{y['ga']}\n{y['og']}\n{y['narx']}\nTel: {y['tel']}"
        )
    return ConversationHandler.END

async def admin(update, context):
    global ADMIN_ID
    if update.effective_user.username != ADMIN:
        await update.message.reply_text("Ruxsat yoq!")
        return
    ADMIN_ID = update.effective_chat.id
    await update.message.reply_text(f"Admin panel\nJami yuklar: {len(yuklar)}")

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ROLE: [CallbackQueryHandler(role)],
            QAYERDAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, qayerdan)],
            QAYERGA: [MessageHandler(filters.TEXT & ~filters.COMMAND, qayerga)],
            OGIRLIK: [MessageHandler(filters.TEXT & ~filters.COMMAND, ogirlik)],
            NARX: [MessageHandler(filters.TEXT & ~filters.COMMAND, narx)],
            TEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, tel)],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("admin", admin))
    print("Bot ishga tushdi!")
    app.run_polling()

if name == "__main__":
    main()
