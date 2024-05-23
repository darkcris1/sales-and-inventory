"""
Module: models.py

Contains Django models for handling categories, items, and deliveries.

This module defines the following classes:
- Category: Represents a category for items.
- Item: Represents an item in the inventory.
- Delivery: Represents a delivery of an item to a customer.

Each class provides specific fields and methods for handling related data.
"""
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import Sum
from functools import cached_property 

class Item(models.Model):
    """
    Represents an item in the inventory.
    """
    slug = AutoSlugField(unique=True , populate_from='name')
    name = models.CharField(max_length=500, blank=False, null=False)
    barcode = models.CharField(max_length=20, unique=True)
    expiry_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the item.
        """
        return f"{self.barcode}: {self.name}"

    def get_absolute_url(self):
        """
        Returns the absolute URL for an item detail view.
        """
        return reverse('item-detail', kwargs={'slug': self.slug})

    @cached_property
    def inventory_count(self):
        return self.reports.aggregate(inventory_count=Sum('ending_inventory')).get('inventory_count', 0) or 0

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Products"



# Script to populate the Item model
def populate_item():
    import json
    from datetime import datetime

    # Specify the path to your JSON file
    json_file_path = "../products.json"

    # Read the JSON data from the file
    with open(json_file_path, "r") as f:
        data = json.load(f)
    for item_data in data:
        if item_data["barcode"]:  # Check if barcode is not empty
            # If expiry_date is empty, set it to None
            # If expiry_date is "No Expiry", set it to None
            exp_date = item_data["expiry_date"]
            expiry_date = None if (exp_date == "No Expiry") or (exp_date == "") or (not exp_date)  else datetime.strptime(item_data["expiry_date"], "%d-%b-%y")


            # Create or update the Item
            item, created = Item.objects.update_or_create(
                barcode=item_data["barcode"],
                defaults={
                    "name": item_data["name"],
                    "expiry_date": expiry_date
                }
            )