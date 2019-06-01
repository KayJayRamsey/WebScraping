import pandas as pd 
import requests 
from bs4 import BeautifulSoup as bs
import os 
from splinter import Browser
import time 

def init_browser():
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser('chrome', **executable_path, headless=True) 
    return browser


def scrape():

    browser = init_browser()
    
    URL = "https://mars.nasa.gov/news/"
    browser.visit(URL)

    html = browser.html
    soup = bs(html, "html.parser")

    #elem = soup.select_one("ul.item_list li.slide")
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()


    URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" 
    browser.visit(URL) 
    
    html_visit = browser.html 
    time.sleep(1) 
    soup = bs(html_visit, 'html.parser') 

    #elem = soup.select_one("ul.item_list li.slide")
    relative_image_path = soup.find_all('img')[2]["src"] 
    featured_image_url = URL + relative_image_path 
    #print(featured_image_url)  
    

    URL = "https://twitter.com/marswxreport?lang=en" 
    browser.visit(URL) 
    
    html_visit = browser.html 
    soup = bs(html_visit, 'html.parser') 
    
    #elem = soup.select_one("ul.item_list li.slide")
    mars_weather_tweet = soup.find('div', class_='js-tweet-text-container').get_text()  
    mars_weather_tweet 
    #mars_weather_tweet.replace('\n', "")   
  

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    time.sleep(1)

    tables = pd.read_html(url)
    
    df = tables[0] 
    html_table = df.to_html()   
    
    #browser.quit() 
    
    
    URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(URL) 
    html_visit = browser.html 
    time.sleep(1) 
    soup = bs(html_visit, 'html.parser') 

    link_display = browser.find_by_css('h3') 
    hemp_list = [] 
    {hemp_list.append(link.value.replace("Enhanced", "")) 
    for link in link_display} 
    hemp_list 

    url_list = []
    for hemp in hemp_list:
        browser.click_link_by_partial_text(hemp)
        image_object = browser.find_by_css('img.wide-image')
        img_url = image_object['src']
        url_list.append(img_url)
        browser.back()
    url_list 

    hemisphere_image_urls = []
    for hemp, url in zip(hemp_list, url_list):
        hemisphere_dict = {"title": hemp, "image_url": url}
        hemisphere_image_urls.append(hemisphere_dict) 
    hemisphere_image_urls 
    
    Mars = {"def_news_title": news_title, "def_news_p": news_p,"def_featured_image_url":featured_image_url,"def_mars_weather_tweet":mars_weather_tweet,
    "def_tables": html_table, "def_hemp_list": hemp_list, "def_url_list": url_list, "hemisphere_image_urls": hemisphere_image_urls} 
    
    browser.quit()
    return Mars    
    
    

    

if __name__ == "__main__":
    print(scrape()) 