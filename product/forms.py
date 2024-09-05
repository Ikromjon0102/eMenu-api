from django import forms
from .models import Product, ProductVariant
from django.forms.models import inlineformset_factory


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'product_image']




from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductVariant

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category', 'description',  'product_image']

ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    fields=['size', 'price'],
    extra=1,  # Start with one empty form
    can_delete=True
)
