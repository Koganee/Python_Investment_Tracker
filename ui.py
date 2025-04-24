import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import matplotlib.pyplot as plt
import json
from graph import plot_stock
from news import get_news
from ai_news_reader import summarize_text
import openai

# Function to load the portfolio (from a JSON file)
def load_portfolio():
    try:
        with open("portfolio.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save the portfolio to a JSON file
def save_portfolio(portfolio):
    with open("portfolio.json", "w") as f:
        json.dump(portfolio, f)

# Function to add a stock to the portfolio
def add_investment():
    ticker = ticker_entry.get().upper()
    shares = float(shares_entry.get())
    
    if not ticker or shares <= 0:
        messagebox.showerror("Input Error", "Please enter a valid ticker and number of shares.")
        return
    
    portfolio = load_portfolio()
    
    # Check if the ticker exists
    stock = yf.Ticker(ticker)
    try:
        stock.history(period="1d")
    except Exception as e:
        messagebox.showerror("Invalid Ticker", f"Could not find ticker: {ticker}")
        return
    
    if ticker in portfolio:
        portfolio[ticker] += shares
    else:
        portfolio[ticker] = shares

    save_portfolio(portfolio)
    messagebox.showinfo("Investment Added", f"Added {shares} shares of {ticker}")

# Function to display the portfolio
def view_portfolio():
    portfolio = load_portfolio()
    portfolio_text.delete(1.0, tk.END)  # Clear previous text
    for widget in input_frame.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") not in ["Add Investment", "View Portfolio"]:
            widget.destroy()

    if not portfolio:
        tk.Label(input_frame, text="Your portfolio is empty.", fg="green", bg="black", font=("Courier", 12)).pack()
        return

    for ticker, shares in portfolio.items():
        button = tk.Button(input_frame, text=f"{ticker}: {shares} shares", fg="green", bg="black", relief="flat", font=("Courier", 12), command=lambda t=ticker: (plot_stock(t, "6mo", graph_frame), get_news(t, news_frame)))
        button.pack(pady=5, fill="x")

    portfolio_text.delete(1.0, tk.END)
    total_value = 0
    for ticker, shares in portfolio.items():
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")
            if not history.empty:
                current_price = history["Close"].iloc[-1]
                value = shares * current_price
                total_value += value
                portfolio_text.insert(tk.END, f"{ticker}: {shares} shares @ ${current_price:.2f} = ${value:.2f}\n")
            else:
                portfolio_text.insert(tk.END, f"{ticker}: ❌ No data available\n")
        except Exception as e:
            portfolio_text.insert(tk.END, f"{ticker}: ⚠️ Error: {e}\n")

    portfolio_text.insert(tk.END, f"\nTotal Portfolio Value: ${total_value:.2f}")


# Setting up the main window
root = tk.Tk()

root.title("Investment Tracker")
input_frame = tk.Frame(root, bg="black")
input_frame.pack(side="left", fill="y", padx=20)

graph_frame = tk.Frame(root, bg="black")
graph_frame.pack(side="top", fill="x", anchor="nw", expand=True)

news_frame = tk.Frame(root, bg="black")
news_frame.pack(side="top", fill="x", anchor="se")

graph_frame.config(highlightbackground="green", highlightthickness=2)

# Draw a border around the input frame
input_frame.config(highlightbackground="green", highlightthickness=2)

news_frame.config(highlightbackground="green", highlightthickness=2)

# Update input fields and buttons to input_frame
ticker_label = tk.Label(input_frame, text="Enter Stock Ticker:", fg="green", bg="black", font=("Courier", 12))
ticker_label.pack()

ticker_entry = tk.Entry(input_frame, fg="green", bg="black", insertbackground="green", font=("Courier", 20))
ticker_entry.pack()

shares_label = tk.Label(input_frame, text="Enter Number of Shares:", fg="green", bg="black", font=("Courier", 12))
shares_label.pack()

shares_entry = tk.Entry(input_frame, fg="green", bg="black", insertbackground="green", font=("Courier", 20))
shares_entry.pack()

add_button = tk.Button(input_frame, text="Add Investment", command=add_investment, fg="green", bg="black", relief="flat", font=("Courier", 12))
add_button.pack()

view_button = tk.Button(input_frame, text="View Portfolio", command=view_portfolio, fg="green", bg="black", relief="flat", font=("Courier", 12))
view_button.pack()

portfolio_text = tk.Text(input_frame, width=50, height=5, fg="green", bg="black", insertbackground="green", font=("Courier", 20))
portfolio_text.pack()

# Set the background color to black and text color to green for the terminal-like theme
root.configure(bg="black")

# Start the Tkinter event loop
root.mainloop()
