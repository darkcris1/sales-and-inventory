from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from .filters import SaleFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableView
import django_tables2 as tables
from django.urls import reverse
from django_tables2.export.views import ExportMixin
from .tables import SaleTable
from django.core.exceptions import ValidationError
from accounts.models import Profile
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Sum
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
class SaleListView(ExportMixin,SingleTableMixin, FilterView):
    """View to list sales and export them."""
    model = Sale
    table_class = SaleTable
    template_name = 'transactions/sales_list.html'
    context_object_name = 'sales'
    paginate_by = 10
    SingleTableView.table_pagination = False
    filterset_class = SaleFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = self.object_list

        # Aggregations
        
        context['total_items'] = sales.aggregate(Sum('ending_inventory')).get('ending_inventory__sum', 0) or 0
        context['total_sales'] = sales.aggregate(Sum('sales')).get('sales__sum', 0) or 0
        context['total_items_decrease'] = sales.aggregate(
            total__sum=Sum('withdrawal') + Sum('sales') + Sum('damage')
        ).get('total__sum', 0) or 0
        context['total_items_increase'] = sales.aggregate(
            total__sum=Sum('delivery') + Sum('initial_stock')
        ).get('total__sum', 0) or 0

        return context

class SaleDetailView(DetailView):
    """View to display details of a sale."""
    model = Sale
    template_name = 'transactions/saledetail.html'


class SaleCreateView(LoginRequiredMixin, CreateView):
    """View to create a new sale."""
    model = Sale
    template_name = 'transactions/salescreate.html'
    fields = ['item','transaction_date', 'sales', 'withdrawal', 'delivery', 'damage', 'initial_stock']

    def get_success_url(self):
        return reverse('saleslist')


    def form_valid(self, form):
        """Handles the form submission and validates product availability."""
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        profile_list = Profile.objects.all()
        if self.request.user.profile in profile_list:
            return False
        else:
            return True

class SaleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update a sale."""
    model = Sale
    template_name = 'transactions/sale_update.html'
    fields = ['item', 'initial_stock', 'delivery','sales','withdrawal', 'damage', 'transaction_date']

    def test_func(self):
        """Checks if the user has the required permissions to access this view."""
        profiles = Profile.objects.all()
        if self.request.user.profile in profiles:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('saleslist')

    def form_valid(self, form):
        """Handles form submission and sets the profile of the sale."""
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class SaleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a sale."""
    model = Sale
    template_name = 'transactions/saledelete.html'

    def get_success_url(self):
        return reverse('saleslist')

    def test_func(self):
        """Checks if the user has the required permissions to access this view."""
        if self.request.user.is_superuser:
            return True
        else:
            return False
