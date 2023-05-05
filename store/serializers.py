from rest_framework import serializers
from .models import (
    Product,
    Collection,
    Reviews,
    Cart,
    CartItem,
    Customer,
    Order,
    OrderItem,
)
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "product_count"]

    product_count = serializers.IntegerField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["id", "name", "description", "date"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Reviews.objects.create(product_id=product_id, **validated_data)


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum(
            [item.quantity * item.product.unit_price for item in cart.items.all()]
        )

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given id was found!")
        return value

    def save(self, **kwargs):
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        cart_id = self.context["cart_id"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            # check implementation of save method and customize the save accordingly
            self.instance = cart_item
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            self.instance = cart_item

        return self.instance

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "placed_at", "payment_status", "customer_id", "items"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("No cart with the given id was found")
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError(
                "Can not place order because cart does not have any items"
            )
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            (customer, created) = Customer.objects.get_or_create(
                user_id=self.context["user_id"]
            )
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related("product").filter(
                cart_id=self.validated_data["cart_id"]
            )

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.unit_price,
                )
                for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=self.validated_data["cart_id"]).delete()

            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status"]
