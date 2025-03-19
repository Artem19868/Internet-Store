from django.db import models

class Users(models.Model):
    user_name = models.CharField('UserName', max_length=250)
    password = models.CharField('Passord', max_length=250)
    email = models.EmailField('User Email')
    card_number = models.CharField('UsercardNumber')

    def __str__(self):
        return super().__str__()
