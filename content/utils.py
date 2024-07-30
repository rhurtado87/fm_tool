import yfinance as yf

def fetch_stock_from_yahoo(symbol_or_company_name):
    try:
        stock = yf.Ticker(symbol_or_company_name)
        data = stock.history(period='1d')

        if data.empty:
            return None, f"No stock data found for {symbol_or_company_name}. Please check the symbol or company name and try again."

        latest_data = data.iloc[-1]
        return {
            'symbol': stock.ticker,
            'name': stock.info['longName'],
            'price': latest_data['Close']
        }, None

    except Exception as e:
        error_msg = f"Error fetching data: {str(e)}"
        print(error_msg)
        return None, error_msg
