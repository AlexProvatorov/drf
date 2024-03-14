from django.core.paginator import Paginator
from django.shortcuts import render
from bookstore.settings import PER_PAGE
from goods.models import Item


def index(request):

    items = Item.item_objects.all()

    paginator = Paginator(items, PER_PAGE)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Book Store',
        'content': 'Книжный магазин - BOOK STORE',
        'items': items,
        'per_page': int(PER_PAGE),
        'page_obj': page_obj,
    }
    return render(request, 'book_store/index.html', context=context)


def about(request):
    context = {
        'title': 'Book Store - О сайте',
        'content': 'Информация о сайте BOOK STORE',
    }
    return render(request, 'book_store/about.html', context)

