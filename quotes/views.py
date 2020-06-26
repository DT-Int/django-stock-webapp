from django.shortcuts import render, redirect
from . models import Stockdatabase
from django.contrib import messages
from . forms import StockForm

def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_d4269b0c95cd4922ad9e983fe640c1a2")

		try:
			api = json.loads(api_requests.content)
		except Exception as e:
			api = "Error..."
		return render(request, 'home.html', {'api': api })
	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol"})


def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock added successfully!"))
			return redirect('add_stock')

	else:
		ticker = Stockdatabase.objects.all()
		output = []
		for ticker_item in ticker:
			api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_d4269b0c95cd4922ad9e983fe640c1a2")
			try:
				api = json.loads(api_requests.content)
				output.append(api)
			except Exception as e:
				api = "Error..."
		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stockdatabase.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock removed!"))
	return redirect(delete_stock)



def delete_stock(request):
	ticker = Stockdatabase.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})