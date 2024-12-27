from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .models import Post, Comment
from tour.models import Category
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.shortcuts import HttpResponse


class PostListView(ListView):
    model = Post
    template_name = "post/blog-archive.html"
    paginate_by = 3
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recent posts
        context['recent_posts'] = Post.objects.all().order_by("-created_at")[:3]
        # All categories
        context['categories'] = Category.objects.all()
        return context

class DetailPostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        recent_posts = Post.objects.all().order_by("-created_at").exclude(id=post.pk)[:3]
        comments = Comment.objects.filter(post=post.pk)
        categories = Category.objects.all()  # Fetch all categories
        form = CommentForm()
        context = {
            "post": post,
            "recent_posts": recent_posts,
            "comments": comments,
            "categories": categories,  # Add categories to context
            "form": form,
        }
        return render(request, "post/blog-single.html", context)

    def post(self, request, pk):
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                post = get_object_or_404(Post, pk=pk)
                f = form.save(commit=False)
                f.post = post
                f.user = request.user
                f.save()
                return redirect("detail_post", pk=post.pk)
            categories = Category.objects.all()  # Fetch all categories
            context = {
                "form": form,
                "categories": categories,
            }
            return render(request, "post/blog-single.html", context)
        return HttpResponse('Error!')
