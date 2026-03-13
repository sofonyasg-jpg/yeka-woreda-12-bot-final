#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
የካ ክፍለ ከተማ ወረዳ 12 ሲቪል ምዝገባና የነዋሪነት አገልግሎት ጽ/ቤት - ቴሌግራም ቦት
"""

import os
import logging
from flask import Flask, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import threading
import time

# ==================== ቶከን ====================
# ይህ ከ Render Environment Variables ይነበባል
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# የጽ/ቤቱ መረጃ
OFFICE_PHONE = "0951969640"
OFFICE_ADDRESS = "ኮተቤ መሳለሚያ ማርያም ቤተክርስትያን ጀርባ"

# ==================== ሎጊንግ ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== Flask አፕ (ለ Render) ====================
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "message": "የካ ወረዳ 12 ቦት በስራ ላይ ነው",
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# ==================== የቦት ትዕዛዞች ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """የ/start ኮማንድ"""
    user = update.effective_user
    
    welcome_message = (
        "🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟\n"
        "       🏛️ **እንኳን ደህና መጡ!** 🏛️\n"
        "🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟\n\n"
        f"👋 እንኳን ደህና መጡ {user.first_name}!\n\n"
        "🏢 **የካ ክፍለ ከተማ ወረዳ 12**\n"
        "ሲቪል ምዝገባና የነዋሪነት አገልግሎት ጽ/ቤት\n\n"
        "ከዚህ በታች ካሉት አገልግሎቶች መርጠው ይቀጥሉ፦"
    )
    
    keyboard = [
        [InlineKeyboardButton("📋 ኩነት ዘርፍ", callback_data='vital')],
        [InlineKeyboardButton("👥 ነዋሪዎች", callback_data='residency')],
        [InlineKeyboardButton("📍 አድራሻ", callback_data='address')],
        [InlineKeyboardButton("📞 ስልክ", callback_data='phone')]
    ]
    
    await update.message.reply_text(
        welcome_message, 
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def vital_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📋 **የኩነት ዘርፍ አገልግሎቶች**\n\nየሚፈልጉትን አገልግሎት ይምረጡ፦"
    
    keyboard = [
        [InlineKeyboardButton("👶 ልደት", callback_data='birth')],
        [InlineKeyboardButton("💍 ጋብቻ", callback_data='marriage')],
        [InlineKeyboardButton("⚰️ ሞት", callback_data='death')],
        [InlineKeyboardButton("⚖️ ፍቺ", callback_data='divorce')],
        [InlineKeyboardButton("🔙 ተመለስ", callback_data='back_to_start')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def residency_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "👥 **የነዋሪዎች አገልግሎት ዘርፍ**\n\nየሚፈልጉትን አገልግሎት ይምረጡ፦"
    
    keyboard = [
        [InlineKeyboardButton("🆔 መታወቂያ", callback_data='id_card')],
        [InlineKeyboardButton("📄 ያላገባ", callback_data='single')],
        [InlineKeyboardButton("🌿 በህይወት መኖር", callback_data='life')],
        [InlineKeyboardButton("🏠 ነዋሪነት", callback_data='residency_cert')],
        [InlineKeyboardButton("🔙 ተመለስ", callback_data='back_to_start')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def service_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    service_info = {
        'birth': {
            'name': '👶 ልደት',
            'req': '• የእናት እና አባት መታወቂያ\n• የህፃኑ ክትባት ካርድ\n• የህፃኑ ፎቶ',
            'fee': 'ወቅታዊ: 60 ብር\nየዘገየ: 150 ብር\nእርማት: 100 ብር'
        },
        'marriage': {
            'name': '💍 ጋብቻ',
            'req': '• የተጋቢዎች መታወቂያ\n• 4 ምስክሮች',
            'fee': 'ወቅታዊ: 120 ብር\nየዘገየ: 250 ብር\nእርማት: 150 ብር'
        },
        'death': {
            'name': '⚰️ ሞት',
            'req': '• የሞት ማስረጃ\n• የሚያስረክበው ሰው መታወቂያ',
            'fee': 'ወቅታዊ: 60 ብር\nየዘገየ: 150 ብር\nእርማት: 150 ብር'
        },
        'divorce': {
            'name': '⚖️ ፍቺ',
            'req': '• የፍርድ ቤት የፍቺ ማስረጃ',
            'fee': 'ወቅታዊ: 120 ብር\nየዘገየ: 150 ብር\nእርማት: 150 ብር'
        },
        'id_card': {
            'name': '🆔 መታወቂያ',
            'req': '• የትውልድ ሰርተፍኬት\n• 2 ፎቶ\n• የቀበሌ ማረጋገጫ',
            'fee': 'አዲስ: 100 ብር\nእድሳት: 100 ብር\nየጠፋ: 200 ብር'
        },
        'single': {
            'name': '📄 ያላገባ',
            'req': '• የነዋሪነት መታወቂያ\n• 3 ምስክሮች',
            'fee': 'አዲስ: 200 ብር\nእድሳት: 250 ብር'
        },
        'life': {
            'name': '🌿 በህይወት መኖር',
            'req': '• የነዋሪነት መታወቂያ\n• 3 ምስክሮች',
            'fee': 'ነፃ'
        },
        'residency_cert': {
            'name': '🏠 ነዋሪነት',
            'req': '• የነዋሪነት መታወቂያ',
            'fee': '35 ብር'
        }
    }
    
    service = service_info.get(query.data)
    if not service:
        return
    
    text = (
        f"{service['name']}\n\n"
        f"📋 **የሚፈለጉ ሰነዶች:**\n{service['req']}\n\n"
        f"💰 **ክፍያ:**\n{service['fee']}\n\n"
        f"📞 **ስልክ:** {OFFICE_PHONE}"
    )
    
    back_to = 'vital' if query.data in ['birth','marriage','death','divorce'] else 'residency'
    keyboard = [[InlineKeyboardButton("🔙 ተመለስ", callback_data=back_to)]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = f"📍 **አድራሻ**\n\n{OFFICE_ADDRESS}"
    keyboard = [[InlineKeyboardButton("🔙 ወደ መነሻ", callback_data='back_to_start')]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = f"📞 **ስልክ ቁጥር**\n\n{OFFICE_PHONE}"
    keyboard = [[InlineKeyboardButton("🔙 ወደ መነሻ", callback_data='back_to_start')]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# ==================== ቦቱን ማስነሳት ====================
def run_bot():
    try:
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found in environment variables!")
            return
            
        app_bot = Application.builder().token(BOT_TOKEN).build()
        
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.add_handler(CallbackQueryHandler(vital_menu, pattern='^vital$'))
        app_bot.add_handler(CallbackQueryHandler(residency_menu, pattern='^residency$'))
        app_bot.add_handler(CallbackQueryHandler(address, pattern='^address$'))
        app_bot.add_handler(CallbackQueryHandler(phone, pattern='^phone$'))
        app_bot.add_handler(CallbackQueryHandler(back_to_start, pattern='^back_to_start$'))
        
        for pattern in ['birth','marriage','death','divorce','id_card','single','life','residency_cert']:
            app_bot.add_handler(CallbackQueryHandler(service_detail, pattern=f'^{pattern}$'))
        
        logger.info("🤖 Bot started successfully")
        app_bot.run_polling()
    except Exception as e:
        logger.error(f"Bot error: {e}")

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🌐 Flask server starting on port {port}")
    app.run(host='0.0.0.0', port=port)
