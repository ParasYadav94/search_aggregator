from django.shortcuts import render
import requests
from product_search.models import Product
from django.views.decorators.csrf import csrf_exempt
import threading
import time
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

start = time.time()


def paytmMall(search_text):
    """
        Api to fetch data form Paytm Mall Provider
    :param search_text:
    :return: json object
    """
    extract_key = "grid_layout"  # as per resulted json "grid_layout" key has all products as values
    query = "https://search.paytm.com/v2/search?userQuery=" + search_text
    print(query, extract_key)
    try:
        response = requests.get(query)
        data = response.json()
        result = data[extract_key]  # as per resulted json "products" key has all products as values
        product_list = []

        for product in result:
            # Create product list
            product_list.append(Product(name=product['name'], price=product['offer_price'],
                                        url=product['url'], image=product['image_url']))

        # Call bulk_create to create records in a single call
        Product.objects.bulk_create(product_list)

        return data
    except json.decoder.JSONDecodeError as err:
        error, = err.args
        print("error for PAYTMALL ", error)
    except Exception as error:
        er, = error.args
        print(er)
        return er


def shopClues(search_text):
    """
        Api to fetch data form Shop Clues Provider
    :param search_text:
    :return: json object
    """
    extract_key = "products"
    query = "https://api.shopclues.com/api/v11/search?q=" + search_text + "&z=1&key=d12121c70dda5edfgd1df6633fdb36c0"
    print("FOR SHOP CLUE", query)
    try:
        response = requests.get(query)
        data = response.json()
        result = data[extract_key]  # as per resulted json "products" key has all products as values
        product_list = []

        for product in result:
            # Create product list
            product_list.append(Product(name=product['product'], price=product['price'],
                                        url=product['product_url'], image=product['image_url']))

        # Call bulk_create to create records in a single call
        Product.objects.bulk_create(product_list)

        print("ShopClues", product_list)
        return data
    except json.decoder.JSONDecodeError as err:
        error, = err.args
        print("error for ShopClues", error)
    except Exception as error:
        er, = error.args
        print(er)
        return er

    # Product.objects.filter(pk=some_value).update(field1='some value')


def tataCliq(search_text):
    """
        Api to fetch data form Tata Cliq Provider
    :param search_text:
    :return: json object
    """

    extract_key = "searchresult"  # as per resulted json "searchresult" key has all products as values
    query = "https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/serpsearch?type=category&channel=mobile&pageSize=20&typeID=al&page=0&searchText=" + search_text + "&isFilter=false&isTextSearch=true"

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                   "Content-Type": "application/x-www-form-urlencoded"}
        response = requests.get(query, headers=headers)

        data = response.json()
        result = data[extract_key]  # as per resulted json "products" key has all products as values
        product_list = []

        for product in result:
            # Create product list
            print(product)
            product_list.append(Product(name=product["productname"], price=product['sellingPrice']['value'],
                                        url=product['imageURL'], image=product['imageURL']))
            # since the tataCliq json doesn't have any product url

        # Call bulk_create to create records in a single call
        Product.objects.bulk_create(product_list)
        print("TataCliq", result)

    except json.decoder.JSONDecodeError as err:
        error, = err.args
        print("error for TataCliq", error)

    except Exception as error:
        er, = error.args
        print(er)
        return er


@csrf_exempt
def search(request):
    if request.POST:
        search_text = request.POST['search']

        lst = search_text.split(' ')
        if len(lst) > 1:
            search_text = '+'.join(lst)
        products = []
        print("Text to be searched", search_text)
        if Product.objects.filter(name__icontains=search_text).exists():
            product_list = Product.objects.filter(name__icontains=search_text).order_by('id')
            page = request.GET.get('page', 1)
            paginator = Paginator(product_list, 50)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

                # creating threads
        t1 = threading.Thread(target=paytmMall, args=(search_text,), name='t1')
        t2 = threading.Thread(target=shopClues, args=(search_text,), name='t2')
        t3 = threading.Thread(target=tataCliq, args=(search_text,), name='t3')

        # starting threads
        t1.start()
        t2.start()
        t3.start()

        # wait until all threads finish
        t1.join()
        t2.join()
        t3.join()

        print("Elapsed Time: %s" % (time.time() - start))
        return render(request, 'search.html', {'error': '', 'data': products})

    else:
        return render(request, 'search.html', {'error': 'Please enter something', 'data': ''})
