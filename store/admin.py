from django.contrib import admin
from .models import Customer, Product, Collection, Order, OrderItem, Cart, CartItem
from django.db.models import Count
from tag.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]
    list_per_page = 10
    ordering = ["user__first_name", "user__last_name"]
    search_fields = ["user__first_name__istartswith", "user__last_name__istartswith"]


""" Custom Filter for Products"""


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low"), (">10", "OK")]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)

        if self.value() == ">10":
            return queryset.filter(inventory__gt=10)


# Inline Editing of Tags for Prodcuts
class TagInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    autocomplete_fields = ["tag"]


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = ["title", "unit_price", "inventory_status", "collection"]
    list_per_page = 10
    ordering = ["title"]
    list_filter = ["collection", "last_update", InventoryFilter]
    actions = ["clear_inventory"]
    autocomplete_fields = ["collection"]
    search_fields = ["title"]
    inlines = [TagInline]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"

        return "OK"

    # Custom Action
    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        object_count = queryset.update(inventory=0)
        self.message_user(request, f"{object_count} were successfully updated.")


# Editing Children using Inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ["product"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "placed_at"]
    list_per_page = 10
    ordering = ["placed_at"]
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "product_count"]
    search_fields = ["title"]

    @admin.display(ordering="product_count")
    def product_count(self, collection):
        return collection.product_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count("product"))


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity"]
