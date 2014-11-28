"""
Django settings for MyDjangoApp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#Django won't start if secret key is not set. The key protects django from remote intrusions
SECRET_KEY = 'XXXXXXX'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#Generate reports for every exception that occurred during template rendering
#DEBUG = True must be set before for this to work
TEMPLATE_DEBUG = True

#A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'database_files',
    'dashboards',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
#Web Server Gateway Interface provides a simple interface between different web servers and applications (web frameworks)
#this prevents programmer from modifying code for every type of servers, i.e. CGI, FastCGI, mod_python etc.
ROOT_URLCONF = 'MyDjangoApp.urls'

#
WSGI_APPLICATION = 'MyDjangoApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user_name',
        'USER': 'user',
        'HOST': 'some_host',
        'PASSWORD': '111',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

MEDIA_URL = '/media/'

STATIC_ROOT = 'path to my static root on server'

#location of the static files for the project (i.e. .js, .css, .img)\
STATIC_URL = '/staff/sukharni/django/dashboards/static/'

#additional locations of static files, for example outside of the app directory
STATICFILES_DIRS = ( os.path.join(os.path.dirname(__file__), '../dashboards/static'),)


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__),  '../templates'),
)

#Default file storage class to be used for any file-related operations that don’t specify a particular storage system.
DEFAULT_FILE_STORAGE = 'database_files.storage.DatabaseStorage'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 'our e-mail port (int)'

