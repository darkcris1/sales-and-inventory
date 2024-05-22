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
        total_items = sales.aggregate(total_items=Sum('quantity'))['total_items'] or 0
        total_sales_value = sales.aggregate(total_sales_value=Sum('total_value'))['total_sales_value'] or 0
        
        context['total_items'] = total_items
        context['total_sales_value'] = total_sales_value

        return context

class SaleDetailView(DetailView):
    """View to display details of a sale."""
    model = Sale
    template_name = 'transactions/saledetail.html'


class SaleCreateView(LoginRequiredMixin, CreateView):
    """View to create a new sale."""
    model = Sale
    template_name = 'transactions/salescreate.html'
    fields = ['item', 'payment_method', 'quantity', 'amount_received']

    def get_success_url(self):
        return reverse('saleslist')

    def form_valid(self, form):
        """Handles the form submission and validates product availability."""
        item = form.cleaned_data['item']
        quantity = form.cleaned_data['quantity']

        price = item.selling_price

        total_price = price * quantity

        form.instance.price = price
        form.instance.total_value = total_price

        amount_received = form.cleaned_data['amount_received']
        balance = amount_received - total_price
        form.instance.balance = balance

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
    fields = ['item', 'payment_method', 'quantity', 'price', 'amount_received']

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
