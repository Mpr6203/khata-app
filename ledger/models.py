

# # Create your models here.

# from django.db import models

# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15, blank=True, null=True)

#     def __str__(self):
#         return self.name


# class Transaction(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     amount = models.FloatField()
#     description = models.CharField(max_length=200)
#     date = models.DateTimeField(auto_now_add=True)


# class Payment(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     amount = models.FloatField()
#     note = models.CharField(max_length=200, blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True)


# class InstantPayment(models.Model):
#     amount = models.FloatField()
#     date = models.DateTimeField(auto_now_add=True)



from django.db import models
from decimal import Decimal


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})" if self.phone else self.name


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)

    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - Credit ₹{self.amount}"

    class Meta:
        ordering = ['date']


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=200, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - Payment ₹{self.amount}"

    class Meta:
        ordering = ['date']


class InstantPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    note = models.CharField(max_length=200, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Instant ₹{self.amount} on {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date']