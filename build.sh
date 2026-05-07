#!/bin/bash
# Script de build para Vercel (Django + PostgreSQL/Supabase)

# Instalar dependências
pip install -r requirements.txt -t .vercel-build

# Coletar arquivos estáticos (se houver)
python manage.py collectstatic --noinput || true

# Executar migrações no banco Supabase
python manage.py migrate || true
