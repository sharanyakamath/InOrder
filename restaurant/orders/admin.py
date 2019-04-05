# from django import forms
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import Permission
# from django.contrib.auth.models import User 

# Register your models here.
from orders.models import Customer, Manager, Restaurant, Item, Order, Bill, Feedback
# from .models import User 

# class UserCreationForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'user_type')

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user


# class CustomUserAdmin(UserAdmin):
#     # The forms to add and change user instances
#     add_form = UserCreationForm
#     list_display = ('username', 'email', 'user_type')  # fields to display in admin page while viewing all users
#     ordering = ("email",)  # order in which displayed

#     fieldsets = (
#         (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
#         )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff',
#                        'is_active', 'user_type')}
#         ),
#     )

#     filter_horizontal = ()


# admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Manager)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Bill)
admin.site.register(Feedback)
# admin.site.register(User)

