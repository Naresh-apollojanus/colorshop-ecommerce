from django.shortcuts import render, redirect
from django.views import View
from .forms import ReviewForm

from .models import Category, Product
from cms.models import Blog, Banner
from .serializers import CategorySerializer
from django.http import JsonResponse
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import csv


# Create your views here.

class HomepageView(View):
    def get(self, request):
        if request.GET.get('close-ad'):
            request.session['show-ad'] = False

        show_ad = request.session.get('show_ad', True)

        context = {
            'categories': Category.objects.order_by('-id').all(),
            'best_seller_products': Product.objects.filter(best_seller=True),
            'blogs': Blog.objects.order_by('-pub_date')[:4],
            'top_banner': Banner.objects.filter(location='top').first(),
            'new_arrivals': Product.objects.order_by('-created_date')[:15],
            'bottom_banner': Banner.objects.filter(location='bottom').first(),
            'show_ad': show_ad
        }
        return render(request, 'index.html', context)


class ProductView(View):

    def get(self, request, product_id):
        context = {
            'product': Product.objects.get(pk=product_id)
        }
        return render(request, 'product.html', context)

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('/')

        context = {
            'form': form,
            'product': product
        }
        return render(request, 'product.html', context)


class CategoryApiView(View):
    def get(self, request):
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'slug', 'Details'])
    for category in Category.objects.all():
        writer.writerow([category.title, category.slug, category.details])

    for product in Product.objects.all():
        writer.writerow([product.title, product.slug])

    return response
