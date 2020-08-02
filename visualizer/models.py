from django.db import models

# Create your models here.
class Referral(models.Model):

    Advocate_First_Name = models.CharField(max_length=200)
    Advocate_Last_Name = models.CharField(max_length=200)
    Advocate_Email = models.CharField(max_length=200)
    Advocate_Name = models.CharField(max_length=200, default='')
    Friend_First_Name = models.CharField(max_length=200)
    Friend_Last_Name = models.CharField(max_length=200)
    Friend_Name = models.CharField(max_length=200, default='')
    Friend_Email = models.CharField(max_length=200)
    Order_Number = models.CharField(max_length=200)
    Completed_At = models.DateField(blank=True, null= True)
    State = models.CharField(max_length=200)
    Total_Amount_Spent = models.DecimalField(max_digits=999,decimal_places=2)

    # def __str__(self):
    #     return self.Advocate_First_Name