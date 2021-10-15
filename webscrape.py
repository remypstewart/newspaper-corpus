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

# Set up selenium headless Chrome browser
opts = Options()
opts.add_argument(" --headless")
chrome_driver = os.getcwd() +"/chromedriver.exe"
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

# Extract article URLs on daily pages 
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
    
# Clean article links
article_links = article_links.drop_duplicates(subset=['URL'])
article_links['full_url'] = 'https://infoweb.newsbank.com' + article_links['URL'].astype(str)
urls = article_links['full_url'].tolist()
print(urls)

# Process article metadata into dataframe
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

# Clean article extraction





