from django import forms
from .models import Transaction, Payment, Customer

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'note']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone']