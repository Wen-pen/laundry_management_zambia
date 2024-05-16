from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .forms import SignupForm, NameForm, CreditForm, QuantityForm, OrderForm, UpdateProfileForm
from django.contrib.auth import logout
from .models import Orders, OrderItem, Sales, CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from collections import Counter

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        username = request.user.id
        real_user = request.user.get_username()
        quant_form = QuantityForm()
        order_query = Orders.objects.filter(user_id_fk=username)
        context = {'order_query':order_query, 
                   'real_user': real_user, 
                   'quant_form': quant_form
                   }
        if request.method == "POST":
            pass
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
            return redirect("/dashboard")
        else:
            credit_form = CreditForm(request.POST)
            order = Orders.objects.last()
            Sales.objects.create(order_id_fk = order)
            return redirect("/dashboard")
        
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
    last_order = orders.last()
    
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
               "last_order": last_order, 
               "order_name": order_name,
               "item_label": item_label,
               "item_data": item_data
    }
    
    return HttpResponse(template.render(context, request))

@login_required
def profile_form(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            CustomUser.objects.filter()
            form.save()
            messages.success(request, f'Your account has been updated!')
            print(request.user.profile_picture)
            return redirect('/profile')
        else:
            print("IWE THIS BINE IS TAPPED")
    form = UpdateProfileForm()
    template = loader.get_template('profile_form.html')
    context = {'form': form}

    return HttpResponse(template.render(context, request))