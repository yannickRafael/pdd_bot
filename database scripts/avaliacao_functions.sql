CREATE OR REPLACE FUNCTION get_avaliacao(p_a_code VARCHAR)
RETURNS INTEGER AS $$
DECLARE
    v_a_id INTEGER;
BEGIN
    IF p_a_code IS NULL THEN
        RAISE EXCEPTION 'a_code not provided'
        USING ERRCODE = 'P0001', DETAIL = 'A-CODE-MP';
    END IF;

    SELECT a_id INTO v_a_id FROM a_avaliacao
    WHERE a_code = p_a_code AND a_is_valid IS TRUE;

    IF v_a_id IS NULL THEN
        RAISE EXCEPTION 'a_code not found or not valid: %', p_a_code
        USING ERRCODE = 'P0001', DETAIL = 'A-CODE-NF';
    END IF;

    RETURN v_a_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_avaliacao(
    p_a_nome VARCHAR,
    p_a_code VARCHAR,
    p_a_caid INTEGER,
    p_a_nota_max INTEGER,
    p_a_created_by INTEGER DEFAULT 0
)
RETURNS SETOF a_avaliacao AS $$
DECLARE
    v_a_id INTEGER;
BEGIN
    IF p_a_nome IS NULL THEN
        RAISE EXCEPTION 'a_nome not provided'
		USING ERRCODE = 'P0001', DETAIL = 'A-NOME-MP';
    END IF;
    IF p_a_code IS NULL THEN
        RAISE EXCEPTION 'a_code not provided'
		USING ERRCODE = 'P0001', DETAIL = 'A-CODE-MP';
    END IF;
    IF p_a_caid IS NULL THEN
        RAISE EXCEPTION 'a_caid not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CA-ID-MP';
    END IF;
    IF p_a_nota_max IS NULL THEN
        RAISE EXCEPTION 'a_nota_max not provided'
		USING ERRCODE = 'P0001', DETAIL = 'A-NOTAMAX-MP';
    END IF;

	IF EXISTS(
		SELECT 1 FROM a_avaliacao
		WHERE a_code = p_a_code AND a_is_valid IS TRUE
	) THEN 
		RAISE EXCEPTION 'An Assessment with code: %, already exists', p_a_code
	    USING ERRCODE = 'P0001', DETAIL = 'A-AE';
	END IF;

    IF NOT EXISTS (
		SELECT 1 FROM ca_cadeira 
		WHERE ca_id = p_a_caid AND ca_is_valid IS TRUE
	) THEN
        RAISE EXCEPTION 'ca_id % not found or not valid', a_caid
		USING ERRCODE = 'P0001', DETAIL = 'CA-ID-NV';
    END IF;

    INSERT INTO a_avaliacao(a_nome, a_code, a_caid, a_nota_max, a_created_by)
    VALUES(p_a_nome, p_a_code, p_a_caid, p_a_nota_max, p_a_created_by)
    RETURNING a_id INTO v_a_id;

    RETURN QUERY SELECT * FROM a_avaliacao WHERE a_id = v_a_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_avaliacao(
    p_a_id INTEGER,
    p_a_nome VARCHAR DEFAULT NULL,
	p_a_code VARCHAR DEFAULT NULL,
    p_a_caid INTEGER DEFAULT NULL,
    p_a_nota_max INTEGER DEFAULT NULL,
    p_a_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF a_avaliacao AS $$
DECLARE
    V_a_nome VARCHAR;
	V_a_code VARCHAR;
    V_a_caid INTEGER;
    V_a_nota_max INTEGER;
BEGIN
    IF p_a_id IS NULL THEN
        RAISE EXCEPTION 'a_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'A-ID-MP';
    END IF;


    IF NOT EXISTS (
		SELECT 1 FROM a_avaliacao 
		WHERE a_id = p_a_id AND a_is_valid IS TRUE
	) THEN
        RAISE EXCEPTION 'a_id % not found or not valid', p_a_id
		USING ERRCODE = 'P0001', DETAIL = 'A-ID-NV';
    END IF;

    IF p_a_caid IS NOT NULL AND NOT EXISTS (
		SELECT 1 FROM ca_cadeira 
		WHERE ca_id = p_a_caid AND ca_is_valid IS TRUE
	) THEN
        RAISE EXCEPTION 'ca_id % not found or not valid', p_a_caid
		USING ERRCODE = 'P0001', DETAIL = 'CA-ID-NV';
    END IF;

    UPDATE a_avaliacao
    SET a_is_valid = FALSE, a_last_edited = NOW(), a_edited_by = p_a_edited_by
    WHERE a_id = p_a_id  AND a_is_valid IS TRUE
    RETURNING a_nome, a_code, a_caid, a_nota_max INTO v_a_nome, v_a_code, v_a_caid, v_a_nota_max;

    INSERT INTO a_avaliacao(a_id, a_nome, a_code, a_caid, a_nota_max)
    VALUES(
		p_a_id, 
		COALESCE(p_a_nome, v_a_nome), 
		COALESCE(p_a_code, v_a_code), 
		COALESCE(p_a_caid, v_a_caid), 
		COALESCE(p_a_nota_max, v_a_nota_max)
	);

    RETURN QUERY SELECT * FROM a_avaliacao WHERE a_id = p_a_id AND a_is_valid IS TRUE;

EXCEPTION WHEN OTHERS THEN
	RAISE;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_avaliacao(
    p_a_id INTEGER,
    p_a_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF a_avaliacao AS $$
BEGIN
    IF p_a_id IS NULL THEN
        RAISE EXCEPTION 'a_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'A-ID-MP';
    END IF;

    IF NOT EXISTS (
		SELECT 1 FROM a_avaliacao 
		WHERE a_id = p_a_id AND a_is_valid IS TRUE
	) THEN
        RAISE EXCEPTION 'a_id % not found or not valid', p_a_id
		USING ERRCODE = 'P0001', DETAIL = 'A-ID-NV';
    END IF;

    UPDATE a_avaliacao
    SET a_is_valid = FALSE, a_last_edited = NOW(), a_edited_by = p_a_edited_by
    WHERE a_id = p_a_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;
END;
$$ LANGUAGE plpgsql;

--DROP FUNCTION create_avaliacao(character varying,character varying,integer,integer,integer)