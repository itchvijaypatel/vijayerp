from django.db import models
from django.contrib.sessions.models import Session
from user_app.models import Erp_User
from django.contrib.auth.models import Group
# Create your models here.


# Business Category Section 
class BusinessCategory(models.Model):
    name    = models.CharField(max_length=255,null=True,blank=True)
    status  =models.BooleanField(default=True)
    def __str__(self):
        return str(self.id)  + '| '+ str(self.name)
    
# Business Category Section 
class BusinessSubCategory(models.Model):
    category    = models.ForeignKey(BusinessCategory,on_delete=models.CASCADE,null=True,blank=True)
    name        = models.CharField(max_length=255,null=True,blank=True)
    status  =models.BooleanField(default=True)
    def __str__(self):
        return str(self.id)  + '|' + str(self.name) + '|' + self.category.name 
    




# Country list 
class Country(models.Model):
    country=models.CharField(max_length=255,null=True,blank=True)
    flag = models.ImageField(upload_to='country_flag', blank=True, null=True)
    status=models.IntegerField(default=True) 

    def __str__(self):
        return str(self.id) +     '|' + str(self.country)


class State(models.Model):
    country=models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(default=True)
    def __str__(self):
        return str(self.state) + str(self.id)

class City(models.Model):
    state=models.ForeignKey(State,on_delete=models.CASCADE,null=True, blank=True)
    city=models.CharField(max_length=255,null=True, blank=True)
    status=models.IntegerField(default=True)
    def __str__(self):
        return str(self.city)+ " " +str(self.state.state)
    

class Pincode(models.Model):
    city_name = models.CharField(max_length=200,null=True,blank=True)
    pincode   = models.CharField(max_length=200,null=True,blank=True) 
    status = models.BooleanField(default=True)



class TaxRate(models.Model):
    rate=models.FloatField(default=0)
    def __str__(self):
        return str(self.rate)

class TaxType(models.Model):
    title=models.CharField(max_length=50,null=True,blank=True)
    rate=models.ManyToManyField(TaxRate,blank=True)
    
    def __str__(self):
        return str(self.title)

class TaxCurrencySymbol(models.Model):
    country=models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
    tax_type=models.ForeignKey(TaxType,on_delete=models.CASCADE,null=True,blank=True)
    tax_name=models.CharField(max_length=255,null=True,blank=True)
    currency_name=models.CharField(max_length=255,null=True,blank=True)
    symbol=models.CharField(max_length=50,null=True,blank=True)
    
    def __str__(self):
        return str(self.country.country) +" "+ str(self.symbol) 



class Erp_Plan(models.Model):
    plan_name=models.CharField(max_length=255,unique=True)#Make one plan type ERP
    monthly_price = models.FloatField(default=0.00)
    yearly_price = models.FloatField(default=0.00)
    no_of_user=models.IntegerField()
    module=models.ManyToManyField(Group,blank=True)
 
    def __str__(self):
        return self.plan_name
    
    def save(self,*args,**kwargs):
        self.plan_name = self.plan_name.upper()
        return super(Erp_Plan,self).save(*args,**kwargs)
      
   




