import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)   


def scrape():
    browser = init_browser()

    mars_data = {
        "news_title": news_title(browser),
        "paragraph_text": paragraph_text(browser),
        "featured_image_url": featured_image(browser),
        "mars_table_html": mars_table(browser),
        "hemisphere_image_urls": hemispheres_image_urls(browser)
    }

    return mars_data

def news_title(browser):
    url = "https://redplanetscience.com"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = getattr(soup.find('div', class_='content_title'), 'text', None)

    return news_title

def paragraph_text(browser):
    url = "https://redplanetscience.com"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

     paragraph_text = getattr(soup.find('div', class_='article_teaser_body'), 'text', None)

    return paragraph_text
    
def featured_image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image = soup.find("div", class_='floating_text_area')

    featured_image_url = featured_image.find('a', class_='showimg fancybox-thumbs')['href']
    featured_image_url = url + featured_image_url
    
    return(featured_image_url)

def mars_table(browser):
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table = mars_table.rename(columns={0:"Description", 1: ""})
    mars_table = mars_table.set_index("Description")
    mars_table_html = mars_table.to_html()
    mars_table_html = mars_table_html.replace('\n', '')
    mars_table.to_html('table.html')

    return mars_table_html


def hemispheres_image_urls(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemi_dict = {}

    for hemisphere in hemispheres:
    #     get a list of the Hemisphere titles
        hemi_dict['title'] = hemisphere.find('h3').text
    #     find the link to go to the hemisphere page
        hemisphere_link= hemisphere.find('a')['href']
    #     click to go to hemisphere page
        browser.visit(f'https://marshemispheres.com/{hemisphere_link}')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    #     find img url for full resolution image
        images = soup.find('img', class_='wide-image')['src']
    #     add website to image_url
        hemi_dict['image_urls'] = 'https://marshemispheres.com/'+ images
    #     add dictionary hemisphere_image_urls list
        hemisphere_image_urls.append(hemi_dict)

    return hemisphere_image_urls

  


