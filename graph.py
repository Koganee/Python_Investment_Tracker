from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import yfinance as yf

def plot_stock(ticker_symbol, period, container_frame):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period)

    fig = Figure(figsize=(12, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(data.index, data['Close'], label="Close Price", color="blue")
    ax.set_title(f"{ticker_symbol} Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(True)

    # Clear old plots (if any)
    for widget in container_frame.winfo_children():
        widget.destroy()

    # Embed in Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=container_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
