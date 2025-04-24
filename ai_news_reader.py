import os
from openai import OpenAI
from shared_data import article_array

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
def summarize_text(article_array):
    for i, url in enumerate(article_array):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes financial news articles."},
                    {"role": "user", "content": f"Summarize the news article from this URL: {url}"}
                ]
            )
            summary = response.choices[0].message.content
            print(f"\nSummary {i+1} for {url}:\n{summary}\n")

        except Exception as e:
            print(f"Error summarizing article {i+1} ({url}): {e}")
