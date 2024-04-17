from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.dateparse import parse_date


# Create your models here.
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    type=models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField(null=True)
    images=models.ImageField(upload_to='comment',null=True,blank=True)
    rating=models.FloatField(null=True)
    like=models.BooleanField(default=False)
    dislike=models.BooleanField(default=False)
    

class company(models.Model):
    name=models.CharField(max_length=20)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    total_sales=models.FloatField(default=0)
    pending_order=models.FloatField(default=0)
    confirmed_order=models.FloatField(default=0)
    
    
    def __str__(self):
        return self.name
        
        
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    minCartValue = models.FloatField(default=True)
    company = models.ForeignKey( company ,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.code
    
class Item(models.Model):
    company=models.ForeignKey(company,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    brand_Name=models.CharField(default='Not defined', max_length=20)
    price = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(
        'category', on_delete=models.SET_NULL, blank=True, null=True)
    subcategory = models.ManyToManyField(
        'subcategory',blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True)
    slug = models.SlugField(unique=True, null=True)
    description_short = models.CharField(max_length=50, blank=True)
    description_long = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='Porduct', default="../static/img/image_not_available.png")
    comments=models.ForeignKey(comments,on_delete=models.CASCADE, null=True , blank=True)
    is_active = models.BooleanField(default=True)
    date_published = models.DateTimeField(auto_now_add=True)
    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("user:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("user:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("user:remove-from-cart", kwargs={
            'slug': self.slug
        })
        
        
class category(models.Model):
    category = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='Category', null=True)
    sales=models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category
    
class subcategory(models.Model):
    main=models.ManyToManyField(category)
    name=models.CharField(max_length=25, unique=True)
    slug=models.SlugField(unique=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)
    
class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)
class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        print(self.item.price)
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
    
class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    def get_absolute_url(self):
        return reverse("shop:order_view", kwargs={
            'pk': self.id
        })

class AboutUs(models.Model):
    user = models.CharField(max_length=100)
    about_us = models.TextField()
    # resume= forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    slug = models.SlugField(unique=True)
    work = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='authorImg', blank=True)
    resume = models.FileField(upload_to='resume', blank=True)
    linkedin_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    Youtube_url = models.CharField(max_length=255, null=True, blank=True)
    Facebook_url = models.CharField(max_length=255, null=True, blank=True)
    github_url = models.CharField(max_length=255, null=True, blank=True)
    other = models.CharField(max_length=255, null=True, blank=True)
    project_Img = models.ImageField(upload_to='project_images', blank=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = 'About Us'


class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contact Form'
        
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    company=models.ForeignKey(company, on_delete=models.CASCADE)
    salary=models.IntegerField(default=10000)
    
