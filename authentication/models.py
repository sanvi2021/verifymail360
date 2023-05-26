from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    Activation_Link = models.CharField(max_length= 256, db_column="Activation_link")
    ip_address = models.CharField(max_length= 100, db_column="IP_Location")
    browser = models.CharField(max_length=100,db_column="Browser_details")

    class Meta:
        db_table = "User"

class User_detail(models.Model):
    user_id = models.AutoField(db_column="User_ID",primary_key= True)
    email_id = models.ForeignKey(User,on_delete= models.PROTECT, db_column="Email_id", related_name="user_email", unique= True)
    password = models.CharField(db_column="Password", max_length= 100)
    created_at = models.DateTimeField(db_column="Created_at", auto_now_add= True)
    modified_at = models.DateTimeField(db_column="Modified_at", auto_now_add=True)
    ip_address = models.CharField(max_length= 100, db_column="IP_Location")
    browser = models.CharField(max_length=100,db_column="Browser_details")

    class Meta:
        db_table = "User_Details"