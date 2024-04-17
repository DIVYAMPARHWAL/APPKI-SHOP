from django.contrib import admin

from .models import Item,company,Coupon,comments,category,OrderItem,Order,Address,Payment,subcategory,AboutUs,Slide,Employee,ContactForm
# Register your models here.
def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon',
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


def copy_items(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


copy_items.short_description = 'Copy Items'


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'quantity',
        'is_active',
    ]
    list_filter = ['title', 'category']
    search_fields = ['title', 'category']
    prepopulated_fields = {"slug": ("title",)}
    actions = [copy_items]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'is_active'
    ]
    list_filter = ['category', 'is_active']
    search_fields = ['category', 'is_active']
    prepopulated_fields = {"slug": ("category",)}


admin.site.register(Item,ItemAdmin)
admin.site.register(AboutUs)
admin.site.register(ContactForm)
admin.site.register(comments)
admin.site.register(company)
admin.site.register(Coupon)
admin.site.register(category,CategoryAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address,AddressAdmin)
admin.site.register(Payment)
admin.site.register(subcategory)
admin.site.register(Employee)
admin.site.register(Slide)
