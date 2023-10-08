from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Login_Info,Product,Cart,Category,Orders,RefferedOrders,DetailOrder
import random,string
import razorpay
from django.core.mail import send_mail
# Create your views here.

is_promoter=False
# True if the method is GET

def promoter(request):
    global is_promoter
    is_promoter = True
    return redirect('/profile')

def buyer(request):
    global is_promoter
    is_promoter = False
    return redirect('/profile')    

def reqGet(request):
    if request.method=="GET":
        return True

#genetrates a referral ID
def finalref():
    referral_id=''
    def ref():
        referral_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return referral_id
    while(True):
        current_ref=ref()
        referral_list=Login_Info.objects.filter(referral_id=current_ref)
        if not referral_list.exists():
            referral_id=current_ref
            break
    return referral_id

# Creating a user in admin table    
def createadminuser(mail,pas):
    u=User.objects.create(username=mail)
    u.set_password(pas)
    u.save()
    

def register(request):
    if reqGet(request):
        return render(request,'register.html')
    else:
        context={}
        fname=request.POST['fname']
        lname=request.POST['lname']
        mail=request.POST['mail']
        pas=request.POST['upass']
        cpas=request.POST['cpass']
        if lname=="" or fname=="" or mail=="" or pas=="" or cpas=="":
            context['errmsg']="Fields cannot be empty !!!"
            return render(request,'register.html',context)
        elif pas!=cpas:
            context['errmsg']="Password Doesn't Match"
            return render(request,'register.html',context)
        else:
            try:
                createadminuser(mail,pas)
                context['success']="Successfuly created"
            except Exception:
                context["errmsg"]="User already exist."
                return render(request,'register.html',context)
            referral_id=finalref()
            c=User.objects.get(username=mail)
            p=Login_Info.objects.create(firstname=fname,lastname=lname,email=mail,password=c.password,referral_id=referral_id,address="")
            return render(request,'register.html',context)


def index(request):
    context={}
    allproduct=Cart.objects.filter(uid=request.user.id)
    context['value']=len(allproduct)
    return render(request,'index.html',context)

def user_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        context={}
        email=request.POST['mail']
        p=request.POST['p']
        u=authenticate(username=email,password=p)
        if u is not None:
            login(request,u)
            allproduct=Cart.objects.filter(uid=request.user.id)
            context['value']=len(allproduct)
            return redirect('/index')
        else:
            context['errmsg']="Invalid email or password!!"
            return render(request,'login.html',context)

def user_logout(request):
    logout(request)
    return redirect('/index')

def home(request):
    context={}
    allproduct=Cart.objects.filter(uid=request.user.id)
    context['value']=len(allproduct)
    product_active=True
    context['product_active']=product_active
    if is_promoter==True:
        context['promoter']=True
    if request.method=='GET':
        p=Product.objects.filter(in_stock=1,status=1)
        if is_promoter==True:
            context['promoter']=True
            p=Product.objects.filter(in_stock=1,status=1,promoting_status=1)
        context['products']=p
        return render(request,'home.html',context)
    else:     
        selected_categories = request.POST.getlist("category")
        if 'reset' in request.POST:
            if(request.POST['reset']):
                selected_categories=[]
                p = Product.objects.filter(in_stock=1,status=1)
                context['products']=p
                if is_promoter==True:
                    context['promoter']=True
                    p=Product.objects.filter(in_stock=1,status=1,promoting_status=1)
                    context['products']=p
                return render(request,'home.html',context)

        print(selected_categories)
        if len(selected_categories)!=0:
            p = Product.objects.filter(category_code__in=selected_categories,in_stock=1,status=1)
            context['select']=selected_categories
            if is_promoter==True:
                context['promoter']=True
                p = Product.objects.filter(category_code__in=selected_categories,in_stock=1,status=1,promoting_status=1)
            context['products']=p
            if 'p' in request.POST:
                sort(request,context)
            return render(request,'home.html',context)
        else:
            p=Product.objects.filter(in_stock=1,status=1)
            if is_promoter==True:
                context['promoter']=True
                p=Product.objects.filter(in_stock=1,status=1,promoting_status=1)
            if 'p' in request.POST:    
                if request.POST['p']=='l2h':
                    para='price'
                    context['l2h']=True
                    p = Product.objects.filter(in_stock=1,status=1).order_by(para)
                    if is_promoter==True:
                        context['promoter']=True
                        p=Product.objects.filter(in_stock=1,status=1,promoting_status=1).order_by(para)
                if request.POST['p']=='h2l':
                    para='-price'
                    context['h2l']=True
                    p = Product.objects.filter(in_stock=1,status=1).order_by(para)
                    if is_promoter==True:
                        context['promoter']=True
                        p=Product.objects.filter(in_stock=1,status=1,promoting_status=1).order_by(para)
        
        context['products']=p
        if request.POST['min'].isdigit() and request.POST['max'].isdigit():
            pricerange(request,context)
        return render(request,'home.html',context)


def sort(request,context):
    p=context['products']
    if is_promoter==True:
        context['promoter']=True
    if request.POST['p']=='l2h':
        print(request.POST['p'])
        para='price'
        p = p.order_by(para)
        context['l2h']=True
        context['h2l']=False
        context['products']=p
        if request.POST['min'].isdigit() and request.POST['max'].isdigit():
            pricerange(request,context)
        return render(request,'home.html',context)
    if request.POST['p']=='h2l':
        print(request.POST['p'])
        para='-price'
        p = p.order_by(para)
        context['h2l']=True
        context['l2h']=False
        context['products']=p
        if request.POST['min'].isdigit() and request.POST['max'].isdigit():
            pricerange(request,context)
        return render(request,'home.html',context)
        
def pricerange(request,context):
    p=context['products']
    min=request.POST['min']
    max=request.POST['max']
    context['min']=min
    context['max']=max
    q1=Q(price__gte = min)
    q2=Q(price__lte = max)
    p=p.filter(q1 & q2)
    context['products']=p
    if is_promoter==True:
        context['promoter']=True
    return render(request,'home.html',context)

def search(request):
    context={}
    find=request.GET['find']
    if find!='':
        p=Product.objects.filter(name__icontains=find)
        context['products']=p
        product_active=True
        context['product_active']=product_active
        context['val']=find
        if is_promoter==True:
            context['promoter']=True
        return render(request,'home.html',context)
    else:
        p=Product.objects.all()
        context['products']=p
        product_active=True
        if is_promoter==True:
            context['promoter']=True
        context['product_active']=product_active
        return redirect('/home')


def profile(request):
    if request.user.is_authenticated:
        context={}
        allproduct=Cart.objects.filter(uid=request.user.id)
        context['value']=len(allproduct)
        currentuser=Login_Info.objects.get(email=request.user.username)
        context['firstname']=currentuser.firstname
        context['lastname']=currentuser.lastname
        context['referral_id']=currentuser.referral_id
        context['address']=currentuser.address
        if is_promoter==True:
            r=RefferedOrders.objects.filter(referral_id=currentuser.referral_id)
            totalcommission=0
            for x in r:
                totalcommission=totalcommission+x.comission_amt
            context['promoter']=True
            context['totalcommission']=totalcommission
        return render(request,'profile.html',context)
    else:
        return redirect('/login')

def save(request):
    if request.user.is_authenticated:
        currentuser=Login_Info.objects.filter(email=request.user.username)
        fname=request.GET['fname']
        lname=request.GET['lname']
        add=request.GET['address']
        print(fname,lname,add)
        currentuser.update(firstname=fname,lastname=lname,address=add)
        return redirect('/profile')
    else:
        return redirect('/login')

def details(request,id):
    context={}
    allproduct=Cart.objects.filter(uid=request.user.id)
    context['value']=len(allproduct)
    p=Product.objects.filter(id=id)
    cat=Category.objects.get(code=p[0].category_code_id)
    context['percent']=cat.promoting_percent
    print(p)
    context['products']=p
    if is_promoter==True:
        context['promoter']=True
    return render(request,'details.html',context)

def addcart(request,rid):
    context={}
    p=Product.objects.filter(id=rid)
    u=User.objects.filter(id=request.user.id)
    if request.user.is_authenticated:
        q1=Q(pid=p[0])
        q2=Q(uid=u[0])
        res=Cart.objects.filter(q1 & q2)
        allproduct=Cart.objects.filter(q2)
        print(len(allproduct))
        context['value']=len(allproduct)
        if res:
            context['dup']="product already exists in Cart!!"
            context['products']=p
            return render(request,'details.html',context)
        else:
            print(p,u)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            allproduct=Cart.objects.filter(q2)
            context['products']=p
            context['value']=len(allproduct)    
            context['success']="Product added Successfully in Cart"
            return render(request,'details.html',context)
    else:
        return redirect('/login')

def cart(request):
    if request.user.is_authenticated: 
        allproduct=Cart.objects.filter(uid=request.user.id)
        context={}
        context['products']=allproduct
        print(len(allproduct))
        context['value']=len(allproduct)
        totalcart=0
        ifpromotedamt=0
        for x in allproduct:
            p=x.pid.price
            com_percent=x.pid.category_code.promoting_percent
            ifpromotedamt=ifpromotedamt+(com_percent*p)/100
            totalcart=x.pid.price+totalcart
        context['totalamt']=totalcart
        currentuser=Login_Info.objects.get(email=request.user.username)
        context['firstname']=currentuser.firstname
        context['lastname']=currentuser.lastname
        context['mail']=currentuser.email
        context['address']=currentuser.address
        context["com"]=ifpromotedamt
        context["len"]=len(allproduct)
        return render(request,'cart.html',context)
    else:
        return redirect('/login')

def remove(request,id):
    if request.user.is_authenticated:
        delid=id
        q1=Q(pid=delid)
        q2=Q(uid=request.user.id)
        c=Cart.objects.filter(q1 & q2).delete()
        return redirect('/cart')
    else:
        return redirect('/login')

def placeorder(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            context={}
            currentuser=Login_Info.objects.get(email=request.user.username)
            print(currentuser.address)
            if(currentuser.address==''):
                context['add']="Add Delivery Address!!"
                allproduct=Cart.objects.filter(uid=request.user.id)
                context['value']=len(allproduct)
                currentuser=Login_Info.objects.get(email=request.user.username)
                context['firstname']=currentuser.firstname
                context['lastname']=currentuser.lastname
                context['referral_id']=currentuser.referral_id
                context['address']=currentuser.address
                return render(request,'profile.html',context)
            else:
                order_num=0
                try:
                    #print(request.POST)
                    order_num=int(order_number_generator(request))
                    ref=request.POST['referral']
                    allproduct=Cart.objects.filter(uid=request.user.id)
                    checkref=refcheck(request,ref)
                    totp=int(request.POST['total0'])
                    #print(totp)
                    purchased_email=Login_Info.objects.get(email=request.user.username)
                    #print(purchased_email)
                    Orders.objects.create(ordernumber=order_num,purchased_email=purchased_email,if_reffered=checkref,price=totp,qty=len(allproduct),status=0)
                    o=Orders.objects.get(ordernumber=order_num)
                    if checkref==True:
                        ifpromotedamt=0
                        for x in allproduct:
                            p=x.pid.price
                            com_percent=x.pid.category_code.promoting_percent
                            ifpromotedamt=ifpromotedamt+(com_percent*p)/100
                            d=DetailOrder.objects.create(ordernumber=o,product_id=x.pid.id)
                            x.delete()
                                         
                        r=RefferedOrders.objects.create(ordernumber=o,referral_id=ref,comission_amt=ifpromotedamt,status=0)
                        return redirect("/makepayment")
                    for x in allproduct:
                        d=DetailOrder.objects.create(ordernumber=o,product_id=x.pid.id)
                        x.delete()
                    return redirect("/makepayment")
                except Exception as e:
                    return HttpResponse(e)
        else:
            return redirect('/login')

def refcheck(request,ref):
    try:
        p=Login_Info.objects.get(referral_id=ref)
        return True
    except:
        return False

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def order_number_generator(request):
    order_num=""
    for i in range(8):
        num=random.randrange(0,9)
        order_num=order_num+str(num)
    #print("orderrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",order_num)
    return order_num


def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_Ql9tB4wL1aiwUh", "XoeVIEv9Hzs5cMFJgva8bAZh"))
    print(client)
    q1=Q(status=0)
    q2=Q(purchased_email=request.user.username)
    onum=Orders.objects.get(q1 & q2)
    print(onum)
    o=DetailOrder.objects.filter(ordernumber=onum)
    oid=str(onum.ordernumber)
    s=onum.price*100
    data = { "amount": s, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print("order id",oid)
    print("total",s)
    print(payment)
    context={}
    context['payment']=payment
    context['user']=Login_Info.objects.get(email=request.user.username)
    return render(request,'payment.html',context)


def sendmail(request):
    pid=request.GET['p1']
    oid=request.GET['p2']
    sign=request.GET['p3']
    myid=request.GET['p4']
    print(myid)
    rec_email=request.user.username
    msg="Your Order has been placed Successfully. Your Order ID : "+myid
    send_mail(
    "marketing Order Status",
    msg,
    "sunnnnnjain@gmail.com",
    [rec_email],
    fail_silently=False,
    )
    o=Orders.objects.filter(ordernumber=myid)
    o.update(status=1)
    o=Orders.objects.get(ordernumber=myid)
    if o.if_reffered==True:
        q1=Q(ordernumber=o.ordernumber)
        q2=Q(status=0)
        ref_id=RefferedOrders.objects.get(q1 & q2)
        ref_rec_mail=Login_Info.objects.get(referral_id=ref_id.referral_id)
        rec_email=ref_rec_mail.email
        msg="You have earned a comission of : "+str(ref_id.comission_amt)
        send_mail(
        "marketing Order Status",
        msg,
        "sunnnnnjain@gmail.com",
        [rec_email],
        fail_silently=False,
        )
        q1=Q(ordernumber=o.ordernumber)
        q2=Q(status=0)
        ref_id=RefferedOrders.objects.filter(q1 & q2)
        ref_id.update(status=1)
    print(pid,oid,sign)
    print('mailed')
    return redirect("/index")






    





