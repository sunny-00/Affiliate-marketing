from django.db import models
# these are added to handle the updating effect that is made in category
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Category(models.Model):
    code=models.CharField(max_length=20,primary_key=True)
    category=models.CharField(max_length=200,unique=True)
    promoting_percent=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(12)])
    status=models.BooleanField(default=1)
    promoting_status=models.BooleanField(default=1)

    def __str__(self):
        return self.category


class Product(models.Model):
    name=models.CharField(max_length=200)
    category_code=models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    qty=models.IntegerField(validators=[MinValueValidator(1)])
    status=models.BooleanField(default=1)
    in_stock=models.BooleanField(default=1)
    promoting_link=models.CharField(max_length=700,unique=True)
    promoting_status=models.BooleanField(default=1)
    pimage=models.ImageField(upload_to="image")

    def __str__(self):
        return self.name


# Checking is the category is active in the table and reflect it on all the products 
# of related category in the product table
@receiver(pre_save,sender=Category)
def update_status(sender,instance,**kwargs):
    if(instance.pk is not None):
        try:
            old_instance=Category.objects.get(pk=instance.pk)
        except:
            pass
        else:
            if (instance.status != old_instance.status):
                Product.objects.filter(category_code=instance).update(status=instance.status)
            if(instance.promoting_status != old_instance.status):
                Product.objects.filter(category_code=instance).update(promoting_status=instance.status)


class Login_Info(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.CharField(max_length=300,primary_key=True)
    password=models.CharField(max_length=1000)
    referral_id=models.CharField(max_length=8)
    address=models.CharField(max_length=700,default=None)


class Orders(models.Model):
    ordernumber=models.IntegerField(primary_key=True)
    purchased_email=models.ForeignKey(Login_Info,on_delete=models.DO_NOTHING)
    if_reffered=models.BooleanField(default=0)
    price=models.IntegerField()
    qty=models.IntegerField()
    status=models.BooleanField(default=0)

class RefferedOrders(models.Model):
    ordernumber=models.ForeignKey(Orders,on_delete=models.CASCADE)
    referral_id=models.CharField(max_length=8)
    comission_amt=models.FloatField()
    status=models.BooleanField(default=0)

class DetailOrder(models.Model):
    ordernumber=models.ForeignKey(Orders,on_delete=models.CASCADE)
    product_id=models.IntegerField()
    

class Cart(models.Model):
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    uid=models.ForeignKey(User,on_delete=models.CASCADE)

    













