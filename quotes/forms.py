from django import forms
from . models import Stockdatabase

class StockForm(forms.ModelForm):
	class Meta:
		model = Stockdatabase
		fields = ["ticker"]