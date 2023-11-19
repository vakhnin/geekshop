from django.urls import path

from baskets.views import basket_add, basket_edit, basket_remove, BasketView

app_name = 'baskets'

urlpatterns = [
    path('', BasketView.as_view(), name='main'),
    path('add/<int:id>/', basket_add, name='basket_add'),
    # path('remove/<int:pk>/', basket_remove, name='basket_remove'),
    path('edit/<int:id_basket>/<slug:action>/', basket_edit, name='basket_edit'),
]
