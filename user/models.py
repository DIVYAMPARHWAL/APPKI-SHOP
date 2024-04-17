from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from shop.models import Item,category,Coupon,company
# Create your models here.




class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class wishlist(models.Model):
    item=models.OneToOneField(Item,on_delete=models.CASCADE)
    company=models.ForeignKey(company,on_delete=models.CASCADE)
    

    