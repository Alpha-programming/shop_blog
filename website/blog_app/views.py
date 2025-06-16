from django.shortcuts import get_object_or_404, render, HttpResponse,redirect
from . import models
from django.contrib.auth import login, logout
from . forms import LoginForm,RegisterForm,CommentForm,ProductForm,ContactForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction


def render_home_page(request):
    slides = models.Slider.objects.all()
    questions = models.FAQ.objects.all()
    products = models.Product.objects.all()

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'slides': slides,
        'questions': questions,
        'products': products,
    }

    return render(request, 'blog_app/index.html', context)

def render_articles_page(request):
    query_params = request.GET.get('category')
    page = request.GET.get('page')

    products = models.Product.objects.all()

    if query_params:
    
        products = products.filter(category__slug=query_params)


    paginator = Paginator(products, 3)
    
    products = paginator.get_page(page)
    

    categories = models.Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'slug': query_params
    }
    return render(request, 'blog_app/products.html', context)


def render_about_page(request):
    return render(request, 'blog_app/about.html')


def render_contacts_page(request):
    return render(request, 'blog_app/contacts.html')

def render_faq_page(request):
    questions = models.FAQ.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'blog_app/faq.html', context)

def render_register_page(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration was successful')
            return redirect('login')

    else:
        form = RegisterForm()

    context = {
        'form':form
    }

    return render(request,'blog_app/register.html',context)

def render_login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, "You've successfully logged in")
                return redirect('home')
            else:
                messages.error(request, 'User not found')
        else:
            messages.error(request, 'Incorrect user or password')
    else:
        form = LoginForm()
    
    context = {
        'form': form
    }
    return render(request,'blog_app/login.html', context)

@login_required(login_url='login')
def render_product_detail_page(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    comments = models.Comment.objects.filter(product=product)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.author = request.user
            form.save()
            messages.success(request, 'Comment added successfully')
            return redirect('product_detail', slug=product.slug)
    else:
        form = CommentForm()

    if request.user.is_authenticated:
        is_viewed = models.ProductCountView.objects.filter(
            product=product,
            user=request.user
        ).exists()
        
        if not is_viewed:
            models.ProductCountView.objects.create(
                product=product,
                user=request.user
            )
            product.views += 1
            product.save()

    try:
        product.likes
    except Exception:
        models.Like.objects.create(product=product)

    try:
        product.dislikes
    except Exception:
        models.Dislike.objects.create(product=product)

    total_likes = product.likes.user.all().count()
    total_dislikes = product.dislikes.user.all().count()

    context = {
        'product': product,
        'comments': comments,
        'form': form,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments': comments.count()
    }
    return render(request, 'blog_app/product_detail.html', context)

class UpdateProduct(UpdateView):
    model = models.Product
    form_class = ProductForm
    template_name = 'blog_app/product_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Handle new gallery images
        gallery_images = self.request.FILES.getlist('gallery')
        for image in gallery_images:
            models.ProductImage.objects.create(product=self.object, photo=image)

        return response

class DeleteProduct(DeleteView):
    model = models.Product
    success_url = '/products/'
    template_name = 'blog_app/product_confirm_delete.html'

def delete_image(request, pk):
    image = get_object_or_404(models.ProductImage, pk=pk)
    
    product_slug = image.product.slug
    image.delete()
    return redirect('update', slug=product_slug)

@login_required(login_url='login')
def handle_product_action(request, product_id, action):
    product = get_object_or_404(models.Product, pk=product_id)
    user = request.user

    like_obj, _ = models.Like.objects.get_or_create(product=product)
    dislike_obj, _ = models.Dislike.objects.get_or_create(product=product)

    if action == 'add_like':
        if user in like_obj.user.all():
            like_obj.user.remove(user.pk)
        else:
            like_obj.user.add(user)
            dislike_obj.user.remove(user.pk)
    elif action == 'add_dislike':
        if user in dislike_obj.user.all():
            dislike_obj.user.remove(user.pk)
        else:
            dislike_obj.user.add(user.pk)
            like_obj.user.remove(user.pk)
    elif action == 'add_basket':
        basket_item, created = models.Basket.objects.get_or_create(user=request.user, product=product)
        if not created:
            basket_item.quantity += 1
            basket_item.save()
    elif action == 'add_favourite':
        favourite_item, created = models.Favourite.objects.get_or_create(user=request.user, product=product)
        if not created:
            favourite_item.save()

    return redirect('product_detail', slug=product.slug)

@login_required(login_url='login')
def render_profile_page(request):
    user = request.user
    products = models.Product.objects.filter(author=user)

    total_likes = 0
    total_dislikes = 0
    total_comments = 0
    total_views = 0
    
    for product in products:
        total_comments += product.comments.all().count()
        total_views += product.productcountview_set.all().count()  

        likes = getattr(product, 'likes', None)
        if likes:
            total_likes += likes.user.all().count()

        dislikes = getattr(product, 'dislikes', None)
        if dislikes:
            total_dislikes += dislikes.user.all().count()

    show_all = request.GET.get('show_all')
    if show_all:
        orders = models.Order.objects.filter(user=user).order_by('-created_at')
    else:
        orders = models.Order.objects.filter(user=user).order_by('-created_at')[:3]

    context = {
        'total_products': products.count(),
        'total_comments': total_comments,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'products': products,
        'orders': orders
    }

    return render(request, 'blog_app/profile.html', context)


@login_required(login_url='login')
def render_basket_page(request):
    basket_items = models.Basket.objects.select_related('product').filter(user=request.user)
    
    products_with_details = []
    total_price = 0
    total_items = 0

    for item in basket_items:
        product = item.product
        quantity = item.quantity
        subtotal = product.price * quantity
        products_with_details.append({
            'pk': item.pk,
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total_price += subtotal
        total_items += quantity

    context = {
        'products_with_details': products_with_details,
        'total_price': total_price,
        'total_items': total_items,
    }
    return render(request, 'blog_app/basket.html', context)

@login_required(login_url='login')
def render_favourites_page(request):
    models.Favourite.objects.filter(user=request.user, product__isnull=True).delete()

    favourite_items = models.Favourite.objects.filter(user=request.user).select_related('product')

    products_info = []
    total_items = 0
    total_price = 0

    for item in favourite_items:
          
        subtotal = item.product.price 
        products_info.append({
            'pk': item.pk,
            'product': item.product,
            'subtotal': subtotal,
        })
        total_items += len(favourite_items)
        total_price += subtotal

    context = {
        'products_info': products_info,
        'total_items': total_items,
        'total_price': total_price,
    }
    return render(request, 'blog_app/favourites.html', context)

def delete_item(request, action, item_id):
    if action == "basket":
        item = get_object_or_404(models.Basket, pk=item_id, user=request.user)
        item.delete()
        messages.success(request, "Item removed from your basket.")
        return redirect("basket")  
    elif action == "favourite":
        item = get_object_or_404(models.Favourite, pk=item_id, user=request.user)
        item.delete()
        messages.success(request, "Item removed from your favourites.")
        return redirect("favourite")  
    else:
        messages.error(request, "Invalid action.")
        return redirect("home")

def search(request):
    query = request.GET.get('q')
    proudcts = models.Product.objects.filter(title__iregex=query)
    context = {
        'products':proudcts,
        'total_products': proudcts.count(),
        'query': query
    }
    return render(request, 'blog_app/search.html', context)

def increase_quantity(request, item_id):
    item = get_object_or_404(models.Basket, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('basket')

def decrease_quantity(request, item_id):
    item = get_object_or_404(models.Basket, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('basket')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            send_mail(
            subject=f"New Contact Message: {subject}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_RECEIVER_EMAIL], 
            fail_silently=False,
            )

            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  
    else:
        form = ContactForm()
    
    return render(request, 'blog_app/contacts.html', {'form': form})

@login_required(login_url='login')
def place_order(request):
    basket_items = models.Basket.objects.filter(user=request.user)

    if not basket_items.exists():
        messages.error(request, "Your basket is empty.")
        return redirect('basket')  

    total = 0
    cart_items = []

    for item in basket_items:
        subtotal = item.product.price * item.quantity
        total += subtotal
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        with transaction.atomic():
            order = models.Order.objects.create(user=request.user, total_price=total)

            for item in cart_items:
                models.OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )

            basket_items.delete()
            return redirect('profile')
        
    return render(request, 'confirm_order.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def cancel_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(models.Order, id=order_id, user=request.user)
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            messages.success(request, 'Your order has been cancelled.')
        else:
            messages.error(request, 'This order cannot be cancelled.')
    return redirect('profile')

def user_logout(request):
    logout(request)
    return redirect('home')
