-- Criar superusuário admin no Neon (Django)
-- Execute este SQL no Neon SQL Editor

-- Inserir/Atualizar usuário admin
INSERT INTO auth_user (
    id,
    password,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    1,
    'pbkdf2_sha256$120000$czJB9TTAyUI9UeAnPNgMPl$pH+DKKuVZ69El/ZlejHV8AFANFVs8IEj1mmSCL3ndig=',
    TRUE,
    'admin',
    '',
    '',
    'admin@sgo.com',
    TRUE,
    TRUE,
    NOW()
) ON CONFLICT (id) DO UPDATE SET
    password = EXCLUDED.password,
    is_superuser = TRUE,
    is_staff = TRUE;

-- Verificar se foi criado
SELECT id, username, is_superuser, is_staff FROM auth_user WHERE username = 'admin';
