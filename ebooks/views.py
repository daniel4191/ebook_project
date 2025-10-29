from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Ebook, Purchase, Review
from .forms import ReviewForm

def ebook_list(request):
    ebook_list = Ebook.objects.all()
    paginator = Paginator(ebook_list, 9)
    page_number = request.GET.get('page')
    ebooks = paginator.get_page(page_number)
    return render(request, 'ebooks/list.html', {'ebooks': ebooks})

def ebook_detail(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    reviews = ebook.reviews.all()
    
    # 구매 여부 확인
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = Purchase.objects.filter(user=request.user, ebook=ebook, is_completed=True).exists()
    
    return render(request, 'ebooks/detail.html', {
        'ebook': ebook,
        'reviews': reviews,
        'is_purchased': is_purchased
    })

@login_required
def ebook_purchase(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    payment_method = request.GET.get('method', 'direct')
    
    # 이미 구매한 경우
    existing_purchase = Purchase.objects.filter(user=request.user, ebook=ebook, is_completed=True).exists()
    if existing_purchase:
        messages.info(request, '이미 구매한 전자책입니다.')
        return redirect('ebooks:detail', pk=ebook.pk)
    
    if request.method == 'POST':
        purchase = Purchase.objects.create(
            user=request.user,
            ebook=ebook,
            payment_method=payment_method,
            purchase_price=ebook.price,
            is_completed=True
        )
        messages.success(request, '구매가 완료되었습니다.')
        return redirect('ebooks:my_ebooks')
    
    return render(request, 'ebooks/purchase.html', {
        'ebook': ebook,
        'payment_method': payment_method
    })

@login_required
def ebook_review_create(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # 구매 여부 확인
    purchase = Purchase.objects.filter(user=request.user, ebook=ebook, is_completed=True).first()
    if not purchase:
        messages.error(request, '해당 도서를 구매 후에 리뷰를 남길 수 있습니다.')
        return redirect('ebooks:detail', pk=ebook.pk)
    
    # 이미 리뷰를 작성한 경우
    existing_review = Review.objects.filter(ebook=ebook, author=request.user).exists()
    if existing_review:
        messages.info(request, '이미 리뷰를 작성하셨습니다.')
        return redirect('ebooks:detail', pk=ebook.pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ebook = ebook
            review.author = request.user
            review.purchase = purchase
            review.save()
            ebook.update_rating()
            messages.success(request, '리뷰가 작성되었습니다.')
            return redirect('ebooks:detail', pk=ebook.pk)
    else:
        form = ReviewForm()
    
    return render(request, 'ebooks/review_form.html', {'form': form, 'ebook': ebook})

@login_required
def my_ebooks(request):
    purchases = Purchase.objects.filter(user=request.user, is_completed=True).select_related('ebook')
    paginator = Paginator(purchases, 9)
    page_number = request.GET.get('page')
    my_ebooks = paginator.get_page(page_number)
    return render(request, 'ebooks/my_ebooks.html', {'my_ebooks': my_ebooks})

@login_required
def ebook_viewer(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # 구매 여부 확인
    is_purchased = Purchase.objects.filter(user=request.user, ebook=ebook, is_completed=True).exists()
    if not is_purchased:
        messages.error(request, '구매한 전자책만 열람할 수 있습니다.')
        return redirect('ebooks:list')
    
    return render(request, 'ebooks/viewer.html', {'ebook': ebook})
