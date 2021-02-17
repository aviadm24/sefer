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
