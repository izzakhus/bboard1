from django.contrib.auth.models import User
from django.core.mail import (EmailMessage, get_connection,
                              EmailMultiAlternatives, send_mail,
                              send_mass_mail, mail_managers)
from django.template.loader import render_to_string
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from testapp.models import Item, Order


class ShopView(View):
    template_name = 'testapp/item_list.html'

    def get(self, request):
        items = Item.objects.all()
        orders = Order.objects.recent()
        context = {
            'items': items,
            'orders': orders,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')

        if action == 'create_order':
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))
            item = get_object_or_404(Item, id=item_id)
            try:
                order = Order.objects.create_order(item, quantity)  # Используем Manager
                messages.success(request, f"Заказ на {item.name} успешно создан!")
            except ValidationError as e:
                messages.error(request, str(e))

        elif action == 'cancel_order':
            order_id = request.POST.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            try:
                result = order.cancel_order()
                messages.success(request, result)
            except ValidationError as e:
                messages.error(request, str(e))

        return redirect('testapp:shop_view')


def test_cookie(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print('КУКИ РАБОТАЮТ!')
        else:
            print('КУКИ НЕ РАБОТАЮТ!')
    request.session.set_test_cookie()
    print('TEST COOKIE', request.session.test_cookie_worked())
    return render(request, 'testapp/test_cookie.html')


def test_mail(request):
    # #### Низкоуровневые #####
    # em = EmailMessage(subject='Test', body='Test',
    #                   to=['user@supersite.kz'])
    # em.send()
    #
    # em = EmailMessage(subject='Ваш новый пароль',
    #                   body='Ваш новый пароль находится во вложении',
    #                   attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@supersite.kz'])
    # em.send()
    #
    # em = EmailMessage(subject='Запрошенный вами файл',
    #                   body='Получите запрошенный вами файл',
    #                   to=['user@supersite.kz'])
    # em.attach_file(r'C:\work\file.txt')
    # em.send()
    #
    # ## на основе шаблонов ###
    # context = {'user': 'Вася Пупкин', '用户': 'Yònghù'}
    # s = render_to_string('email/letter.txt', context)
    # em = EmailMessage(subject='Оповещение', body=s,
    #                   to=['vpupkin@othersite.kz'])
    # em.send()
    #
    # ## соединения, массовая рассылка ###
    # con = get_connection()
    # con.open()
    # email1 = EmailMessage(subject='Запрошенный вами файл',
    #                       body='Получите запрошенный вами файл',
    #                       to=['user@supersite.kz'], connection=con)
    # email1.send()
    # email2 = EmailMessage(subject='Запрошенный вами файл',
    #                       body='Получите запрошенный вами файл',
    #                       to=['user@supersite.kz'], connection=con)
    # email2.send()
    # email3 = EmailMessage(subject='Запрошенный вами файл',
    #                       body='Получите запрошенный вами файл',
    #                       to=['user@supersite.kz'], connection=con)
    # email3.send()
    # con.close()
    #
    # con = get_connection()
    # con.open()
    # email1 = EmailMessage(subject='Запрошенный вами файл',
    #                       body='Получите запрошенный вами файл',
    #                       to=['user@supersite.kz'])
    # email2 = EmailMessage(subject='Запрошенный вами файл',
    #                       body='Получите запрошенный вами файл',
    #                       to=['user@supersite.kz'])
    # email3 = EmailMessage(subject='Запрошенный вами файл',
    #                       body='Получите запрошенный вами файл',
    #                       to=['user@supersite.kz'])
    # con.send_messages([email1, email2, email3])
    # con.close()
    #
    # ## составное письмо ###
    # em = EmailMultiAlternatives(subject='Test', body='Test',
    #                             to=['user@supersite.kz'])
    # em.attach_alternative('<h1>Test</h1>', 'text/html')
    # em.send()
    #
    #
    # #### Высокоуровневые #####
    # send_mail('Test email', 'Test!!!', 'webmaster@supersite.kz',
    #           ['user@othersite.kz'], html_message='<h1>Test!!!</h1>')
    #
    # msg1 = ('Подписка', 'Подтвердите пожалуйста подписку',
    #         'subscribe@supersite.kz',
    #         ['user@othersite.kz', 'megauser@megasite.kz'])
    # msg2 = ('Подписка', 'Ваша подписка подтверждена',
    #         'subscribe@supersite.kz',
    #         ['user@othersite.kz', 'otheruser@megasite.kz'])
    # send_mass_mail((msg1, msg2))
    #
    # user = User.objects.get(username='admin')
    # user.email_user('Подъём!', 'Admin, не спи!', fail_silently=True)
    #
    # mail_managers('Подъём!', 'Редакторы, не спите!',
    #               html_message='<strong>Редакторы, не спите!</strong>')
    return render(request, 'testapp/test_email.html')


def hide_comment(request):
    if request.user.has_perm('testapp.hide_comments'):
        # пользователь может скрывать комменты
        pass
