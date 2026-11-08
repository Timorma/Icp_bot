import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import io

def generate_chart(df: pd.DataFrame, symbol: str, analysis: dict) -> bytes:
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    
    df_tail = df.tail(80)
    ax.plot(df_tail['datetime'], df_tail['close'], color='#00e676', linewidth=1.5, label='Price (Market Feed)')
    ax.fill_between(df_tail['datetime'], df_tail['low'], df_tail['high'], color='#00e676', alpha=0.1)
    
    demand_low, demand_high = analysis['demand_zone']
    supply_low, supply_high = analysis['supply_zone']
    
    ax.axhspan(demand_low, demand_high, color='#00c853', alpha=0.25, label='Demand Zone (OB/CRT)')
    ax.axhspan(supply_low, supply_high, color='#ff1744', alpha=0.25, label='Supply Zone (OB/CRT)')
    
    ax.axhline(analysis['entry'], color='#ffeb3b', linestyle='--', linewidth=1.2, label=f"Entry: {analysis['entry']:.4f}")
    ax.axhline(analysis['sl'], color='#ff5252', linestyle=':', linewidth=1.2, label=f"SL: {analysis['sl']:.4f}")
    ax.axhline(analysis['tp1'], color='#69f0ae', linestyle='-.', linewidth=1.2, label=f"TP1: {analysis['tp1']:.4f}")
    ax.axhline(analysis['tp2'], color='#00e676', linestyle='-', linewidth=1.2, label=f"TP2: {analysis['tp2']:.4f}")

    ax.set_title(f"ICB Institutional Analysis - {symbol.upper()}", fontsize=14, fontweight='bold', color='#ffffff', pad=12)
    ax.set_ylabel("Price", fontsize=10, color='#cccccc')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.grid(True, linestyle=':', alpha=0.3, color='#444444')
    ax.legend(loc='upper left', frameon=True, facecolor='#1e1e1e', edgecolor='#333333', fontsize=8)
    
    plt.xticks(rotation=25, fontsize=8)
    plt.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    plt.close(fig)
    return img_buf.getvalue()
