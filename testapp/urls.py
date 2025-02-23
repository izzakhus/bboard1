from django.urls import path

from testapp.views import test_cookie, test_mail, ShopView

app_name = 'testapp'

urlpatterns = [
    path('cookie/', test_cookie, name='test_cookie'),
    path('email/', test_mail, name='test_mail'),
    path('shop/', ShopView.as_view(), name='shop_view'),
]
