from django.shortcuts import render
import requests
from .models import Index, Texts, TitleMeta


def tree_parse(jsonDict=None, index=None, returnDict=None):
    print("index: ", index)
    index += 1
    try:
        if "contents" in jsonDict.keys():
            tree_parse(jsonDict=jsonDict["contents"], index=index, returnDict=returnDict)
    except (AttributeError, KeyError):
        subDict= {}
        if type(jsonDict)=="dict":
            try:
                subDict[jsonDict["heTitle"]] = jsonDict["title"].replace(' ', '_')
                print('\t'*index + jsonDict["title"])
            except KeyError:
                # print('\t'+co["heCategory"])
                subDict[jsonDict["heCategory"]] = jsonDict["category"].replace(' ', '_')
                print('\t'*index + jsonDict["category"])
            try:
                returnDict[jsonDict["heCategory"]] = subDict
            except KeyError:
                returnDict[jsonDict["heTitle"]] = subDict
        else:
            for elem in jsonDict:
                tree_parse(jsonDict=elem, index=index, returnDict=returnDict)
                # try:
                #     subDict[elem["heTitle"]] = elem["title"].replace(' ', '_')
                #     print('\t' * index + jsonDict["title"])
                # except KeyError:
                #     # print('\t'+co["heCategory"])
                #     subDict[elem["heCategory"]] = elem["category"].replace(' ', '_')
                #     print('\t' * index + jsonDict["category"])
                # try:
                #     returnDict[elem["heCategory"]] = subDict
                # except KeyError:
                #     returnDict[elem["heTitle"]] = subDict
    return returnDict


def get_contents(sub_dict):
    try:
        for s in sub_dict["contents"]:
            print('\t\t\t\t' + str(s.keys()))
            get_contents(s)
    except:
        try:
            print('\t\t\t\t\t', sub_dict["title"])
            print("sb: ", {sub_dict["heTitle"]: sub_dict["title"].replace(' ', '_')})
        except KeyError:
            print("key error in :", sub_dict)
            return {}
        return {sub_dict["heTitle"]: sub_dict["title"].replace(' ', '_')}


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
        # print(subJson["heCategory"])
        catDict['indexNum'] = num
        catDict['heCat'] = subJson["heCategory"]
        catDict['cat'] = subJson["category"]
        indexNames.append(catDict)
    # print(indexNames)
    jsonResponse = dict(model.json[number])
    mainDict = {}
    # index = 0
    # mainDict = tree_parse(jsonDict=jsonResponse, index=index, returnDict=mainDict)
    for c in jsonResponse["contents"]:
        subDict = {}
        subList = []
        print(c.keys())
        try:
            for co in c["contents"]:
                print(co.keys())
                try:
                    subDict[co["heTitle"]] = co["title"].replace(' ', '_')
                    subList.append(subDict)
                    print('\t\t'+co["title"])
                except KeyError:
                    # print('\t'+co["heCategory"])
                    sb = get_contents(co)
                    print("sb: ", sb)
                    subDict = sb
                    subList.append(subDict)
                    # subDict[co["heCategory"]] = co["category"].replace(' ', '_')
                    # print('\t\t\t' + co["category"])
                except TypeError:
                    try:
                        sb = get_contents(co)
                        print("sb: ", sb)
                        subDict = sb
                        subList.append(subDict)
                        # for i in co["contents"]:
                        #     print('\t\t\t\t'+str(i.keys()))
                        #     for ii in i["contents"]:
                        #         print('\t\t\t\t\t', i.keys())
                    except KeyError:
                        pass

        except KeyError:  # from dict(model.json[number]) number 3 and on
            try:
                subDict[c["heTitle"]] = c["title"].replace(' ', '_')
                print('\t'+c["title"])
            except:
                print('\tcategory:'+c["heCategory"])
                subDict[c["heCategory"]] = c["category"].replace(' ', '_')
        try:
            mainDict[c["heCategory"]] = subList
            print(len(subList))
        except KeyError:
            mainDict[c["heTitle"]] = subList''
    print(mainDict)

    # print(type(jsonResponse))

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
        url = "http://www.sefaria.org/api/index/{}".format(slug.replace('_', ' '))
        print("url: ", url)
        if not TitleMeta.objects.filter(url=url).exists():
            print("index response not saved in db")
            response = requests.get(url)
            response.raise_for_status()
            model = Index()
            model.url = url
            model.json = response.json()
            model.save()
        else:
            print("index response all ready saved in db")
            model = TitleMeta.objects.get(url=url)
        jsonResponse = dict(model.json)
        print("keys: ", jsonResponse.keys())
        return render(request, "texts.html", {'error': jsonResponse["error"], 'book': "no var book found"})