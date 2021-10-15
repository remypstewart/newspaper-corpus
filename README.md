### [Return to Portfolio Directory](https://remypstewart.github.io/)

The digitization of traditional media outlets has facilitated the integration of natural language processing techniques to understand relevant social topics. For one of my dissertation chapters I will be examining how local newspapers reinforce cultural stereotypes around race, gender, and class that drives individual political preferences. There is a lack of preestablished data sets for regional newspapers compared to national level sources such as the New York Times or Google News. Given that local media outlets influence policy opinions that regional residents can have a sizable influence over compared to national politics, I wanted to address this data source gap through compiling an original newspaper corpus. 

I focused on the [San Francisco Chronicle](https://www.sfchronicle.com/) as the city’s major local newspaper as digitally archived on [Access World Database](https://www.newsbank.com/libraries/colleges-universities/solutions/access-world-news-research-collection-2021-edition) that I hold a subscription with through my Cornell University Library affiliation. A common issue with web scraping data is having to automate the navigation of nested website pages, such as articles stored within the hierarchy of a collection of links for a particular day within a year. The selenium library provides a headless web driver to browse through individual daily URLs through nested links. I instantiate a Chrome driver instance from a previously downloaded executable file included in my path directory. I also load in a list of all individual SF Chronical daiy links spanning from January 1st to September 30th of 2021 that I obtained from an early webscrape. 

```python
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import newspaper
from newspaper import Article
from newspaper import Config


data_2021 = pd.read_csv('data_2021.csv')
url_list = data_2021['URL'].to_list()

opts = Options()
opts.add_argument(" --headless")
chrome_driver = os.getcwd() +"/chromedriver.exe"
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
```

Beautiful Soup is an additional web scraping library that is particularly well suited to extract page information from HTML div and class tags. After having the driver extract the page source from the daily article listings, I identify the link classes that include the individual article links to process into a seperate dataframe. An initial review of the title demonstrates that each link will lead to a seperate digitized article with the titles serving as a validity check to the successful link extraction. 

```python
article_links = pd.DataFrame()

url_list_title = []
url_list_url =[]


for url in url_list:
    url_list_title = []
    url_list_url =[]
    
    driver.get(url)
    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file)
    print(soup.title.get_text())
    results = soup.find_all("a", class_= "toc__item--link")
    for results in results:
        count = 0
        
        link = results.get('href')
        list_url.append(link)
        name = results.get('title')
        list_title.append(name)
        
        count +=1

    temp_df = pd.DataFrame({'URL': list_url, 'Title': list_title})
    # Append to the final DataFrame
    article_links = article_links.append(temp_df, ignore_index = True)
    print(article_links)
```
![alt text](/images/selenium.png)

Before moving to scraping individual articles, I perform some light preprocessing by dropping duplicate urls, adding the protocol and domain parameters to each URL, and generating a list of article links to iterate through within the next code block of the scrape. 

```python
article_links = article_links.drop_duplicates(subset=['URL'])
article_links['full_url'] = 'https://infoweb.newsbank.com' + article_links['URL'].astype(str)
urls = article_links['full_url'].tolist()
print(urls)
```
![alt text](/images/URLS.png)

With my nested extraction of article links from individual days completed, I then employ the Newspaper3k library to extract relevant article information such as the author, posting date, and article body text into a Pandas dataframe. This package is specifically designed for newspaper scraping and is effective at identifying article metadata across domain formats. The extraction is nested in a try-except block to account for potential errors such as dead URLs. I set some additional configuration parameters by identifying my browser's user agent to bypass the site log in requirements, as well as set a request rest period to prevent site permission denials caused by excessive queries within a short time frame.  

```python
rows = []

config = Config()
config.browser_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47"
config.request_timeout = 10

for url in url_long:
    try:
        a = Article(url,config=config, language='en')
        a.download()
        a.parse()
         
        author = a.authors
        title = a.title
        text = a.text
        
        print(author, title, text)
        row = {'url':url,'author':author, title':title,'text':text}
        rows.append(row)
               
    except Exception as e:
        print(e)
        row = {'url':url,'author':'N/A','title':'N/A','text':'N/A'}
        rows.append(row)
        
df = pd.DataFrame(rows)
```
![alt text](/images/articles.png)

An initial review of the extraction results indicates further processing and cleaning is needed to prepare a final product dataset of individual SF Chronicle articles. 
Remove the substantively meaningless "Author Byline" and brakets from the Author column
Seperate out from the "title" column both the name of the piece and the published date
Clean the article body text by removing line break parameters, 
View an individual article to check if the additional dataset cleaning was sucessful 


```python
```
![alt text](/images/clean.png)


