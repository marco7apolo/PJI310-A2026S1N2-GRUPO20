-- Schema inicial para Neon (SGO)
-- Execute este SQL no Neon SQL Editor antes do primeiro deploy

-- 1. Criar superusuário admin (senha: admin1234xrl)
INSERT INTO auth_user (
    id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
) VALUES (
    1,
    'pbkdf2_sha256$120000$czJB9TTAyUI9UeAnPNgMPl$pH+DKKuVZ69El/ZlejHV8AFANFVs8IEj1mmSCL3ndig=',
    TRUE, 'admin', '', '', 'admin@sgo.com', TRUE, TRUE, NOW()
) ON CONFLICT (id) DO UPDATE SET
    password = EXCLUDED.password,
    is_superuser = TRUE,
    is_staff = TRUE;

-- 2. Verificar
SELECT id, username, is_superuser, is_staff FROM auth_user WHERE username = 'admin';

-- 3. (Opcional) Criar dados de exemplo
-- Clientes
INSERT INTO reparo_cliente (id_cliente, nome, cep, endereco, telefone) VALUES
(1, 'Cliente Exemplo', '01310-100', 'Av. Paulista, 1578, São Paulo, SP', '(11) 99999-9999')
ON CONFLICT DO NOTHING;

-- Técnicos
INSERT INTO reparo_tecnico (id_tecnico, nome) VALUES
(1, 'Técnico Exemplo')
ON CONFLICT DO NOTHING;

-- Equipamentos
INSERT INTO reparo_equipamento (id_equipamento, id_cliente_id, tipo, marca, modelo, numero_serial) VALUES
(1, 1, 'CELULAR', 'SAMSUNG', 'Galaxy S21', 'SN123456789')
ON CONFLICT DO NOTHING;

-- Reparos
INSERT INTO reparo_reparo (id_reparo, id_equipamento_id, id_tecnico_id, data_entrada, data_saida, descricao_defeito, descricao_reparo, pecas_substituidas, custo_reparo) VALUES
(1, 1, 1, '2026-05-01', '2026-05-07', 'Tela quebrada', 'Troca de tela', 'Tela OLED', 500.00)
ON CONFLICT DO NOTHING;
