from django.shortcuts import render, redirect
from django.views.generic import View


from product.models import Product





class ProductView(View):
    def get(self, request):
        products = Product.objects.all()

        context = {
            'products':products,
        }
        return render(request, 'product.html', context)


class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id = product_id)
        # sizes = Sizes.objects.filter(product_id = product_id)

        context = {
            'product' : product,
            # 'sizes': sizes
        }

        return render(request, 'detail.html', context)

# chatgpt version
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    variations = product.variants.all()

    context = {
        'product': product,
        'variations': variations,
    }

    return render(request, 'product_detail.html', context)


# class AddProductView(View):
#     def get(self, request):
#         product_form = AddProductForm()
#         # size_form = SizeForm()
#
#         context = {
#             "product_form" : product_form,
#             # 'size_form': size_form
#         }
#
#         return render(request, 'add_product.html', context)
#
#     def post(self, request):
#         product_form = AddProductForm(data=request.data)
#         # size_form = SizeForm(data=request.Post)
#         if product_form.is_valid():
#             product = Product.objects.create(
#                 name = request.data['name'],
#
#                 description = request.data['description'],
#                 product_image = request.data['product_image'],
#                 category = request.data['category']
#             )
#             # size = Sizes.objects.create(
#             #     product_id = product.id,
#             #     size = request.data['size'],
#             #     price = request.data['price']
#             # )
#
#             product.save()
#             # size.save()
#
#             return redirect('products_list')
#
#         context = {
#             "product_form" : product_form,
#             # 'size_form': size_form
#         }
#
#         return render(request, 'add_product.html', context)




# def create_product(request):
#     if request.method == "POST":
#         product_form = ProductForm(request.POST, request.FILES)
#         formset = ProductVariationFormSet(request.POST)
#
#         if product_form.is_valid() and formset.is_valid():
#             product = product_form.save()
#             variations = formset.save(commit=False)
#             for variation in variations:
#                 variation.product = product
#                 variation.save()
#             messages.success(request, 'Product created successfully!')
#             return redirect('product_list')  # Replace with your actual redirect
#     else:
#         product_form = ProductForm()
#         formset = ProductVariationFormSet()
#
#     context = {
#         'product_form': product_form,
#         'formset': formset,
#     }
#     return render(request, 'create_product.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm, ProductVariantFormSet

def create_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        formset = ProductVariantFormSet(request.POST, prefix='variants')

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save()
            variants = formset.save(commit=False)
            for variant in variants:
                variant.product = product
                variant.save()
            messages.success(request, 'Product and its variants were successfully created!')
            return redirect('product_list')
        else:
            print(formset.errors)  # Debugging: Print formset errors if any
    else:
        product_form = ProductForm()
        formset = ProductVariantFormSet(prefix='variants')

    context = {
        'product_form': product_form,
        'formset': formset,
    }
    return render(request, 'create_product.html', context)
