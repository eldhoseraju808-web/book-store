from django.db import models

# Create your models here.
class reg_tbl(models.Model):
    fname=models.CharField(max_length=25)
    mobile=models.IntegerField()
    email=models.EmailField()
    pssw=models.CharField(max_length=16)
    cpssw=models.CharField(max_length=16)


class pro_tbl(models.Model):
    bnm=models.CharField(max_length=25)
    prc=models.IntegerField()
    pimg=models.FileField(upload_to='pic')
    des=models.TextField()

class cart_tbl(models.Model):
    products=models.ForeignKey(pro_tbl,on_delete=models.CASCADE)
    customer=models.ForeignKey(reg_tbl,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    
