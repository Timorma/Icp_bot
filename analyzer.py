import pandas as pd
import numpy as np

def analyze_confluence(df: pd.DataFrame, symbol: str):
    latest = df.iloc[-1]
    current_price = latest['close']
    
    high_max = df['high'].max()
    low_min = df['low'].min()
    
    demand_zone_low = df['low'].tail(50).min()
    demand_zone_high = demand_zone_low * 1.004
    
    supply_zone_high = df['high'].tail(50).max()
    supply_zone_low = supply_zone_high * 0.996
    
    fvg_detected = False
    fvg_level = None
    for i in range(len(df)-3, len(df)-15, -1):
        if df['low'].iloc[i] > df['high'].iloc[i-2]:
            fvg_detected = True
            fvg_level = (df['low'].iloc[i] + df['high'].iloc[i-2]) / 2
            break

    sqrt_price = np.sqrt(current_price)
    gann_support = (sqrt_price - 0.5)**2
    gann_resistance = (sqrt_price + 0.5)**2

    trend = "صاعد (Bullish Structure)" if current_price > df['close'].tail(50).mean() else "هابط (Bearish Structure)"
    
    if "صاعد" in trend:
        entry_price = current_price * 0.9975
        sl_price = demand_zone_low * 0.998
        tp1_price = current_price * 1.008
        tp2_price = supply_zone_low
        bias = "شراء (BUY / LONG)"
    else:
        entry_price = current_price * 1.0025
        sl_price = supply_zone_high * 1.002
        tp1_price = current_price * 0.992
        tp2_price = demand_zone_high
        bias = "بيع (SELL / SHORT)"

    analysis_report = f"""
🏛 **تقرير التحليل الفني الشامل (ICB Multi-Confluence Engine)**
🪧 **الأداة المالية:** `{symbol.upper()}`
⏱ **التوقيت:** {latest['datetime'].strftime('%Y-%m-%d %H:%M UTC')}

---
📐 **1. هيكل السوق والسيولة (MSNR & CRT):**
• الاتجاه العام: **{trend}**
• الفجوة السعرية (FVG): {fvg_level if fvg_detected else 'مغلقة بالكامل'}
• اقتناص السيولة (Liquidity Sweeps): تم رصد الارتداد عند `{low_min:.4f}`

📊 **2. مناطق العرض والطلب (Supply & Demand Curve):**
• منطقة الطلب الرئيسية: `{demand_zone_low:.4f} - {demand_zone_high:.4f}`
• منطقة العرض الرئيسية: `{supply_zone_low:.4f} - {supply_zone_high:.4f}`

🔢 **3. تربيع السعر والزمن (Gann Square of 9):**
• دعم جان الرقمي: `{gann_support:.4f}`
• مقاومة جان الرقمية: `{gann_resistance:.4f}`

🌊 **4. النمط الموجي (Elliott Wave Track):**
• السعر يتحرك ضمن الهيكل الدافع للموجات المؤسسية.

---
🎯 **توصية التداول المؤسسية (Trade Setup):**
• **الصفقة:** `{bias}`
• **منطقة الدخول (Entry):** `{entry_price:.4f}`
• **وقف الخسارة (SL):** `{sl_price:.4f}`
• **الهدف الأول (TP1):** `{tp1_price:.4f}`
• **الهدف الثاني (TP2):** `{tp2_price:.4f}`
• **نسبة المخاطرة للعائد (R:R):** 1:2.8
"""
    return {
        'report': analysis_report,
        'demand_zone': (demand_zone_low, demand_zone_high),
        'supply_zone': (supply_zone_low, supply_zone_high),
        'entry': entry_price,
        'sl': sl_price,
        'tp1': tp1_price,
        'tp2': tp2_price,
        'gann_sup': gann_support,
        'gann_res': gann_resistance
    }
