CREATE OR REPLACE FUNCTION get_estudante(
    p_e_code VARCHAR
)
RETURNS INTEGER AS $$
DECLARE
    v_e_id INTEGER;
BEGIN
    IF p_e_code IS NULL THEN
        RAISE EXCEPTION 'e_code not provided'
        USING ERRCODE = 'P0001', DETAIL = 'E-CODE-MP';
    END IF;

    SELECT e_id INTO v_e_id
    FROM e_estudante
    WHERE e_code = p_e_code AND e_is_valid IS TRUE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'e_code % not found or not valid', p_e_code
        USING ERRCODE = 'P0001', DETAIL = 'E-CODE-NV';
    END IF;

    RETURN v_e_id;

EXCEPTION WHEN OTHERS THEN
    RAISE;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_estudante(
	p_e_nome VARCHAR,
	p_e_code VARCHAR,
	p_e_created_by INTEGER DEFAULT 0
)
RETURNS SETOF e_estudante AS $$
DECLARE 
	v_e_id INTEGER;
BEGIN
	IF p_e_nome IS NULL THEN
		RAISE EXCEPTION 'e_nome not provided'
		USING ERRCODE = 'P0001', DETAIL = 'E-NOME-MP';
	END IF;
	IF p_e_code IS NULL THEN
		RAISE EXCEPTION 'e_code not provided'
		USING ERRCODE = 'P0001', DETAIL = 'E-CODE-MP';
	END IF;

	IF EXISTS (
	    SELECT 1 FROM e_estudante
	    WHERE e_code = p_e_code AND e_is_valid IS TRUE
	) THEN
	    RAISE EXCEPTION 'A Student with code: %, already exists', p_e_code
	    USING ERRCODE = 'P0001', DETAIL = 'E-AE';
	END IF;


	INSERT INTO e_estudante(e_nome, e_code, e_created_by)
	VALUES(p_e_nome, p_e_code, p_e_created_by)
	RETURNING e_id INTO v_e_id;

	RETURN QUERY SELECT * FROM e_estudante e WHERE e.e_id = v_e_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;	
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_estudante(
	p_e_id INTEGER,
	p_e_nome VARCHAR,
	p_e_code VARCHAR,
	p_e_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF e_estudante AS $$
DECLARE 
	v_e_nome VARCHAR;
	v_e_code VARCHAR;
BEGIN
	IF p_e_id IS NULL THEN
		RAISE EXCEPTION 'e_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'E-ID-MP';
	END IF;
	

	IF NOT EXISTS(
		SELECT 1 FROM e_estudante
		WHERE e_id = p_e_id AND e_is_valid IS TRUE
	) THEN
		RAISE EXCEPTION 'e_id not found or not valid: %', p_e_id
		USING ERRCODE = 'P0001', DETAIL = 'E-ID-NV';
	END IF;

	UPDATE e_estudante
	SET e_is_valid = FALSE, e_last_edited = NOW(), e_edited_by = p_e_edited_by
	WHERE e_id = p_e_id AND e_is_valid IS TRUE
	RETURNING e_nome, e_code INTO v_e_nome, v_e_code;

	INSERT INTO e_estudante(e_id, e_nome, e_code)
	VALUES(p_e_id, COALESCE(p_e_nome, v_e_nome ), COALESCE(p_e_code, v_e_code));

	RETURN QUERY SELECT * FROM e_estudante
	WHERE e_id = p_e_id AND e_is_valid IS TRUE;
	
EXCEPTION WHEN OTHERS THEN
	RAISE;	
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_estudante(
	p_e_id INTEGER,
	p_e_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF e_estudante AS $$
BEGIN
	IF p_e_id IS NULL THEN
		RAISE EXCEPTION 'e_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'E-ID-MP';
	END IF;

	IF NOT EXISTS(
		SELECT 1 FROM e_estudante
		WHERE e_id = p_e_id AND e_is_valid IS TRUE
	) THEN
		RAISE EXCEPTION 'e_id not found or not valid: %', p_e_id
		USING ERRCODE = 'P0001', DETAIL = 'E-ID-NV';
	END IF;
	
	UPDATE e_estudante
	SET e_is_valid = FALSE, e_last_edited = NOW(), e_edited_by = p_e_edited_by
	WHERE e_id = p_e_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;	
END;
$$ LANGUAGE plpgsql;

--DROP FUNCTION update_estudante(integer,character varying,integer)