
# [Mission to Mars](https://missiontomarz.herokuapp.com/)

Selenium and Splinter are not playing nicely with Heroku, so this does not work yet.

## Step 1 - Scraping
Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.


*  Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.

### NASA Mars News
*  Scrape the NASA Mars News Site ( https://mars.nasa.gov/news/ ) and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.


```python
import pandas as pd
import time
import requests
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup

#browser.windows.current.close()
```


```python
url01 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
```


```python
browser = Browser("chrome", headless=False)
```


```python
browser.visit(url01)
time.sleep(10) # Wait for that javascript to run and populate the page
```


```python
soup = BeautifulSoup(browser.html, "html.parser")
news_title = soup.find("div", class_="content_title").a.text.strip()
news_p = soup.find("div", class_="article_teaser_body").text
```

### JPL Mars Space Images - Featured Image


*  Visit the url for JPL's Featured Space Image here ( https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars ).
*  Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
*  Make sure to find the image url to the full size .jpg image.
*  Make sure to save a complete url string for this image.


```python
url02 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
```


```python
browser.visit(url02)
time.sleep(2)
browser.click_link_by_partial_text("FULL IMAGE")
time.sleep(2)
browser.click_link_by_partial_text("more info")
soup = BeautifulSoup(browser.html, "html.parser")
featured_image_url = "https://www.jpl.nasa.gov" + soup.article.figure.a["href"]
tiff_url = "https:" + soup.find("div", class_="download_tiff").a["href"]
jpg_url = "https:" + soup.find_all("div", class_="download_tiff")[1].a["href"]
```

### Mars Weather


*  Visit the Mars Weather twitter account here ( https://twitter.com/marswxreport?lang=en ) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.


```python
url03="https://twitter.com/marswxreport?lange=en"
```


```python
browser.visit(url03)
soup = BeautifulSoup(browser.html, "html.parser")
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
```

### Mars Facts


*  Visit the Mars Facts webpage here ( http://space-facts.com/mars/ ) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
*  Use Pandas to convert the data to a HTML table string.


```python
url04="http://space-facts.com/mars/"
```


```python
df = pd.read_html(url04)[0]
```


```python
df.columns = ["description", "value"]
df.set_index("description")
html_df = df.to_html()
html_df.replace("\n", "")
```




    '<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>description</th>      <th>value</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>Equatorial Diameter:</td>      <td>6,792 km</td>    </tr>    <tr>      <th>1</th>      <td>Polar Diameter:</td>      <td>6,752 km</td>    </tr>    <tr>      <th>2</th>      <td>Mass:</td>      <td>6.42 x 10^23 kg (10.7% Earth)</td>    </tr>    <tr>      <th>3</th>      <td>Moons:</td>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <th>4</th>      <td>Orbit Distance:</td>      <td>227,943,824 km (1.52 AU)</td>    </tr>    <tr>      <th>5</th>      <td>Orbit Period:</td>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <th>6</th>      <td>Surface Temperature:</td>      <td>-153 to 20 °C</td>    </tr>    <tr>      <th>7</th>      <td>First Record:</td>      <td>2nd millennium BC</td>    </tr>    <tr>      <th>8</th>      <td>Recorded By:</td>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>'



### Mars Hemisperes


*  Visit the USGS Astrogeology site here ( https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars ) to obtain high resolution images for each of Mar's hemispheres.
*  You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
*  Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
*  Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


```python
url05="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
```


```python
browser.visit(url05)
time.sleep(2)
soup = BeautifulSoup(browser.html, "html.parser")
# browser.click_link_by_partial_text('FULL IMAGE')
```


```python
url_base = "https://astrogeology.usgs.gov"
hemisphere_urls = []
for div in soup.find("div", class_="full-content").find_all("div", class_="item"):
    hemisphere_urls.append(url_base + div.a["href"])
```


```python
hemisphere_list = []
for urls in hemisphere_urls:
    print(urls)
    browser.visit(urls)
    time.sleep(2)
    soup = BeautifulSoup(browser.html, "html.parser")
    hemisphere_image_url = soup.find("div", class_="downloads").find_all("li")[1].a["href"]
    hemisphere_name = soup.find("h2", class_="title").text
    hemisphere_dict = {"img_url": hemisphere_image_url,
                       "title": hemisphere_name}
    hemisphere_list.append(hemisphere_dict)
```

    https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced
    


```python
hemisphere_list
```




    [{'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif',
      'title': 'Cerberus Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif',
      'title': 'Schiaparelli Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif',
      'title': 'Syrtis Major Hemisphere Enhanced'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif',
      'title': 'Valles Marineris Hemisphere Enhanced'}]


