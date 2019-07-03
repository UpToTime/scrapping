#webscrapper using requests and bs4
from bs4 import BeautifulSoup as bs
import requests

#check the websites robots.txt for allowed crawling sections
##e.g www.....com/robots.txt

#------------------static scrapping and exploring the page-------

#function to save the web page  locally
#requests fetchs the content using .get method
def save_html(url, path):
    html=requests.get(url)
    with open(path, 'wb') as f:
        f.write(html.content)
        
#function to open the saved page
def open_html(path):
    with open(path, 'rb') as f:
        return f.read()

#url of the webiste
url = 'https://www.allsides.com/media-bias/media-bias-ratings'

#save_html(url,'allsides')
html=open_html("allsides")

#beautifulsoup parsing
soup=bs(html,"html.parser")

#To find elements and data inside our HTML 
#select_one, single element
#select, which returns a list of elements
#Both of these methods use CSS selectors to find elements,
table_data = soup.select('tbody tr')
row=table_data[0]

name = row.select_one('.source-title').text.strip() #tag text
allsides_page = row.select_one('.source-title a')['href'] #getting a link
allsides_page = 'https://www.allsides.com' + allsides_page 
bias = row.select_one('.views-field-field-bias-image a')['href']
bias_side = bias.split('/')[-1]#getting anchor element 

agree = row.select_one('.agree').text
agree = int(agree)

disagree = row.select_one('.disagree').text
disagree = int(disagree)

agree_ratio = agree / disagree

'''select_one('body') gets the body eleement 
to get <a class="temp"></a> use select_one('.temp')
to get <a id="temp"></a> use select_one('#temp')
to get <a class="temp example"></a> use select_one('.temp.example')
to get <div class="temp"><a></a></div> use select_one('.temp a'). 
to get <div class="temp"><a class="example"></a></div> use select_one('.temp .example')'''
#--------------------------------------------------------------- scraping dynamically ------------
#main loop to collect data one time
from time import sleep

data= []
pages = [
    'https://www.allsides.com/media-bias/media-bias-ratings',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=1',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=2'
]#other webpages 
for page in pages:
    r = requests.get(page)
    soup = bs(r.content, 'html.parser')
    
    rows = soup.select('tbody tr')

    for row in rows:
        d = dict()

        d['name'] = row.select_one('.source-title').text.strip()
        d['allsides_page'] = 'https://www.allsides.com' + row.select_one('.source-title a')['href']
        d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
        d['agree'] = int(row.select_one('.agree').text)
        d['disagree'] = int(row.select_one('.disagree').text)
        d['agree_ratio'] = d['agree'] / d['disagree']

        data.append(d)
    
    sleep(10)

print("done scrapping wait for files")
import json

with open('allsides.json', 'w') as f:
    json.dump(data, f)

print("json file ready")
#save the data locally in json form.
import pandas as pd

df = pd.read_json(open('allsides.json', 'r'))

df.set_index('name', inplace=True)
#save the json to csv using pandas
df.to_csv("allsides.csv")
    
print("csv file ready")    
    
 







