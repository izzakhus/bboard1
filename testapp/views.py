from django.contrib.auth.models import User
from django.core.mail import (EmailMessage, get_connection,
                              EmailMultiAlternatives, send_mail,
                              send_mass_mail, mail_managers)
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Student, Course
from datetime import date


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
    ##### Низкоуровневые #####
    # em = EmailMessage(subject='Test', body='Test',
    #                   to=['user@supersite.kz'])
    # em.send()
    #
    # em = EmailMessage(subject='Ваш новый пароль',
    #                   body='Ваш новый пароль находится во вложении',
    #                   attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@supersite.kz'])
    # em.send()

    # em = EmailMessage(subject='Запрошенный вами файл',
    #                   body='Получите запрошенный вами файл',
    #                   to=['user@supersite.kz'])
    # em.attach_file(r'C:\work\file.txt')
    # em.send()

    ### на основе шаблонов ###
    # context = {'user': 'Вася Пупкин', '用户': 'Yònghù'}
    # s = render_to_string('email/letter.txt', context)
    # em = EmailMessage(subject='Оповещение', body=s,
    #                   to=['vpupkin@othersite.kz'])
    # em.send()

    ### соединения, массовая рассылка ###
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

    ### составное письмо ###
    # em = EmailMultiAlternatives(subject='Test', body='Test',
    #                             to=['user@supersite.kz'])
    # em.attach_alternative('<h1>Test</h1>', 'text/html')
    # em.send()


    ##### Высокоуровневые #####
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

    # user = User.objects.get(username='admin')
    # user.email_user('Подъём!', 'Admin, не спи!', fail_silently=True)

    # mail_managers('Подъём!', 'Редакторы, не спите!',
    #               html_message='<strong>Редакторы, не спите!</strong>')

    return render(request, 'testapp/test_email.html')

def hide_comment(request):
    if request.user.has_perm('testapp.hide_comments'):
        # пользователь может скрывать комменты
        pass


def populate_data(request):
    Student.objects.all().delete()
    Course.objects.all().delete()

    s1 = Student.objects.create(first_name="Иван", last_name="Петров", email="ivan@example.com", enrollment_date=date(2023, 9, 1))
    s2 = Student.objects.create(first_name="Мария", last_name="Иванова", email="maria@example.com", enrollment_date=date(2023, 10, 1))
    s3 = Student.objects.create(first_name="Алексей", last_name="Сидоров", email="alex@example.com", enrollment_date=date(2023, 9, 15))

    c1 = Course.objects.create(title="Python для начинающих", description="Основы программирования", start_date=date(2024, 1, 10))
    c2 = Course.objects.create(title="Веб-разработка", description="HTML, CSS, Django", start_date=date(2024, 2, 1))

    c1.students.add(s1, s2)
    c2.students.add(s2, s3)

    return render(request, 'success.html', {'message': 'Данные успешно добавлены'})


def course_students(request):
    courses = Course.objects.select_related().values('title', 'start_date', 'students__first_name', 'students__last_name')

    students = Student.objects.prefetch_related('courses').values('first_name', 'last_name', 'courses__title')

    context = {
        'courses': courses,
        'students': students,
    }
    return render(request, 'course_students.html', context)
