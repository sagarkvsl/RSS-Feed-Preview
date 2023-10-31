from flask import Flask, render_template, request
import feedparser
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    feed_url = request.form.get('feed_url')
    feed = feedparser.parse(feed_url)
    entries = feed.entries

    for entry in entries:
        if 'content' in entry:
            for content in entry.content:
                if content.type == 'text/html':
                    content_html = content.value
                    # Extract image URLs using BeautifulSoup (you need to install BeautifulSoup4).
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(content_html, 'html.parser')
                    images = [img['src'] for img in soup.find_all('img')]
                    if images:
                        entry.image_url = images[0]
                    break

    return render_template('preview.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
