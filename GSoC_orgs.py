import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from progress.bar import Bar
import sys
year = 2018
if len(sys.argv)==2:
        year = sys.argv[1]
url = 'https://summerofcode.withgoogle.com/archive/'+year+'/organizations/'

r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')

rows = soup.select('section div ul li')

link_list = []

for row in rows:
        abc = 'https://summerofcode.withgoogle.com' + row.select_one('a')['href']
        link_list.append(abc)

OrgName = []
Contactlink = []
techlist = []
slots = []
ideas = []

with Bar('Processing...',max=len(link_list)) as bar:
        for i,org_url in enumerate(link_list):
                lisat = []
                r = requests.get(org_url)
                soup = BeautifulSoup(r.text, 'html.parser')
                org = soup.find('div', class_="banner__text")              
                OrgName.append(f"=HYPERLINK(\"{org_url}\",\"{org.h3.text}\")")
                technologies = soup.find_all('li', class_="organization__tag--technology")
                for technology in technologies:
                        lisat.append(technology.text)
                mys = ', '.join(lisat)
                techlist.append(mys)
                irc = soup.select_one(".org__meta-button")['href']
                Contactlink.append(irc)
                projects = soup.find('ul', class_="project-list-container")
                slot = projects.findChildren('li')
                slots.append(len(slot))
                idea = soup.select_one(".org__button-container md-button")['href']
                # idea = ideas[0].select_one('md-button')['href']
                ideas.append(idea)
                bar.next()
        
        

table = {'Org' : OrgName , 'Technologies' : techlist , 'Slots' : slots , 'Ideas Page' : ideas , 'Contact' : Contactlink}

df = DataFrame(table)
export_csv = df.to_csv(r'GSoC-Orgs.csv')
        
print(r'Done!')
