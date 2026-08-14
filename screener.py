import os
import sys
import datetime
import pandas as pd
import yfinance as yf
import requests

# Cleaned Known Stocks list extracted directly from Streamlit code
KNOWN_STOCKS = [
    'PALL', 'PLTM', 'IHF', 'ESTC', 'PRU', 'RGEN', 'UBS', 'TRV', 'WEN', 'OKLO', 'IBB', 'Q', 'OUST', 'VPG', 'WOLF', 'NOK', 'HSBC', 'DLTR', 'SKHY', 'RDDT', 'RL', 'CROX', 'LEVI', 'FOTO', 'GNRC', 'KLIC', 'IWM', 'HBMX', 'PWR', 'EUV', 'GRID', 'MAGS', 'SPCX', 'IBM', 'ELV', 'OSCR', 'QNT', 'HYDR', 'ALGM', 'LGN', 'IESC', 'AEHR', 'ACLS', 'MKSI', 'SMTC', 'AMKR', 
    'LSCC', 'DIOD', 'POWI', 'AA', 'ABBV', 'ALAB', 'AMGN', 'APO', 'BOTZ', 'CRCL', 'CRWV', 'D', 'DRAM', 'DUK', 'EEM', 'EWJ', 'EWY', 'EXC', 'FIGR', 
    'GEV', 'GILD', 'GXC', 'JEF', 'KMI', 'KRMN', 'LIN', 'MNST', 'NASA', 'NEM', 'NTR', 'OR', 
    'OWL', 'QQQ', 'RNG', 'RKT', 'SCCO', 'SHLD', 'SO', 'SOLS', 'SPMO', 'SPY', 'SPHB', 'TSEM', 'UNP', 'VTV', 
    'VUG', 'WGMI', 'WMB', 'XEL', 'XMAG', 'XYZ', 'ZIM', 'VICR', 'SLX', 'CBOE', 'SIMO', 'FLEX', 'POWL', 'VLO', 'DOCN', 
    'IYZ', 'LNG', 'AAOI', 'AXTI', 'USO', 'JNJ', 
    'HP', 'GLD', 'ALB', 'BUG', 'BX', 'DOW', 'VZ', 'REMX', 'GDX', 'SIL', 'VEEV', 'SNDK', 'TLT', 'APH', 'ARM', 'FANG', 
    'NBIS', 'NVT', 'OXY', 'FORM', 'IBIT', 'QTUM', 'IAI', 'KWEB', 'IHI', 'UFO', 'ITA', 'IYT', 'CVS', 'HUM', 'NEE', 
    'HPE', 'PLAB', 'INOD', 'TTMI', 'CCJ', 'BE', 'SLV', 'PICK', 'COPX', 'MAR', 'XAR', 'VSXY', 'GLW', 'ANF', 'AEO', 
    'AEP', 'GH', 'SANM', 'ROK', 'PSN', 'IAT', 'HROW', 'PL', 'AVAV', 'CIEN', 'COHR', 'NU', 'WULF', 'IREN', 'CIFR', 
    'RDW', 'PH', 'LITE', 'ACHR', 'CACI', 'CRS', 'URA', 'NVO', 'NLR', 'ITB', 'EOSE', 'APP', 'RKLB', 'ASTS', 
    'IONQ', 'RMBS', 'RTX', 'NOC', 'LMT', 'HON', 'ONDS', 'CLS', 'LEU', 'VRT', 'VST', 'NRG', 'CEG', 'SMCI', 'CRDO', 
    'SOFI', 'XLP', 'XLE', 'HIMS', 'HOOD', 'XLV', 'HACK', 'XOP', 'CIBR', 'ICLN', 'XLB', 'XLU', 'XLRE', 'IGV', 
    'XLF', 'IPAY', 'XLC', 'XLI', 'KRE', 'XLK', 'CLOU', 'KBE', 'XME', 'XTL', 'JETS', 'SMH', 'XLY', 'XHB', 
    'XBI', 'XRT', 'MJ', 'META', 'MSFT', 'AAPL', 'AMZN', 'GOOGL', 'NVDA', 'TSLA', 'ARKX', 'ARKQ', 'ARKF', 
    'ARKW', 'ARKK', 'ARKG', 'CCL', 'RCL', 'UAL', 'BA', 'DAL', 'NCLH', 'AAL', 'LUV', 'PINS', 'SNAP', 
    'IBKR', 'SCHW', 'JPM', 'MS', 'GS', 'BAC', 'WFC', 'SPGI', 'BLK', 'NDAQ', 'C', 'LI', 'BIDU', 'NIO', 'XPEV', 
    'BABA', 'PDD', 'JD', 'DQ', 'JKS', 'ENPH', 'FSLR', 'TAN', 'SEDG', 'CSIQ', 'SPWR', 'RUN', 'PBW', 'CLX', 'PG', 
    'EL', 'LULU', 'SBUX', 'NKE', 'MELI', 'EBAY', 'FDX', 'UPS', 'SE', 'JMIA', 'ETSY', 'SHOP', 
    'Z', 'OPEN', 'CHWY', 'CVNA', 'BARK', 'GM', 'BLNK', 'QS', 'F', 'RIVN', 'FCEL', 'CHPT', 'LCID', 
    'UPST', 'PYPL', 'AFRM', 'V', 'MA', 'AXP', 'BITO', 'COIN', 'RIOT', 'MARA', 'MSTR',
    'DKNG', 'PENN', 'BETZ', 'REGN', 'VRTX', 'MRK', 'UNH', 'TMO', 'ISRG', 'ABT', 'IDXX', 'TDOC', 'CRSP', 
    'BRK-B', 'ETN', 'CAT', 'U', 'RBLX', 'SKLZ', 'FSLY', 'TRIP', 'EXPE', 'BKNG', 'ABNB', 'DIS', 'WMT', 
    'COST', 'TGT', 'LOW', 'HD', 'DT', 'SNPS', 'CDNS', 'MDB', 'ORCL', 'NOW', 'ADP', 'SNOW', 'DDOG', 
    'FROG', 'ADSK', 'INTU', 'TEAM', 'WDAY', 'CRM', 'PAYC', 'ANET', 'ADBE', 'ACN', 'EPAM', 'ZM', 'TTD', 'TWLO', 
    'DASH', 'APPS', 'DOCU', 'AI', 'AKAM', 'QLYS', 'PANW', 'FTNT', 'CRWD', 'TENB', 'OKTA', 'ZS', 
    'NET', 'S', 'UMC', 'ASML', 'KEYS', 'CRUS', 'AMD', 'AVGO', 'MU', 'KLAC', 'TXN', 'QRVO', 'TSM', 'SWKS', 'AMBA', 
    'STM', 'MCHP', 'ON', 'QCOM', 'SOXX', 'MRVL', 'ADI', 'LRCX', 'AMAT', 'WDC', 'NXPI', 'TER', 'MPWR', 'INTC', 
    'GFS', 'STX', 'A', 'ZBRA', 'ENTG', 'ONTO', 'TRMB', 'BNTX', 'PFE', 'MRNA', 'NVAX', 'FCX', 'CF', 'DRI', 
    'PEP', 'XOM', 'LLY', 'CL', 'MCD', 'KO', 'GE', 'CVX', 'FISV', 'DE', 'WM', 'HLT', 'FUTU', 'UBER', 
    'TIGR', 'EQIX', 'DPZ', 'CSCO', 'COKE', 'SONY', 'FDS', 'MCO', 'GRAB', 'PTON', 'AMT', 'LIT', 'CMG', 'IPO', 
    'INMD', 'NNDM', 'MP', 'FUBO', 'SPOT', 'ALGN', 'PZZA', 'LOVE', 'LMND', 'POOL', 'PLTR', 'ROKU', 
    'CELH', 'NFLX', 'DHI', 'DELL'
]

KNOWN_STOCKS = list(dict.fromkeys(KNOWN_STOCKS))

def run_screener():
    print(f"Downloading historical data for {len(KNOWN_STOCKS)} stocks...")
    raw_data = yf.download(KNOWN_STOCKS, period="6mo", interval="1d", auto_adjust=True, progress=False)

    matching_stocks = []

    for ticker in KNOWN_STOCKS:
        try:
            if isinstance(raw_data.columns, pd.MultiIndex):
                if ticker not in raw_data.columns.levels[1]:
                    continue
                df = pd.DataFrame({
                    'Open': raw_data['Open'][ticker],
                    'High': raw_data['High'][ticker],
                    'Low': raw_data['Low'][ticker],
                    'Close': raw_data['Close'][ticker],
                    'Volume': raw_data['Volume'][ticker]
                }).dropna()
            else:
                df = raw_data[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()

            if len(df) < 50:
                continue

            close_ser = df['Close']
            high_ser = df['High']
            low_ser = df['Low']
            vol_ser = df['Volume']

            latest_close = float(close_ser.iloc[-1])
            latest_low = float(low_ser.iloc[-1])
            latest_vol = float(vol_ser.iloc[-1])

            # Condition 1: Price > 20
            if latest_close <= 20:
                continue

            sma50_close = close_ser.rolling(window=50).mean().iloc[-1]
            sma50_vol = vol_ser.rolling(window=50).mean().iloc[-1]

            if pd.isna(sma50_close) or pd.isna(sma50_vol) or sma50_vol == 0:
                continue

            # ATR(14)
            tr = pd.concat([
                high_ser - low_ser,
                (high_ser - close_ser.shift(1)).abs(),
                (low_ser - close_ser.shift(1)).abs()
            ], axis=1).max(axis=1)
            
            atr14 = tr.rolling(window=14).mean().iloc[-1]

            if pd.isna(atr14) or atr14 == 0:
                continue

            # Condition 2: LoD <= 70
            lod_dist = 100 * (latest_close - latest_low) / atr14
            if lod_dist > 70:
                continue

            # Condition 3: ATR extension <= 4
            atr_extension = (latest_close - sma50_close) / atr14
            if atr_extension < 0 or atr_extension > 4.0:
                continue

            # Condition 4: Rel Vol >= 25%
            rel_vol = (latest_vol / sma50_vol) * 100
            if rel_vol < 25.0:
                continue

            matching_stocks.append({
                'ticker': ticker,
                'price': round(latest_close, 2),
                'lod_dist': round(lod_dist, 1),
                'atr_extension': round(atr_extension, 2),
                'rel_vol': round(rel_vol, 1)
            })

        except Exception:
            continue

    return matching_stocks


def send_telegram_notification(matches):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Error: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment variables.")
        sys.exit(1)

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    if not matches:
        messages = [f"📊 *Stock Screener Alert ({today_str})*\n\nNo tickers fulfilled all criteria today."]
    else:
        header = (
            f"📊 *Stock Screener Results ({today_str})*\n"
            f"Found *{len(matches)}* stock(s) fulfilling all criteria:\n"
            f"• Price > $20\n• LoD < 70%\n• ATR Extension < 4x\n• Rel Vol ≥ 25%\n"
            f"----------------------------------------\n\n"
        )

        stock_lines = []
        for stock in sorted(matches, key=lambda x: x['ticker']):
            line = (
                f"• *{stock['ticker']}* — Price: *${stock['price']}*\n"
                f"   └ LoD: `{stock['lod_dist']}%` | ATR Ext: `{stock['atr_extension']}x` | Rel Vol: `{stock['rel_vol']}%`\n\n"
            )
            stock_lines.append(line)

        # Chunk messages to stay safely under Telegram's 4096 character limit
        messages = []
        current_msg = header

        for line in stock_lines:
            if len(current_msg) + len(line) > 3800:
                messages.append(current_msg)
                current_msg = line
            else:
                current_msg += line

        if current_msg:
            messages.append(current_msg)

    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    for idx, msg_text in enumerate(messages):
        payload = {
            "chat_id": chat_id,
            "text": msg_text,
            "parse_mode": "Markdown"
        }
        response = requests.post(telegram_url, json=payload, timeout=20)
        
        if response.status_code != 200:
            print(f"Failed to send Telegram message part {idx + 1}/{len(messages)}. Response {response.status_code}: {response.text}")
            sys.exit(1)

    print(f"Successfully sent {len(messages)} message(s) to Telegram for {len(matches)} matching stock(s).")


if __name__ == "__main__":
    results = run_screener()
    send_telegram_notification(results)
