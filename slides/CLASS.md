## MelbDjango School

### Lesson Eight — Authentication & Deploying

---

## WIFI

Common Code / cc&20!4@

---

MelbDjango Project -- how is it going?

---

# Authentication in Django

---

## What does "authenticate" mean?

---

## What does "authenticate" mean?

<dl>
<dt>authenticare</dt>
<dd>from Latin, to establish as genuine</dd>
</dl>

---

## Why do we want it?

- Allow only some people to do something
- Know who wrote a blog article

---

## Django ships with an authentication system

- `django.contrib.auth`
- User model: `django.contrib.auth.models.User`
- Login / Logout:
  - Views in `django.contrib.auth.views`
  - Helper methods in `django.contrib.auth`

---

## Check if a user is authenticated

```python
def myview(request):
    if request.user.is_authenticated():
        # Do something for authenticated users.
        ...
    else:
        # Do something for anonymous users.
        ...
```

[Documentation](https://docs.djangoproject.com/en/1.8/topics/auth/default/#authentication-in-web-requests)

---

## Limiting access to logged-in users

```python
from django.conf import settings
from django.shortcuts import redirect

def myview(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)

    # Authenticated users reach this point
    ...
```

[Documentation](https://docs.djangoproject.com/en/1.8/topics/auth/default/#limiting-access-to-logged-in-users)

---

## Limiting access to logged-in users (simplification)

```python
from django.contrib.auth.decorators import login_required

@login_required
def myview(request):
    # Authenticated users reach this point
    ...
```

[Documentation](https://docs.djangoproject.com/en/1.8/topics/auth/default/#the-login-required-decorator)

---

## Limiting access to Class Based Views

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class ProtectedView(TemplateView):
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)
```
[Documentation](https://docs.djangoproject.com/en/1.8/topics/class-based-views/intro/#decorating-the-class)

---

## `LoginRequired` mixin for Class Based Views

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'secret.html'
```

- Django 1.9 will ship with a `LoginRequiredMixin` 🙂

---

## Logging a user in

- Either use the Django admin
- Use `django.contrib.auth.views.login` view. Add this to your `urls.py`:

  ```python
  from django.contrib.auth import views as auth_views
  url(
      r'^accounts/login/$', auth_views.login,
      {'template_name': 'myapp/login.html'}
  ),
  ```
  **Remember the template**: [example](https://docs.djangoproject.com/en/1.8/topics/auth/default/#django.contrib.auth.views.login)

- Your own login view: [Documentation](https://docs.djangoproject.com/en/1.8/topics/auth/default/#how-to-log-a-user-in)

---

## "Owning" an object

```python
from django.conf import settings
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
```

---

## We're Almost Done!

- One more class:
  - Deploying your Django App
  - Demo Day!

- MelbDjango School 201 will launch soon!
