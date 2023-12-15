from calendar import monthrange
import uuid
import random
import string

from .models import *
from django.http import HttpResponse,JsonResponse
from io import BytesIO,StringIO

import datetime
from Bhaarataaraerp.settings import TEMPLATES_BASE_URL , EMAIL_HOST_USER ,TEMPLATES_BASE_URL_TEST , BASE_URL
from .models import *
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
# --------------------------------
def generate_tokens():
    random_token = uuid.uuid4().hex
    return random_token
from django.template.loader import get_template 
from django.core.mail import EmailMessage 
from product.models import OfferDiscount_Type

from xhtml2pdf import pisa

from sales.models import *
from invoice.models import *
from purchase.models import *
from hrm_app.models import Candiate
from leads.models import Leads_Account,Leads_Contact,Leads_Deal,Leads_Leads_Data
from django.core.files.base import ContentFile

from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.authtoken.models import Token
from django.db.models import Q




def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
        
        
        
# --------------------------------
def generate_tokens():
    random_token = uuid.uuid4().hex
    return random_token

def serach_multifield_name(search_value,first_name,last_name):
    value = Q(*[Q((f'{first_name}__istartswith', term)) | Q((f'{last_name}__istartswith', term)) for term in search_value.split()])
    
    return value
    


# Store Admin Token

def store_admin_authenticate_token(view_func):
    def wrapper_func(request, *args, **kwargs):
        response = {}
        if 'Authorization' in request.headers and request.headers['Authorization'] != "" :
            api_token = request.headers['Authorization']
          
            if StoreAdminToken.objects.filter(token=api_token).exists():
                return view_func(request, *args, **kwargs)
            else:
                response['message'] = "Invalid Authorization token"
                
                return JsonResponse(response,status=401)  # when getting 401 status then user will logout or Invalid token
        else:
            response['message'] = "Authorization token is missing"
            return JsonResponse(response,status=404)
    return wrapper_func


#  Super Admin Token 
def superuser_authenticate_token(view_func):
    def wrapper_func(request, *args, **kwargs):
        response = {}
        if 'Authorization' in request.headers and request.headers['Authorization'] != "" :
            api_token = request.headers['Authorization']
          
            if SuperAdminToken.objects.filter(token=api_token).exists():
                return view_func(request, *args, **kwargs)
            else:
                response['message'] = "Invalid Authorization token"
                return JsonResponse(response,status=401)  # when getting 401 status then user will logout or Invalid token
        else:
            response['message'] = "Authorization token is missing"
            return JsonResponse(response,status=404)
    return wrapper_func

# New token Function 
def new_token():
        token = uuid.uuid1().hex
        return token
    
# Send Forget Password to user
def send_forget_password_email(user):
    token = new_token()
    exp_time = datetime.datetime.now() + datetime.timedelta(minutes=30)

    PasswordResetTokenData.objects.update_or_create(user=user,defaults={'user': user, 'token': token, 'validity': exp_time})

    email_data = {
        'token': token,
        'email': user.email,
        'base_url': TEMPLATES_BASE_URL
    }

    message = get_template('forget_pass/forget_pass.html').render(email_data)
    msg = EmailMessage('Reset Password', body=message, to=[user.email])
    msg.content_subtype = 'html'
    msg.send()

    return Response({"message":"password forget email sent succesfully","resposne_code":200})



def render_to_new_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    
    if not pdf.err:
        return result.getvalue()
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def invoice_upload_file(inovice_id,template_path,folderName,created_by,store):
    
    invoice = Invoice.objects.get(id=inovice_id)
    
    if invoice.invoice_type == 'PURCHASE':
        items=Purchase_Item.objects.filter(order=invoice.purchase_order)
    if invoice.invoice_type == 'SALE':
        items = Sales_Item.objects.filter(sales_order=invoice.sales_order)

    template_path=template_path
    
    context= {'pagesize':'A4',
                'invoice':invoice,
                'items':items,
                # 'customer_gst_details':customer_gst_details,
            }
    
    pdf= render_to_new_pdf(template_path, context)
    receipt_file=ContentFile(pdf)
    
    if not DocumentFolder.objects.filter(store=store,folder_name__iexact=folderName).exists():
        folders = DocumentFolder.objects.create(store=store,folder_name=folderName)
    else:
        folders = DocumentFolder.objects.get(store=store,folder_name=folderName)
        
    files=DocumentFile.objects.create(folder=folders,file_name=f"invoice{invoice.reference_no}.pdf",created_by=created_by)
    files.file.save(f"invoice{invoice.reference_no}.pdf",receipt_file,save=True)
    
    return True
    
    
    
    
    
    

import random
import string

generated_ids = []

def gst_random_request_id():
	length = 8
	"""
	This function generates a random request ID with the specified length.
	The request ID consists of the prefix 'REQ' followed by a random mixture of characters.
	"""
	char_set = string.ascii_letters + string.digits
	# Combine lowercase and uppercase letters and digits
	suffix = ''.join(random.choices(char_set, k=length))
	request_id = f"REQ{suffix}"
	if request_id not in generated_ids:
		generated_ids.append(request_id)
		return request_id
    






###############  ------------- Start Wallet Transaction Function ---------------------- ###########################


from datetime import date, timedelta

def filter_func(selected_range):
    today = date.today()

    # selected_range = 'This Month'  # Example: This Month

    # # Calculate the date range based on the selected option
    # today = date.today()
    
    if selected_range == 'Today':
        start_date = today
        end_date = today

    elif selected_range == 'Yesterday':
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(days=1)

    elif selected_range == 'This Week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif selected_range == 'Previous Week':
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = today - timedelta(days=today.weekday() + 1)
    elif selected_range == 'This Month':
        start_date = date(today.year, today.month, 1)
        end_date = today
    elif selected_range == 'Previous Month':
        if today.month == 1:
            start_date = date(today.year - 1, 12, 1)
        else:
            start_date = date(today.year, today.month - 1, 1)
        end_date = date(today.year, today.month - 1, monthrange(today.year, today.month - 1)[1])
    elif selected_range == 'This Quarter':
        start_date = date(today.year, ((today.month - 1) // 3) * 3 + 1, 1)
        end_date = today
    elif selected_range == 'Previous Quarter':
        if today.month in [1, 2, 3]:
            start_date = date(today.year - 1, 10, 1)
            end_date = date(today.year - 1, 12, 31)
        elif today.month in [4, 5, 6]:
            start_date = date(today.year, 1, 1)
            end_date = date(today.year, 3, 31)
        elif today.month in [7, 8, 9]:
            start_date = date(today.year, 4, 1)
            end_date = date(today.year, 6, 30)
        else:
            start_date = date(today.year, 7, 1)
            end_date = date(today.year, 9, 30)
    elif selected_range == 'This Year':
        start_date = date(today.year, 1, 1)
        end_date = today
    elif selected_range == 'Previous Year':
        start_date = date(today.year - 1, 1, 1)
        end_date = date(today.year - 1, 12, 31)

    # start_date   = start_date.date()
    # end_date     = end_date.date()
    final_date  =  {
        'start_date':start_date,
        'end_date':end_date,
    }

    return (final_date)










def send_sms(user_id,sms_content):
    user=User.objects.filter(id=user_id).first()
    user_obj_profile=UserProfile.objects.filter(user=user).first()
	
    
    url = str('http://sendsms.designhost.in/index.php/smsapi/httpapi/?uname=aaratechnologies&password=123456&sender=ATAARA&tempid=1207161911490829122&receiver=')+str(user_obj_profile.mobile_number)+str('&route=TA&msgtype=1&sms=') +str(sms_content)+str('Please do not share it with anyone. Regards, Aara Tech')
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)


    print(response.text,'TTTTTTTTT')
    if response.status_code == 200:
        return response.status_code
       
    else:
        # request failed
        print("Error: status code {}".format(response.status_code),'RRRRRRRRRRRRrrrr')
                    



import base64
import secrets
           
import random   
            

def make_wallet_transaction(user_id, amount, trans_type,description):
    user_obj=User.objects.filter(id=user_id).first()
    if not Wallet.objects.filter(user=user_obj).exists():
        number = random.randint(1000, 9999)
        w=Wallet.objects.create(user=user_obj,balance=0.0,password=number,mobile_number=user_obj.mobile_no)
        sms_content=f'Dear User your wallet passowrd is {w.password} !'
        sended=send_sms(user_obj.id,sms_content)
        print(sended,'sended password')
        
    wallet_obj = Wallet.objects.get(user=user_obj)
    if trans_type == 'CREDIT':
        print('1')
        money_transactions = WalletTransaction.objects.create(
            user=user_obj,
            status = 'SUCCESS',
            description=description,
            transaction_type = 'CREDIT',
            wallet = wallet_obj,
            transaction_amount = amount,
            previous_amount = round(wallet_obj.balance,2),
            remaining_amount = round(float(wallet_obj.balance),2) + round(float(amount),2),
            date = timezone.now()
           
        )
        transaction_id= str(money_transactions.id)+str(user_obj.id)+secrets.token_urlsafe(3)
        money_transactions.transaction_id = transaction_id
        money_transactions.save()
        Wallet.objects.filter(user=user_obj).update(balance = round(float(wallet_obj.balance),2) + round(float(amount),2))


    elif trans_type == 'DEBIT':
        print(2)
        money_transactions = WalletTransaction.objects.create(
        user=user_obj,
        status = 'SUCCESS',
        description=description,
        transaction_type = 'DEBIT',
        wallet = wallet_obj,
        transaction_amount = amount,
        previous_amount = round(wallet_obj.balance,2),
        remaining_amount = round(float(wallet_obj.balance),2) - round(float(amount),2),
        date = timezone.now()
            
        )
        transaction_id= str(money_transactions.id)+str(user_obj.id)+secrets.token_urlsafe(3)
        money_transactions.transaction_id = transaction_id
        money_transactions.save()
        Wallet.objects.filter(user=user_obj).update(balance = round(float(wallet_obj.balance),2) - round(float(amount),2))





def make_wallet_commission_per_orderitem(user_id, amount, trans_type,description,status):
    user_obj=User.objects.filter(id=user_id).first()
    if not Wallet.objects.filter(user=user_obj).exists():
        number = random.randint(1000, 9999)
        w=Wallet.objects.create(user=user_obj,balance=0.0,password=number,mobile_number=user_obj.mobile_no)
        sms_content=f'Dear User your wallet passowrd is {w.password} !'
        sended=send_sms(user_obj.id,sms_content)
        print(sended,'sended password')
        
    wallet_obj = Wallet.objects.get(user=user_obj)
    if trans_type == 'CREDIT' and status == 'SUCCESS' : 
        print('1')
        money_transactions = WalletTransaction.objects.create(
            user=user_obj,
            status = status,
            description=description,
            transaction_type = 'CREDIT',
            wallet = wallet_obj,
            transaction_amount = amount,
            previous_amount = round(wallet_obj.balance,2),
            remaining_amount = round(float(wallet_obj.balance),2) + round(float(amount),2),
            date = timezone.now()
           
        )
        transaction_id= str(money_transactions.id)+str(user_obj.id)+secrets.token_urlsafe(3)
        money_transactions.transaction_id = transaction_id
        money_transactions.save()
        Wallet.objects.filter(user=user_obj).update(balance = round(float(wallet_obj.balance),2) + round(float(amount),2))


    elif trans_type == 'DEBIT' and status == 'SUCCESS' : 
        print(2)
        money_transactions = WalletTransaction.objects.create(
        user=user_obj,
        status = status,
        description=description,
        transaction_type = 'DEBIT',
        wallet = wallet_obj,
        transaction_amount = amount,
        previous_amount = round(wallet_obj.balance,2),
        remaining_amount = round(float(wallet_obj.balance),2) - round(float(amount),2),
        date = timezone.now()
            
        )
        transaction_id= str(money_transactions.id)+str(user_obj.id)+secrets.token_urlsafe(3)
        money_transactions.transaction_id = transaction_id
        money_transactions.save()
        Wallet.objects.filter(user=user_obj).update(balance = round(float(wallet_obj.balance),2) - round(float(amount),2))
        
        
    elif trans_type == 'CREDIT' and status == 'PENDING' : 
        print('1')
        money_transactions = WalletTransaction.objects.create(
            user=user_obj,
            status = status,
            description=description,
            transaction_type = 'CREDIT',
            wallet = wallet_obj,
            transaction_amount = amount,
            previous_amount = round(wallet_obj.balance,2),
            remaining_amount = round(float(wallet_obj.balance),2) + round(float(amount),2),
            date = timezone.now()
           
        )
        transaction_id= str(money_transactions.id)+str(user_obj.id)+secrets.token_urlsafe(3)
        money_transactions.transaction_id = transaction_id
        money_transactions.save()
     
    elif trans_type == 'DEBIT' and status == 'PENDING' : 
        print(2)
        money_transactions = WalletTransaction.objects.create(
        user=user_obj,
        status = status,
        description=description,
        transaction_type = 'DEBIT',
        wallet = wallet_obj,
        transaction_amount = amount,
        previous_amount = round(wallet_obj.balance,2),
        remaining_amount = round(float(wallet_obj.balance),2) - round(float(amount),2),
        date = timezone.now()
            
        )
        transaction_id= str(money_transactions.id)+str(user_obj.id)+secrets.token_urlsafe(3)
        money_transactions.transaction_id = transaction_id
        money_transactions.save()
       




def make_update_wallet_commission_per_orderitem(user_id,transaction_id, trans_type,description,status):
    user_obj=User.objects.filter(id=user_id).first()
    wallet_obj = Wallet.objects.get(user=user_obj)
    if trans_type == 'CREDIT' and status == 'SUCCESS' : 
        
        
        money_transactions = WalletTransaction.objects.filter(id=transaction_id).first()
        money_transactions.status='SUCCESS'
        money_transactions.description=description
        money_transactions.save()
        Wallet.objects.filter(user=user_obj).update(balance = round(wallet_obj.balance,2) + round(money_transactions.transaction_amount,2))


    elif trans_type == 'DEBIT' and status == 'SUCCESS' : 
        print(2)
        money_transactions = WalletTransaction.objects.filter(id=transaction_id).first()
        money_transactions.status='SUCCESS'
        money_transactions.description=description
        money_transactions.save()
        Wallet.objects.filter(user=user_obj).update(balance = round(wallet_obj.balance,2) - round(money_transactions.transaction_amount,2))
 
        
    elif trans_type == 'CREDIT' and status == 'FAIL' : 
        print('1')
        money_transactions = WalletTransaction.objects.filter(id=transaction_id).first()
        money_transactions.status='FAIL'
        money_transactions.description=description
        money_transactions.save()
       


    elif trans_type == 'DEBIT' and status == 'FAIL' : 
        print(2)
        money_transactions = WalletTransaction.objects.filter(id=transaction_id).first()
        money_transactions.status='FAIL'
        money_transactions.description=description
        money_transactions.save()
       

###############  ------------- Start Wallet Transaction Function ---------------------- ###########################


def tax_currency_symbol(name):
    dic={}
    if Country.objects.filter(name=name).exists():
        country=Country.objects.get(name=name)
        if TaxCurrencySymbol.objects.filter(country=country).exists():
            tax_currency_symbol=TaxCurrencySymbol.objects.get(country=country)
            tax_type=TaxType.objects.get(id=tax_currency_symbol.tax_type.id)
            tax_rate=tax_type.rate.all()
            rate_list=[]
            for r in tax_rate:
                rate_dic={}
                rate_dic['rate']=r.rate
                rate_list.append(rate_dic)
                
            dic['country']=tax_currency_symbol.country.name
            dic['tax_type']=tax_type.title
            dic['rate']=rate_list
            
            dic['currency_name']=tax_currency_symbol.currency_name
            dic['symbol']=tax_currency_symbol.symbol
            # data_list.append(dic)
            return dic
        else:
            return False
    else:
        return False
    
    
def check_value_blank_none(data):
    result=''
    for key,value in data.items():
        if value=='' or value is None:
            result=" ".join(key.split('_')).title()
            break
        
    return result

def check_maindatory_field(data,list):
    
    result=''
    for key,value in data.items():
        if value =="" or value is None:
            if key in list:
                result=" ".join(key.split('_')).title()
                break
    return result


def get_store_plan_details(plan):
    
    store_plan = {}
    modules = Modules.objects.filter(plan_type__title='ERP')
    
    for p in modules:
        key = p.module_name[:-7].lower()
        if plan.modules.filter(id=p.id).exists():
            store_plan[key] = True
        else:
            store_plan[key] = False
    
    return store_plan


def GetStoreUserToken(token):
    
    if Token.objects.filter(key=token).exists():
        user=Token.objects.get(key=token).user
        
        if User_Store.objects.filter(user=user).exists():
            user=User_Store.objects.filter(user=user).first()
            return user
        else:
            return Response(data= {'message':"User doesn't exist",'response_code':201})
    else:
        return Response(data= {'message':"Invalid Authorization token",'response_code':201})
    
    


def password_generator(length):
    letter = string.ascii_letters + string.digits
    password = "".join(random.sample(letter,length))
    return password



def send_new_mail(store,email,template_path,context):
    template = get_template(template_path).render(context)
    if SettingEmailConfiguration.objects.filter(store__id=store.id).exists():
        backend = email_configuration(store.id)
        user_name = str(backend.username)
        msg = EmailMessage(store.store_name+ " - Account Credentials : Powered By Bhaarat ERP",body=template,from_email=user_name,to=[email],connection=backend)
        msg.content_subtype = "html"
        msg.send()
    else:
        msg = EmailMessage(store.store_name+ " - Account Credentials : Powered By Bhaarat ERP",body=template,to=[email])
        msg.content_subtype = "html"
        msg.send()
        
        
def get_associate_data(folder_type,user):
    
    if folder_type == "Customer":
        associate_data = Customer.objects.filter(store=user.store).values('id','first_name','last_name')
            
    elif folder_type == "Candidate":
        associate_data = Candiate.objects.filter(store=user.store).values('id','first_name','last_name')
        
    elif folder_type == "Employee":
        associate_data = [dict(id=i.emp_id,name=i.user.get_full_name()) for i in EmployeesInfo.objects.filter(store=user.store)]
        
    elif folder_type == "Vendor":
        associate_data = Vendor.objects.filter(store=user.store).values('id','first_name','last_name')

    elif folder_type == "Lead":
        associate_data = Leads_Leads_Data.objects.filter(store=user.store).values('id','first_name','last_name')

    elif folder_type == "Contact":
        associate_data = Leads_Contact.objects.filter(store=user.store).values('id','first_name','last_name')
        
    elif folder_type == "Account":
        associate_data = Leads_Account.objects.filter(store=user.store).values('id','account_name')
        
    elif folder_type == "Deal":
        associate_data = Leads_Deal.objects.filter(store=user.store).values('id','deal_name')
    else:
        associate_data = []
        
    return associate_data

        
        