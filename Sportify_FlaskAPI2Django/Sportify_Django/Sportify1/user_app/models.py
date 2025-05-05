# from django.db import models
# from django.contrib.auth.models import User

# class Address(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
#     house_street = models.CharField(max_length=200)
#     landmark = models.CharField(max_length=100, blank=True, null=True)
#     pincode = models.CharField(max_length=10)
#     state = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.user.username}'s address"

#     def get_full_address(self):
#         return f"{self.house_street}, {self.landmark}, {self.pincode}, {self.state}"


from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100, blank=True)
    house_street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)  # <-- Add this

    
    def __str__(self):
        return f"{self.name} - {self.house_street}, {self.city}"
    
    def get_full_address(self):
        return f"{self.house_street}, {self.city}, {self.state} - {self.pincode}"
