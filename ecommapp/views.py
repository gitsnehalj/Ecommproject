from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from ecommapp.models import product,Cart
from django.db.models import Q

# Create your views here.
def about(request):
    return HttpResponse("hello i am in about page...")
def contact(request):
    return HttpResponse("hello  this is contact page")
def edit(request,rid):
    return HttpResponse("id is:"+rid)
def addition(request,x1,x2):
    t=int(x1)+int(x2)
    t1=str(t)
    return HttpResponse("addition is "+t1)
def hello(request):
    context={}
    context['greet']="hello we are learning django..."
    context['x']=10
    context['y']=20
    context['l']=[10,20,30,40,50]
    context['products']=[
        {'id':1,'name':'samsung','cat':'mobile','price':2000},
	{'id':2,'name':'jeans','cat':'clothes','price':500},
	{'id':3,'name':'vivo','cat':'mobile','price':1500},
    ]

    return render(request,'hello.html',context)

def home(request):

  
              p=product.objects.filter(is_active=True)
              print(p)
              context={}
              context['products']=p
              return render(request,'index.html',context)


def product_details(request,pid):
     p=product.objects.filter(id=pid)
     context={}
     context['products']=p
     return render(request,'product_details.html',context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Field cannot be empty"
            return render(request,'register.html',context)
        elif upass !=ucpass:
            context['errmsg']="Password and Confirm password must be same "
            return render(request,'register.html',context)

        else:
         try:
          u=User.objects.create(password=upass,username=uname,email=uname)
          u.set_password(upass)
          u.save()
          context['sucess']="User created Sucessfully ,Please Login"
          return render(request,'register.html',context)
         except Exception:
             context['errmsg']="Username already exist "
             return render(request,'register.html',context) 
    else:

         return render(request,'register.html') 

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="field canot be empty"
       
            
        else:
         u=authenticate(username=uname,password=upass)  
        if u is not None:
           login(request,u)
           return redirect('/home')
        else:
            context['errmsg']="invalid Username  & password"
            return render(request,'login.html',context)
    else:
        return render(request,'login.html')    

def user_logout(request):
    logout(request)
    return redirect('/home')       
      
def catfilter(request,cv):
    q1=Q(is_active=True )
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)  #select * from product where is_active=true and cat=cv
    #p=product.objects.filter( q1)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def sort(request,sv):
    
      if sv=='0':
          col='price'     #asc
      else:
          col='-price'    #desc
      p=product.objects.filter(is_active=True).order_by(col)   #select * from product where is_active=true order by asc/desc
      context={}
      context['products'] =p
      return render(request,'index.html',context)
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3) #select * from product where price>=? and price<=? and is_status=active
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    userid=request.user.id
    u=User.objects.filter(id=userid)

    p=product.objects.filter(id=pid)
    q1=Q(uid=u[0])
    q2=Q(pid=p[0])
    c=Cart.objects.filter(q1 & q2)
    n=len(c)
    context={}
    context['products']=p
    if n==1:
        context['msg']="product already exist in cart"
    else:    
         c=Cart.objects.create(uid=u[0],pid=p[0])
         c.save()
    
         context['success']="product Added sucessfully...."
    return  render(request,'product_details.html',context)
    
def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    print(c)
    context={}
    context['data']=c
    return render(request,'cart.html',context)