import pandas as pd
import time
import requests
import os
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup

def init_browser():
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.binary_location = os.environ['GOOGLE_CHROME_BIN']
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], chrome_options=chrome_options)

def scrape():
    url01 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser = init_browser()

    browser.visit(url01)
    time.sleep(5) # Wait for that javascript to run and populate the page

    soup = BeautifulSoup(browser.html, "html.parser")
    news_title = soup.find("div", class_="content_title").a.text.strip()
    news_p = soup.find("div", class_="article_teaser_body").text

    url02 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url02)
    time.sleep(2)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(2)
    browser.click_link_by_partial_text("more info")
    soup = BeautifulSoup(browser.html, "html.parser")
    featured_image_url = "https://www.jpl.nasa.gov" + soup.article.figure.a["href"]
    tiff_url = "https:" + soup.find("div", class_="download_tiff").a["href"]
    jpg_url = "https:" + soup.find_all("div", class_="download_tiff")[1].a["href"]

    url03="https://twitter.com/marswxreport?lange=en"

    browser.visit(url03)
    soup = BeautifulSoup(browser.html, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    url04="http://space-facts.com/mars/"

    df = pd.read_html(url04)[0]

    df.columns = ["description", "value"]
    df.set_index("description")
    html_df = df.to_html(index=None)

    url05="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url05)
    time.sleep(2)
    soup = BeautifulSoup(browser.html, "html.parser")

    url_base = "https://astrogeology.usgs.gov"
    hemisphere_urls = []
    for div in soup.find("div", class_="full-content").find_all("div", class_="item"):
        hemisphere_urls.append(url_base + div.a["href"])

    hemisphere_list = []
    for urls in hemisphere_urls:
        browser.visit(urls)
        time.sleep(2)
        soup = BeautifulSoup(browser.html, "html.parser")
        hemisphere_image_url = soup.find("div", class_="downloads").find_all("li")[0].a["href"]
        hemisphere_name = soup.find("h2", class_="title").text
        hemisphere_dict = {"img_url": hemisphere_image_url,
                        "title": hemisphere_name}
        hemisphere_list.append(hemisphere_dict)
    
    return_dictionary = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "tiff_url": tiff_url,
        "jpg_url": jpg_url,
        "mars_weather": mars_weather,
        #"df": df,
        "html_df": html_df,
        "hemisphere_list": hemisphere_list
    }

    return return_dictionary