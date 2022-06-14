from django.shortcuts import render
from ESsearch import searchEngine

dic = searchEngine.init_dictionary()


def index(request):
    return render(request, "index.html")


def search(request):
    request.encoding = "utf-8"
    query = request.GET['query']
    search_type = request.GET['type']
    page = int(request.GET['page']) - 1
    if len(query) == 0 or len(search_type) == 0:
        result = []
    else:
        result = searchEngine.search(query, dic, search_type, page)
    return render(request, "index.html", {"poem_list": result})
