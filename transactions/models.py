from django.db import models
from store.models import Item
from accounts.models import Profile
from django_extensions.db.fields import AutoSlugField

# Create your models here.

PAYMENT_CHOICES = [
    ('MP', 'MPESA'),
    ('VISA', 'VISA'),
    ('CS', 'CASH'),
    ('VM', 'VOOMA'),
    ('BK', 'BANK')
]

class Sale(models.Model):
    slug = AutoSlugField(unique=True , populate_from='item__name')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    quantity = models.FloatField(default=0.00, blank=False, null=False)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=20, blank='True', null=True)
    price = models.FloatField(default=0.00, blank=False, null=False)
    total_value = models.FloatField(blank=True, null=True)
    amount_received = models.FloatField(default=False, blank=False, null=False)
    balance = models.FloatField(default=False, blank=False, null=False)
    profile = models.ForeignKey(Profile, verbose_name=('Served by'), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        amt_received = self.amount_received
        price = self.price
        quantity = self.quantity
        self.total_value = price * quantity
        self.balance = amt_received - self.total_value
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.item.name)


def generateItem():
    asd = Sale.objects.first()
    for i in range(0, 1000):
        asd.pk = None
        asd.save()
