import tkinter as tk
import requests
import webbrowser
from ai_news_reader import summarize_text
from shared_data import article_array

def open_url(url):
    webbrowser.open_new_tab(url)

def get_news(ticker, container_frame):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey=RZ9TR2URTTMNGMFR'
    r = requests.get(url)
    data = r.json()
    # Clear old content
    for widget in container_frame.winfo_children():
        widget.destroy() 

    for article in data.get("feed", [])[:2]:
        url = article.get("url")
        article_array.append(url)




    ai_button = tk.Button(container_frame, text="Generate AI Summary Of Articles", command=lambda: summarize_text(article_array), fg="white", bg="green", relief="raised", font=("Courier", 20), bd = 3, activebackground="black", activeforeground="green")
    ai_button.pack()    

    # Loop through each article in the "feed"
    for article in data.get("feed", []):
        title = article.get("title", "N/A")
        summary = article.get("summary", "N/A")
        published = article.get("time_published", "N/A")
        url = article.get("url")

        # Create a frame for each article
        article_frame = tk.Frame(container_frame, bg="black", padx=10, pady=5)
        article_frame.pack(fill="x", pady=5)

        # Title as button
        title_button = tk.Button(article_frame, text=title, fg="green", bg="black", font=("Courier", 12, "bold"), relief="flat", anchor="w", justify="left", wraplength=600, command=lambda url=url: open_url(url))
        title_button.pack(fill="x")

        # Summary
        summary_label = tk.Label(article_frame, text=summary, fg="white", bg="black", font=("Courier", 10), wraplength=600, justify="left")
        summary_label.pack(anchor="w")

        # Published time
        time_label = tk.Label(article_frame, text=f"Published: {published}", fg="gray", bg="black", font=("Courier", 8))
        time_label.pack(anchor="w")
