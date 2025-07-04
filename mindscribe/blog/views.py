from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Post, Profile, Comment
from .forms import PostForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm

def home(request):
    featured_posts = Post.objects.filter(featured=True)[:3]  # Или другой логика выбора
    context = {
        'featured_posts': featured_posts
    }
    return render(request, 'blog/home.html', context)

@login_required
def profile(request):
    return render(request, 'blog/profile/profile.html')

@login_required
def profile_edit(request):
    # Получаем или создаем профиль
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile  # Используем полученный профиль
        )
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)  # Используем полученный профиль

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile/profile_edit.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/posts/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    return redirect('post_detail', pk=post.pk)

@require_POST
@csrf_exempt  # Только для тестирования, в production используйте правильную CSRF защиту
def edit_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk, author=request.user)
        comment.text = request.POST.get('text', '')
        comment.save()
        return JsonResponse({
            'status': 'success',
            'text': comment.text,
            'updated_date': comment.updated_date.strftime("%d.%m.%Y %H:%M")
        })
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Комментарий не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author or request.user == comment.post.author:
        comment.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Недостаточно прав'})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/posts/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UserPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/profile/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-published_date')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm  # Используем нашу форму вместо явного указания полей
    template_name = 'blog/posts/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return post.is_author(self.request.user)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/posts/post_confirm_delete.html'
    success_url = reverse_lazy('user_posts')
    
    def test_func(self):
        post = self.get_object()
        return post.is_author(self.request.user)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/auth/register.html', {'form': form})

def about(request):
    return render(request, 'blog/info/about.html')

def contact(request):
    return render(request, 'blog/info/contact.html')