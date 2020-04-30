from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

# Set Executable Path & Initialize Chrome Browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    scrape_data={}

    # NASA Mars News Web Site Scrape
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Delay
    time.sleep(1)

    html = browser.html
    news_soup = bs(html, 'html.parser')
    mars_news = news_soup.find('li', class_='slide')
    news_title = mars_news.find('div', class_="content_title").text
    news_p = mars_news.find('div', class_="article_teaser_body").text
    # news_p
    # print(news_title)
    # print('-' * 25)
    # print(news_p)
    scrape_data['Article Title']=news_title
    scrape_data['Article Desc']=news_p

    # JPL Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Delay
    time.sleep(1)

    # Ask Splinter to Go to Site and Click full_image
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find "More Info" and Click It
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # parse results html with bs
    html = browser.html
    image_soup = bs(html, "html.parser")

    img_url = image_soup.select_one("figure.lede a img").get("src")
    # print(img_url)

    # Append previous result to main url
    featured_image_url = f"https://www.jpl.nasa.gov{img_url}"

    scrape_data['img_url']=featured_image_url


    # visit Mars weather twitter account
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Delay
    time.sleep(1)

    # Request information from Mars' twitter page
    twitter_weather = requests.get('https://twitter.com/marswxreport?lang=en')

    # Use bs object; parse with 'html.parser'
    weather_soup = bs(twitter_weather.text, "html.parser")

    # Parent container for the top weather tweet
    tweet_containers = weather_soup.find_all("div", class_='js-tweet-text-container')

    # Parse, print weather tweet
    mars_weather = tweet_containers[0].text
    # print(mars_weather) 

    scrape_data['Mars Weather']=mars_weather


    # Mars Facts Web Scraper (from pandas read)
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Delay
    time.sleep(1)

    # Read the tables from the webpage
    mars_facts = pd.read_html(url)

    # selecting table
    mars_facts_df = mars_facts[0]

    # rename df column
    mars_facts_df.columns = ["Mars Facts", "Values"]

    mars_facts_df.set_index("Mars Facts", inplace=True)

    # replacing line breaks with blanks by converting df to html table
    mars_story = (mars_facts_df.to_html()).replace('\n', '')

    scrape_data['Mars Story']=mars_story


    # Mars Hemispheres Web Scraper
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Delay
    time.sleep(2)

    # Get a list of all the hemispheres
    # looping through numbers of links 
    # find element on each loop
    # find sample image anchor tag & extract <href>

    hemisphere_img_urls = []
    links = browser.find_by_css("a.product-item h3")
    for i in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css('a.product-item h3')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere['img_url']  = sample_elem['href']
        hemisphere_img_urls.append(hemisphere)
        
        #navigate browser backwards
        browser.back()

    # Show list of dictionaries containing titles and url's
    scrape_data['Hemisphere One Title'] = hemisphere_img_urls[0]['title']
    scrape_data['Hemisphere One Image'] = hemisphere_img_urls[0]['img_url']

    scrape_data['Hemisphere Two Title'] = hemisphere_img_urls[1]['title']
    scrape_data['Hemisphere Two Image'] = hemisphere_img_urls[1]['img_url']

    scrape_data['Hemisphere Three Title'] = hemisphere_img_urls[2]['title']
    scrape_data['Hemisphere Three Image'] = hemisphere_img_urls[2]['img_url']

    scrape_data['Hemisphere Four Title'] = hemisphere_img_urls[3]['title']
    scrape_data['Hemisphere Four Image'] = hemisphere_img_urls[3]['img_url']

    # news_p
    # print(hemisphere_img_urls[0]['title'])
    # print('-' * 25)
    # print(hemisphere_img_urls[0]['title'])

    # Close browser after scraping
    browser.quit()

    return scrape_data

if __name__ == '__main__':
    print(scrape())

    























