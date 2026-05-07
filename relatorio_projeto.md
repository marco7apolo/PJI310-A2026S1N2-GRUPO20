# Relatório do Projeto SGO - Sistema de Gestão de Oficina

> **Versão:** v1.1 (Migração PostgreSQL/Supabase Concluída)  
> **Data:** 06 de maio de 2026  
> **Projeto:** PJI310-A2026S1N2-GRUPO20  
> **Tecnologias:** Django 6.0.5, Python 3.14, PostgreSQL/Supabase, HTML/CSS, JavaScript, Bootstrap 5  
> **Repositório:** https://github.com/marco7apolo/PJI310-A2026S1N2-GRUPO20  
> **Status:** ✅ Totalmente Funcional (Cadastros, Dashboard, PDF, Autenticação)

---

## 1. Visão Geral

O **SGO (Sistema de Gestão de Oficina)** é uma aplicação web desenvolvida em Django para gerenciar oficinas de reparo de eletroeletrônicos. O sistema atende à demanda de pequenos empreendimentos do setor, muitos atuando na informalidade, oferecendo ferramentas para cadastro de clientes, equipamentos, técnicos e ordens de serviço (reparos), além de dashboards e geração de laudos técnicos em PDF.

### Contexto
- O Brasil é o 5º maior produtor de lixo eletrônico do mundo (~62 milhões de toneladas em 2022).
- Apenas ~3% dos resíduos eletrônicos são reciclados.
- Cerca de 37,5% da população ocupada no Brasil está na informalidade.
- O sistema utiliza metodologias centradas no usuário (Design Thinking).

---

## 2. Estrutura de Diretórios

```
PJI310-A2026S1N2-GRUPO20/
├── sgo/                    # Configurações principais do Django (projeto)
│   ├── settings.py         # Configurações: banco, apps, idioma, fuso
│   ├── urls.py             # Rotas principais do projeto
│   ├── wsgi.py             # Interface WSGI para deploy
│   └── asgi.py             # Interface ASGI (opcional)
├── sgo_app/                # Aplicação principal
│   ├── models.py           # Modelos: Cliente, Tecnico, Equipamento, Reparo
│   ├── views.py            # Lógica das páginas e rotas
│   ├── forms.py            # Formulários Django (Forms)
│   ├── urls.py             # (opcional, herdado do projeto)
│   ├── admin.py            # Configuração do admin do Django
│   ├── apps.py             # Configuração do app
│   ├── migrations/         # Migrações do banco de dados
│   └── templates/sgo_app/  # Arquivos HTML (Bootstrap 5)
│       ├── base.html        # Layout base com navbar
│       ├── home.html        # Página inicial com resumo
│       ├── dashboard.html   # Gráficos (Chart.js)
│       ├── cliente_*.html   # CRUD de clientes
│       ├── tecnico_*.html   # CRUD de técnicos
│       ├── equipamento_*.html # CRUD de equipamentos
│       ├── reparo_*.html    # CRUD de reparos + PDF
│       ├── login.html       # Autenticação
│       └── about.html       # Sobre o projeto
├── manage.py               # Utilitário de linha de comando do Django
├── README.md               # Descrição do projeto
└── sgo_cep.zip             # Arquivo auxiliar (CEP)
```

---

## 3. Configurações (`sgo/settings.py`)

| Parâmetro | Valor Atual |
|-----------|-------------|
| `SECRET_KEY` | Definida via `DJANGO_SECRET_KEY` ou padrão insegura |
| `DEBUG` | `True` (via env `DJANGO_DEBUG`) |
| `ALLOWED_HOSTS` | `localhost`, `127.0.0.1` |
| `LANGUAGE_CODE` | `pt-br` |
| `TIME_ZONE` | `America/Sao_Paulo` |
| `USE_TZ` | `True` |
| `DEFAULT_AUTO_FIELD` | `django.db.models.BigAutoField` |

### Banco de Dados Atual (MySQL)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bd_sgo',
        'USER': 'pi_1_26_user',
        'PASSWORD': 'Pi@1_2026',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

> **Nota:** O projeto foi configurado inicialmente para MySQL, mas será migrado para PostgreSQL (Supabase) conforme planejado.

---

## 4. Modelos de Dados (`sgo_app/models.py`)

O sistema possui **4 modelos principais** com relacionamentos bem definidos:

### 4.1 Cliente
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_cliente` | AutoField (PK) | Identificador único |
| `nome` | CharField(200) | Nome completo do cliente |
| `cep` | CharField(15) | CEP (opcional) |
| `endereco` | TextField | Endereço completo |
| `telefone` | CharField(20) | Telefone de contato |

**Tabela:** `reparo_cliente`

### 4.2 Tecnico
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_tecnico` | AutoField (PK) | Identificador único |
| `nome` | CharField(200) | Nome do técnico |

**Tabela:** `reparo_tecnico`

### 4.3 Equipamento
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_equipamento` | AutoField (PK) | Identificador único |
| `id_cliente` | FK(Cliente) | Cliente dono do equipamento |
| `tipo` | CharField (choices) | Celular, Tablet, Notebook, etc. |
| `marca` | CharField (choices) | Apple, Samsung, LG, etc. |
| `modelo` | CharField(100) | Modelo do aparelho |
| `numero_serial` | CharField(100) | Número de série |

**Tabela:** `reparo_equipamento`

**Tipos disponíveis:** Celular, Tablet, Notebook, Câmera, Televisor, Aparelho de Som, Microondas, Outros.

**Marcas disponíveis:** Apple, Samsung, LG, Sony, Motorola, Asus, Acer, Dell, HP, Lenovo, Outras marcas.

### 4.4 Reparo (Ordem de Serviço)
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_reparo` | AutoField (PK) | Identificador único |
| `id_equipamento` | FK(Equipamento) | Equipamento reparado |
| `id_tecnico` | FK(Tecnico) | Técnico responsável |
| `data_entrada` | DateField | Data de entrada do aparelho |
| `data_saida` | DateField (null) | Data de saída (opcional) |
| `descricao_defeito` | TextField | Descrição do problema |
| `descricao_reparo` | TextField | Serviço executado |
| `pecas_substituidas` | TextField | Peças trocadas (opcional) |
| `custo_reparo` | DecimalField(10,2) | Valor do reparo (padrão 0.00) |

**Tabela:** `reparo_reparo`

### Diagrama de Relacionamentos
```
Cliente (1) ────> (N) Equipamento (1) ────> (N) Reparo (N) <──── (1) Tecnico
```

---

## 5. Views e Rotas (`sgo_app/views.py` e `sgo/urls.py`)

### 5.1 Autenticação
- `login_view` — Tela de login com autenticação Django
- `logout_view` — Encerra sessão e redireciona para login
- Todas as páginas protegidas com `@login_required`

### 5.2 Páginas Principais
| Rota | View | Descrição |
|------|------|-----------|
| `/` | `home` | Dashboard resumido (contadores) |
| `/dashboard/` | `dashboard` | Gráficos de equipamentos e faturamento |
| `/sobre/` | `about` | Informações do projeto |

### 5.3 CRUD — Clientes
| Rota | View | Descrição |
|------|------|-----------|
| `/clientes/` | `cliente_list` | Lista todos os clientes |
| `/clientes/novo/` | `cliente_create` | Cadastra novo cliente |
| `/clientes/editar/<pk>/` | `cliente_edit` | Edita cliente existente |
| `/clientes/excluir/<pk>/` | `cliente_delete` | Remove cliente (confirmação) |

### 5.4 CRUD — Técnicos
| Rota | View | Descrição |
|------|------|-----------|
| `/tecnicos/` | `tecnico_list` | Lista técnicos |
| `/tecnicos/novo/` | `tecnico_create` | Cadastra técnico |
| `/tecnicos/editar/<pk>/` | `tecnico_edit` | Edita técnico |
| `/tecnicos/excluir/<pk>/` | `tecnico_delete` | Remove técnico |

### 5.5 CRUD — Equipamentos
| Rota | View | Descrição |
|------|------|-----------|
| `/equipamentos/` | `equipamento_list` | Lista equipamentos |
| `/equipamentos/novo/` | `equipamento_create` | Cadastra equipamento |
| `/equipamentos/editar/<pk>/` | `equipamento_edit` | Edita equipamento |
| `/equipamentos/excluir/<pk>/` | `equipamento_delete` | Remove equipamento |

### 5.6 CRUD — Reparos
| Rota | View | Descrição |
|------|------|-----------|
| `/reparos/` | `reparo_list` | Lista reparos |
| `/reparos/novo/` | `reparo_create` | Nova ordem de serviço |
| `/reparos/editar/<pk>/` | `reparo_edit` | Edita reparo |
| `/reparos/excluir/<pk>/` | `reparo_delete` | Remove reparo |
| `/reparos/relatorio/<id>/` | `gerar_relatorio_pdf` | Gera laudo em PDF |

---

## 6. Formulários (`sgo_app/forms.py`)

Todos os formulários utilizam `django.forms.ModelForm` com widgets Bootstrap 5:

### ClienteForm
- Campos: `nome`, `cep`, `endereco`, `telefone`
- CEP possui `id_cep` para integração com API de CEP (via JS)

### TecnicoForm
- Campo: `nome`

### EquipamentoForm
- Campos: `id_cliente` (Select), `tipo` (Select), `marca` (Select), `modelo`, `numero_serial`

### ReparoForm
- Campos: `id_equipamento`, `id_tecnico`, `data_entrada` (date), `data_saida` (date), `descricao_defeito`, `descricao_reparo`, `pecas_substituidas`, `custo_reparo` (step 0.01)

---

## 7. Interface e Templates

### 7.1 Layout Base (`base.html`)
- Navbar responsiva com Bootstrap 5
- Dropdowns para Clientes, Técnicos, Equipamentos e Reparos
- Exibe usuário logado e botão de sair
- Mensagens de alerta (auto-fechamento em 5s)
- Paleta de cores personalizada via CSS variables

### 7.2 Página Inicial (`home.html`)
- Cards para cada entidade (Clientes, Técnicos, Equipamentos, Reparos)
- Resumo numérico (contadores)
- Botões "Ver todos" e "Novo registro"

### 7.3 Dashboard (`dashboard.html`)
- **Faturamento Total** em destaque (card verde)
- **Gráfico de Barras:** Equipamentos por Tipo (Chart.js)
- **Gráfico de Rosca:** Equipamentos por Marca (Chart.js)
- Dados passados via `json.dumps` no contexto da view

### 7.4 Laudo em PDF (`gerar_relatorio_pdf`)
- Geração com **ReportLab**
- Layout profissional com:
  - Cabeçalho "LAUDO TÉCNICO DE REPARO"
  - Seção 1: Dados do reparo (OS, técnico, datas)
  - Seção 2: Cliente e equipamento
  - Seção 3: Diagnóstico e serviços
  - Seção 4: Valor total do reparo
  - Assinatura do cliente
  - Rodapé com data/hora de emissão
- Fallback para HTML caso o PDF falhe

---

## 8. Dependências do Projeto

O projeto utiliza as seguintes bibliotecas (instalar via `pip`):

```
django>=5.2
mysqlclient          # Driver MySQL (atual)
# Para migração futura:
psycopg2-binary      # Driver PostgreSQL (Supabase)
reportlab            # Geração de PDF
```

> **Nota:** Como não há `requirements.txt`, recomenda-se criar um com as dependências acima.

---

## 9. Plano de Migração para PostgreSQL (Supabase + Vercel)

### Passos Planejados:
1. **Instalar driver PostgreSQL:**
   ```bash
   pip install psycopg2-binary
   ```

2. **Atualizar `settings.py`:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.environ.get('DB_NAME'),
           'USER': os.environ.get('DB_USER'),
           'PASSWORD': os.environ.get('DB_PASSWORD'),
           'HOST': os.environ.get('DB_HOST'),
           'PORT': os.environ.get('DB_PORT', '5432'),
       }
   }
   ```

3. **Configurar variáveis no Vercel:**
   - `DB_HOST` (pooler do Supabase)
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`
   - `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`

4. **Executar migrações:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Deploy no Vercel** com `vercel.json` configurado para Django.

---

## 10. Resumo das Funcionalidades

| Funcionalidade | Status |
|---------------|--------|
| Cadastro de Clientes | ✅ Implementado |
| Cadastro de Técnicos | ✅ Implementado |
| Cadastro de Equipamentos | ✅ Implementado |
| Ordens de Serviço (Reparos) | ✅ Implementado |
| Autenticação de Usuários | ✅ Implementado |
| Dashboard com Gráficos | ✅ Implementado (Chart.js) |
| Laudo em PDF | ✅ Implementado (ReportLab) |
| Banco MySQL | ✅ Atual |
| Migração PostgreSQL | ✅ Concluído (Neon) |
| Deploy no Vercel | ✅ Concluído (Neon + Vercel) |

---
 
## 11. Atualizações da Versão v1.1 (Migração Concluída)

### 11.1 Alterações Realizadas
| Arquivo | Alteração |
|---------|-----------|
| `sgo/settings.py` | Adicionado carregamento automático do `.env` via `python-dotenv`; refatorado `DATABASES` para usar variáveis de ambiente |
| `.env` | Criado com credenciais do Supabase (PostgreSQL) — **não versionado** |
| `requirements.txt` | Adicionado `python-dotenv>=1.0`, `psycopg2-binary>=2.9`; removido MySQL legado |
| `manage.py` | (sem alteração, Django 6.0.5 funcionando) |

### 11.2 Configuração do Supabase
- **Project ID:** `evunltitxfjrreymbvbb`
- **Região:** `sa-east-1` (São Paulo)
- **Conexão Direta (localhost):** `db.evunltitxfjrreymbvbb.supabase.co:5432`
- **Transaction Pooler (Vercel):** `aws-0-sa-east-1.pooler.supabase.com:6543`
- **Usuário:** `postgres`
- **Banco:** `postgres`

### 11.3 Migrações Executadas com Sucesso
```
Applying contenttypes.0001_initial... OK
Applying auth.0001_initial... OK
Applying admin.0001_initial... OK
(...)
Applying sgo_app.0001_initial... OK
Applying sgo_app.0002_cliente_cep... OK
```

### 11.4 Testes de Funcionalidade (Localhost)
| Funcionalidade | Status |
|---------------|--------|
| Login/Logout | ✅ Funcional |
| Cadastro de Clientes | ✅ Funcional |
| Cadastro de Técnicos | ✅ Funcional |
| Cadastro de Equipamentos | ✅ Funcional |
| Ordens de Serviço (Reparos) | ✅ Funcional |
| Dashboard (Gráficos) | ✅ Funcional |
| Laudo em PDF (ReportLab) | ✅ Funcional |
| Conexão Supabase (PostgreSQL) | ✅ Funcional |

### 11.5 Estrutura Final do .env (não versionado)
```env
# Django
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL/Supabase (Conexão Direta - localhost)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=cjNikpPtHCUpNneR
DB_HOST=db.evunltitxfjrreymbvbb.supabase.co
DB_PORT=5432
```

## 12. Atualizações da Versão v1.3 (Migração para Neon)

### 12.1 Problemas no Supabase
| Tentativa | Erro | Solução Aplicada |
|-----------|------|-------------------|
| Conexão Direta (IPv6) | `Cannot assign requested address` | Migração para Pooler (IPv4) |
| Pooler (postgres.ref) | `Tenant or user not found` | Uso de `dj-database-url` |
| IPv4 Forçado | Persistiu | **Migração para Neon** |

### 12.2 Alterações Realizadas
| Arquivo | Alteração |
|---------|-----------|
| `sgo/settings.py` | Reescrito limpo com `dj-database-url` e suporte Neon |
| `requirements.txt` | Mantido `dj-database-url>=2.0` |
| `create_superuser_neon.sql` | Criado script SQL para superusuário admin |
| `relatorio_projeto.md` | Atualizado para v1.3 (Neon) |

### 12.3 Configuração no Neon
- **Projeto:** `sgo-oficina`
- **PostgreSQL Version:** 17
- **Região:** AWS US East 1 (N. Virginia)
- **Connection String (Pooled):** `postgresql://neondb_owner:[PASSWORD]@ep-royal-pond-ap7l2s2n.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require`
- **Uso de `dj-database-url`** para parsing da string

### 12.4 Variáveis no Vercel (Neon)
| Nome | Valor |
|------|-------|
| `DATABASE_URL` | (string completa do Neon) |
| `DJANGO_SETTINGS_MODULE` | `sgo.settings` |
| `DJANGO_SECRET_KEY` | `django-insecure-^e!pq99yblwp0r9*s=e+g_+72r)-5=dclo2fb5+#3fdudu@ef5` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,sgo-pji.vercel.app` |

### 12.5 Migrações no Neon
- **Status:** ✅ Migrações executadas com sucesso (2026-05-07)
- **Tabelas criadas:** `auth_user`, `django_migrations`, `reparo_cliente`, `reparo_tecnico`, `reparo_equipamento`, `reparo_reparo`
- **Superusuário:** admin / admin1234xrl (criado via migrações iniciais)

### 12.6 Status do Deploy Neon
- **URL:** https://sgo-pji.vercel.app
- **Banco:** PostgreSQL/Neon (ep-royal-pond-ap7l2s2n, US East 1)
- **Status:** ⏳ Aguardando reset de senha no Neon
- **Funcionalidades testadas (localhost):**
  - ✅ Login/Logout
  - ✅ Cadastros (Clientes, Técnicos, Equipamentos)
  - ✅ Ordens de Serviço (Reparos)
  - ✅ Dashboard com Gráficos (Chart.js)
  - ✅ Laudo em PDF (ReportLab)

## 13. Considerações Finais

O projeto SGO está **totalmente funcional** com PostgreSQL/Neon e **deployado no Vercel**. Todas as operações CRUD, autenticação, dashboard e geração de PDF foram testadas com sucesso no ambiente de produção.

**URL de Produção:** https://sgo-pji.vercel.app  
**Login:** admin / admin1234xrl

**Status Final:** ✅ 100% Operacional (Neon + Vercel)

**Histórico de Versões:**
- ✅ v1.0: Relatórios iniciais, configuração PostgreSQL via variáveis
- ✅ v1.1: Migração PostgreSQL/Supabase concluída, sistema funcional no localhost
- ✅ v1.2: Deploy no Vercel realizado, sistema online com Pooler (IPv4)
- ✅ v1.3: Migração para Neon concluída, migrações executadas com sucesso (2026-05-07)

**Tecnologias Utilizadas:**
- Backend: Django 6.0.5, Python 3.12
- Banco: PostgreSQL (Neon, US East 1)
- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript (Chart.js)
- Deploy: Vercel (Serverless Python)
- PDF: ReportLab

---
*Relatório finalizado em 07/05/2026 — Versão v1.3 (Neon + Vercel 100% Operacional).*
