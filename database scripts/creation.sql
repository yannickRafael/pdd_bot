CREATE SEQUENCE IF NOT EXISTS e_estudante_seq;
CREATE TABLE IF NOT EXISTS e_estudante(
	row_id SERIAL PRIMARY KEY,
	e_id INTEGER NOT NULL DEFAULT nextval('e_estudante_seq')::INTEGER,

	e_nome VARCHAR(50) NOT NULL,
	e_code VARCHAR(50) NOT NULL,

	e_created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	e_created_by INTEGER DEFAULT 0,
	e_last_edited TIMESTAMPTZ,
	e_edited_by INTEGER,
	e_is_valid BOOLEAN DEFAULT TRUE
);
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_e_estudante
ON e_estudante(e_id) WHERE e_is_valid IS TRUE;

CREATE SEQUENCE IF NOT EXISTS cu_curso_seq;
CREATE TABLE IF NOT EXISTS cu_curso(
	row_id SERIAL PRIMARY KEY,
	cu_id INTEGER NOT NULL DEFAULT nextval('cu_curso_seq')::INTEGER,

	cu_nome VARCHAR(50) NOT NULL,
	cu_code VARCHAR(50) NOT NULL,

	cu_created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	cu_created_by INTEGER DEFAULT 0,
	cu_last_edited TIMESTAMPTZ,
	cu_edited_by INTEGER,
	cu_is_valid BOOLEAN DEFAULT TRUE
);
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_cu_curso
ON cu_curso(cu_id) WHERE cu_is_valid IS TRUE;
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_code_curso
ON cu_curso(cu_code) WHERE cu_is_valid IS TRUE;

CREATE SEQUENCE IF NOT EXISTS ca_cadeira_seq;
CREATE TABLE IF NOT EXISTS ca_cadeira(
	row_id SERIAL PRIMARY KEY,
	ca_id INTEGER NOT NULL DEFAULT nextval('ca_cadeira_seq')::INTEGER,

	ca_nome VARCHAR(50) NOT NULL,
	ca_code VARCHAR(50) NOT NULL,
	ca_cuid INTEGER NOT NULL,
	ca_link VARCHAR(100),

	ca_created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	ca_created_by INTEGER DEFAULT 0,
	ca_last_edited TIMESTAMPTZ,
	ca_edited_by INTEGER,
	ca_is_valid BOOLEAN DEFAULT TRUE
);
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_ca_cadeira
ON ca_cadeira(ca_id) WHERE ca_is_valid IS TRUE;
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_code_cadeira
ON ca_cadeira(ca_code) WHERE ca_is_valid IS TRUE;


CREATE SEQUENCE IF NOT EXISTS a_avaliacao_seq;
CREATE TABLE IF NOT EXISTS a_avaliacao(
	row_id SERIAL PRIMARY KEY,
	a_id INTEGER NOT NULL DEFAULT nextval('a_avaliacao_seq')::INTEGER,

	a_nome VARCHAR(50) NOT NULL,
	a_code VARCHAR(50) NOT NULL,
	a_caid INTEGER NOT NULL,
	a_nota_max INTEGER NOT NULL,

	a_created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	a_created_by INTEGER DEFAULT 0,
	a_last_edited TIMESTAMPTZ,
	a_edited_by INTEGER,
	a_is_valid BOOLEAN DEFAULT TRUE
);
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_a_avaliacao
ON a_avaliacao(a_id) WHERE a_is_valid IS TRUE;
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_code_avaliacao
ON a_avaliacao(a_code) WHERE a_is_valid IS TRUE;

CREATE SEQUENCE IF NOT EXISTS p_performance_seq;
CREATE TABLE IF NOT EXISTS p_performance(
	row_id SERIAL PRIMARY KEY,
	p_id INTEGER NOT NULL DEFAULT nextval('p_performance_seq')::INTEGER,

	p_nota INTEGER NOT NULL,
	p_eid INTEGER NOT NULL,
	p_aid INTEGER NOT NULL,

	p_created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	p_created_by INTEGER DEFAULT 0,
	p_last_edited TIMESTAMPTZ,
	p_edited_by INTEGER,
	p_is_valid BOOLEAN DEFAULT TRUE
);
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_p_performance
ON p_performance(p_id) WHERE p_is_valid IS TRUE;







