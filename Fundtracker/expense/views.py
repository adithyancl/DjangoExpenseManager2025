from django.shortcuts import render,redirect
from django.views.generic import View
from expense.forms import ExpenseCreateForm,SignupForm,User,LoginForm
from expense.models import Transaction
from django.db.models import Sum,Max
from  django.contrib.auth import authenticate,login,logout
# Create your views here.

class SignUpView(View):
    template_name="register.html"

    form_class=SignupForm

    def get(self,request,*args,**kwargs):

        form=self.form_class()

        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)
            print("user created")

            return redirect("signin")
        
        return render(request,self.template_name,{"form":form_instance})
    

class SignInView(View):

    template_name="login.html"

    form_class=LoginForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        form_instance= self.form_class(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pwd =form_instance.cleaned_data.get("password")

            user_obj=authenticate(request,username=uname,password=pwd)

            if user_obj:

                login(request,user_obj)

                print(request.user)
                

                return redirect("summaryexpense")
            else:
                print("login failed")
            
        return render(request,self.template_name,{"form":form_instance})
    

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")






    




class ExpenseCreateView(View):

    template_name="expense_add.html"

    form_class=ExpenseCreateForm
    
    def get(self,request,*args,**kwargs):

        form= self.form_class()

        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
        
        #step1 initialize form with request.POST 

        form_instance=self.form_class(request.POST)

        # check form has no error

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            # data=form_instance.cleaned_data

            # qs= Transaction.objects.create(**data)  we dont need thsi two lines because we use modelform.there is always def save()helps to do  the operati9on


        return redirect("listexpense")
            
class ExpenseListView(View):

    template_name="expense_list.html"

    def get(self,request,*args,**kwargs):
        
        selected_category=request.GET.get("category","all")

        if selected_category =="all":

            qs= Transaction.objects.all()

        else:

            qs= Transaction.objects.filter(category=selected_category)

        
        categories=Transaction.objects.all().values_list("category",flat=True).distinct()
        print(categories)

        return render(request,self.template_name,{"data":qs,"categories":categories,"selected_category":selected_category})
    

class ExpenseDetailView(View):

    template_name="expense_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Transaction.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})
 

class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):
        
        id = kwargs.get("pk")

        Transaction.objects.get(id=id).delete()

        return redirect("listexpense")



# url :localhost:800/expense/{id}/change/
# we need get and post


class ExpenseUpdateView(View):
    
    template_name="expense_update.html"

    form_class=ExpenseCreateForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        trans_obj=Transaction.objects.get(id=id)#qs

        # instance_dict={
        #     "title":instance.title,
        #     "amount":instance.amount,
        #     "category":instance.category,
        #     "payment_method":instance.payment_method,
        #     "priority":instance.priority,
        # }

     

        form_instance=self.form_class(instance=trans_obj)

        return render(request,self.template_name,{"form":form_instance})
    
    def post (self,request,*args,**kwargs):

        id=kwargs.get("pk")

        trans_obj=Transaction.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=trans_obj)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("listexpense")
        


class ExpenseSummeryView(View):

    template_name="expense_summary.html"

    def get(self,request,*args,**kwargs):

        expense_total=Transaction.objects.all().aggregate(total=Sum("amount"))

        category_summary=Transaction.objects.all().values("category").annotate(total=Sum("amount"))

        payment_summary=Transaction.objects.all().values("payment_method").annotate(total=Sum("amount"))

        priority_summary=Transaction.objects.all().values("priority").annotate(total=Sum("amount"))

        context={
            "total_expense":expense_total.get("total"),

            "category_summary":category_summary,

            "payment_summary":payment_summary,

            "priority_summary":priority_summary,
        }
        

        return render(request,self.template_name,context)





        
