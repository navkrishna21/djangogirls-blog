from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from .forms import PostForm
from .forms import CommentForm
from django.utils import timezone
from django.shortcuts import redirect

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	
	comments = Comment.objects.filter(post = post)
	if request.method == "POST":
		
		form = CommentForm(request.POST)
		
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=pk)

	form = CommentForm()
	return render(request, 'blog/post_detail.html', {'post': post , 'form': form , 'comments' : comments })

def post_new(request):
	if request.method == "POST":
		    form = PostForm(request.POST)
		    if form.is_valid():
		        post = form.save(commit=False)
		        post.author = request.user
		        post.published_date = timezone.now()
		        post.save()
		        return redirect('post_detail', pk=post.pk)
	else:
	    form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request,pk):
	Post.objects.filter(pk=pk).delete()
	return redirect('post_list')

def comment_add(request,pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		
		form = CommentForm(request.POST)
		
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=pk)
	else:
		return HttpResponse('<h1>Page was found</h1>')


def comment_delete(request,pk,cid):
	Comment.objects.filter(pk=cid).delete()
	return redirect('post_detail', pk=pk)

def comment_edit(request,pk,cid):
	comment = get_object_or_404(Comment, pk=cid)
	
	post = get_object_or_404(Post, pk=pk)
	
	if comment.post != post:
		return HttpResponse('<h1>Page was found</h1>')

	if request.method == "POST":
		
		form = CommentForm(request.POST, instance=comment)
		
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=pk)

	comments = Comment.objects.filter(post = post)		

	form = CommentForm(instance=comment)
	
	return render(request, 'blog/post_detail.html', {'post': post , 'comment_edit_form': form , 'comments' : comments , 'edit_comment' : comment } )

	#Comment.objects.filter(pk=cid).delete()
	#return redirect('post_detail', pk=pk)