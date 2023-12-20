from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewsDetail,SearchList, NewsCreate,ArticleCreate, NewsUpdate,ArticleList, ArticleNewsList, ArticleUpdate, ArticleDelete, NewsDelete,ArticleDetail

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('',ArticleNewsList.as_view(), name = 'global'),
   path('news/', NewsList.as_view(), name='news_list'),
   path('article/', ArticleList.as_view(), name='article_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('article/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
   path('search/',SearchList.as_view(), name = 'post_search'),
   path('news/create/', NewsCreate.as_view(), name = 'news_create'),
   path('article/create/', ArticleCreate.as_view(), name = 'article_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('news/<int:pk>/delete',NewsDelete.as_view(), name = 'news_delete'),
   path('article/<int:pk>/delete',ArticleDelete.as_view(), name = 'article_delete'),

]