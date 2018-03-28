"""
Views which allow users to create and activate accounts.

"""

from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from .models import *
from _datetime import datetime
from main.forms import ResendActivationForm
from django.db.models import Q
from datetime import timedelta

REGISTRATION_FORM_PATH = getattr(settings, 'REGISTRATION_FORM',
                                 'main.forms.RegistrationForm')
REGISTRATION_FORM = import_string(REGISTRATION_FORM_PATH)
ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = getattr(
    settings, 'ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS', True)


class UserProfileView(View):
    template_name = 'profile.html'

    def last_day_of_month(self, date):
        next_month = date.replace(day=28) + datetime.timedelta(days=4)
        return next_month - datetime.timedelta(days=next_month.day)

    def get_credits(self, user, today, flag=True):

        # Calculate User's own credit
        previous_duration = 0
        today_duration = 0
        day_of_month = today.replace(day=1)

        # Total credits from first day of moth to yesterday
        past_call_history = Call_History.objects.filter(
            Q(user_id=user.id) & Q(date__lt=today) & Q(date__gte=day_of_month)).all()
        if past_call_history:
            for call in past_call_history:
                if "min" in call.duration:
                    duration = call.duration.split("min")[0]
                    previous_duration += int(duration)

        # Total credits of today
        today_call_history = Call_History.objects.filter(Q(user_id=user.id) & Q(date=today)).all()
        if today_call_history:
            for call in today_call_history:
                if "min" in call.duration:
                    duration = call.duration.split("min")[0]
                    today_duration += int(duration)

        if flag == True:  # If flag=True, return total credit count
            return previous_duration+today_duration
        else:  # If flag=False, return today credit count
            return today_duration

    def get(self, request):
        year_list = []
        for i in range(2017, 2101):
            year_list.append(i)

        month_name_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                           "October", "November", "December"]

        if 'year-filter' in request.GET:
            year = int(request.GET['year-filter'])
            month = int(request.GET['month-filter'])
            date = datetime(year, month+1, 1).date()-timedelta(days=1)
            result = []
            users = User.objects.all()
            for user in users:
                referred_by = User.objects.filter(email=user.referred_by).first()
                if referred_by:
                    referred_user_name = "{} {}".format(referred_by.first_name, referred_by.last_name)
                    total_credit = self.get_credits(user, date, True)

                    # Calculate Referral Count
                    total_referral_count = 0
                    referred_users = User.objects.filter(referred_by=user.email).all()

                    for referred_user in referred_users:
                        total_referral_count += self.get_credits(referred_user, date, True)

                    total_referral_balance = round(total_referral_count * 0.004, 2)
                    total_month_cashback = round(total_credit * 0.04 + total_referral_balance, 2)

                    user_info = {
                        'user': user,
                        'total_credit': total_credit,
                        'total_personal_balance': round(total_credit * 0.04, 2),
                        'referred_by': referred_user_name,
                        'total_ref_balance': total_referral_balance,
                        'total_balance': total_month_cashback
                    }
                    result.append(user_info)

            return render(request, self.template_name, {
                'workbook': result,
                'filter_year': year,
                'filter_month': month_name_list[month-1],
                'year_list': year_list,
                'month_list': month_name_list
            })

        current_user = request.user
        today = datetime.now().date()

        today_credit = self.get_credits(current_user, today, False)
        total_credit = self.get_credits(current_user, today, True)

        # Calculate Referral Count
        total_referral_count = 0
        referred_users = User.objects.filter(referred_by=current_user.email).all()

        for user in referred_users:
            total_referral_count += self.get_credits(user, today, True)

        total_referral_balance = round(total_referral_count*0.004, 2)
        total_month_cashback = round(total_credit*0.04+total_referral_balance, 2)

        # Last Four Months' data
        last_four_months = []
        date = today
        for i in range(1, 5):
            date = date.replace(day=1)-timedelta(days=1)

            #Calculate cashback of each month of last 4
            credits = self.get_credits(current_user, date, True)
            referral_count = 0
            referred_users = User.objects.filter(referred_by=current_user.email).all()
            for user in referred_users:
                referral_count += self.get_credits(user, date, True)
            referral_balance = round(referral_count * 0.004, 2)
            month_cashback = round(credits * 0.04 + referral_balance, 2)

            if month_cashback == 0:
                month_cashback_str = 'Nill'
            else:
                month_cashback_str = "£{}".format(month_cashback)

            month_data = {"month_name": date.strftime("%B"), "status": "N/A", "cash": month_cashback_str}

            last_four_months.insert(i - 1, month_data)

        #Save total credit of user
        current_user.credit_count = total_credit
        current_user.save()
        return render(request, self.template_name, {'total_credit': total_credit,
                                                    'today_credit': today_credit,
                                                    'total_referral_balance': total_referral_balance,
                                                    'total_cashback': total_month_cashback,
                                                    'user': current_user,
                                                    'current_month': today.strftime("%B").upper(),
                                                    'four_months_info': last_four_months,
                                                    'year_list': year_list,
                                                    'month_list': month_name_list
                                                    })

class RegistrationView(FormView):
    """
    Base class for user registration views.

    """
    disallowed_url = 'registration_disallowed'
    form_class = REGISTRATION_FORM
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'registration/registration_form.html'

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed and if user is logged in before even bothering to
        dispatch or do other processing.

        """
        if ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS:
            if self.request.user.is_authenticated:
                if settings.LOGIN_REDIRECT_URL is not None:
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    raise Exception((
                        'You must set a URL with LOGIN_REDIRECT_URL in '
                        'settings.py or set '
                        'ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS=False'))

        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = self.register(form)
        success_url = self.get_success_url(new_user)

        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = success_url
        except ValueError:
            return redirect(success_url)
        else:
            return redirect(to, *args, **kwargs)

    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return True

    def register(self, form):
        """
        Implement user-registration logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user=None):
        """
        Use the new user when constructing success_url.

        """
        return super(RegistrationView, self).get_success_url()


class ActivationView(TemplateView):
    """
    Base class for user activation views.

    """
    http_method_names = ['get']
    template_name = 'registration/activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(*args, **kwargs)
        if activated_user:
            success_url = self.get_success_url(activated_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, *args, **kwargs):
        """
        Implement account-activation logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError


class ResendActivationView(FormView):
    """
    Base class for resending activation views.
    """
    form_class = ResendActivationForm
    template_name = 'registration/resend_activation_form.html'

    def form_valid(self, form):
        """
        Regardless if resend_activation is successful, display the same
        confirmation template.

        """
        self.resend_activation(form)
        return self.render_form_submitted_template(form)

    def resend_activation(self, form):
        """
        Implement resend activation key logic here.
        """
        raise NotImplementedError

    def render_form_submitted_template(self, form):
        """
        Implement rendering of confirmation template here.

        """
        raise NotImplementedError


class ApprovalView(TemplateView):

    http_method_names = ['get']
    template_name = 'registration/admin_approve.html'

    def get(self, request, *args, **kwargs):
        approved_user = self.approve(*args, **kwargs)
        if approved_user:
            success_url = self.get_success_url(approved_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super(ApprovalView, self).get(request, *args, **kwargs)

    def approve(self, *args, **kwargs):
        """
        Implement admin-approval logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError
