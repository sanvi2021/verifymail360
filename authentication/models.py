from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True, db_column="username")
    email = models.EmailField(max_length=255, unique=True, db_index=True, db_column="email")
    is_verified = models.BooleanField(default=False, db_column="verified")
    is_active = models.BooleanField(default=True, db_column="active")
    is_staff = models.BooleanField(default=False, db_column="staff")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")
    ip_address = models.CharField(max_length= 100, db_column="IP_Location")
    browser = models.CharField(max_length=100,db_column="Browser_details")
    # auth_provider = models.CharField(
    #     max_length=255, blank=False,
    #     null=False, default=AUTH_PROVIDERS.get('email'))
    class Meta:
        db_table = "User"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token)
    #     }


# class User(AbstractUser):
#     Activation_Link = models.CharField(max_length= 256, db_column="Activation_link")
#     ip_address = models.CharField(max_length= 100, db_column="IP_Location")
#     browser = models.CharField(max_length=100,db_column="Browser_details")

#     class Meta:
#         db_table = "User"

# class User_detail(models.Model):
#     user_id = models.AutoField(db_column="User_ID",primary_key= True)
#     email_id = models.ForeignKey(User,on_delete= models.PROTECT, db_column="Email_id", related_name="user_email", unique= True)
#     password = models.CharField(db_column="Password", max_length= 100)
#     created_at = models.DateTimeField(db_column="Created_at", auto_now_add= True)
#     modified_at = models.DateTimeField(db_column="Modified_at", auto_now_add=True)
#     ip_address = models.CharField(max_length= 100, db_column="IP_Location")
#     browser = models.CharField(max_length=100,db_column="Browser_details")

#     class Meta:
#         db_table = "User_Details"