from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from user_app.models import *
from main_app.models import *
from rest_framework.authtoken.models import Token
from rest_framework import routers, serializers, viewsets
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
