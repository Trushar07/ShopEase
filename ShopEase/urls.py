from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "ShopEase Administration"
admin.site.index_title = "Welcome Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("store/", include("store.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("__debug__/", include("debug_toolbar.urls")),
]
