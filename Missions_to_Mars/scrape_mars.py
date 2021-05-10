import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)   


def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    paragraph = soup.find('div', class_='article_teaser_body').text

    

    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image = soup.find("div", class_='floating_text_area')

    featured_image_url = featured_image.find('a', class_='showimg fancybox-thumbs')['href']
    featured_image_url = url + featured_image_url
    featured_image_url


    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table = mars_table.rename(columns={0:"Description", 1: ""})
    mars_table = mars_table.set_index("Description")
    mars_table_html = mars_table.to_html()
    mars_table_html = mars_table_html.replace('\n', '')
    mars_table.to_html('table.html')



    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for hemisphere in hemispheres:
    #     get a list of the Hemisphere titles
        title = hemisphere.find('h3').text
    #     find the link to go to the hemisphere page
        hemisphere_link= hemisphere.find('a')['href']
    #     click to go to hemisphere page
        browser.visit(f'https://marshemispheres.com/{hemisphere_link}')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    #     find img url for full resolution image
        images = soup.find('img', class_='wide-image')['src']
    #     add website to image_url
        image_urls = 'https://marshemispheres.com/'+ images
    #     create dictionary with img_urls and titles
        hemisphere = {"title": {title}, "img_url": {image_urls}}
    #     add dictionary hemisphere_image_urls list
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    data = {
        "news_title": "hello",
        "paragraph text": "paragraph here",
        "featured_image_url": featured_image_url,
        "mars_table_html": mars_table_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return data


