from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("products", views.ProductViewset, basename="products")
router.register("collections", views.CollectionViewset)
router.register("carts", views.CartViewset, basename="carts")
router.register("customers", views.CustomerViewset)
router.register("orders", views.OrderViewset, basename="orders")

""" Nested Router eg. products/1/review/1"""

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewset, basename="product-reviews")

""" Nested Router for Cart Items eg. carts/uuid/items/1"""
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewset, basename="cart-items")

urlpatterns = router.urls + product_router.urls + cart_router.urls

# urlpatterns = [
#     path("products/", views.ListCreateProduct.as_view()),
#     path("collections/", views.ListCreateCollection.as_view()),
# ]
