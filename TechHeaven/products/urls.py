from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import(
    product_list,
    product_detail,
    product_create,
    product_update,
    product_delete,
    product_search
)


urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<uuid:product_id>/', product_detail, name='product_detail'),
    path('product/create/', product_create, name='product_create'),
    path('product/update/<uuid:product_id>/', product_update, name='product_update'),
    path('product/delete/<uuid:product_id>/', product_delete, name='product_delete'),
    path('product/search/', product_search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)