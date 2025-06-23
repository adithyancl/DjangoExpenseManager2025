from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    
    title= models.CharField(max_length=200)

    created_data= models.DateTimeField(auto_now=True)

    amount= models.FloatField()

    CATEGORY_OPTIONS=(
        ("Food","Food"),
        ("Fuel","Fuel"),
        ("Travel","Travel"),
        ("Bills","Bills"),
        ("Shopping","Shopping"),
        ("HealthCare","HealthCare"),
        ("Miscellanious","Miscellanious")

    )

    category= models.CharField(max_length=100,choices=CATEGORY_OPTIONS,default="Food")

    PAYMENT_OPTIONS=(
        ("UPI","UPI"),
        ("CASH","CASH")

    )

    payment_method= models.CharField(max_length=200,choices=PAYMENT_OPTIONS,default="CASH")

    PRIORITY_OPTION=(
        ("NEED","NEED"),
        ("WANT","WANT")
    )

    priority= models.CharField(max_length=200,choices=PRIORITY_OPTION,default="NEED")


    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    