from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from access.decorators import require_auth, require_policy


class DummyReq:
    def __init__(self, user):
        self.user = user


class DecoratorsTests(TestCase):
    def test_require_auth_denies_anonymous(self):
        @require_auth
        def view(request):
            return 'ok'

        req = DummyReq(AnonymousUser())
        resp = view(req)
        # JsonResponse returned
        self.assertEqual(resp.status_code, 401)

    def test_require_auth_allows_user(self):
        u = User.objects.create_user(username='a', password='p')
        @require_auth
        def view(request):
            return 'ok'
        req = DummyReq(u)
        # Django's AnonymousUser not authenticated; a real User is sufficient here
        resp = view(req)
        self.assertEqual(resp, 'ok')

    def test_require_policy_denies(self):
        def check(request, *a, **k):
            return False

        @require_policy(check)
        def view(request):
            return 'ok'

        req = DummyReq(User())
        resp = view(req)
        self.assertEqual(resp.status_code, 403)
