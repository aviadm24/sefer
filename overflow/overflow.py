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


def excel_parsing(request):  # based on - https://github.com/anuragrana/excel-file-upload-django
    if request.method == "GET":
        return render(request, 'main/excel_parsing.html', {})
    else:
        print(request.POST)
        search_word = request.POST.get('search_word')
        print(request.FILES)
        excel_file = request.FILES.get("excel_file")
        df = pd.read_excel(excel_file, engine='openpyxl')
        print(list(df)[4])
        hamlaza = list(df)[4]
        options = [search_word]

        # selecting rows based on condition
        rslt_df = df[df[hamlaza].isin(options)]
        print("rslt_df:")
        print(rslt_df)
        # wb = openpyxl.load_workbook(excel_file)
        # sheets = wb.sheetnames
        # worksheet = wb[sheets[0]]
        # active_sheet = wb.active
        # excel_data = list()
        # for row_num, row in enumerate(worksheet.iter_rows()):
        #     if row_num > 50000:
        #         row_data = list()
        #         hasTheWord = False
        #         for cell in row:
        #             cell_data = str(cell.value)
        #
        #             if search_word in cell_data:
        #                 hasTheWord = True
        #                 cell_data = "<mark>"+cell_data+"</mark>"
        #                 print(cell_data)
        #             row_data.append(cell_data)
        #         if hasTheWord:
        #             excel_data.append(row_data)
        #     elif row_num <= 1:
        #         row_data = list()
        #         for cell in row:
        #             cell_data = str(cell.value)
        #             row_data.append(cell_data)
        #         excel_data.append(row_data)

        # return render(request, 'main/excel_parsing.html', {"excel_data": rslt_df})
        # https: // stackoverflow.com / questions / 48622486 / how - to - display - a - pandas - dataframe -as-datatable
        # https: // stackoverflow.com / questions / 52644035 / how - to - show - a - pandas - dataframe - into - a - existing - flask - html - table
        return render(request, 'main/excel_parsing.html', {"tables": [rslt_df.to_html(classes='dataframe', header="true")]})
