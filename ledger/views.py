

# # Create your views here.

# from django.shortcuts import render, redirect, get_object_or_404
# from django.db.models import Sum
# from datetime import date
# from itertools import chain

# from .models import Customer, Transaction, Payment, InstantPayment
# from .forms import TransactionForm, PaymentForm, CustomerForm


# # ---------------- DASHBOARD ----------------
# def dashboard(request):

#     # Add instant payment
#      # 🔥 HANDLE FORM FIRST
#     if request.method == "POST" and 'add_instant' in request.POST:
#         amount = request.POST.get('amount')

#         if amount:
#             try:
#                 amount = float(amount)
#                 InstantPayment.objects.create(amount=amount)
#             except:
#                 pass

#         return redirect('dashboard')  # ✅ REQUIRED
        

#     today = date.today()

#     instant_total = InstantPayment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
#     instant_today = InstantPayment.objects.filter(date__date=today).aggregate(Sum('amount'))['amount__sum'] or 0

#     khata_received = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
#     khata_today = Payment.objects.filter(date__date=today).aggregate(Sum('amount'))['amount__sum'] or 0

#     total_credit = Transaction.objects.aggregate(Sum('amount'))['amount__sum'] or 0

#     total_outstanding = total_credit - khata_received

#     # Top customers
#     customers = Customer.objects.all()
#     data = []

#     for c in customers:
#         credit = Transaction.objects.filter(customer=c).aggregate(Sum('amount'))['amount__sum'] or 0
#         payment = Payment.objects.filter(customer=c).aggregate(Sum('amount'))['amount__sum'] or 0
#         balance = credit - payment

#         if balance > 0:
#             data.append({'customer': c, 'balance': balance})

#     top_customers = sorted(data, key=lambda x: x['balance'], reverse=True)[:5]

#     return render(request, 'dashboard.html', {
#         'instant_total': instant_total,
#         'instant_today': instant_today,
#         'khata_received': khata_received,
#         'khata_today': khata_today,
#         'total_credit': total_credit,
#         'total_outstanding': total_outstanding,
#         'top_customers': top_customers
#     })


# # ---------------- CUSTOMER LIST ----------------
# def customer_list(request):

#     search = request.GET.get('search')
#     customers = Customer.objects.all()

#     if search:
#         customers = customers.filter(name__icontains=search)

#     form = CustomerForm()

#     if request.method == "POST":
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             customer = form.save()
#             return redirect('customer_detail', customer_id=customer.id)

#     customer_data = []
#     total_due = 0

#     for c in customers:
#         credit = Transaction.objects.filter(customer=c).aggregate(Sum('amount'))['amount__sum'] or 0
#         payment = Payment.objects.filter(customer=c).aggregate(Sum('amount'))['amount__sum'] or 0
#         balance = credit - payment

#         total_due += balance

#         customer_data.append({
#             'customer': c,
#             'balance': balance
#         })

#     return render(request, 'customer_list.html', {
#         'customer_data': customer_data,
#         'form': form,
#         'total_due': total_due,
#         'search_query': search
#     })


# # ---------------- CUSTOMER DETAIL ----------------
# def customer_detail(request, customer_id):

#     customer = get_object_or_404(Customer, id=customer_id)

#     t_form = TransactionForm()
#     p_form = PaymentForm()

#     if request.method == "POST":

#         if 'add_transaction' in request.POST:
#             t_form = TransactionForm(request.POST)
#             if t_form.is_valid():
#                 obj = t_form.save(commit=False)
#                 obj.customer = customer
#                 obj.save()

#         elif 'add_payment' in request.POST:
#             p_form = PaymentForm(request.POST)
#             if p_form.is_valid():
#                 obj = p_form.save(commit=False)
#                 obj.customer = customer
#                 obj.save()

#         return redirect('customer_detail', customer_id=customer.id)

#     transactions = Transaction.objects.filter(customer=customer)
#     payments = Payment.objects.filter(customer=customer)

#     entries = sorted(chain(transactions, payments), key=lambda x: (x.date, x.id))

#     # running balance
#     running_balance = 0
#     entry_list = []

#     for e in entries:
#         if hasattr(e, 'description'):
#             running_balance += e.amount
#             type_ = 'credit'
#         else:
#             running_balance -= e.amount
#             type_ = 'payment'

#         entry_list.append({
#             'entry': e,
#             'type': type_,
#             'balance': running_balance
#         })

#     return render(request, 'customer_detail.html', {
#         'customer': customer,
#         'entries': entry_list,
#         't_form': t_form,
#         'p_form': p_form
#     })

# # -------- EDIT TRANSACTION --------
# def edit_transaction(request, id):
#     transaction = get_object_or_404(Transaction, id=id)

#     if request.method == "POST":
#         form = TransactionForm(request.POST, instance=transaction)
#         if form.is_valid():
#             form.save()
#             return redirect('customer_detail', customer_id=transaction.customer.id)
#     else:
#         form = TransactionForm(instance=transaction)

#     return render(request, 'edit_form.html', {'form': form, 'title': 'Edit Transaction'})


# # -------- DELETE TRANSACTION --------
# def delete_transaction(request, id):
#     transaction = get_object_or_404(Transaction, id=id)
#     customer_id = transaction.customer.id
#     transaction.delete()
#     return redirect('customer_detail', customer_id=customer_id)


# # -------- EDIT PAYMENT --------
# def edit_payment(request, id):
#     payment = get_object_or_404(Payment, id=id)

#     if request.method == "POST":
#         form = PaymentForm(request.POST, instance=payment)
#         if form.is_valid():
#             form.save()
#             return redirect('customer_detail', customer_id=payment.customer.id)
#     else:
#         form = PaymentForm(instance=payment)

#     return render(request, 'edit_form.html', {'form': form, 'title': 'Edit Payment'})


# # -------- DELETE PAYMENT --------
# def delete_payment(request, id):
#     payment = get_object_or_404(Payment, id=id)
#     customer_id = payment.customer.id
#     payment.delete()
#     return redirect('customer_detail', customer_id=customer_id)



from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from datetime import date
from itertools import chain
from decimal import Decimal

from .models import Customer, Transaction, Payment, InstantPayment
from .forms import TransactionForm, PaymentForm, CustomerForm


# ---------------- DASHBOARD ----------------
def dashboard(request):

    # HANDLE POST
    if request.method == "POST" and 'add_instant' in request.POST:
        amount = request.POST.get('amount')

        if amount:
            try:
                InstantPayment.objects.create(amount=Decimal(amount))
            except Exception as e:
                print("Error:", e)

        return redirect('dashboard')

    today = date.today()

    instant_total = InstantPayment.objects.aggregate(total=Sum('amount'))['total'] or 0
    instant_today = InstantPayment.objects.filter(date__date=today).aggregate(total=Sum('amount'))['total'] or 0

    khata_received = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    khata_today = Payment.objects.filter(date__date=today).aggregate(total=Sum('amount'))['total'] or 0

    total_credit = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0

    total_outstanding = total_credit - khata_received

    # 🔥 OPTIMIZED TOP CUSTOMERS
    customers = Customer.objects.all().prefetch_related('transactions', 'payments')

    data = []
    for c in customers:
        credit = sum(t.amount for t in c.transactions.all())
        payment = sum(p.amount for p in c.payments.all())
        balance = credit - payment

        if balance > 0:
            data.append({'customer': c, 'balance': balance})

    top_customers = sorted(data, key=lambda x: x['balance'], reverse=True)[:5]

    return render(request, 'dashboard.html', {
        'instant_total': instant_total,
        'instant_today': instant_today,
        'khata_received': khata_received,
        'khata_today': khata_today,
        'total_credit': total_credit,
        'total_outstanding': total_outstanding,
        'top_customers': top_customers
    })


# ---------------- CUSTOMER LIST ----------------
def customer_list(request):

    search = request.GET.get('search', '')
    customers = Customer.objects.all()

    if search:
        customers = customers.filter(name__icontains=search)

    form = CustomerForm()

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', customer_id=customer.id)

    # 🔥 OPTIMIZED QUERY
    customers = customers.prefetch_related('transactions', 'payments')

    customer_data = []
    total_due = 0

    for c in customers:
        credit = sum(t.amount for t in c.transactions.all())
        payment = sum(p.amount for p in c.payments.all())
        balance = credit - payment

        total_due += balance

        customer_data.append({
            'customer': c,
            'balance': balance
        })

    return render(request, 'customer_list.html', {
        'customer_data': customer_data,
        'form': form,
        'total_due': total_due,
        'search_query': search
    })


# ---------------- CUSTOMER DETAIL ----------------
def customer_detail(request, customer_id):

    customer = get_object_or_404(Customer, id=customer_id)

    t_form = TransactionForm()
    p_form = PaymentForm()

    if request.method == "POST":

        if 'add_transaction' in request.POST:
            t_form = TransactionForm(request.POST)
            if t_form.is_valid():
                obj = t_form.save(commit=False)
                obj.customer = customer
                obj.save()

        elif 'add_payment' in request.POST:
            p_form = PaymentForm(request.POST)
            if p_form.is_valid():
                obj = p_form.save(commit=False)
                obj.customer = customer
                obj.save()

        return redirect('customer_detail', customer_id=customer.id)

    transactions = customer.transactions.all()
    payments = customer.payments.all()

    entries = sorted(chain(transactions, payments), key=lambda x: (x.date, x.id))

    running_balance = Decimal(0)
    entry_list = []

    for e in entries:
        if isinstance(e, Transaction):
            running_balance += e.amount
            type_ = 'credit'
        else:
            running_balance -= e.amount
            type_ = 'payment'

        entry_list.append({
            'entry': e,
            'type': type_,
            'balance': running_balance
        })

    return render(request, 'customer_detail.html', {
        'customer': customer,
        'entries': entry_list,
        't_form': t_form,
        'p_form': p_form
    })


# -------- EDIT TRANSACTION --------
def edit_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=transaction.customer.id)
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'edit_form.html', {
        'form': form,
        'title': 'Edit Transaction'
    })


# -------- DELETE TRANSACTION --------
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    customer_id = transaction.customer.id
    transaction.delete()
    return redirect('customer_detail', customer_id=customer_id)


# -------- EDIT PAYMENT --------
def edit_payment(request, id):
    payment = get_object_or_404(Payment, id=id)

    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=payment.customer.id)
    else:
        form = PaymentForm(instance=payment)

    return render(request, 'edit_form.html', {
        'form': form,
        'title': 'Edit Payment'
    })


# -------- DELETE PAYMENT --------
def delete_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    customer_id = payment.customer.id
    payment.delete()
    return redirect('customer_detail', customer_id=customer_id)