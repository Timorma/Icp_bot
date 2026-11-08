import logging
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

from fetcher import fetch_market_data
from analyzer import analyze_confluence
from chart_drawer import generate_chart

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "👋 أهلاً بك في بوت Institutional Code Breaker (ICB) للتحليل الفني الشامل! 🚀\n\n"
        "أرسل اسم أي أداة مالية (مثل: XAUUSD, BTCUSD, EURUSD, US30) وسأقوم فوراً بـ:\n"
        "1️⃣ جلب بيانات وحركة السوق الحية.\n"
        "2️⃣ إجراء تحليل متكامل (جان، العرض والطلب، CRT، إليوت، والسيولة).\n"
        "3️⃣ إرسال تقرير مفصل + شارت مرسوم بأسعار الدخول، وقف الخسارة، والأهداف."
    )
    await update.message.reply_text(welcome_msg)

async def handle_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.strip().upper()
    await update.message.reply_text(f"⏳ جاري تحليل الأداة `{symbol}` وفقاً لمدارس التحليل المؤسسي...")
    
    try:
        df = fetch_market_data(symbol)
        analysis_data = analyze_confluence(df, symbol)
        chart_bytes = generate_chart(df, symbol, analysis_data)
        
        await update.message.reply_text(analysis_data['report'], parse_mode='Markdown')
        await update.message.reply_photo(photo=io.BytesIO(chart_bytes), caption=f"📊 الشارت الفني المباشر لـ {symbol}")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التحليل: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_analysis))
    
    print("🚀 البوت يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == '__main__':
    main()
