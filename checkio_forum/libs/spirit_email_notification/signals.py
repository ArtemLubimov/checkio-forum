from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from spirit.comment.models import Comment
from spirit.comment.bookmark.models import CommentBookmark
from spirit.topic.notification.models import TopicNotification
from huey.djhuey import task


@task()
@receiver(post_save, sender=Comment)
@receiver(post_save, sender=CommentBookmark)
def send_email_notification(sender, instance, raw, **kwargs):
    if isinstance(instance, Comment):
        quote_url = reverse(
            'spirit:comment:publish',
            kwargs={'topic_id': instance.topic.id, 'pk': instance.id})
        body_context = {
            'comment': instance,
            'quote_url': quote_url,
            'domain': settings.DOMAIN
        }
        body = render_to_string('spirit_email_notification/new_comment.html', body_context)
        comment_all = Comment.objects.filter(topic=instance.topic).exclude(user=instance.user)
        topic_notification_all = TopicNotification.objects.filter(topic=instance.topic).exclude(is_active=True)
        email_not_send = {topic.user.email for topic in topic_notification_all}
        email_to_send = {comment.user.email for comment in comment_all}
        email_to_send.difference_update(email_not_send)
        for email in email_to_send:
            send_mail(
                'EoC Comment. {}'.format(instance.topic.title),
                body,
                settings.DEFAULT_FROM_EMAIL,
                [email])
    else:
        comment_all = Comment.objects.filter(topic=instance.topic)
        for comment in comment_all:
            quote_url = reverse(
                'spirit:comment:publish',
                kwargs={'topic_id': instance.topic.id, 'pk': comment.id})
            body_context = {
                'comment': comment,
                'quote_url': quote_url,
                'domain': settings.DOMAIN
            }
        body = render_to_string('spirit_email_notification/mention.html', body_context)
        topic_notification_all = TopicNotification.objects.filter(topic=instance.topic, action=1).exclude(user=instance.user)
        email_to_send = {topic.user.email for topic in topic_notification_all}
        comment_all = Comment.objects.filter(topic=instance.topic).exclude(user=instance.user)
        email_not_send = {comment.user.email for comment in comment_all}
        email_to_send.difference_update(email_not_send)
        for email in email_to_send:
            send_mail('EoC Mention. {}'.format(instance.topic.title),
                      body,
                      settings.DEFAULT_FROM_EMAIL,
                      [email])




def send_report_email(sender, instance, raw, **kwargs):
    if raw:
        return
    topic = instance.topic

    if topic.category.title not in settings.MONITORING_QA_CATEGORIES:
        return

    subject = u'EoC QA: {}'.format(topic.title),
    body = u'FROM: {user}\n{text}\nhttps://{current_domain}{link}'.format(
        user=instance.user.username,
        text=instance.comment,
        current_domain=settings.DOMAIN,
        link=instance.get_absolute_url()
    )
    EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.MONITORING_QA_RECIPIENTS
    ).send()

post_save.connect(send_report_email, sender=Comment)


def send_report_email(sender, instance, raw, **kwargs):
    if raw:
        return
    user = instance.user

    if user.username not in settings.MONITORING_PR_USERS:
        return

    subject = u"Proof-Reading comment {}".format(instance.pk)
    body = u"{text}\n\nhttps://{current_domain}{link}".format(
        text=instance.comment, link=instance.get_absolute_url(), current_domain=settings.DOMAIN)

    EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.MONITORING_PR_READER],
        headers={'Reply-To': user.email}
    ).send()

post_save.connect(send_report_email, sender=Comment)
