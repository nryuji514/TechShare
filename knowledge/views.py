from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Knowledge, Tag, Profile
from .forms import KnowledgeForm, CommentForm, ProfileForm
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


#ホーム画面表示
@login_required
def home(request):
    posts = Knowledge.objects.all().order_by('-created_at')[:5]
    
    return render(request, 'home.html',{'posts':posts})

#一覧表示
@login_required
def knowledge_list(request):
    posts = Knowledge.objects.all().order_by('-created_at')
    return render(request,'knowledge_list.html',{'posts':posts})

#詳細、コメント表示
@login_required
def knowledge_detail(request,pk):
    post = get_object_or_404(Knowledge,pk=pk)
    comments=post.comments.all()
    form=CommentForm()
    
    return render(request,'knowledge_detail.html',{
        'post':post,
        'comments':comments,
        'form':form
    })

#投稿作成
@login_required
def knowledge_create(request):
    if request.method == 'POST':
        form=KnowledgeForm(request.POST)

        if form.is_valid():
            post =form.save(commit=False)

            post.author=request.user

            post.save()
            
            tag_text=request.POST.get("tag_input", "")
            for t in tag_text.split(","):
                t=t.strip()
                if not t:
                    continue

                tag, _ = Tag.objects.get_or_create(name=t)
                post.tags.add(tag)

            return redirect('knowledge_list')
    else:
        form=KnowledgeForm()

    return render(request, 'knowledge_form.html',{'form':form})

#投稿編集
@login_required
def knowledge_edit(request, pk):
    post = get_object_or_404(Knowledge, pk=pk, author=request.user)

    if request.method == 'POST':
        form = KnowledgeForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save()

            post.tags.clear()
            tag_text = request.POST.get("tag_input", "")
            for t in tag_text.split(","):
                t = t.strip()
                if not t:
                    continue

                tag, _ = Tag.objects.get_or_create(name=t)
                post.tags.add(tag)

            return redirect('knowledge_detail', pk=post.pk)
    else:
        form = KnowledgeForm(instance=post)

    tag_value = ", ".join(t.name for t in post.tags.all())

    return render(request, 'knowledge_form.html', {
        'form': form,
        'is_edit': True,
        'tag_value': tag_value,
        'post': post,
    })

#コメント追加
@login_required
def add_comment(request,pk):
    post=get_object_or_404(Knowledge,pk=pk)

    if request.method == 'POST':
        form=CommentForm(request.POST)

        if form.is_valid():
            comment=form.save(commit=False)
            comment.knowledge=post
            comment.user=request.user
            comment.save()

    return redirect('knowledge_detail',pk=pk)

#マイページ表示
@login_required
def mypage(request):
    Profile.objects.get_or_create(user=request.user)
    posts = Knowledge.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'mypage.html', {'posts':posts})

#プロフィール編集
@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('mypage')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_form.html', {'form': form})

#プロフィール画像アップロード（マイページから）
@login_required
def avatar_upload(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and request.FILES.get('avatar'):
        profile.avatar = request.FILES['avatar']
        profile.save()

    return redirect('mypage')

#投稿削除
@login_required
def delete_post(request,pk):
    post=get_object_or_404(Knowledge,pk=pk,author=request.user)

    if request.method == 'POST':
        post.delete()

    return redirect('mypage')

@login_required
def tag_posts(request, tag_name):

    tag = get_object_or_404(Tag, name=tag_name)

    posts = Knowledge.objects.filter(tags__id=tag.id)

    return render(
        request, 
        'knowledge_list.html', 
        {
            'posts':posts, 
            'selected_tag':tag
        }
    )

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})