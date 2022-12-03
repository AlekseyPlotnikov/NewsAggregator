import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from .models import Headline

requests.packages.urllib3.disable_warnings()


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    print(len(headlines))
    context = {
        'object_list': headlines,
    }
    return render(request, "home.html", context)


def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.theonion.com/"

    content = session.get(url, verify=False).content
    soup = BSoup(content, "html.parser")
    #print(soup)
    News = soup.find_all('div', {"class": "sc-12t6q4b-1 bUFifn"})
    #пока не понятно что сюда (class": ) вставлять
    #print(News)
    for artcile in News:
        #print(artcile)
        main = artcile.find_all('a')[0]
        link = main['href']

        #print(main.find('img')['srcset'])
        title = main['title']
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        if main.find('img')['srcset']:
            image_src = str(main.find('img')['srcset']).split(" ")[-4]
            new_headline.image = image_src
        else:
            new_headline.image = None
        #print(new_headline.url)

        new_headline.save()
    return redirect("../")
