"""
Configurações do Django para o projeto SGO.

Gerado por `django-admin startproject` com Django 5.2.

Documentação: https://docs.djangoproject.com/en/5.2/topics/settings/
Referência completa: https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

# Caminhos: use BASE_DIR / 'subpasta'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Ajustes rápidos para desenvolvimento — não use em produção sem revisão.
# Lista de verificação: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# ATENÇÃO: em produção, use uma chave secreta forte e armazenada com segurança.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-^e!pq99yblwp0r9*s=e+g_+72r)-5=dclo2fb5+#3fdudu@ef5',
)

# ATENÇÃO: desative DEBUG em produção.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

_allowed = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]


# Aplicações instaladas e middleware

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'sgo_app.apps.RepairsConfig',
    'sgo_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sgo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sgo.wsgi.application'


# Banco de dados
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Configuração via variáveis de ambiente (suporte a PostgreSQL/Supabase e MySQL)
# Variáveis necessárias para PostgreSQL/Supabase:
#   DB_ENGINE=django.db.backends.postgresql
#   DB_NAME=nome_do_banco (geralmente "postgres" no Supabase)
#   DB_USER=usuario (formato: postgres.[project-ref] no Supabase)
#   DB_PASSWORD=senha_forte
#   DB_HOST=host (ex: aws-0-us-east-1.pooler.supabase.com)
#   DB_PORT=6543 (porta do Transaction Pooler do Supabase)
# Para MySQL local (desenvolvimento legado):
#   DB_ENGINE=django.db.backends.mysql
#   DB_NAME=bd_sgo
#   DB_USER=pi_1_26_user
#   DB_PASSWORD=Pi@1_2026
#   DB_HOST=127.0.0.1
#   DB_PORT=3306

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Validação de senha
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Idioma e fuso horário (Brasil)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos (CSS, JavaScript, imagens)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Tipo padrão de chave primária
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'  # Para onde o usuário vai após logar
LOGOUT_REDIRECT_URL = 'login' # Para onde vai após deslogar