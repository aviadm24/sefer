from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Index, Texts, MainCategories, TitleMeta, Links, Ycomment
from .forms import YcommentForm, FileUploadForm
import json
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .gematria import int_to_gematria
import openpyxl
import pandas as pd
import numpy as np


class YcommentListView(ListView):
    model = Ycomment
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        form = FileUploadForm()
        context['form'] = form
        return context

    def get_queryset(self):
        return Ycomment.objects.filter(user=self.request.user)


def add_file(request):
    form = FileUploadForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    else:
        pass
    return redirect('ycomment-list')


def add_comment(request):
    form = YcommentForm()
    if request.method == "POST":
        # print("post: ", request.POST)
        form = YcommentForm(request.POST)  # if no files
        if form.is_valid():
            # print("form: ", form.cleaned_data)
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return JsonResponse({"msg": "comment successfully saved.", "user_name": request.user.username})
        else:
            return JsonResponse({"msg": "comment not saved.", "user_name": request.user.username})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_comment(request, id=0):
    print("id: ", id)
    comment = get_object_or_404(Ycomment, pk=id)  # Get your current cat

    if request.method == 'GET':  # If method is POST,
        comment.delete()  # delete the cat.
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {"msg": "comment deleted successfully"})


def is_authenticated(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return JsonResponse({"msg": "true", "user_name": request.user.username})
        else:
            return JsonResponse({"msg": "false"})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
        # print("index response not saved in db")
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


def get_json_field_or_empty_string(json, field):
    try:
        val = json[field]
    except KeyError:
        val = ''
    return val


def get_index_names(model=None):
    if not model:
        model = get_model(Index, "http://www.sefaria.org/api/index")
    indexNames = []
    for num, subJson in enumerate(model.json):
        catDict = {}
        catDict['indexNum'] = num
        catDict['heCat'] = subJson["heCategory"]
        catDict['cat'] = subJson["category"]
        indexNames.append(catDict)
    return indexNames


def get_correct_page_range(primary_category, length):
    page_list = []
    hebrewLetterList = []
    if primary_category == "Talmud":
        last = 0
        for num in range(2, int(length+2)//2+1):
            page_list.append(str(num)+'a')
            page_list.append(str(num)+'b')
            hebrewLetterList.append((str(num)+'a', int_to_gematria(str(num))+'.'))
            hebrewLetterList.append((str(num)+'b', int_to_gematria(str(num)) + ':'))
            last = num
        if length % 2 != 0:
            page_list.append(str(last+1) + 'a')
            hebrewLetterList.append((str(num)+'a', int_to_gematria(str(last+1)) + '.'))

        return page_list, hebrewLetterList
    else:
        return range(1, length + 1), hebrewLetterList


def get_next_prev(jsonResponse):
    try:
        next = jsonResponse['next']
        # print("next: ", next)
        prev = jsonResponse['prev']
        # print("prev: ", prev)
    except (KeyError, AttributeError):
        next = 'no next page'
        prev = 'no prev page'
    return next, prev


def home(request):
    url = "http://www.sefaria.org/api/index"
    model = get_model(Index, url)
    indexNames = get_index_names(model=model)
    if not MainCategories.objects.filter(url=url).exists():
        mainCategories = MainCategories()
        mainCategories.url = url
        mainCategories.catJson = json.dumps(indexNames)
        mainCategories.save()
    return render(request, "home.html", {"indexNames": indexNames})


def index(request, number=0):
    print("number: ", number)
    url = "http://www.sefaria.org/api/index"
    model = get_model(Index, url)
    indexNames = get_index_names(model=model)
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
    return render(request, "index.html", {"jsonResponse": mainDict, "indexNames": indexNames})


def titles(request):
    url = "http://www.sefaria.org/api/index/titles"
    model = get_model(Index, url)
    jsonResponse = dict(model.json)
    # print("Entire JSON response")
    # print(jsonResponse.keys())
    return render(request, "titles.html", {"jsonResponse": jsonResponse["books"]})


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



def texts(request, slug=None):
    print("slug: ", slug)
    form = YcommentForm()
    linksToPass = []
    user_comments = []
    all_comments = []
    if slug:
        if request.user.is_authenticated:
            user_comments = Ycomment.objects.filter(user=request.user).filter(url=request.build_absolute_uri())
            print("current url: ", request.build_absolute_uri())
            print("user_comments: ", user_comments)
        else:
            all_comments = Ycomment.objects.all()
        url = "http://www.sefaria.org/api/texts/{}".format(slug)
        print(url)
        model = get_model(Texts, url)
        jsonResponse = dict(model.json)
        # print("res: ", jsonResponse.keys())
        # for s in ['ref', 'heRef', 'order', 'sections', 'heSectionRef', 'sectionRef']:
        #     print(s, " - ", jsonResponse[s])
        link_url = "http://www.sefaria.org/api/links/{}".format(jsonResponse['ref'])
        link_model = get_model(Links, link_url)
        links_list = link_model.json

        for link in links_list:
            linkdDictToPass = {}
            linkDict = dict(link)
            linkdDictToPass['sourceRef'] = linkDict['sourceRef']
            linkdDictToPass['sourceHeRef'] = linkDict['sourceHeRef']
            linksToPass.append((linkdDictToPass))
        # print("linkes: ", len(links_list))
        try:
            book = jsonResponse['book'].replace(' ', '_')
        except KeyError:
            print("no book key in json response")
        try:
            next, prev = get_next_prev(jsonResponse)
            length = jsonResponse['length']
            page_range, hebrewLetterList = get_correct_page_range(jsonResponse['primary_category'], length)
            indexNames = get_index_names()
            return render(request, "texts.html",
                          {"jsonResponse": jsonResponse["he"], "next": next, 'prev': prev, "length": length,
                           "range": page_range, "hebrewLetterList": hebrewLetterList, 'book': book, 'links': linksToPass, "form": form,
                           "indexNames": indexNames, "user_comments": user_comments, "all_comments": all_comments})
        except KeyError:
            next, prev = get_next_prev(jsonResponse)
            # print(jsonResponse.keys())
            indexNames = get_index_names()
            return render(request, "texts.html",
                          {"jsonResponse": jsonResponse["he"], 'book': book, 'next': next, 'prev': prev, 'links': linksToPass,
                           "form": form, "indexNames": indexNames, "user_comments": user_comments, "all_comments": all_comments})


def contact(request):
    return render(request, "main/contact.html", {})


def about(request):
    return render(request, "main/about.html", {})


def dashboard(request):
    return render(request, "main/dashboard.html", {})


def search_results(request):
    return render(request, "main/search_results.html", {})


def excel_parsing(request):  # based on - https://github.com/anuragrana/excel-file-upload-django
    if request.method == "GET":
        return render(request, 'main/excel_parsing.html', {})
    else:
        print(request.POST)
        search_word = request.POST.get('search_word')
        print(request.FILES)
        excel_file = request.FILES.get("excel_file")
        search_json = request.POST.get('hidden_input')
        print(type(search_json))
        print(search_json)
        df = pd.read_excel(excel_file, engine='openpyxl')
        df.dropna(axis=1, how='all', inplace=True)
        try:
            df = df.replace(np.nan, '', regex=True)
        except AttributeError:
            pass
        df_head = list(df)
        indexes = list(range(1, len(df_head)+1))
        select_elements = dict(zip(indexes, df_head))
        options = [search_word]
        if search_word:
            if not search_json:
                print(list(df)[4])
                hamlaza = list(df)[4]
                rslt_df = df[df[hamlaza].isin(options)]
            else:
                search_list = json.loads(search_json)
                print(search_list)
                df_list = []
                for s_word in search_list:
                    print('s_word: ', s_word)
                    # tmp_df = df[df[s_word].isin(options)]
                    tmp_df = df[df[s_word].str.contains(search_word)]
                    df_list.append(tmp_df)
                rslt_df = pd.concat(df_list)
        else:
            rslt_df = df

        # https: // stackoverflow.com / questions / 48622486 / how - to - display - a - pandas - dataframe -as-datatable
        # https: // stackoverflow.com / questions / 52644035 / how - to - show - a - pandas - dataframe - into - a - existing - flask - html - table
        return render(request, 'main/excel_parsing.html', {"tables": [rslt_df.to_html(classes='dataframe', header="true")], "select_elements": select_elements})
