from logging import raiseExceptions
import requests
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup
import csv


#çıktı json veya veritabanı olarak olacak
#

def get_source(url):
#It pulls the source code of the page whose url is given in xml format.
        r = requests.get(url)
        if r.status_code == 200:
            return BeautifulSoup(r.content, "lxml")
        else:
            return False


def go_page_with_keyword(keyword): # gerek olmayabilir

    source = get_source(f"https://www.sikayetvar.com/{keyword}") 
    
    return source

def get_all_complaint_links(page_links,links_list):
#

    for link in page_links:
        # links_list.append(get_complaints_links(get_source(link),links_list))
        content = get_source(link)

        for link in content.find_all("h2", attrs={"class":"complaint-title"}):
            complaint_link = link.find("a").get("href")
            links_list.append("https://www.sikayetvar.com/" + complaint_link.strip())


    return links_list

def get_pages_links(search_url , max_page_number):
#max sayfa sayısına göre şikayetlerin sayfalarının urllerini oluşturur ve return eder

    search_pages_urls = []

    for i in range(1,int(max_page_number)):
        url_new = search_url + f"?page={i}".strip()
        search_pages_urls.append(url_new)
    
    return search_pages_urls

def find_total_page(content):
#toplam kaç sayfa şikayet olduğunu return eder
    page_number = []

    for a in content.find_all("a", attrs={"class": "pager"}):
        page_number.append(a.text)    
        
    return max(page_number)

def get_all_content(all_links):

    for link in all_links:

        source = get_source(link)

        title = get_title(source)
        author = get_author(source)
        date = get_complaint_date(source)
        paragraph = get_complaint_p(source)

        complaints_dict[link] = [title,author,date,paragraph]

    return complaints_dict
        
def get_title(source):
#şikayetin linkine gidip contenti alıp ordaki başlığı çeker
    try:
        title = source.find("h1", attrs={"class" : "complaint-title"})

        return title.text

    except:
        return "Şikayet yayından kaldırılmış"

def get_author(source):

    try:
        author = source.find("div", attrs = {"class" : "profile-desc"})

        return author.find("a").text
    except:
        return "Şikayet yayından kaldırılmış"

def get_complaint_date(source):

    try:
        date = source.find("span", attrs = {"class" : "post-time"})["title"]

        return date
    except:
        return "Şikayet yayından kaldırılmış"


def get_complaint_p(source):

    try:
        p = source.find("div", attrs = {"class" : "card-text"})

        return p.find("p").text
        
    except:
        return "Şikayet yayından kaldırılmış"

keyword = input("Marka veya kategori giriniz: ")

#go_page_with_keyword(keyword)

search_url = f"https://www.sikayetvar.com/{keyword}"

search_page_content = get_source(search_url)


links_list = []

complaints_dict = {}

complaint_links = []

total_page = find_total_page(search_page_content)
print(total_page)

all_links = get_all_complaint_links(get_pages_links(search_url, 10), links_list)

get_all_content(all_links)

df = DataFrame.from_dict(complaints_dict,orient = 'index', columns = ["Baslik", "yazar", "tarih", "sikayet"])  
df.to_csv("sikayetvar.csv",index = False)