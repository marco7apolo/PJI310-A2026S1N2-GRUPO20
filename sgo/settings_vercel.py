"""
Configurações específicas para o Vercel (PostgreSQL/Supabase via Conexão Direta IPv4)
"""
from .settings import *
import socket

# Força uso de IPv4 (desativa IPv6) para evitar "Cannot assign requested address"
socket.has_ipv6 = False

# String de conexão direta (funcionou localmente) - usando IPv4 forçado
# Formato: postgresql://user:password@host:port/database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'cjNikpPtHCUpNneR',
        'HOST': 'db.evunltitxfjrreymbvbb.supabase.co',
        'PORT': '5432',
    }
}

# Debug desligado no Vercel
DEBUG = False

# Aceita domínios do Vercel
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']
