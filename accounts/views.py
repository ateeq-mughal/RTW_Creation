from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from ordered_set import OrderedSet
from datetime import date
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
# Create your views here.

today = date.today()

def index(request):
    
    if request.user.is_anonymous:
        print("ANONY HAI")
        return redirect('/login') 

    print("NAHI HAI")
    return render(request, 'index.html')


# @login_required(redirect_field_name='login')
def internalTransfer(request):

    if request.user.is_anonymous:
        print("ANONY HAI")
        return redirect('/login') 

    df = pd.read_csv('static/products_export.csv')
    df1 = df[['Title', 'Variant SKU', 'Image Src']]
    df2 = df1.dropna(subset=['Title'], how='all')
    sku_variant_list = df2["Variant SKU"].tolist()
    sku_unique_set = set()
    sku_list = []
    for sku in sku_variant_list:
        sku_list.append(sku.split('-')[0])
        sku_unique_set.add(sku.split('-')[0])

    df2['Unique SKU'] = sku_list

    img_link = df2["Image Src"].tolist()
    for link in img_link:
        img_link[img_link.index(link)] = link.split("?", 1)[0]+'?width=250'

    df2['Image Src'] = img_link
    df2 = df2[['Title','Unique SKU','Variant SKU','Image Src']]

    product_dict = dict()

    for unique_sku in sku_unique_set:
        # print(unique_sku)
        product_dict[unique_sku] = df2.loc[df2['Unique SKU'] == unique_sku]

    class_level1 = []
    for key in product_dict:
        class_level1.append(product_dict[key].iloc[0].tolist())

    names = {}
    for unique_sku in sku_unique_set:
        name = list(OrderedSet(product_dict[unique_sku].iloc[0][0].split()) & OrderedSet(product_dict[unique_sku].iloc[1][0].split()))
        names[unique_sku] = ' '.join(name).title()
        
    for product in class_level1:
        product[0] = names[product[1]]

    # print(len(class_level1))
    int_len_of_unique_sku = len(class_level1)//4
    len_of_unique_sku = []
    for i in range(int_len_of_unique_sku):
        len_of_unique_sku.append(i)

    class_level1_row = []
    all_unique = []
    count = 1
    # print(len(class_level1)//4)
    for i in range(1,(len(class_level1)//4)+1):
        for col in range(1,5):
            # print(count)
            try:
                class_level1_row.append(class_level1[count])
            except IndexError:
                break
            count += 1
        all_unique.append(class_level1_row)
        class_level1_row = []

    context = {
        'unique_sku' : all_unique,
        'date' : today.strftime(" %d/%m/%Y ")
    }
        

    return render(request, 'internalTransfer.html', context)

def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
    
        else:
            print("MAATTT CHALAAna")
            return render(request, 'login.html')
    
    if not request.user.is_anonymous:
        return redirect('/')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')
