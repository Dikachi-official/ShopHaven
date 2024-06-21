from django.urls import path
from . import views


app_name = 'conversation'

urlpatterns = [
    #FULL INBOX LIST URL
    path('', views.inbox, name="inbox"),
    
    # DELETE INDIVDUAL MSG FROM INBOX
    path('delete/<int:id>', views.delete_conversation, name="delete"),
    
    #MSG DETAIL URL
    path('<int:id>/', views.inbox_detail, name='inbox-detail'),
    
    # NEW MESSAGE URL
    path('new/<int:id>/', views.new_conversation, name='new'),
]
