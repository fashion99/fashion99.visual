from django import forms

from .models import Product


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data:
            return []
        if isinstance(data, (list, tuple)):
            return [forms.FileField.clean(self, item, initial) for item in data]
        return [forms.FileField.clean(self, data, initial)]


class ProductForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'code', 'price', 'stock_quantity', 'low_stock_threshold', 'is_active']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'stock_quantity': forms.NumberInput(attrs={'min': '0'}),
            'low_stock_threshold': forms.NumberInput(attrs={'min': '0'}),
        }


class StockAdjustmentForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity change', help_text='Use a negative number for stock leaving the shop.')

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if self.product and self.product.stock_quantity + quantity < 0:
            raise forms.ValidationError('Stock cannot go below zero.')
        if quantity == 0:
            raise forms.ValidationError('Enter a non-zero quantity.')
        return quantity