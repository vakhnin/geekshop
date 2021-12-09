from django.urls import path

from baskets.views import basket_add, basket_edit, BasketDeleteView

app_name = 'baskets'
urlpatterns = [

    path('add/<int:id>/', basket_add, name='basket_add'),
    path('remove/<int:pk>/', BasketDeleteView.as_view(), name='basket_remove'),
    path('edit/<int:id_basket>/<int:quantity>/', basket_edit, name='basket_edit'),

]
