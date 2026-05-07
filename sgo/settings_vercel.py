"""
Configurações específicas para o Vercel (PostgreSQL/Supabase via Pooler)
"""
from .settings import *

# Força configurações do banco para o Vercel
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.evunltitxfjrreymbvbb',
        'PASSWORD': 'cjNikpPtHCUpNneR',
        'HOST': 'aws-0-sa-east-1.pooler.supabase.com',
        'PORT': '6543',
    }
}

# Debug desligado no Vercel
DEBUG = False

# Aceita domínios do Vercel
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']
