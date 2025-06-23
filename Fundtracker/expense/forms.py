from django import forms

from expense.models import Transaction

from django.contrib.auth.models import User


#create,update

#

class ExpenseCreateForm(forms.ModelForm):

    class Meta:

        model=Transaction

        exclude=("created_data","owner",)

        widgets={

            "title":forms.TextInput(attrs={"class": "form-control mb-2"}),

            "amount":forms.NumberInput(attrs={"class": "form-control mb-2"}),

            "category":forms.Select(attrs={"class": "form-control form-select mb-2"}),

            "payment_method":forms.Select(attrs={"class":"form-control form-select mb-2"}),

            "priority":forms.Select(attrs={"class":"form-control form-select mb-2"})
        }




    # title= forms.CharField()

    # amount= forms.FloatField()

    # category=forms.ChoiceField(choices=Transaction.CATEGORY_OPTIONS)

    # payment_method=forms.ChoiceField(choices=Transaction.PAYMENT_OPTIONS)

    # priority= forms.ChoiceField(choices=Transaction.PRIORITY_OPTION)

class SignupForm(forms.ModelForm):

    class Meta:

        model=User

        fields=["username","email","password"]


class LoginForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField()




