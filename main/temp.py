def search_titles(request):
    url = "http://www.sefaria.org/api/index"
    model = get_model(Index, url)
    indexNames = get_index_names(model=model)
    listOfCatdict = []
    for number in range(len(indexNames)):
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
        listOfCatdict.append(mainDict)
    if request.POST:
        data = request.POST.dict()
        title = data.get('search_title')
        print('title: ', title)
    bookNameList = []
    for catDict in listOfCatdict:
        print(catDict.values())
        bookNameList.append(catDict.values())
    return render(request, "titles.html", {"bookNameList": bookNameList})
