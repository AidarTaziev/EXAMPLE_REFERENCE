from django.conf import settings
from django.core.mail import send_mail


def send_poly_order_to_email(send_data):
    email_subject = 'example.tyu :: Заявка на покупку полимера '

    email_body = " Марка: %s \n" \
                 " Количество тонн: %s \n" \
                 " Наименование компании - заказчика(грузополучатель): %s \n" \
                 " Период отгрузки c %s по %s \n" \
                 " Метод отгрузки: %s \n" \
                 " Условия доставки: %s \n" \
                 " Пункт назначения(адрес): %s \n" \
                 " Имя заказчика: %s \n" \
                 " Телефон заказчика: %s \n " \
                 " E-mail заказчика: %s \n" \
                 " Дополнительная информация менеджеру: %s" % \
                 (send_data['idgoods'], send_data['numbers'], send_data['consignee'], \
                  send_data['shipment_from'], send_data['shipment_to'],
                  send_data['idshipment_methods'], \
                  send_data['idshipment_conditions'], send_data['address'],
                  send_data['contact_name'], \
                  send_data['contact_phone'], send_data['contact_email'],
                  send_data['message'])

    # отправляем сообщение менеджерам на email
    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['tazievaidar1998@mail.ru'],
              fail_silently=False)
