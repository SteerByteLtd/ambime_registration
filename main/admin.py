from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from import_export.admin import ImportExportModelAdmin
from import_export import resources
import timestring
from .models import RegistrationProfile, User, Call_History
from .users import UsernameField


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_name', 'email', 'landline1', 'landline2', 'is_active']
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ['is_superuser']

    def get_name(self, obj):
        return ("{} {}").format(obj.first_name, obj.last_name)

    get_name.short_description = "Full Name"


@admin.register(RegistrationProfile)
class RegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = [field.name for field in RegistrationProfile._meta.fields if field.name != "id"]
    raw_id_fields = ['user']
    search_fields = ('user__{0}'.format(UsernameField()),
                     'user__first_name', 'user__last_name')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not already
        activated.

        """

        site = get_current_site(request)
        for profile in queryset:
            RegistrationProfile.objects.activate_user(profile.activation_key, site)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.

        """

        site = get_current_site(request)
        for profile in queryset:
            user = profile.user
            RegistrationProfile.objects.resend_activation_mail(user.email, site, request)

    resend_activation_email.short_description = _("Re-send activation emails")

class CallHistoryResource(resources.ModelResource):
    # /call_time = Field(column_name='date')
    class Meta:
        model = Call_History
        exclude = ['user', 'date']

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        if dataset.headers:
            dataset.headers = [str(header).lower().strip() for header in dataset.headers]

            # if id column not in headers in your file
        if 'id' not in dataset.headers:
            print("---------befor impor-------")
            dataset.insert_col(0, col=["", ] * dataset.height, header="id")

    def save_instance(self, instance, using_transactions=True, dry_run=True):
        self.before_save_instance(instance, using_transactions, dry_run)

        if not dry_run:
            user_id = User.objects.filter(
                Q(landline1=instance.phone_number) | Q(landline2=instance.phone_number)).first().id
            instance.user_id = user_id
            instance.date = timestring.Date(instance.call_time).date
            print(instance.user_id)
            instance.save()
        else:
            pass

        self.after_save_instance(instance, using_transactions, dry_run)


@admin.register(Call_History)
class CallHistory_Admin(ImportExportModelAdmin):
    list_display = ['get_name', 'phone_number', 'town',  'duration']
    list_filter = ['date']
    resource_class = CallHistoryResource

    def get_name(self, obj):
        return ("{} {}").format(obj.user.first_name, obj.user.last_name)

    get_name.short_description = "Name"

