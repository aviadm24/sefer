from django.shortcuts import render
import requests
from .models import Index, Texts, MainCategories, TitleMeta, Links
import json


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def get_model(Model, url):
    if not Model.objects.filter(url=url).exists():
        print("index response not saved in db")
        response = requests.get(url)
        response.raise_for_status()
        model = Model()
        model.url = url
        model.json = response.json()
        model.save()
    else:
        print("index response all ready saved in db")
        model = Model.objects.get(url=url)
    return model


def index(request, number=0):
    print("number: ", number)
    url = "http://www.sefaria.org/api/index"
    model = get_model(Index, url)
    indexNames = []
    for num, subJson in enumerate(model.json):
        catDict = {}
        # print(subJson["heCategory"])
        catDict['indexNum'] = num
        catDict['heCat'] = subJson["heCategory"]
        catDict['cat'] = subJson["category"]
        indexNames.append(catDict)
    if not MainCategories.objects.filter(url=url).exists():
        mainCategories = MainCategories()
        mainCategories.url = url
        mainCategories.catJson = json.dumps(indexNames)
        mainCategories.save()

    jsonResponse = dict(model.json[number])
    mainDict = {}
    # index = 0
    # mainDict = tree_parse(jsonDict=jsonResponse, index=index, returnDict=mainDict)
    for c in jsonResponse["contents"]:
        titles = json_extract(c, "title")
        heTitles = json_extract(c, "heTitle")
        subDict = dict(zip(heTitles, titles))
        # print(subDict)
        try:
            mainDict[c["heCategory"]] = subDict
        except KeyError:
            mainDict[c["heTitle"]] = subDict
    # print(mainDict)
    return render(request, "index.html", {"jsonResponse": mainDict, "indexNames": indexNames})


def titles(request):
    response = requests.get("http://www.sefaria.org/api/index/titles")
    response.raise_for_status()
    # access JSOn content
    jsonResponse = dict(response.json())
    print("Entire JSON response")
    print(jsonResponse.keys())
    return render(request, "titles.html", {"jsonResponse": jsonResponse["books"]})


def texts(request, slug=None, chapter=None):
    print(slug)
    if chapter:
        url = "http://www.sefaria.org/api/texts/{}.{}".format(slug.replace('_', ' '), chapter)
        link_url = "http://www.sefaria.org/api/links/{}.{}".format(slug.replace('_', ' '), chapter)
        link_model = get_model(Links, link_url)
        jsonResponse = dict(link_model.json[0])
        print("linkes: ", jsonResponse)

    else:
        url = "http://www.sefaria.org/api/texts/{}".format(slug.replace('_', ' '))
        catJson = MainCategories.objects.get(url="http://www.sefaria.org/api/index").catJson
        indexNames = json.loads(catJson)
        if slug in [d.values() for d in indexNames]:
            model = get_model(Texts, url)
            jsonResponse = dict(model.json[0])
            # print("res: ", jsonResponse)
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
            return render(request, "index.html", {"jsonResponse": mainDict, "indexNames": indexNames})

    print(url)
    model = get_model(Texts, url)
    jsonResponse = dict(model.json)
    print("keys: ", jsonResponse.keys())
    try:
        book = jsonResponse['book'].replace(' ', '_')
        # print(jsonResponse["he"])
    except KeyError:
        print("no book key in json response")
    try:
        length = jsonResponse['length']
        return render(request, "texts.html",
                      {"jsonResponse": jsonResponse["he"], "length": length, "range": range(1, length + 1),
                       'book': book})
    except KeyError:
        next = jsonResponse['next']
        next = next.split(':')[0]
        print('next: ', next)

        return render(request, "texts.html",
                      {"jsonResponse": jsonResponse["he"], 'book': book, 'next': next})
    # try:
    # except:
    #     url = "http://www.sefaria.org/api/index/{}".format(slug.replace('_', ' '))
    #     print("url: ", url)
    #     if not TitleMeta.objects.filter(url=url).exists():
    #         print("index response not saved in db")
    #         response = requests.get(url)
    #         response.raise_for_status()
    #         model = Index()
    #         model.url = url
    #         model.json = response.json()
    #         model.save()
    #     else:
    #         print("index response all ready saved in db")
    #         model = TitleMeta.objects.get(url=url)
    #     jsonResponse = dict(model.json)
    #     print("keys: ", jsonResponse.keys())
    #     return render(request, "texts.html", {'error': jsonResponse["error"], 'book': "no var book found"})