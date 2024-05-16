from django import forms
from .models import CustomUser, OrderItem
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField

class SignupForm(forms.ModelForm):
    class Meta: 
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'email': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control text-center'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'phone_number': PhoneNumberPrefixWidget(

                attrs={'class': 'form-control text-center'},
            ),
        }

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ("service_type", "special_instructions", "category", "optional_instructions")
    def has_changed(self, *args, **kwargs):
        return True
    
class NameForm(forms.Form):
    number = PhoneNumberField(region="ZM")

class CreditForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    street_address = forms.CharField(label="Street Address")
    city = forms.CharField(label="City")
    country = forms.CharField(label="Country")
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiry Date')
    cc_code = SecurityCodeField(label='CVV/CVC')

class QuantityForm(forms.Form):
    number = forms.IntegerField(max_value=10, min_value=1, required=True, label="Number of Items")

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

