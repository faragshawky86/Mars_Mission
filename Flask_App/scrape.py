from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import time


def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)


def scrape_mars_nasa():
    browser = init_browser()

    # Visit site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news title
    news_title1 = soup.find("div",{"class":"content_title"})
    news_title = news_title1.find("a").text
   
    # Get the news paragraph text
    news_p = soup.findAll("div", {"class": "article_teaser_body"})[0].text

    # Store data in a dictionary
    mars_news_title ={
        "news_title": news_title,
        "news_p": news_p
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_news_title

def scrape_mars_jpl():
    browser = init_browser()

    # Visit site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get featured image
    get_featured_image_url= soup.find('article', {"class":"carousel_item"})["style"]
    featured_image_split = get_featured_image_url.split("background-image: url(")[1]
    featured_image_split2=featured_image_split.split(")")[0]
    featured_image_split3 = featured_image_split2.split("'")[1]
    
    base_url = "https://www.jpl.nasa.gov"
    
    featured_image_url = base_url + featured_image_split3


    # Store data in a dictionary
    mars_jpl_data = {
        "featured_image_url": featured_image_url
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_jpl_data


def scrape_mars_weather():
    browser = init_browser()

    # Visit site
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get featured image
    mars_weather= soup.find('p', {"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).text

    # Store data in a dictionary
    mars_weather_data = {
        "mars_weather": mars_weather
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_weather_data

def get_hemisphere_img():
    browser = init_browser()
    
    hemisphere_images = []
    for x in range(4):
        
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        
        browser.find_by_css("a.product-item h3")[x].click()
        
        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")
        
        base_url = "https://astrogeology.usgs.gov"

        # Get featured image
        hemisphere_title = soup.find('h2', {"class":"title"}).text
        hemisphere_image_urls = soup.find('img', {"class":"wide-image"})["src"]
        
        hemisphere_dict ={
            "title":hemisphere_title,
            "img_url": base_url + hemisphere_image_urls
        }

        # Store data in a dictionary
        hemisphere_images.append(hemisphere_dict)

        browser.back()

        # Return results
    return hemisphere_images

def get_mars_html():
    mars_table_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_table_url , encoding= "utf-8")
    mars_df = tables[0]
    mars_df.columns = ['Data Name', 'Data Value']
    mars_df.head()

    #html 
    html_table = mars_df.to_html()
    html_table1 = html_table.replace('\n', '')
    html_table2 = str(html_table1)
    html_table3 = html_table2.replace('<table border="1" class="dataframe">',"")
    html_table4 = html_table3.replace('</table>',"")

    mars_dict = {
        "mars_html": html_table4
    }

    return mars_dict





