from django.shortcuts import render
import requests
from .models import Index, Texts


def index(request, number=0):
    print("number: ", number)
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
    for num, subJson in enumerate(model.json):
        catDict = {}
        print(subJson["heCategory"])
        catDict['indexNum'] = num
        catDict['heCat'] = subJson["heCategory"]
        catDict['cat'] = subJson["category"]
        indexNames.append(catDict)
    print(indexNames)
    jsonResponse = dict(model.json[number])
    mainDict = {}
    for c in jsonResponse["contents"]:
        subDict = {}
        print(c.keys())
        try:
            for co in c["contents"]:
                # print(co.keys())
                try:
                    subDict[co["heTitle"]] = co["title"].replace(' ', '_')
                    print('\t\t'+co["title"])
                except:
                    # print('\t'+co["heCategory"])
                    subDict[co["heCategory"]] = co["category"].replace(' ', '_')
                    print('\t\t\t' + co["category"])
        except KeyError:  # from dict(model.json[number]) number 3 and on
            try:
                subDict[c["heTitle"]] = c["title"].replace(' ', '_')
                print('\t'+c["title"])
            except:
                # print('\t'+co["heCategory"])
                subDict[c["heCategory"]] = c["category"].replace(' ', '_')
        try:
            mainDict[c["heCategory"]] = subDict
        except KeyError:
            mainDict[c["heTitle"]] = subDict
    print(mainDict)

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
    print("keys: ", jsonResponse.keys())
    try:
        book = jsonResponse['book'].replace(' ', '_')
        print(jsonResponse["he"])
    except KeyError:
        print("no book key in json response")
    try:
        length = jsonResponse['length']
        return render(request, "texts.html",
                      {"jsonResponse": jsonResponse["he"], "length": length, "range": range(1, length + 1),
                       'book': book})
    except KeyError:
        print("no length key in json response")

    if not jsonResponse["error"]:
        return render(request, "texts.html", {"jsonResponse": jsonResponse["he"], 'book': book})
    else:
        return render(request, "texts.html", {'error': jsonResponse["error"], 'book': "no var book found"})