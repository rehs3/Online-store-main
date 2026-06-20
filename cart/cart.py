from decimal import Decimal
from catalog.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        # Mantém a chave 'cart' na sessão, mas muda o nome do atributo para 'items'
        self.items = request.session.get('cart', {})

    def add(self, product, quantity, update_quantity=False):
        product_id = str(product.id)

        if product_id not in self.items:
            self.items[product_id] = {'quantity': 0, 'price': product.price}

        if update_quantity:
            self.items[product_id]['quantity'] = quantity
        else:
            self.items[product_id]['quantity'] += quantity

        if self.items[product_id]['quantity'] > product.quantity:
            self.items[product_id]['quantity'] = product.quantity

        self.save()

    def save(self):
        self.session['cart'] = self.items
        self.session.modified = True

    def remove(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            self.save()

    def __iter__(self):
        products_keys = self.items.keys()
        products = Product.objects.filter(id__in=products_keys)

        for product in products:
            self.items[str(product.id)]['product'] = product
            self.items[str(product.id)]['product_id'] = product.id
            self.items[str(product.id)]['product_quantity'] = product.quantity

        for item in self.items.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.items.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.items.values())

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
        self.session.modified = True
