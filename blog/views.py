from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse  
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the user is the author of the post
    if post.author != request.user:
        return redirect('post_list')  # or return a forbidden response

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    # Include the user profile information if needed
    context = {
        'form': form,
        'user': request.user,
        'post': post
    }
    
    return render(request, 'blog/post_form.html', context)

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, id= request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_like', args=[str(pk)]))
