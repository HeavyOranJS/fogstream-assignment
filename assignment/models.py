from django.db import models
from django.contrib.auth.models import User, UserManager

# class UserManager(UserManager):
#     self.create_user()

class User(User):
    def __str__(self):
        return self.username

