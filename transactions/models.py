from django.db import models
from store.models import Item
from accounts.models import Profile
from django_extensions.db.fields import AutoSlugField
from functools import cached_property 
from datetime import date
from django.db.models import Manager, Sum
from django.db.models import Max
# Create your models here.

class SaleManager(Manager):
  def get_queryset(self):
    return super().get_queryset().annotate(
        ending_inventory=Sum('initial_stock') + Sum('delivery') - Sum('withdrawal') - Sum('sales') - Sum('damage')
    )

class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, related_name='reports')
    transaction_date = models.DateField(default=date.today ,blank=True)
    initial_stock = models.IntegerField(default=0.00, blank=True)
    damage = models.IntegerField(default=0.00, blank=True)
    withdrawal = models.IntegerField(default=0.00, blank=True)
    delivery = models.IntegerField(default=0.00, blank=True)
    sales = models.IntegerField(default=0.00, blank=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ForeignKey(Profile, verbose_name=('Served by'), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SaleManager()

    
    class Meta:
        verbose_name_plural = 'Iventory Reports'

    @cached_property
    def ending_inventory(self):
        return self.ending_inventory

    @cached_property
    def begin_inventory(self):
        """Calculate the beginning inventory based on previous transaction date ending inventory"""
        previous_sales = Sale.objects.filter(
            item=self.item,
            transaction_date__lt=self.transaction_date
        )
        previous_ending_inventory = previous_sales.aggregate(Max('transaction_date'))['transaction_date__max']
        if previous_ending_inventory:
            previous_sale = previous_sales.get(transaction_date=previous_ending_inventory)
            return previous_sale.ending_inventory
        else:
            # If there are no previous sales, return initial stock
            return self.initial_stock