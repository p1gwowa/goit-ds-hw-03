import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

#  Function for getting urls for authors from every page
def get_url_author():
    url_list = []
    page_list = ['/page/1/']
    prev_len = len(page_list)
    html_doc = requests.get(URL)
    soup  = BeautifulSoup(html_doc.text, 'html.parser')
    
    page_sel = soup.select('div[class=col-md-8] nav ul[class=pager] li[class=next] a[href]')

# Condition for parsing from every page 
    while True:
        for page in page_sel:
            page_list.append(page['href'])
            sel = soup.select('div[class=quote] span a[href]')
            for link in sel:
                if link['href'] in url_list:
                    pass
                else:
                    url_list.append(link['href'])
        if len(page_list) != prev_len:
            prev_len = len(page_list)
        else:
            break
        html_doc = requests.get(URL + page['href'])
        soup  = BeautifulSoup(html_doc.text, 'html.parser')
        page_sel = soup.select('div[class=col-md-8] nav ul[class=pager] li[class=next] a[href]')

# Parsing from last page
        sel = soup.select('div[class=quote] span a[href]')
        for link in sel:
            if link['href'] in url_list:
                pass
            else:
                url_list.append(link['href'])
 
    return url_list

# Function for parsing of authors' info
def get_authors_info(author_sources: list):
   
    authors_list = []
    for link in author_sources:
        html_doc = requests.get(URL + link)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        sel = soup.select('div[class=author-details]')
        author_dict = {"fullname": None, 
                "born_date": None, 
                "born_location": None, 
                "description": None}
        for el in sel:
            author_dict["fullname"] = el.find('h3').text
            author_dict["born_date"] = el.find('span', attrs={'class': 'author-born-date'}).text
            author_dict["born_location"] = el.find('span', attrs={'class': 'author-born-location'}).text
            author_dict['description'] = el.find('div').text
        authors_list.append(author_dict)

    return authors_list

# Function for parsing tags
def get_tags():

    page_list = ['/page/1/']
    prev_len = len(page_list)
    html_doc = requests.get(URL)
    soup  = BeautifulSoup(html_doc.text, 'html.parser')
    tags_list = []
    page_sel = soup.select('div[class=col-md-8] nav ul[class=pager] li[class=next] a[href]')

# Condition for parsing from every page   
    while True:
        for page in page_sel:
            page_list.append(page['href'])
            
            quotes = soup.find_all('span', class_='text')
            authors = soup.find_all('small', class_='author')
            tags = soup.find_all('div', class_='tags')
            for i in range(0, len(quotes)):
                tag_dict = {"tags": [], 
                        "author": None, 
                        "quote": None}
                tag_dict['quote'] = quotes[i].text
                tag_dict['author'] = authors[i].text
                tagsforquote = tags[i].find_all('a', class_='tag')
                for tagforquote in tagsforquote:
                    tag_dict['tags'].append(tagforquote.text)
                tags_list.append(tag_dict)
        if len(page_list) != prev_len:
            prev_len = len(page_list)
        else:
            break
        html_doc = requests.get(URL + page['href'])
        soup  = BeautifulSoup(html_doc.text, 'html.parser')
        page_sel = soup.select('div[class=col-md-8] nav ul[class=pager] li[class=next] a[href]')

# Parsing from last page
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        for i in range(0, len(quotes)):                
            tag_dict = {"tags": [], 
                        "author": None, 
                        "quote": None}
            tag_dict['quote'] = quotes[i].text
            tag_dict['author'] = authors[i].text
            tagsforquote = tags[i].find_all('a', class_='tag')
            for tagforquote in tagsforquote:
                tag_dict['tags'].append(tagforquote.text)
            tags_list.append(tag_dict)    
        
    return tags_list


if __name__ == '__main__':

    URL = "http://quotes.toscrape.com"

# Creating .json files
    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(get_authors_info(get_url_author()), f, ensure_ascii=False, indent=4)

    with open('qoutes.json', 'w', encoding='utf-8') as f:
        json.dump(get_tags(), f, ensure_ascii=False, indent=4)
        
# Reading .json files for adding them to MongoDB
    with open('authors.json', 'r', encoding='utf-8') as file:
        data_authors = json.load(file)

    with open('qoutes.json', 'r', encoding='utf-8') as file:
        data_qoutes = json.load(file)

    client = MongoClient(
    "mongodb+srv://pigwowa:qwerty1234@cluster0.mz77bil.mongodb.net/",
    server_api=ServerApi('1')
    )
    
    db = client.parsing_book

# Inserting data to MongoDB
    insert_data_author = db.authors.insert_many(data_authors)

    insert_data_qoutes = db.qoutes.insert_many(data_qoutes)
