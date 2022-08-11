from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from .models import BlogPost
from .forms import CreateBlogPostForm, UpdateBlogPostForm,NewCommentForm
from account.models import Account
from django.http import HttpResponseRedirect
from django.urls import reverse


def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email =request.user.email).first()
		obj.author = author
		form = CreateBlogPostForm()
		obj.save()

	context['form'] = form

	return render(request, 'blog/create_blog.html', context)




def detail_blog_view(request, slug):
	
	context = {}
	blog_post = get_object_or_404(BlogPost, slug=slug)
	liked=False
	if request.method == 'POST':
		
		if blog_post.likes.filter(username=request.user.username).exists():
			blog_post.likes.remove(request.user)
		else:
			blog_post.likes.add(request.user)
		
		form = NewCommentForm(request.POST or None)
		if form.is_valid():
			obj = form.save(commit=False)
			author = Account.objects.filter(email =request.user.email).first()
			obj.author = author
			obj.post=blog_post
			form = NewCommentForm()
			obj.save()
		
		return HttpResponseRedirect(request.path)
		
	if blog_post.likes.filter(username=request.user.username).exists():
		liked = True

	context={'blog_post': blog_post,'number_of_likes':blog_post.number_of_likes(), 'post_is_liked':liked}

	return render(request, 'blog/detail_blog.html', context)
	
	




def edit_blog_view(request, slug):
	
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse("You are not the author of this post.")

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj
	
	form = UpdateBlogPostForm(
			initial={
					"title": blog_post.title, 
					"body": blog_post.body,
					"image": blog_post.image,
				}
			)
	context['form'] = form

	return render(request, 'blog/edit_blog.html', context)




def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = BlogPost.objects.filter(
			Q(title__contains=q)|
			Q(body__icontains=q)
			).distinct()
		for post in posts:
			queryset.append(post)

	return list(set(queryset)) 


