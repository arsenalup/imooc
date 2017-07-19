from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from mxonline .settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    charts = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    length = len(charts) - 1
    random = Random()
    for i in range(randomlength):
        str += charts[random.randint(0, length)]
    return str


def send_register_email(email, send_type):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code =random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '网站注册激活连接'
        email_body = '请点击连接激活：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '网站密码找回连接'
        email_body = '请点击连接找回连接：http://127.0.0.1:8000/reset/{0}'.format(code)

    elif send_type == 'update_email':
        email_title = '邮箱修改连接'
        email_body = '邮箱验证码为：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


