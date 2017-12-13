from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os
import http.cookiejar
import json

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')


query = "clear1.jpg"# you can change the query for the image  here
image_type="ActiOn"
query= query.split()
query='+'.join(query)
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
print(url)
#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((str(link),Type))

print("there are total" , len(ActualImages),"images")

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib.request.Request(img, headers={'User-Agent' : header})
        raw_img = urllib.request.urlopen(req).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print("cntr",cntr)
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print("could not load : "+img)
        print(e)


### python2

from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


query = "clear1.jpg"# you can change the query for the image  here
image_type="ActiOn"
query= query.split()
query='+'.join(query)
url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
#http://www.google.com/searchbyimage?image_url=http://localhost:8888/notebooks/clear1.jpg"
print url
#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print  "there are total" , len(ActualImages),"images"

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print cntr
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e


API key  AIzaSyCtM_S87osTDTpBdQXmhhXdHxHdWUI3Dq8
CSE ID 015365584411748541007:xltepgoybmc

import requests
import os
import sys
import re
import shutil

url = 'https://www.googleapis.com/customsearch/v1?key={}&cx={}&searchType=image&q={}'
apiKey = os.environ['AIzaSyCtM_S87osTDTpBdQXmhhXdHxHdWUI3Dq8']
cx = os.environ['015365584411748541007:xltepgoybmc']
q = sys.argv[1]

i = 1
for result in requests.get(url.format(apiKey, cx, q)).json()['items']:
  link = result['link']
  image = requests.get(link, stream=True)
  if image.status_code == 200:
    m = re.search(r'[^\.]+$', link)
    filename = './{}-{}.{}'.format(q, i, m.group())
    with open(filename, 'wb') as f:
      image.raw.decode_content = True
      shutil.copyfileobj(image.raw, f)
    i += 1
Dear Dirk,
Here is the first round of feedback from our side. If there is anything unclear, we will be happy to discuss tomorrow. Please take into consideration the proposed selection of your case studies.

Very good introduction of the topic, the observation of separation of activities to the level of pedestrian traffic (and not only zoning) is an interesting place to focus on. It is important to talk abut the division of functions as a modernist heritage. 

However, I think it will be difficult to compare a 2 million (4 million metropolitan) people city of Brasilia (built for 500 000) which is in the middle of uninhabited land in Brazil and Seestadt Aspern at the outskirts of Vienna in the middle of urban Europe (connected by all kinds of transport and activity) - merely based on urban planning approaches. It is true that the approach to Brasilia is very radical and pervasive, but even in its manifestation it is not what is what it was planned to be (there is more people, more disorder). Brasilia is the political capital of a country. Seestadt is a suburb.

I think it would be better to find a similar context to Seestadt Aspern when a modernist extra-city was constructed at outskirts of a larger city. An example that comes to mind is New Belgrade - a modernist suburb entirely constructed on modernist principles, after WWII (I have some literature on this). There is of course a lot of other examples. It would be equally interesting to choose one near Vienna or, even more interesting to opt for Lelystad near Amsterdam, https://en.wikipedia.org/wiki/Lelystad (it has similar economical premises as Austria, it was built in one go, founded in 1967 and very prominently modern).

In any case (whichever comparison you decide to make) a concrete framework of comparison needs to be articulated: are you going to look for the way pedestrian zones are embedded (or not even planned) in the two cases? Or are you going to look more into the organization of public space in general, and zoning? Design of public space? This can be answered through a recount of the two approaches (modernist approach, Jan Gehl approach) which can be the starting point for the work to be done on the thesis. You should focus on the way certain policies are articulated (I am not at all familiar with the work of Jan Gehl apart from his movie The Human Scale; I do not know how he articulates a planning approach, and if at all). For tomorrow's presentation, you should be able to introduce him to us.

Best Regards,
