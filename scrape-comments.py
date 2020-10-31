from selenium import webdriver
from selenium.common import exceptions
#from selenium.webdriver.chrome.options import Options
import sys
import time
import pandas as pd

def scrape(url):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')

    '''
        from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
     
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
     
    driver.get("chromedriver\chromedriver.exe")

    '''

    #chrome_options = Options()
    #chrome_options.add_argument("--incognito")
    #driver = webdriver.Chrome(options=options)

    driver=webdriver.Chrome("chromedriver\chromedriver",chrome_options=options)
    driver.get(url)
    #driver.maximize_window()
    time.sleep(5)

    try:
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        # Note: Youtube may have changed their HTML layouts for
        # videos, so raise an error for sanity sake in case the
        # elements provided cannot be found anymore.
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down 'til "next load".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # One last scroll just in case.
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    try:
        # Extract the elements storing the usernames and comments.
        # username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    print("> VIDEO TITLE: " + title + "\n")
    print("> COMMENTS:")

    comments=[]
    for comment in comment_elems:
        #print(comment.text + "\n")
        comments.append(comment.text)

    dataset=pd.DataFrame(comments)
    dataset.to_csv("comments.csv")
    print("Done!")

    driver.close()

if __name__ == "__main__":
    scrape("https://www.youtube.com/watch?v=eQJteHRyclI")