from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from guardian.mixins import GuardianUserMixin

from .validators import UsernameValidator, PKUEmailValidator


class Department(models.Model):
    department = models.CharField(
        _('department'),
        unique=True,
        max_length=100
    )

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return self.department


class User(AbstractUser, GuardianUserMixin):
    username_validator = UsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=10,
        unique=True,
        help_text=_('Required. It\'s your pku id. 10 characters. Digits only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    name = models.CharField(
        _('name'),
        max_length=40,
        blank=True
    )

    email = models.EmailField(
        _('pku email address'),
        validators=[PKUEmailValidator()],
        help_text=_('This is your pku email address, because some clients only require email address.')
    )

    nickname = models.CharField(
        _('nickname'),
        max_length=50,
        blank=True
    )

    website = models.URLField(
        _('website'),
        max_length=100,
        blank=True
    )

    gender = models.SmallIntegerField(
        _('gender'),
        choices=(
            (0, _('unknown')),
            (1, _('male')),
            (2, _('female'))
        ),
        default=0
    )

    birthdate = models.DateField(
        _('birthdate'),
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        blank=True
    )

    address = models.CharField(
        _('address'),
        max_length=50,
        blank=True
    )

    preferred_email = models.EmailField(
        _('preferred email address'),
        blank=True,
        help_text=_('This is your usual email address which we will use to get in touch with you.')
    )

    is_teacher = models.BooleanField(
        _('is teacher'),
        choices=((False, _('student')), (True, _('teacher'))),
        default=False,
        help_text=_(
            'Designates whether the user is a teacher.'
        )
    )

    in_school = models.BooleanField(
        _('is in school'),
        default=True,
        choices=(
            (False, _('Not in School')),
            (True, _('In School'))
        ),
        help_text=_('Designate whether the user is in school.')
    )

    department = models.ForeignKey(
        to=Department,
        on_delete=models.DO_NOTHING,
        verbose_name=_('department'),
        null=True, blank=True
    )

    introduce = models.TextField(
        _('introduce'),
        null=True, blank=True,
        help_text=_('Your personal introduction.')
    )

    is_admin = models.BooleanField(
        _('is admin'),
        default=False,
        choices=(
            (False, _('False')),
            (True, _('True'))
        ),
        help_text=_('Admin user can manage this site.')
    )

    last_iaaa_login = models.DateTimeField(_('last iaaa login'), blank=True, null=True)

    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        pass

    def get_pku_email(self):
        if self.is_teacher:
            return self.username + '@pku.edu.cn'
        elif int(self.username[0]) < 2:
            return self.username + '@pku.edu.cn'
        elif int(self.username[0:2]) >= 20:  # TODO: 每年更新毕业生邮箱
            return self.username + '@stu.pku.edu.cn'
        else:
            return self.username + '@alumni.pku.edu.cn'

    def get_preferred_email(self):
        if self.preferred_email:
            return self.preferred_email
        elif self.email:
            return self.email
        else:
            self.email = self.get_pku_email()
            self.save()
            return self.email

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return super().get_full_name()
