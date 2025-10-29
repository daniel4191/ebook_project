from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import InquiryForm
from .models import Inquiry

@login_required
def inquiry_create(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            
            # 이메일 전송
            try:
                send_mail(
                    subject=f'[Ebook 플랫폼] 새로운 문의: {inquiry.title}',
                    message=f'문의자: {inquiry.user.email}\n\n{inquiry.content}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f'이메일 전송 실패: {e}')
            
            messages.success(request, '소중한 의견 감사드립니다. 빠른 시일 내에 답변드리겠습니다.')
            return redirect('inquiries:create')
    else:
        form = InquiryForm()
    
    return render(request, 'inquiries/create.html', {'form': form})
