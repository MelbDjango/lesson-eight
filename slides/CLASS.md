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

## Creating object with current user

- Do **not** include the `author` field in the form!

```python

class ArticleCreateView(LoginRequiredMixin, CreateView):
    # ...

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)
```

---

## Limiting access to object owner

```python

class ArticleDetailView(LoginRequiredMixin, DetailView):
    # ...

    def get_queryset(self):
        qs = super(ArticleDetailView, self).get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs
```

- Same works for `ListView`, `UpdateView`, `DeleteView`.
  - Do **not** include the `author` field in the form for `UpdateView`!
- This will return an HTTP 404 (Not Found) error when a user is not the author

---

![](http://i.imgur.com/WjfRf2H.png)

---

### Why Heroku?

- Cheap during development and testing (reasonable after that)
- Quick and easy to get started
- Scales really well
- git based workflow
- Release management and rollback

---

### Packages we'll use

- Heroku Toolkit
- dj-database-url
- whitenoise
- gunicorn
- Django
- (virtualenv)

---

### Heroku Toolbelt

- Availale for all major platforms
- Has commands for setting up domains, etc.
- Let's you access logs and run management commands

---

### Heroku Toolbelt

```shell
> heroku --help

Usage: heroku COMMAND [--app APP] [command-specific-options]

Primary help topics, type "heroku help TOPIC" for more details:

  addons    #  manage addon resources
  apps      #  manage apps (create, destroy)
  auth      #  authentication (login, logout)
  config    #  manage app config vars
  domains   #  manage custom domains
  logs      #  display logs for an app
  ps        #  manage dynos (dynos, workers)
  releases  #  manage app releases
  run       #  run one-off commands (console, rake)
  sharing   #  manage collaborators on an app
```

https://toolbelt.heroku.com/

---

### dj-database-url

- Abstracts away our `DATABASES` configuration
  - On Heroku, we don't know our DB details
- Sets up your database based on `DATABASE_URL` environment variable
- Supports PostgreSQL, PostGIS, MySQL, MySQL (GIS) and SQLite
- Install it locally: `pip install dj-database-url`

---

### dj-database-url

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///{}'.format(
        DATABASES['default']['NAME'])
    )
}
```

https://github.com/kennethreitz/dj-database-url

---

### Static Files

- In development Django serves your static files
- In production you don't really want that
- You can set up nginx, Apache or uWSGI to do it
- `whitenoise` provides a happy middleground (and it's super easy!)

- `pip install whitenoise`

---

### whitenoise

```python
# wsgi.py

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())
```

```python
# settings.py

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

https://github.com/evansd/whitenoise

---

### Running the Application

- Goodbye `./manage.py runserver`!
- Hello `gunicorn`

- You can use other `WSGI` compliant servers too
  - uWSGI
  - Apache/mod_wsgi

- (you don't need to install this one locally)

---

### gunicorn

```
# Procfile

web: gunicorn melbdjangoheroku.wsgi --log-file -
```

http://gunicorn.org

---

### Don't use FastCGI

- FastCGI support is deprecated and will be removed in Django 1.9
- This was useful in shared hosting environments, but Heroku is the better way!

---

### Django settings

```python
# settings.py

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['<your-app>.herokuapp.com']
```

---

### Setting Debug = False

- In Production we need to make sure `DEBUG=False`
  - This is _really_ important
- Larger applications tend to use different settings for each environment
  - Check out `django-classy-settings` and

```python
# Use an environment variable, default to the safe value
# export DJANGO_DEBUG=True
DEBUG = os.environ.get('DJANGO_DEBUG', False)

# Use _your_ environment to do the switch
DEBUG = os.uname()[0] == 'Darwin'
```

---

### Your secret_key

- Django's `SECRET_KEY` needs to remain secret!
  - If your project is open source, you need to use a secret key that's _not_ in your repository
  - This is good practice either way
- Use the `heroku config:set` command

```
> heroku config:set DJANGO_SECRET_KEY=<long-random-string>
```

```python
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'ThIs-K3Y-iSnT-a-5eCrEt')
```

---

### Our new requirements.txt

```
# requirements.txt

Django==1.8.4
dj-database-url==0.3.0
gunicorn==19.3.0
whitenoise==2.0.3
psycopg2==2.6.1
```

http://slides.com/brntn/managing-your-django-requirements/#/

---

### Actually Deploying our Application

- Commit your configuration
- run `heroku create`
- `git push heroku master`
- heroku looks after:
  - installing (and removing) requirements
  - collectstatic
- `heroku run python manage.py migrate`
- `heroku run python manage.py createsuperuser`


---

### Things that aren't Heroku

- PaaS aimed at Python/Django:
  - Gondor.io
  - Python Anywhere
  - Open Shift

- Or, your "own" box:
  - Digital Ocean
  - AWS / Azure

---

### The Django Deployment Checklist

- There's a bunch of other stuff you should _check_ before deploying
- Check the docs:
  - https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

---

## We're Almost Done!

- One more class:
  - Some more advanced Django topics
  - Demo Day!

- MelbDjango School 201 will launch soon!
