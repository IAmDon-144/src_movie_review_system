from django.urls import path, include
from .views import home,getMovie,about,help,contact,reviewPost,deleteReview,replyPost,seeReplies,addLove,showRatedlist


urlpatterns = [


    path('', home, name='home'),
    path('about/', about, name='about'),
    path('help/', help, name='help'),
    path('contact/', contact, name='contact'),
    path('<pk>/<str:title>/<str:code>/preview', getMovie, name='preview-movie'),
    path('<pk>/comment/',reviewPost , name='comment-post'),
    path('<pk>/reply/',replyPost , name='reply-comment'),
    path('<pk>/replies/',seeReplies, name='see-replies'),
    path('<pk>/<ck>/dc/', deleteReview, name='delete-review'),
    path('add-love/', addLove, name='add-love'),
    path('ratelist/', showRatedlist, name='rate-list'),
    path('tranding/', showRatedlist, name='tranding-list'),







]

from django.urls import path, include
from .views import home,getMovie,about,help,contact,reviewPost,deleteReview,replyPost,seeReplies,addLove,showRatedlist,showTranding,catagoryFilter


urlpatterns = [


    path('', home, name='home'),
    path('about/', about, name='about'),
    path('help/', help, name='help'),
    path('contact/', contact, name='contact'),
    path('<pk>/<str:title>/<str:code>/preview', getMovie, name='preview-movie'),
    path('<pk>/<str:title>/category', catagoryFilter, name='category-filter'),
    path('<pk>/comment/',reviewPost , name='comment-post'),
    path('<pk>/reply/',replyPost , name='reply-comment'),
    path('<pk>/replies/',seeReplies, name='see-replies'),
    path('<pk>/<ck>/dc/', deleteReview, name='delete-review'),
    path('add-love/', addLove, name='add-love'),
    path('ratelist/', showRatedlist, name='rate-list'),
    path('tranding/', showTranding, name='tranding-list'),







]

