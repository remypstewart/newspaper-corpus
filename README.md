### [Return to Portfolio Directory](https://remypstewart.github.io/)

The digitization of traditional media outlets has facilitated the integration of natural language processing techniques to understand relevant social topics. For one of my dissertation chapters I will be examining how local newspapers reinforce cultural stereotypes around race, gender, and class that drives individual political preferences. There is a lack of preestablished data sets for regional newspapers compared to national level sources such as the New York Times or Google News corpus. Given that local media outlets influence policy opinions that regional residents can have a sizable influence over compared to national politics, I wanted to address this data source gap through compiling an original newspaper corpus. 

I focused on the [San Francisco Chronicle](https://www.sfchronicle.com/) as the city’s major local newspaper as digitally archived on [Access World Database](https://www.newsbank.com/libraries/colleges-universities/solutions/access-world-news-research-collection-2021-edition) that I hold a subscription with through my Cornell University Library affiliation. A common issue within web scraping is having to automate the navigation of nested pages, such as articles stored within the hierarchy of a collection of links for a particular day within a year. The selenium library provides a headless Chrome web driver to browse through the individual daily URLs.



```python
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import newspaper
from newspaper import Article
from newspaper import Config

opts = Options()
opts.add_argument(" --headless")
chrome_driver = os.getcwd() +"/chromedriver.exe"
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
```

to hold each day’s URLs for all SF Chronicle article from January 2021 to the end of September 2021. 


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


```python
article_links = article_links.drop_duplicates(subset=['URL'])
article_links['full_url'] = 'https://infoweb.newsbank.com' + article_links['URL'].astype(str)
urls = article_links['full_url'].tolist()
print(urls)
```
![alt text](/images/URLS.png)

Newspaper3k is designed to seamlessly extract relevant article information such as the author, posting date, and article body text. 


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

```python
```
