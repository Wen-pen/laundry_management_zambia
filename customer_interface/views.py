from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .forms import SignupForm, NameForm, CreditForm, QuantityForm, OrderForm
from django.contrib.auth import logout
from .models import Orders, OrderItem, Sales
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.core.paginator import Paginator

@login_required
def dashboard(request, page):
    if request.user.is_authenticated:
        username = request.user.id
        real_user = request.user.get_username()
        quant_form = QuantityForm()
        order_query = Orders.objects.filter(user_id_fk=username)
        ordered_query = order_query.order_by("order_date")
        paginator = Paginator(ordered_query, per_page=5)
        page_obj = paginator.get_page(page)
        context = {
                   'real_user': real_user, 
                   'quant_form': quant_form,
                   'page_obj': page_obj
                   }
        if request.method == "POST":
            quant_form = QuantityForm(request.POST)
            if quant_form.is_valid():
                number = quant_form.cleaned_data.get('number')
                print(number)
                if number > 10 or number < 1:
                    messages.error("Please enter a number between 1 and 10")
                else:
                    return redirect(f"/orders/{number}")
    else:
        context = {}
    
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def payments(request, methods):
    if request.method == "POST":
        if methods == "mtn" or methods == "airtel":
            name_form = NameForm(request.POST)
            order = Orders.objects.last()
            Sales.objects.create(order_id_fk = order)
            return redirect("/dashboard/1")
        else:
            credit_form = CreditForm(request.POST)
            order = Orders.objects.last()
            Sales.objects.create(order_id_fk = order)
            return redirect("/dashboard/1")
        
    template = loader.get_template('payments.html')
    name_form = NameForm()
    credit_form = CreditForm()
    context = {
                "method": methods, 
                "name_form": name_form,
                "credit_form": credit_form,

            }
    return HttpResponse(template.render(context, request))

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    form = SignupForm() 
    context = {'form': form}
    template = loader.get_template('registration/register.html')
    return HttpResponse(template.render(context, request))

def default(request):
    context = {}
    template = loader.get_template("landing.html")
    return HttpResponse(template.render(context, request))

def logout_view(request):
    logout(request)
    
@login_required
def orders(request, quantity):
    if quantity >= 1 and quantity <= 10:
        OrderModelFormSet = modelformset_factory(OrderItem, form=OrderForm, extra=quantity)
        user = request.user
        Order_Form = OrderModelFormSet(queryset=OrderItem.objects.none())
        if request.method == "POST":
            Order_Form = OrderModelFormSet(request.POST)
            if request.user.is_authenticated:
                if Order_Form.is_valid():
                    instances = Order_Form.save(commit=False)
                    order_save = Orders(user_id_fk = user)
                    order_save.save()
                    
                    for instance in instances:
                        order_id_fk = order_save
                        instance.order_id_fk = order_id_fk
                        instance.save()

                    return redirect("/prices")

        context = {"formset": Order_Form}
        template = loader.get_template('orders.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect("/dashboard/1")

@login_required
def prices(request):
    order_query = Orders.objects.last()
    order_query_items = OrderItem.objects.filter(order_id_fk= order_query.id)
    template = loader.get_template('prices.html')
    context = {'order': order_query, "order_items": order_query_items}
    return HttpResponse(template.render(context, request))

def rejected(request):
    order_query = Orders.objects.last()
    order_query.delete()
    print(order_query)
    return redirect('/dashboard')
   
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, "Please correct the error below")
    else:
        form = PasswordChangeForm(request.user)
        context = {'form': form}
        template = loader.get_template('registration/change_password.html')
        return HttpResponse(template.render(context, request))
@login_required   
def view_items(request, id):
    order = Orders.objects.filter(id = id)
    print(order.values_list('id', flat=True))
    order_items = OrderItem.objects.filter(order_id_fk = id)
    template = loader.get_template("itemview.html")
    context = {"order_items": order_items, "order": order}
    return HttpResponse(template.render(context, request))

@login_required
def profile_view(request):
    total_price = 0
    count_arr = []
    order_name = []
    order_item_arr = []

    template = loader.get_template('profile.html')
    orders = Orders.objects.filter(user_id_fk = request.user.id)
    first_order = orders.filter(order_status = "Pending").first()

    
    for order in orders:
        total_price = total_price + order.price_calculated
        order_items = OrderItem.objects.filter(order_id_fk = order)
        for item in order_items:
            order_item_arr.append(item.category)
        order_name.append("Order No " + str(order.id))
        count = order_items.count()
        count_arr.append(count)
    
    item_label = list(Counter(order_item_arr).keys())
    item_data  = list(Counter(order_item_arr).values())

    if orders.count() < 1:
        average_price = 0
    else:
        average_price = total_price // orders.count()
    
    context = {
               'orders': orders, 
               'price': average_price, 
               "count": count_arr,
               "first_order": first_order, 
               "order_name": order_name,
               "item_label": item_label,
               "item_data": item_data
    }
    
    return HttpResponse(template.render(context, request))