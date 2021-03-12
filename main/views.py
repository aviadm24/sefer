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
        print("post: ", request.POST)
        form = YcommentForm(request.POST)  # if no files
        if form.is_valid():
            print("form: ", form.cleaned_data)
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
    if primary_category == "Talmud":
        last = 0
        for num in range(2, int(length+2)//2+1):
            page_list.append(str(num)+'a')
            page_list.append(str(num)+'b')
            last = num
        if length % 2 != 0:
            page_list.append(str(last+1) + 'a')

        return page_list
    else:
        return range(1, length + 1)


def get_next_prev(jsonResponse):
    try:
        next = jsonResponse['next']
        print("next: ", next)
        prev = jsonResponse['prev']
        print("prev: ", prev)
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
    print("Entire JSON response")
    print(jsonResponse.keys())
    return render(request, "titles.html", {"jsonResponse": jsonResponse["books"]})


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
        print("res: ", jsonResponse.keys())
        for s in ['ref', 'heRef', 'order', 'sections', 'heSectionRef', 'sectionRef']:
            print(s, " - ", jsonResponse[s])
        link_url = "http://www.sefaria.org/api/links/{}".format(jsonResponse['ref'])
        link_model = get_model(Links, link_url)
        links_list = link_model.json

        for link in links_list:
            linkdDictToPass = {}
            linkDict = dict(link)
            linkdDictToPass['sourceRef'] = linkDict['sourceRef']
            linkdDictToPass['sourceHeRef'] = linkDict['sourceHeRef']
            linksToPass.append((linkdDictToPass))
        print("linkes: ", len(links_list))
        try:
            book = jsonResponse['book'].replace(' ', '_')
        except KeyError:
            print("no book key in json response")
        try:
            next, prev = get_next_prev(jsonResponse)
            length = jsonResponse['length']
            page_range = get_correct_page_range(jsonResponse['primary_category'], length)
            indexNames = get_index_names()
            return render(request, "texts.html",
                          {"jsonResponse": jsonResponse["he"], "next": next, 'prev': prev, "length": length,
                           "range": page_range, 'book': book, 'links': linksToPass, "form": form,
                           "indexNames": indexNames, "user_comments": user_comments, "all_comments": all_comments})
        except KeyError:
            next, prev = get_next_prev(jsonResponse)
            print(jsonResponse.keys())
            indexNames = get_index_names()
            return render(request, "texts.html",
                          {"jsonResponse": jsonResponse["he"], 'book': book, 'next': next, 'prev': prev, 'links': linksToPass,
                           "form": form, "indexNames": indexNames, "user_comments": user_comments, "all_comments": all_comments})


def contact(request):
    return render(request, "main/contact.html", {})


def about(request):
    return render(request, "main/about.html", {})
