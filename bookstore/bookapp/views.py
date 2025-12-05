from django.shortcuts import render,redirect
from . models import reg_tbl,pro_tbl,cart_tbl
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request,'index.html')

def reg(request):
    if request.method=='POST':
        fnm=request.POST.get('fn')
        mob=request.POST.get('mb')
        eml=request.POST.get('em')
        psw=request.POST.get('ps')
        cpsw=request.POST.get('cps')
        obj=reg_tbl.objects.create(fname=fnm,mobile=mob,email=eml,pssw=psw,cpssw=cpsw)
        obj.save()
        if obj:
            return render(request,'login.html')
        else:
            return render(request,'reg.html')

    return render(request,'reg.html')

def log(request):
    if request.method=="POST":
        em=request.POST.get("email")
        ps=request.POST.get("password")
        obj=reg_tbl.objects.filter(email=em,pssw=ps)
        if obj:
            request.session['ema']=em
            request.session['psa']=ps
            for m in obj:
                idno=m.id
                request.session['idl']=idno
            return render(request,'home.html')
        else:
            msg='Invalid credentials..'
            request.session['ema']=''
            request.session['psa']=''
            return render(request,'login.html',{'error':msg}) 
    return render(request,'login.html')

def details(tab):
    obj=reg_tbl.objects.all()
    return render(tab,'details.html',{'data':obj})

def edit(request):
    idl=request.GET.get('idno')
    obj=reg_tbl.objects.filter(id=idl)
    return render(request,'edit.html',{'data':obj})
 
def delete(request,idl):
    obj=reg_tbl.objects.filter(id=idl)
    obj.delete()
    return render(request,'details.html')

def product(request):
    if request.method=='POST':
        bookn=request.POST.get('bn')
        bkimg=request.FILES.get('bi')
        price=request.POST.get('prcc')
        dess=request.POST.get('ds')
        obj= pro_tbl.objects.create(bnm=bookn,prc=price,pimg=bkimg,des=dess)
        obj.save()
        if obj:
            msg=' successfully uploded'
            return render(request,"product.html",{"success":msg})
    return render(request,'product.html')

def books(request):
    query = request.GET.get('q')  

    if query:
        obj = pro_tbl.objects.filter(
            Q(bnm__icontains=query) |   
            Q(des__icontains=query)     
        )
    else:
        obj = pro_tbl.objects.all()

    return render(request, 'books.html', {"books": obj})

def cart(req,idn):
    products= pro_tbl.objects.get(id=idn)
    cid= req.session['idl']
    customer=reg_tbl.objects.get(id=cid)
    cartitem,created=cart_tbl.objects.get_or_create(products=products,customer=customer)
    if not created:
        cartitem.qty+=1
        cartitem.save()
    messages.success(req,"item added to cart")
    return redirect('/books')

def viewcart(request):
    cid=request.session['idl']
    cobj = reg_tbl.objects.get(id=cid)
    cartobj= cart_tbl.objects.filter(customer=cobj)
    if cartobj:
        total_price=0
        for m in cartobj:
            pro= m.products.prc*m.qty
            total_price+=pro
        return render(request,'cart.html',{'cart':cartobj,'total':total_price})
    else:
        return render(request,"cart.html",{"info":"your cart in empty..."})
    
def cartdelete(request,pid):
    products=cart_tbl.objects.get(id=pid)
    products.delete()
    return redirect("/viewcart")

