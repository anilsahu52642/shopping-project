from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator



STATE_CHOICES=(
    ('Andaman & Nocobar Island','Andaman & Nocobar Island'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),

)




class customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=64)
    locality=models.CharField(max_length=64)
    city=models.CharField(max_length=64)
    zipcode=models.IntegerField()
    state=models.CharField(max_length=64,choices=STATE_CHOICES)


    def __str__(self):
        return str(self.id)



CATAGORY_CHOICES=(('m','mobile'),('l','laptop'),('tw','top wear'),('bw','bottom wear'))

class product(models.Model):
    title=models.CharField(max_length=64)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=64)
    catagory=models.CharField(max_length=64,choices=CATAGORY_CHOICES)
    product_image=models.ImageField(upload_to='productimg')


    def __str__(self):
        return str(self.id)



class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.product.discount_price*self.quantity



STATUS_CHOICES=(('accepted','accepted'),('packed','packed'),('on the way','on the way'),('delivered','delivered'),('cancel','cancel'))

class orderplaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE,default=None)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=64,choices=STATUS_CHOICES,default='pending')


    @property
    def total_cost2(self):
        return self.product.discount_price*self.quantity
