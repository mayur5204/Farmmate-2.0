from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    """View for the main community page with paginated post listing"""
    category = request.GET.get('category', '')
    if category:
        posts = Post.objects.filter(category=category)
    else:
        posts = Post.objects.all()

    # Pagination with 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'community/post_list.html', context)


def post_detail(request, pk):
    """View for showing a single post with its comments"""
    post = get_object_or_404(Post, pk=pk)
    # Get top-level comments (no parent)
    comments = post.comments.filter(parent=None)
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            
            # Check if this is a reply to another comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                new_comment.parent = parent_comment
                
            new_comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'community/post_detail.html', context)


@login_required
def create_post(request):
    """View for creating new posts"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'community/post_form.html', {
        'form': form,
        'title': 'Create Post',
        'button_text': 'Post'
    })


@login_required
def edit_post(request, pk):
    """View for editing existing posts"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the user is the author of the post
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "You cannot edit someone else's post.")
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'community/post_form.html', {
        'form': form,
        'post': post,
        'title': 'Edit Post',
        'button_text': 'Update'
    })


@login_required
def delete_post(request, pk):
    """View for deleting posts"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the user is the author of the post
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "You cannot delete someone else's post.")
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted successfully!')
        return redirect('post_list')
    
    return render(request, 'community/post_confirm_delete.html', {'post': post})


@login_required
def delete_comment(request, pk):
    """View for deleting comments"""
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    
    # Check if the user is the author of the comment
    if request.user != comment.author and not request.user.is_staff:
        messages.error(request, "You cannot delete someone else's comment.")
        return redirect('post_detail', pk=post_pk)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
    
    return redirect('post_detail', pk=post_pk)


@login_required
def like_post(request, pk):
    """AJAX view for liking/unliking posts"""
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
            
        return JsonResponse({
            'likes_count': post.get_like_count(),
            'liked': liked
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
