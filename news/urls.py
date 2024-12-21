from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, NewsFilter, PostCreate, PostUpdate, PostDelete, SubscribeToCategory

urlpatterns = [
   path('', PostList.as_view(), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', NewsFilter.as_view(), name='news_filter'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('article/create/', PostCreate.as_view(), name='article_create'),
   path('news/<int:pk>/edit', PostUpdate.as_view(), name='news_update'),
   path('article/<int:pk>/edit', PostUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('article/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
   path('category/<int:category_id>/subscribe/', SubscribeToCategory.as_view(), name='subscribe_to_category')
]