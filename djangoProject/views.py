from django.shortcuts import render
from ESsearch import searchEngine

dic = searchEngine.init_dictionary()


def index(request):
    return render(request, "index.html")


def search(request):
    request.encoding = "utf-8"
    query = request.GET['query']
    print(request.GET['select-query'])
    result = searchEngine.search(query, dic, False)
    return render(request, "index.html", {"poem_list": result})
