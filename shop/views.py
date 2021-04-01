from django.shortcuts import render, get_object_or_404
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.views.generic import ListView # 基於 class 的 view
#from django.db.models import Count
from .models import Category, Product
from cart.forms import CartAddProductForm
from search.forms import SearchForm
from django.contrib.postgres.search import SearchVector

def product_list(request, category_slug=None):
    # 無分頁機制
    category = None
    categories = Category.objects.all()
    products = Product.objects.all().filter(available=True)
    if category_slug is not None:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)

    return render(request, "shop/product/list.html",
                  {"category": category,
                   "categories": categories,
                   "products": products})

    '''
    # 加上分頁機制
    # P.S. 不直接 all_posts_ (顯示全部貼文)
    #      而是先用 object_list 暫存，再丟給 Paginator 處理分頁
    object_list = Post.published_manager.all().order_by("title")

    # 加上標籤功能
    tag_ = None

    # 當 label 不為空值 => 即: 當「任一個 label(標籤分類) 被按下」時則 ...
    # P.S. 滿足 if-statement 則會導引至「有關 '(label)' 的所有貼文:」頁面
    #      URL 導引機制可在 blog/urls.py 設定
    if label is not None:
        # 抓出符合 user 所按下 label文字 的 '標籤' (Tag instance)
        tag_ = get_object_or_404(Tag, slug=label)
        # 篩選出含有上述 '標籤' 的已發佈 posts
        object_list = object_list.filter(tags__in=[tag_])

    paginator = Paginator(object_list, 3) # 每頁最多貼文數
    page_n = request.GET.get("page")
    try:
        all_posts_ = paginator.page(page_n)
    except EmptyPage:
        all_posts_ = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        all_posts_ = paginator.page(1)

    return render(request, "blog/post/list.html",
                  {"page": page_n,
                   "all_posts": all_posts_,
                   "tag": tag_})
    '''

def product_detail(request, id, product_slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=product_slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    #search_form = SearchForm()
    '''
    # comments_: 所有未被禁言的評論
    # P.S. Post-Comment 為 1-N 關係
    #      利用 Comment 模型類的 "comments"
    #      可反向查詢 (post => comments)
    comments_ = post_.comments.filter(active=True) #.order_by("create_date")

    # 新評論
    new_comment_ = None
    if request.method == "POST":
        comment_form_ = CommentForm(request.POST)
        if comment_form_.is_valid():
            # 建立一個 Comment 物件，但先不儲存到 DB
            # P.S.利用評論(模型)表單來暫存一個新評論 (=>建立 Comment instance)
            new_comment_ = comment_form_.save(commit=False)
            # 設定該 Comment 物件的對應 post(貼文) 屬性為 post_ (=>該貼文隸屬於該 post)
            new_comment_.post = post_
            # 正式將該 Comment 物件儲存到 DB
            new_comment_.save()
            """
            data = comment_form_.cleaned_data
            Comment.objects.create(
               post = post_,
               name = data.name,
               email = data.email,
               body = data.body,
               active = True
            )
            """
    else:
        comment_form_ = CommentForm()

    RECOMMEND_POST_AMOUNT = 4
    # 逐一列出與此篇貼文的 tags 有任一相同 tag 的其它貼文的 "id"
    post_tag_ids_ = post_.tags.values_list("id", flat=True)
    # 用上述 id 抓出所有相關貼文，並剔除貼文本身
    similar_posts_ = Post.published_manager\
                         .filter(tags__in=post_tag_ids_)\
                         .exclude(id=post_.id)
    similar_posts_ = similar_posts_.annotate(same_tags=Count("tags"))\
                                   .order_by("-same_tags", "-publish_date")[:RECOMMEND_POST_AMOUNT]

    return render(request, "blog/post/detail.html",
                  {"post": post_,
                   "comments": comments_,
                   "new_comment": new_comment_,
                   "comment_form": comment_form_,
                   "similar_posts": similar_posts_
                  })
    '''
    return render(request, "shop/product/detail.html",
                  {"product": product,
                   "cart_product_form": cart_product_form,
                   })
    #"search_form": search_form
'''
def post_search(request):
    form = SearchForm()
    query = None
    results = list()
    if "query" in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = form.cleaned_data["query"]
            results = Product.objects.annotate(
                          search=SearchVector("name", 
                                              "category",
                                              "description")
                      ).filter(search=query)
    return render(request,
                  "search/search.html",
                  {"search_form": search_form, 
                   "query": query,
                   "results": results})
'''