from django.shortcuts import render
from .models import Product, Slider, Category, Cart
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Create your views here.

def index(request):
    models = Product. objects. select_related('author'). filter(featured=True)
    slides = Slider.objects. order_by('order')
    return render(request, 'index.html', {'products': models, 'slides': slides})

def product(request, pid):
    model = get_object_or_404(Product, pk=pid)
    return render(request, 'product.html', {'product': model})


def category(request, cid=None):
    category = None
    query = request.GET.get('query')
    selected_category = request.GET.get('category')

    where = {}

    if selected_category and selected_category.isdigit():
        cid = int(selected_category)

    if cid:
        category = get_object_or_404(Category, pk=cid)
        where['category_id'] = cid

    if query:
        where['name__icontains'] = query

    models = Product.objects.filter(**where)

    paginator = Paginator(models, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()  # 🔥 مهم جداً

    return render(request, 'category.html', {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,   # 🔥 هذا هو المفتاح
    })

def cart (request):
    return render(request, 'cart.html')

def checkout (request):
    return render(request, 'checkout.html')

def checkout_complete (request):
    return render(request, 'checkout-complete.html')

def cart_add (request, pid):
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key
    cart_model = Cart.objects.filter(session_id=session_id).last()

    if cart_model is None:
        cart_model = Cart.objects.create(session_id=session_id, items=[pid])
    else:
        if not isinstance(cart_model.items, list):
            cart_model.items = list(cart_model.items)
        if pid not in cart_model.items:
            cart_model.items.append(pid)
            cart_model.save()

    return JsonResponse({
        'message': _('Product added to cart successfully'),
        'items_count': len(cart_model.items),
    })


def cart_remove (request, pid):
    session_id = request.session.session_key

    if not session_id:
        return JsonResponse({})

    cart_model = Cart.objects.filter(session_id=session_id).last()

    if cart_model is None:
        return JsonResponse({})

    if pid in cart_model.items:
        cart_model.items.remove(pid)
        cart_model.save()

    return JsonResponse({
        'message': _('Product removed from cart successfully'),
    })