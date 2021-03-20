import logging

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from oidc_provider.models import Client
from oidc_provider.signals import user_accept_consent

from .models import Faq
from .tasks import consent_accept_email

logger = logging.getLogger(__name__)


@receiver(user_accept_consent)
def user_accept_consent_send_email(sender, **kwargs):
    consent_accept_email.delay(client_id=kwargs['client'].id,
                               user_id=kwargs['user'].id,
                               scope=kwargs['scope'])


@receiver(post_save, sender=Client)
def client_create(sender, **kwargs):
    if kwargs['created']:
        client = kwargs['instance']
        user = client.owner
        user.add_obj_perm('view_client', client)
        user.add_obj_perm('change_client', client)


@receiver(post_delete, sender=Faq)
@receiver(post_save, sender=Faq)
def oidc_client_faq_update(sender, **kwargs):
    key = make_template_fragment_key('oidc_client_faq_page')
    cache.delete(key)
    logger.info(f'Delete oidc_client_faq_page cache.')
