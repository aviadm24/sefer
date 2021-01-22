from django.shortcuts import render
import requests
from .models import Index, Texts


def index(request):
    url = "http://www.sefaria.org/api/index"
    if not Index.objects.filter(url=url).exists():
        print("index response not saved in db")
        response = requests.get(url)
        response.raise_for_status()
        model = Index()
        model.url = url
        model.json = response.json()
        model.save()
    else:
        print("index response all ready saved in db")
        model = Index.objects.get(url=url)
    indexNames = []
    for subJson in model.json:
        catDict = {}
        print(subJson["heCategory"])
        catDict['heCat'] = subJson["heCategory"]
        catDict['cat'] = subJson["category"]
        indexNames.append(catDict)
    print(indexNames)
    jsonResponse = dict(model.json[1])
    mainDict = {}
    for c in jsonResponse["contents"]:
        subDict = {}
        # print(c["heCategory"])
        for co in c["contents"]:
            # print(co.keys())
            try:
                subDict[co["heTitle"]] = co["title"].replace(' ', '_')
                # print('\t'+co["heTitle"])
            except:
                # print('\t'+co["heCategory"])
                subDict[co["heCategory"]] = co["category"]
        mainDict[c["heCategory"]] = subDict
    # print(mainDict)

    # print(type(jsonResponse))

    return render(request, "index.html", {"jsonResponse": mainDict, "indexNames": indexNames})


def titles(request):
    response = requests.get("http://www.sefaria.org/api/index/titles")
    response.raise_for_status()
    # access JSOn content
    jsonResponse = dict(response.json())
    print("Entire JSON response")
    print(jsonResponse)

    return render(request, "titles.html", {"jsonResponse": jsonResponse})


def texts(request, slug=None, chapter=None):
    print(slug)
    if chapter:
        url = "http://www.sefaria.org/api/texts/{}.{}".format(slug.replace('_', ' '), chapter)
    else:
        url = "http://www.sefaria.org/api/texts/{}".format(slug.replace('_', ' '))
    print(url)
    if not Texts.objects.filter(url=url).exists():
        print("texts response not saved in db")
        response = requests.get(url)
        response.raise_for_status()
        model = Texts()
        model.url = url
        model.json = response.json()
        model.save()
    else:
        print("texts response all ready saved in db")
        model = Texts.objects.get(url=url)
    jsonResponse = dict(model.json)
    print(jsonResponse.keys())
    length = jsonResponse['length']
    book = jsonResponse['book'].replace(' ', '_')
    return render(request, "texts.html", {"jsonResponse": jsonResponse["he"], "length": length, "range": range(1, length+1),
                                          'book': book})