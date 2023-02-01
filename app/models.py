from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



class category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class seller(models.Model):
    seller_id = models.BigAutoField(primary_key=True)
    seller_name = models.CharField(max_length=10)
    seller_email_id = models.EmailField(max_length=50)
    seller_mobile_no = models.BigIntegerField()
    #seller_login_pass = models.CharField(max_length=20)
    seller_add = models.TextField(max_length=100)
    GST_no = models.CharField(max_length=20)

    def __str__(self):
        return self.seller_name


class product(models.Model):
    pr_name = models.CharField(max_length=200)
    pr_id = models.BigAutoField(primary_key=True)
    pr_price = models.FloatField(max_length=20, default=1)
    pr_status = models.BooleanField(default=1)
    category_id = models.ForeignKey(category, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(seller, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)
    description = models.TextField()
    pr_image = models.ImageField(upload_to='product_img')

    def __str__(self):
        return str(self.pr_name)


class customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(product, related_name="product", through="orders")
    c_id = models.BigAutoField(primary_key=True)
    c_name = models.CharField(max_length=20)
    email_id = models.CharField(max_length=20)
    mobile_no = models.BigIntegerField()
    c_add = models.TextField(max_length=100)

    def __str__(self):
        return self.c_name

class cart(models.Model):
    
    order_no = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #c_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    Product = models.ForeignKey(product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_quantity = models.PositiveIntegerField(null=True, default=1)

    def __str__(self):
        return str(self.order_no)

    @property
    def total_cost(self):
        return self.order_quantity * self.Product.pr_price


class orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    c_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    pr_id = models.ForeignKey(product, on_delete=models.CASCADE)
    order_no = models.ForeignKey(cart, on_delete=models.CASCADE)
    cart_quantity = models.PositiveIntegerField(null=True, default=1)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_no)

    class Meta:
        unique_together = ('c_id','pr_id')

class order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    Product = models.ForeignKey(product, on_delete=models.CASCADE)
    #order = models.IntegerField(primary_key=True)
    cart_quantity = models.PositiveIntegerField(null=True, default=1)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.cart_quantity * self.Product.pr_price


'''class warehouse(models.Model):
    pr_id = models.OneToOneField(product, on_delete=models.CASCADE, primary_key=True)
    order_no = models.OneToOneField(cart, on_delete=models.CASCADE)
    #quantity = models.ForeignKey(product, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['pr_id', 'order_no']]


class payment(models.Model):
    pay_id = models.BigAutoField(primary_key=True)
    pay_type = models.CharField(max_length=20)
    order_no = models.OneToOneField(cart, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pay_id)'''