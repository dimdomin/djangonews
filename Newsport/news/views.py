# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscription
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


class ArticleNewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context
class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/news_all.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context

    def get_queryset(self):
        return Post.objects.filter(categoryType='Nw').order_by('-dateCreation')

class ArticleList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/article_all.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context
    def get_queryset(self):
        return Post.objects.filter(categoryType='Ar').order_by('-dateCreation')

class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    ordering = '-dateCreation'
    # Используем другой шаблон — article.html
    template_name = 'flatpages/article.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'
    def get_queryset(self):
        return Post.objects.filter(categoryType='Nw').order_by('-dateCreation')

class ArticleDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — article.html
    template_name = 'flatpages/article.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'
    def get_queryset(self):
        return Post.objects.filter(categoryType='Ar').order_by('-dateCreation')

class SearchList(ListView):
   model = Post
   ordering = 'title1'
   template_name = 'flatpages/search.html'
   context_object_name = 'news'
   paginate_by = 10  # вот так мы можем указать количество записей на странице

   # Переопределяем функцию получения списка товаров
   def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.news_create',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'Nw'
        return super().form_valid(form)

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.article_create',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_create.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'Ar'
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.news_update',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_create.html'
    success_url = reverse_lazy('news_detail')

class ArticleUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('simpleapp.article_update',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_create.html'
    success_url = reverse_lazy('article_detail')

class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.news_delete',)
    model = Post
    template_name = 'flatpages/news_delete.html'
    success_url = reverse_lazy('global')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.article_delete',)
    model = Post
    template_name = 'flatpages/news_delete.html'
    success_url = reverse_lazy('global')


class CategoryListView(NewsList):
    model = Post
    template_name = 'category_list_sub.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category,id =self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory = self.postCategory)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscriptions.html', {'category':category, 'message':message})


#@login_required
#@csrf_protect
#def subscriptions(request):
 #   if request.method == 'POST':
  #      category_id = request.POST.get('category_id')
   #     category = Category.objects.get(id=category_id)
    #    action = request.POST.get('action')

     #   if action == 'subscribe':
      #      Subscription.objects.create(subscriber=request.user, category=category)
       # elif action == 'unsubscribe':
        #    Subscription.objects.filter(
         #       subscriber=request.user,
          #      category=category,
           # ).delete()

#    categories_with_subscriptions = Category.objects.annotate(
 #       user_subscribed=Exists(
  #          Subscription.objects.filter(
   #             subscriber=request.user,
    #            category=OuterRef('pk'),
     #       )
      #  )
#    ).order_by('name')
 #   return render(
  #      request,
   #     'subscriptions.html',
    #    {'categories': categories_with_subscriptions},
    #)