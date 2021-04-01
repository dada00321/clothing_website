from django.shortcuts import render
from shop.models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchForm

def post_search(request):
    form = SearchForm()
    query = None
    results = list()
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("name", weight='A')
            search_vector += SearchVector("description", weight='B')
            search_query = SearchQuery(query)
            search_rank = SearchRank(search_vector,
                                     search_query)
            
            # 一般查詢(+以 rank 排序)
            '''
            results = Product.objects.annotate(
                        search=search_vector,
                        rank=search_rank
                      ).filter(search=search_query)\
                       .order_by("-rank")
            '''
            
            # 加權查詢(+以 rank 排序)
            results = Product.objects.annotate(
                        rank=search_rank
                      ).filter(rank__gte=0.000001)\
                       .order_by("-rank")
            
            '''
            # 自訂搜尋方法
            results = Product.objects.filter(Product(name__contains=f'{query}') | Product(description__contains=f'{query}'))
            '''
            
    return render(request,
                  "search/search.html",
                  {"form": form, 
                   "query": query,
                   "results": results})
