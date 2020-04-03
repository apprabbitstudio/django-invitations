import re

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .adapters import get_invitations_adapter
from .exceptions import AlreadyAccepted, AlreadyInvited, UserRegisteredEmail
from .utils import get_invitation_model

from .app_settings import app_settings


Invitation = get_invitation_model()


class CleanEmailMixin(object):

    def validate_invitation(self, email):
        if Invitation.objects.all_valid().filter(
                email__iexact=email, accepted_at__isnull=True):
            raise AlreadyInvited
        elif Invitation.objects.filter(
                email__iexact=email, accepted_at__isnull=False):
            raise AlreadyAccepted
        elif get_user_model().objects.filter(email__iexact=email):
            raise UserRegisteredEmail
        else:
            return True

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_invitations_adapter().clean_email(email)

        errors = {
            "already_invited": _("This e-mail address has already been"
                                 " invited."),
            "already_accepted": _("This e-mail address has already"
                                  " accepted an invite."),
            "email_in_use": _("An active user is using this e-mail address"),
        }
        try:
            self.validate_invitation(email)
        except(AlreadyInvited):
            raise forms.ValidationError(errors["already_invited"])
        except(AlreadyAccepted):
            raise forms.ValidationError(errors["already_accepted"])
        except(UserRegisteredEmail):
            raise forms.ValidationError(errors["email_in_use"])
        return email


class InviteForm(forms.Form, CleanEmailMixin):
    def __init__(self, *args, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        if app_settings.USE_FULLNAME_FIELD:
            self.fields['fullname'] = forms.CharField(required=True,
              widget=forms.TextInput(attrs={"placeholder": "Fullname"}))
        else:
            self.fields['first_name'] = forms.CharField(required=True,
              widget=forms.TextInput(attrs={"placeholder": "First name"}))
            self.fields['last_name'] = forms.CharField(required=True,
              widget=forms.TextInput(attrs={"placeholder": "Last name"}))

        # If the phone field is false don't enable the email field.
        if (app_settings.ENABLE_EMAIL_FIELD is True or
            app_settings.ENABLE_PHONE_FIELD is False):
            required = app_settings.EMAIL_FIELD_REQUIRED
            if app_settings.ENABLE_PHONE_FIELD is False:
                required = True
            self.fields['email'] = forms.EmailField(label="E-mail",
                required=required,
                widget=forms.TextInput(attrs={
                    "type": "email", "placeholder": "E-mail"}))

        if app_settings.ENABLE_PHONE_FIELD:
            self.fields['phone'] = forms.CharField(label="Phone",
              required=app_settings.PHONE_FIELD_REQUIRED or True,
              max_length=20,
              widget=forms.TextInput(attrs={
                "type": "tel", "placeholder": "Phone"}))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone:
            return phone
        phone = re.sub('[+()-]', '', str(phone)).replace(" ", "")
        # Is the phone number a number
        try:
            int(phone)
        except ValueError:
            raise forms.ValidationError('Invalid Phone Number')
        # Phone number must be at least 11 in length
        if len(phone) == 10:
            phone = "%s%s" % (app_settings.COUNTRY_CODE_DEFAULT, phone)
        if len(phone) < 11 and len(phone) <= 13:
            raise forms.ValidationError('Invalid Phone Number')
        return "+%s" % phone

    def cleann_fullname(self):
        fullname = self.cleaned_data['fullname']
        if not re.search('([a-zA-Z]{2,})([\s])([a-zA-Z]{1,})', '', fullname):
            raise forms.ValidationError('Invalid fullname')
        return fullname

    def save(self, *args, **kwargs):
        if app_settings.USE_FULLNAME_FIELD:
            first_name, last_name = self.cleaned_data['fullname'].split(' ', 1)
        else:
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']

        phone = ''
        if app_settings.ENABLE_PHONE_FIELD:
            phone = self.cleaned_data['phone']

        email = ''
        if app_settings.ENABLE_EMAIL_FIELD:
            email = self.cleaned_data['email']

        params = {}
        params['first_name'] = first_name
        params['last_name'] = last_name
        params['email'] = email
        params['phone'] = phone

        instance = Invitation.create(**params)
        return instance

class InvitationAdminAddForm(InviteForm):

    def save(self, *args, **kwargs):
        cleaned_data = super(InvitationAdminAddForm, self).clean()
        if app_settings.USE_FULLNAME_FIELD:
            first_name, last_name = self.cleaned_data['fullname'].split(' ', 1)
        else:
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']

        phone = ''
        if app_settings.ENABLE_PHONE_FIELD:
            phone = self.cleaned_data['phone']

        email = ''
        if app_settings.ENABLE_EMAIL_FIELD:
            email = self.cleaned_data['email']

        return Invitation.create(
            first_name=first_name, last_name=last_name,
            email=email, phone=phone
        )

        params = {}
        params['first_name'] = first_name
        params['last_name'] = last_name
        params['email'] = email
        params['phone'] = phone

        if cleaned_data.get("inviter"):
            params['inviter'] = cleaned_data.get("inviter")

        instance = Invitation.create(**params)
        super(InvitationAdminAddForm, self).save(*args, **kwargs)
        return instance

    class Meta:
        model = Invitation
        fields = ("inviter",)


class InvitationAdminChangeForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = '__all__'
