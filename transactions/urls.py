from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    SaleListView,
    SaleDetailView,
    SaleCreateView,
    SaleUpdateView,
    SaleDeleteView,
)

urlpatterns = [
    path('sales/',SaleListView.as_view(), name="saleslist"),
    path('sale/<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('new-sale/', SaleCreateView.as_view(), name='sale-create'),
    path('sale/<slug:slug>/update/', SaleUpdateView.as_view(), name='sale-update'),
    path('sale/<slug:slug>/delete/', SaleDeleteView.as_view(), name='sale-delete'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)