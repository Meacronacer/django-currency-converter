from django.shortcuts import render
import requests


def exchange(request):
    response = requests.get('https://cdn.jsdelivr.net/gh/prebid/currency-file@1/latest.json?date=20230206').json()
    currency = response.get('conversions').get('USD')

    if request.method == 'GET':
        context = {
            'currency': currency
        }

        return render(request, 'main/index.html', context)

    if request.method == 'POST':

        if request.POST.get('from-amount') == '' or float(request.POST.get('from-amount')) < 0:
            return render(request, 'main/index.html', {'currency':currency})

        from_amount = request.POST.get('from-amount')
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((currency[to_curr] / currency[from_curr] * float(from_amount)), 2)

        context = {
            'converted_amount':converted_amount,
            'currency': currency,
            'from_amount': from_amount,
            'from_curr': from_curr,
            'to_curr': to_curr
        }

        return render(request, 'main/index.html', context)