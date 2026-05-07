"""
Configurações específicas para o Vercel (PostgreSQL/Supabase via Pooler)
"""
from .settings import *
import dj_database_url

# String de conexão direta para o Pooler (IPv4)
DATABASE_URL = 'postgresql://postgres.evunltitxfjrreymbvbb:cjNikpPtHCUpNneR@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'

# Configura o banco via dj-database-url
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

# Debug desligado no Vercel
DEBUG = False

# Aceita domínios do Vercel
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']
