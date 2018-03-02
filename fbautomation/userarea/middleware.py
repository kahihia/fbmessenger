import django
from django.shortcuts import redirect

from pinax.stripe.actions import customers, subscriptions
from pinax.stripe.conf import settings

try:
    from django.urls import resolve
except ImportError:
    from django.core.urlresolvers import resolve

try:
    from django.utils.deprecation import MiddlewareMixin as MixinorObject
except ImportError:
    MixinorObject = object


class ActiveSubscriptionMiddleware(MixinorObject):
    """ Middlware.

    This middlware is checking if user
    has active subscreption and if not
    redirects to given page from subscription
    required page.
    """

    def process_request(self, request):
        # TODO Add messages limit check.
        is_authenticated = request.user.is_authenticated
        if django.VERSION < (1, 10):
            is_authenticated = is_authenticated()

        if is_authenticated and not request.user.is_staff:
            url_name = resolve(request.path).url_name
            if url_name in settings.PINAX_STRIPE_SUBSCRIPTION_REQUIRED_URLS:
                customer = customers.get_customer_for_user(request.user)
                if not subscriptions.has_active_subscription(customer):
                    return redirect(
                        settings.PINAX_STRIPE_SUBSCRIPTION_REQUIRED_REDIRECT
                    )
