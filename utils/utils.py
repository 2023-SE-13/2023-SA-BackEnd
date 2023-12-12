from django.core.mail import send_mail


def send_email(email):
    # 生成验证码
    import random
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 6):
        rand_str += str1[random.randrange(0, len(str1))]
    # 发送邮件：
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    message = "您的验证码是" + rand_str + "，当前会话内有效，请尽快填写"
    email_box = [email]
    send_mail('重置密码验证', message, 'judgement9259@163.com', email_box, fail_silently=False)
    return rand_str