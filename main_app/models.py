from django.db import models

from user_app.models import Erp_User

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







class Company(models.Model):
    
    erp_user=models.OneToOneField(Erp_User,on_delete=models.CASCADE)
    qr_code_image = models.ImageField(upload_to='qr_code', blank=True,null=True)
    qr_code_unique_no=models.CharField(max_length=250,null=True,blank=True,unique=True)
    business_type = models.ForeignKey(BusinessSubCategory,null=True, blank=True,on_delete=models.CASCADE) 
    name = models.CharField(max_length=255, null=True, blank=True,unique=True)
    
    logo = models.ImageField(upload_to='logo', blank=True, null=True)
    ifse = models.CharField(max_length=40, blank=True, null=True)
    bank_name = models.CharField(max_length=40, blank=True, null=True)
    account_no = models.CharField(max_length=50,null=True, blank=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    ## address
    address = models.CharField(max_length=255, null=True, blank=True)
    country= models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    
    # gst details
    gst_number          = models.CharField(max_length=40,null=True,blank=True)
    pan_number          = models.CharField(max_length=40,null=True,blank=True)
    business_legal_name = models.CharField(max_length=250,null=True,blank=True)
    business_trade_name = models.CharField(max_length=250,null=True,blank=True)
    gst_registered_on   = models.CharField(max_length=250,null=True,blank=True)
    
    
    website = models.CharField(max_length=100, null=True, blank=True)
    is_reseller = models.BooleanField(default=False)
    reseller_id = models.CharField(max_length=50,default=0,null=True,blank=True)
    

    swift_code = models.CharField(max_length=40, blank=True, null=True)
    upi_code = models.ImageField(upload_to="upi",blank=True, null=True)
    signature = models.ImageField(upload_to="signature",blank=True, null=True)
    status   = models.IntegerField(default=0,null=True,blank=True)
    active_status = models.IntegerField(default=0)
    
    latitude = models.CharField(max_length=250,null=True,blank=True)
    longitude   = models.CharField(max_length=250,null=True,blank=True)
    
    
    #inventory status
    variant_status= models.BooleanField(default=True)
    spec_status=models.BooleanField(default=True)
    sync_status = models.BooleanField(default=True)
    bulk_product_status = models.BooleanField(default=True)
    #Sales status
    customer_status = models.BooleanField(default=True)
    #purchase status
    purchase_order_mail_status = models.BooleanField(default=True)
    vendor_mail_status = models.BooleanField(default=True)
    #HRM status   
    hiring_status = models.BooleanField(default=True)
    candidate_bulk_upload_status = models.BooleanField(default=True)
    hiring_history_status = models.BooleanField(default=True)
    attendance_status = models.BooleanField(default=True)
    attendance_bulk_upload_status = models.BooleanField(default=True)
    team_status = models.BooleanField(default=True)
    #CRM status 
    leads_status = models.BooleanField(default=True)
    sales_target_status = models.BooleanField(default=True)
    customer_bulk_upload_status = models.BooleanField(default=True)
    #Finance 
    gst_filling_status = models.BooleanField(default=True)
    email_calendar_invitaion= models.BooleanField(default=True)

    # delivery app
    delivery_manages_by= models.CharField(max_length=255,null=True,blank=True)
    
    manufacturing_status = models.BooleanField(default=False)

    currency=models.CharField(max_length= 100, null=True, blank=True)
    flag = models.ImageField(upload_to='flag', blank=True, null=True)
    
    
    is_real_time_sync=models.BooleanField(default=False)
    
    is_active_status=models.BooleanField(default=True)

    
 
    def __str__(self):
        return str(self.name) +" | " + str(self.id)  +" | " + str(self.erp_user)