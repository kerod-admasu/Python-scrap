import botogram
import requests
from bs4 import BeautifulSoup
from io import BytesIO

chan = botogram.channel("@kerod_chan", "6901794159:AAFGaxUs_CWvLARysrPG0zYcRgPz6BjaGms") 

def scrape_news():
    url = "http://www.aau.edu.et/blog/category/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_articles = []
    all_content = soup.find('div', id='content')
    article_elements = all_content.find_all('div', class_='post')

    for article in article_elements:
        title = article.h2.a.text
        description_content = article.find('div', class_="entry")
        description = description_content.p.text.strip()
        link = description_content.a['href']

        # Extract image URL
        image_tag = article.find('img', class_='wp-post-image')
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None

        news_articles.append({'title': title, 'description': description, 'link': link, 'image_url': image_url})

    return news_articles

news = scrape_news()

for new in news:
    title = new['title']
    description = new['description']
    image_url = new.get('image_url', '')

    # Send text
    chan.send(title)
    chan.send(description)

    # Send image
    if image_url:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_data = BytesIO(image_response.content)
            chan.send_photo(image_data, caption=f"Image for {title}")
