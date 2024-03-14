from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Pet(models.Model):
    gender = (('male', 'male'), ('female', 'female'))
    image = models.ImageField(upload_to='media')
    name = models.CharField(max_length=150)
    breed = models.CharField(max_length=150)
    gender = models.CharField(max_length=30, choices=gender)
    description = models.CharField(max_length=500)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class log(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.IntegerField()


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_tot(self):
        total = self.product.price*self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    zipcode = models.CharField(max_length=150, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

# class CartItem(models.Model):
#     pet= models.ForeignKey(Pet,on_delete=models.CASCADE,related_name='pets')
#     quantity=models.IntegerField(default=0)
#     class Meta:
#         db_table='cart_items'
#         ordering=('pet',)

#     def __str__(self):
#         return self.pet.name


class Customer1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=10, default='NA')

    def str(self):
        return self.user.username


class Cartitem(models.Model):
    customer = models.ForeignKey(Customer1, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cart_items'

    def __str__(self):
        return self.pet.name


class ShippingAddress1(models.Model):
    customer = models.ForeignKey(
        Customer1, on_delete=models.CASCADE, null=True)
    building_name = models.CharField(max_length=300, null=False, blank=False)
    street = models.CharField(max_length=200, blank=True)
    landmark = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=30, null=False)
    zipcode = models.CharField(max_length=8, null=False)
    date_added = models.DateTimeField(auto_now_add=True)


class Order1(models.Model):
    customer = models.ForeignKey(
        Customer1, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transation_id = models.CharField(max_length=100, null=False)
    shipping_address = models.ForeignKey(
        ShippingAddress1, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem1(models.Model):
    product = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(
        Order1, related_name='items', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=9, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_cost(self):
        return self.price*self.quantity
