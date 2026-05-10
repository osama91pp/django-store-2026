from .models import Category, Cart, Product

def store_website(request):
    categories = Category.objects.order_by('order')
    cart_items_count = 0
    cart_total_price = 0
    cart_products = []
    session_id = request.session.session_key

    if session_id:
        cart_model = Cart.objects.filter(session_id=session_id).last()
        if cart_model:
            cart_items = list(cart_model.items or [])
            cart_items_count = len(cart_items)
            cart_products = Product.objects.filter(pk__in=cart_items).all()
            cart_total_price = sum(product.price for product in cart_products)

    return {
        'categories': categories,
        'cart_items_count': cart_items_count,
        'cart_total_price': cart_total_price,
        'cart_products': cart_products,
    }