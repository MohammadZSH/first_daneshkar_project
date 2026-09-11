from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('customer', 'مشتری (Customer)'),
        ('seller', 'فروشنده (Seller)'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='customer', label="نقش کاربری")
    phone = forms.CharField(max_length=20, required=False, label="شماره تماس")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        selected_role = self.cleaned_data.get('role')
        if selected_role == 'seller':
            user.is_seller = True
            user.is_customer = False
        else:
            user.is_customer = True
            user.is_seller = False

        if commit:
            user.save()
            # Set phone on customer profile if exists
            if hasattr(user, 'customer_profile') and self.cleaned_data.get('phone'):
                user.customer_profile.phone = self.cleaned_data.get('phone')
                user.customer_profile.save()
        return user


class AddBalanceForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=1.00,
        label="مبلغ افزایش موجودی"
    )
