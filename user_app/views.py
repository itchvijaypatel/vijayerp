# Create your views here.
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from company_app.models import *
from user_app.models import *
from main_app.models import *
from rest_framework.authtoken.models import Token
from rest_framework import routers, serializers, viewsets
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
import datetime as dt
from django.core import files
from django.core.files.base import ContentFile
from .utils import *
import qrcode
import os
from unidecode import unidecode
from geopy.geocoders import Nominatim
from PIL import Image, ImageDraw
from io import BytesIO
from django_otp.oath import totp
import pyotp
# Create your views here.



@csrf_exempt
def Erp_User_Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        pwd = request.POST.get("password")
        
        if Erp_User.objects.filter(email=email).exists():
            if Erp_User.objects.filter(email=email, is_active=True).exists():
                chk_user = Erp_User.objects.get(email=email)
                user = authenticate(request, username=chk_user.username, password=pwd)
                
                if user is not None:
                   
                    # For Token creation
                    if not Token.objects.filter(user=user).exists():
                        Token.objects.get_or_create(user=user)
                    logout(request)
                    login(request, user)
                    
                    if request.user.is_superuser:
                        return redirect("admin_dashboard")
                    else:
                        try:
                            if request.user.is_admin == True:
                                if Company.objects.filter(user=user).exists():
                                    company_obj=Company.objects.filter(user=user).first()
                                    if Company_Purchase_Plan.objects.filter(company=company_obj,is_active=True).exists():
                                        purchase_plan_obj=Company_Purchase_Plan.objects.filter(company=company_obj,is_active=True).first()
                                        l_date = purchase_plan_obj.purchase_date
                                        # delta = l_date + timedelta(days=license.days)
                                        # now = timezone.now()
                                        # remaining_days = delta - now
                                        # if remaining_days.days <= 0:
                                        #     license.status = False
                                        #     license.paid = False
                                        #     license.save()
                                        if company_obj.is_active_status:
                                            ## create barcode for store
                                            EAN = barcode.get_barcode_class("ean13")
                                            barcode_number = random.randint(100000000000, 9999999999999)
                                            store_qr_code_unique_no = barcode_number
                                            qrcode_img = qrcode.make(store_qr_code_unique_no)
                                            canvas = Image.new("RGB", (300, 300), "white")
                                            draw = ImageDraw.Draw(canvas)
                                            canvas.paste(qrcode_img)
                                            buffer = BytesIO()
                                            canvas.save(buffer, "png")

                                            if (company_obj.store_qr_code_unique_no is None or company_obj.store_qr_code_unique_no == ""):
                                                company_obj.store_qr_code_unique_no = store_qr_code_unique_no

                                                company_obj.store_qr_code_image.save(f"MySTOREQRCode{company_obj.store_name}.png",File(buffer),save=False,)
                                                company_obj.save()
                                                
                                            module = "Login"
                                            sub_module = "Admin Login"
                                            heading = "Admin Login Welcome TO ERP"
                                            activity_msg = ("try to login and login successfully")
                                            user_id = request.user.id
                                            user_name = request.user.username
                                            icon = "login"
                                            platform = 0
                                            platform_icon = "web-login by admin"
                                            # save_activity( module,sub_module,heading,activity_msg,user_id,user_name,icon,platform,platform_icon,)
                                            # device=get_user_totp_device(user)
                                            # if device and device.confirmed:
                                            #     return redirect("/verify-two-factor-authentication/")
                                            # elif device and not device.confirmed:
                                            #     return redirect("/dashboard/")
                                            # else:
                                            #     return redirect("/set-two-factor-authentication/")
                                        else:
                                            messages.warning(request, f"Hi {chk_user.first_name} ,Your Store {store_obj.store_name} is inactive due some invalid activity ! ")
                                            messages.warning(request, f"Please contact us Support Team for Re-Active Store .")
                                            return render(request, "main_app/login1.html")

                                    else:
                                        return redirect("/buylicense/")
                                else:
                                    return redirect("/buylicense/")
                                
                              
                                        
                                        
                                    else:
                                        plan = request.session.get("plan")
                                        slug = request.session.get("slug")
                                        print(slug)
                                        print(plan)

                                        if plan is not None and slug is not None:
                                            return redirect(f"/add_store/{plan}/{slug}")
                                        else:
                                            messages.success(request, "User has no store")
                                            return redirect("/")
                              
                            else:
                                # messages.success(request, 'User has no role. Contact ERP Admin')
                                messages.success(request, "User is not Admin")
                                return redirect("/")
                        except:
                            return render(request, "401.html")
                else:
                    messages.info(request, "Incorrect Password")
                    return redirect("/")
            else:
                messages.info(request, "Email Not Verified")
                return redirect("/")
        else:
            messages.info(request, "Incorrect Email")
            # return redirect('login_page')
            return redirect("/")
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    else:
        return render(request, "main_app/login1.html")




@csrf_exempt
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        pwd = request.POST.get("password")
        
        if User.objects.filter(email=email).exists():
            if User.objects.filter(email=email, is_active=True).exists():
                chk_user = User.objects.get(email=email)
                user = authenticate(request, username=chk_user.username, password=pwd)
                
                if user is not None:
                   
                    # For Token creation
                    if not Token.objects.filter(user=user).exists():
                        Token.objects.get_or_create(user=user)
                    logout(request)
                    login(request, user)
                    
                    if request.user.is_superuser:
                        return redirect("admin_dashboard")
                    else:
                        try:
                            if request.user.role.level.level == "Store Admin":
                                
                                license = None
                                try:
                                    license = Licsense.objects.get(user=user, status=True, paid=True)
                                except Licsense.DoesNotExist:
                                    return redirect("/buylicense/")
                                l_date = license.license_date
                                delta = l_date + timedelta(days=license.days)
                                now = timezone.now()
                                remaining_days = delta - now
                                if remaining_days.days <= 0:
                                    license.status = False
                                    license.paid = False
                                    license.save()
                                if Licsense.objects.filter(user=user, status=True, paid=True).exists():
                                    store_license = Licsense.objects.get(user=user, status=True, paid=True)
                                    if store_license.store:
                                        store_obj = Store.objects.get(id=store_license.store.id)
                                        
                                        if store_obj.is_store_active_status:
                                            ## create barcode for store
                                            EAN = barcode.get_barcode_class("ean13")
                                            barcode_number = random.randint(100000000000, 9999999999999)
                                            store_qr_code_unique_no = barcode_number
                                            qrcode_img = qrcode.make(store_qr_code_unique_no)
                                            canvas = Image.new("RGB", (300, 300), "white")
                                            draw = ImageDraw.Draw(canvas)
                                            canvas.paste(qrcode_img)
                                            buffer = BytesIO()
                                            canvas.save(buffer, "png")

                                            if (store_obj.store_qr_code_unique_no is None or store_obj.store_qr_code_unique_no == ""):
                                                store_obj.store_qr_code_unique_no = store_qr_code_unique_no

                                                store_obj.store_qr_code_image.save(f"MySTOREQRCode{store_obj.store_name}.png",File(buffer),save=False,)
                                                store_obj.save()
                                                
                                            module = "Login"
                                            sub_module = "Admin Login"
                                            heading = "Admin Login Welcome TO ERP"
                                            activity_msg = ("try to login and login successfully")
                                            user_id = request.user.id
                                            user_name = request.user.username
                                            icon = "login"
                                            platform = 0
                                            platform_icon = "web-login by admin"
                                            save_activity( module,sub_module,heading,activity_msg,user_id,user_name,icon,platform,platform_icon,)
                                            device=get_user_totp_device(user)
                                            if device and device.confirmed:
                                                return redirect("/verify-two-factor-authentication/")
                                            elif device and not device.confirmed:
                                                return redirect("/dashboard/")
                                            else:
                                                return redirect("/set-two-factor-authentication/")
                                        else:
                                            messages.warning(request, f"Hi {chk_user.first_name} ,Your Store {store_obj.store_name} is inactive due some invalid activity ! ")
                                            messages.warning(request, f"Please contact us Bhaaraterp Support Team for Re-Active Store .")
                                            return render(request, "main_app/login1.html")

                                    else:
                                        plan = request.session.get("plan")
                                        slug = request.session.get("slug")
                                        print(slug)
                                        print(plan)

                                        if plan is not None and slug is not None:
                                            return redirect(f"/add_store/{plan}/{slug}")
                                        else:
                                            messages.success(request, "User has no store")
                                            return redirect("/")
                                else:
                                    return redirect("/buylicense/")
                            else:
                                # messages.success(request, 'User has no role. Contact ERP Admin')
                                messages.success(request, "User is not Admin")
                                return redirect("/")
                        except:
                            return render(request, "401.html")
                else:
                    messages.info(request, "Incorrect Password")
                    return redirect("/")
            else:
                messages.info(request, "Email Not Verified")
                return redirect("/")
        else:
            messages.info(request, "Incorrect Email")
            # return redirect('login_page')
            return redirect("/")
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    else:
        return render(request, "main_app/login1.html")


@csrf_exempt   
def set_two_factor_authentication(request):
    
    if request.user.is_authenticated:
        
        if request.method == "POST":
            
            device = get_user_totp_device(request.user)
            if not device:
                device = request.user.totpdevice_set.create(name=request.user.get_full_name(),confirmed=False)

            qrcode_img=qrcode.make(device.config_url)
            canvas=Image.new("RGB", (525,525),"white")
            draw=ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            buffer=BytesIO()
            canvas.save(buffer,"PNG")
            
            if not QR_Code_Of_Two_Step_Authencation.objects.filter(user=request.user).exists():
                qr=QR_Code_Of_Two_Step_Authencation.objects.create(user=request.user)
                qr.qrcode.save(f'qrcode',File(buffer),save=True)
            else:
                qr=QR_Code_Of_Two_Step_Authencation.objects.filter(user=request.user).first()

            canvas.close()
            return JsonResponse({"success":"Scan QR code","qrcode":qr.qrcode.url})
        else:
            return render(request,'main_app/set_two_factor_authentication.html')
    return redirect('/401/')

 
@csrf_exempt   
def verify_two_factor_authentication(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            otp=request.POST.get('otp')
            device = get_user_totp_device(request.user)
            
            if device and not device.confirmed:
                if device.verify_token(otp):
                    device.confirmed = True
                    device.save()
                    
                    return JsonResponse({"success":"OTP verify successully"})
                else:
                    return JsonResponse({"error":"Invalid OTP"})
            else:
                if device.verify_token(otp):
                    if request.user.store_role.level.level == 'Store Admin':
                        return redirect("/dashboard/")
                    else:
                        return redirect("/emp_dashboard")
                else:
                    messages.info(request, "Invalid OTP")
                    return redirect('/verify-two-factor-authentication/')
        else:
            return render(request,'main_app/verify_totp_user.html')
    return redirect('/401/')



@csrf_exempt   
def two_factor_authentication_enable_or_disable(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            auth=request.POST.get('auth')
            otp=request.POST.get('otp')
            
            device = get_user_totp_device(request.user)
            
            if auth == "enable":
                if device.verify_token(otp):
                    
                    device.confirmed = True
                    device.save()
                    
                    return JsonResponse({"success":"Two step auth enabled successully"})
                else:
                    return JsonResponse({"error":"Invalid OTP"})
            else:
                if device.verify_token(otp):
                    
                    device.confirmed = False
                    device.save()
                    return JsonResponse({"success":"Two step auth disabled successully"})
                else:
                    return JsonResponse({"error":"Invalid OTP"})

    return redirect('/401/')

