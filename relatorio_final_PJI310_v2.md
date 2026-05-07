# Relatório Final - Projeto SGO (Sistema de Gestão de Oficina)
## PJI310 - Projeto Integrador | Univesp 2026

> **Versão:** v2.0 (Final - Deploy 100% Operacional)  
> **Data:** 07 de maio de 2026  
> **Projeto:** PJI310-A2026S1N2-GRUPO20  
> **Tecnologias:** Django 5.2, Python 3.14, PostgreSQL/Neon, HTML/CSS, JavaScript, Bootstrap 5, Vercel  
> **Repositório:** https://github.com/marco7apolo/PJI310-A2026S1N2-GRUPO20  
> **URL de Produção:** https://sgo-pji.vercel.app/  
> **Status:** ✅ Totalmente Funcional (Cadastros, Dashboard, PDF, Autenticação, Deploy)

---

## 📋 Sumário

1. [Visão Geral](#1-visão-geral)
2. [Jornada de Desenvolvimento](#2-jornada-de-desenvolvimento)
3. [Migração do Banco de Dados](#3-migração-do-banco-de-dados)
4. [Deploy na Vercel](#4-deploy-na-vercel)
5. [Commits Realizados](#5-commits-realizados)
6. [Funcionalidades Implementadas](#6-funcionalidades-implementadas)
7. [Configurações Técnicas](#7-configurações-técnicas)
8. [Conclusão](#8-conclusão)

---

## 1. Visão Geral

O **SGO (Sistema de Gestão de Oficina)** é uma aplicação web desenvolvida em Django para gerenciar oficinas de reparo de eletroeletrônicos. O sistema atende à demanda de pequenos empreendimentos do setor, muitos atuando na informalidade, oferecendo ferramentas para cadastro de clientes, equipamentos, técnicos e ordens de serviço (reparos), além de dashboards e geração de laudos técnicos em PDF.

### Contexto Social
- O Brasil é o 5º maior produtor de lixo eletrônico do mundo (~62 milhões de toneladas em 2022)
- Apenas ~3% dos resíduos eletrônicos são reciclados
- Cerca de 37,5% da população ocupada no Brasil está na informalidade
- O sistema utiliza metodologias centradas no usuário (Design Thinking)

---

## 2. Jornada de Desenvolvimento

### Fase 1: Configuração Inicial e MySQL
- Configuração inicial do projeto Django
- Desenvolvimento local com MySQL
- Implementação dos modelos: Cliente, Tecnico, Equipamento, Reparo
- Criação das views, forms e templates com Bootstrap 5

### Fase 2: Migração para PostgreSQL/Supabase
**Objetivo:** Preparar para deploy em nuvem

**Desafios encontrados:**
- Erro de conexão IPv6: `Cannot assign requested address`
- Erro de Pooler: `Tenant or user not found`
- Tentativas com Supabase Pooler e Direct Connection

**Resultado:** Migração para Supabase abandonada devido a incompatibilidades de rede

### Fase 3: Migração para Neon (Sucesso)
**Decisão:** Trocar Supabase pelo Neon (mais compatível com Vercel)

**Configuração Neon:**
- Projeto: `sgo-oficina`
- Versão PostgreSQL: 17
- Região: AWS US East 1
- Connection type: Pooled (para melhor performance serverless)

**String de conexão utilizada:**
```
postgresql://neondb_owner:PASSWORD_REMOVIDO@ep-royal-pond-ap7l2s2n-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### Fase 4: Configuração Django para Produção
**Alterações em `sgo/settings.py`:**
- Implementação de `dj-database-url` para parse da `DATABASE_URL`
- Configuração de variáveis de ambiente com `python-dotenv`
- `DEBUG=False` para produção
- `ALLOWED_HOSTS` configurado para Vercel

**Código da configuração do banco:**
```python
# Banco de dados - usa dj-database-url se disponível
try:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### Fase 5: Deploy na Vercel
**Configurações realizadas:**

1. **Variáveis de Ambiente no Vercel:**
   - `DJANGO_SETTINGS_MODULE=sgo.settings`
   - `DATABASE_URL` (string completa do Neon)
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,sgo-pji.vercel.app`

2. **Erros encontrados e soluções:**
   - Erro: `Requested setting PASSWORD_HASHERS, but settings are not configured`
     - Solução: Definir `DJANGO_SETTINGS_MODULE=sgo.settings`
   - Erro: `password authentication failed`
     - Solução: Resetar senha do Neon e atualizar `DATABASE_URL`
   - Erro: `Usuário ou senha inválidos` no login
     - Solução: Redefinir senha do superuser via Django shell

3. **Criação do Superuser:**
   - Usuário: `admin`
   - Senha: `SENHA_REMOVIDA`
   - Criado via SQL no Neon e confirmado via Django shell

---

## 3. Migração do Banco de Dados

### Tabelas Migradas
| Tabela | Descrição |
|--------|-----------|
| `auth_user` | Usuários do Django (admin) |
| `django_session` | Sessões de autenticação |
| `sgo_app_cliente` | Cadastro de clientes |
| `sgo_app_tecnico` | Cadastro de técnicos |
| `sgo_app_equipamento` | Cadastro de equipamentos |
| `sgo_app_reparo` | Ordens de serviço/reparos |

### Comandos de Migração Executados
```bash
# Migrações locais com Neon
python manage.py migrate

# Resultado:
# Applying sessions.0001_initial... OK
# Applying sgo_app.0001_initial... OK
# Applying sgo_app.0002_cliente_cep... OK
```

---

## 4. Deploy na Vercel

### URL de Produção
**https://sgo-pji.vercel.app/**

### Funcionalidades Testadas em Produção
- ✅ Login com admin/SENHA_REMOVIDA
- ✅ Cadastro de clientes
- ✅ Cadastro de técnicos
- ✅ Cadastro de equipamentos
- ✅ Criação de ordens de serviço
- ✅ Geração de PDF (laudo técnico)
- ✅ Dashboard com gráficos

### Estrutura do Deploy
- **Plataforma:** Vercel
- **Projeto:** sgo-pji
- **Framework:** Django (auto-detectado)
- **Banco:** Neon PostgreSQL (Pooled connection)

---

## 5. Commits Realizados

### Histórico de Commits (Principais)
```
commit 9c15aec - Configuração inicial settings.py com variáveis de ambiente
commit fd42b8a - Adição do dj-database-url e python-dotenv
commit 80cc62d - Migração para PostgreSQL/Supabase (v1.1)
commit 73a05d0 - Correção de erros de migração
commit 729b962 - Atualização de relatórios v1.2
commit 55aed05 - Migração para Neon (v1.3)
commit dc6e539 - Correções finais settings.py
commit f6a89d0 - Relatório v1.3 final
commit [novo] - Deploy Vercel 100% operacional (v2.0)
```

### Arquivos Versionados
- `sgo/settings.py` - Configurações principais
- `sgo_app/models.py` - Modelos do sistema
- `sgo_app/views.py` - Lógica das views
- `requirements.txt` - Dependências
- `relatorio_projeto.md` - Relatórios de progresso
- `.gitignore` - Arquivos ignorados (.env, __pycache__)

---

## 6. Funcionalidades Implementadas

### 6.1 Autenticação
- Login de usuários
- Logout
- Proteção de rotas com `@login_required`

### 6.2 Cadastros (CRUD)
- **Clientes:** Nome, CPF, telefone, email, endereço, CEP
- **Técnicos:** Nome, especialidade, contato
- **Equipamentos:** Tipo, marca, modelo, número de série
- **Reparos:** Cliente, equipamento, técnico, descrição, custo, status

### 6.3 Dashboard
- Contadores de registros
- Gráficos de equipamentos por tipo (Chart.js)
- Gráficos de equipamentos por marca
- Faturamento total

### 6.4 Relatórios PDF
- Geração de laudo técnico em PDF
- Utiliza ReportLab
- Download direto no navegador

### 6.5 Interface
- Bootstrap 5 responsivo
- Navbar com navegação
- Mensagens de feedback (success, error)
- Ícones Font Awesome

---

## 7. Configurações Técnicas

### 7.1 Stack Tecnológica
| Camada | Tecnologia |
|--------|------------|
| Backend | Django 5.2, Python 3.14 |
| Banco | PostgreSQL 17 (Neon) |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Gráficos | Chart.js |
| PDF | ReportLab |
| Deploy | Vercel |
| Controle de Versão | Git/GitHub |

### 7.2 Dependências (requirements.txt)
```
django>=5.2
psycopg2-binary
reportlab
python-dotenv
dj-database-url
```

### 7.3 Variáveis de Ambiente
| Variável | Descrição | Valor (exemplo) |
|----------|-----------|-----------------|
| `DJANGO_SETTINGS_MODULE` | Módulo de settings | `sgo.settings` |
| `DATABASE_URL` | String de conexão PostgreSQL | `postgresql://...` |
| `DJANGO_SECRET_KEY` | Chave secreta Django | `django-insecure-...` |
| `DJANGO_DEBUG` | Modo debug | `False` (prod) / `True` (local) |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1,sgo-pji.vercel.app` |

---

## 8. Conclusão

O projeto SGO foi desenvolvido com sucesso, superando diversos desafios técnicos relacionados à migração de banco de dados e deploy em nuvem. A jornada envolveu:

1. **Migração de MySQL para PostgreSQL** (Supabase → Neon)
2. **Configuração de ambiente de produção** com variáveis de ambiente
3. **Deploy em plataforma serverless** (Vercel)
4. **Resolução de erros de conexão** (IPv6, Pooler, autenticação)
5. **Testes completos** de todas as funcionalidades

O sistema está **100% operacional** em produção, com todas as funcionalidades testadas e aprovadas.

### Credenciais de Acesso
- **URL:** https://sgo-pji.vercel.app/login/
- **Usuário:** admin
- **Senha:** SENHA_REMOVIDA

### Repositório
https://github.com/marco7apolo/PJI310-A2026S1N2-GRUPO20

---

## Anexos

### A. Estrutura de Diretórios
```
PJI310-A2026S1N2-GRUPO20/
├── sgo/                    # Configurações principais do Django
│   ├── settings.py         # Configurações: banco, apps, ambiente
│   ├── urls.py             # Rotas principais
│   ├── wsgi.py             # Interface WSGI
│   └── asgi.py             # Interface ASGI
├── sgo_app/                # Aplicação principal
│   ├── models.py           # Modelos: Cliente, Tecnico, Equipamento, Reparo
│   ├── views.py            # Lógica das páginas
│   ├── forms.py            # Formulários Django
│   ├── urls.py             # Rotas da app
│   ├── admin.py            # Configuração do admin
│   └── templates/sgo_app/  # Templates HTML
│       ├── base.html
│       ├── login.html
│       ├── home.html
│       ├── dashboard.html
│       ├── cliente_*.html
│       ├── tecnico_*.html
│       ├── equipamento_*.html
│       ├── reparo_*.html
│       └── reparo_pdf.html
├── manage.py               # Script de gerenciamento Django
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis locais (não versionado)
├── .gitignore              # Arquivos ignorados
└── relatorio_final_PJI310_v2.md  # Este relatório
```

### B. Erros e Soluções
| Erro | Causa | Solução |
|------|-------|---------|
| `Cannot assign requested address` | IPv6 no Supabase | Migrou para Neon |
| `Tenant or user not found` | Pooler Supabase | Usou Pooled connection Neon |
| `password authentication failed` | Senha expirada | Reset no Neon |
| `relation auth_user does not exist` | Migrations não rodaram | `python manage.py migrate` |
| `Usuário ou senha inválidos` | Senha incorreta | `user.set_password()` no shell |

---

**Relatório gerado em:** 07 de maio de 2026  
**Projeto:** PJI310 - Projeto Integrador | Univesp  
**Grupo:** GRUPO20
