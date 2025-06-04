CREATE OR REPLACE FUNCTION get_curso(p_cu_code VARCHAR)
RETURNS INTEGER AS $$
DECLARE
    v_cu_id INTEGER;
BEGIN
    IF p_cu_code IS NULL THEN
        RAISE EXCEPTION 'cu_code not provided'
        USING ERRCODE = 'P0001', DETAIL = 'CU-CODE-MP';
    END IF;

    SELECT cu_id INTO v_cu_id FROM cu_curso
    WHERE cu_code = p_cu_code AND cu_is_valid IS TRUE;

    IF v_cu_id IS NULL THEN
        RAISE EXCEPTION 'cu_code not found or not valid: %', p_cu_code
        USING ERRCODE = 'P0001', DETAIL = 'CU-CODE-NF';
    END IF;

    RETURN v_cu_id;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION create_curso(
    p_cu_nome VARCHAR,
    p_cu_code VARCHAR,
    p_cu_created_by INTEGER DEFAULT 0
)
RETURNS SETOF cu_curso AS $$
DECLARE
	v_cu_id INTEGER;
BEGIN
    IF p_cu_nome IS NULL THEN
        RAISE EXCEPTION 'cu_nome not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CU-NOME-MP';
    END IF;
    IF p_cu_code IS NULL THEN
        RAISE EXCEPTION 'cu_code not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CU-CODE-MP';
    END IF;

	IF EXISTS(
		SELECT 1 FROM cu_curso
		WHERE cu_code = p_cu_code AND cu_is_valid IS TRUE
	) THEN
		RAISE EXCEPTION 'A Course with code: %, already exists', p_cu_code
	    USING ERRCODE = 'P0001', DETAIL = 'CU-AE';
	END IF;

    INSERT INTO cu_curso(cu_nome, cu_code, cu_created_by)
    VALUES(p_cu_nome, p_cu_code, p_cu_created_by)
    RETURNING cu_id INTO v_cu_id;

    RETURN QUERY 
	SELECT * FROM cu_curso WHERE cu_id = v_cu_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;	
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_curso(
    p_cu_id INTEGER,
    p_cu_nome VARCHAR,
	p_cu_code VARCHAR,
    p_cu_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF cu_curso AS $$
DECLARE
    v_cu_nome VARCHAR;
    v_cu_code VARCHAR;
BEGIN
    IF p_cu_id IS NULL THEN
        RAISE EXCEPTION 'cu_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CU-ID-MP';
    END IF;

    IF NOT EXISTS(
        SELECT 1 FROM cu_curso
        WHERE cu_id = p_cu_id AND cu_is_valid IS TRUE
    ) THEN
        RAISE EXCEPTION 'cu_id not found or not valid: %', p_cu_id
		USING ERRCODE = 'P0001', DETAIL = 'CU-ID-NV';
    END IF;

    UPDATE cu_curso
    SET cu_is_valid = FALSE, cu_last_edited = NOW(), cu_edited_by = p_cu_edited_by
    WHERE cu_id = p_cu_id AND cu_is_valid IS TRUE
    RETURNING cu_nome, cu_code INTO v_cu_nome, v_cu_code;

    INSERT INTO cu_curso(cu_id, cu_nome, cu_code)
    VALUES(p_cu_id, COALESCE(p_cu_nome, v_cu_nome) , COALESCE(p_cu_code, v_cu_code));

    RETURN QUERY SELECT * FROM cu_curso
    WHERE cu_id = p_cu_id AND cu_is_valid IS TRUE;

EXCEPTION WHEN OTHERS THEN
	RAISE;		
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_curso(
    p_cu_id INTEGER,
    p_cu_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF cu_curso AS $$
BEGIN
    IF p_cu_id IS NULL THEN
        RAISE EXCEPTION 'cu_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CU-ID-MP';
    END IF;

    IF NOT EXISTS(
        SELECT 1 FROM cu_curso
        WHERE cu_id = p_cu_id AND cu_is_valid IS TRUE
    ) THEN
        RAISE EXCEPTION 'cu_id not found or not valid: %', p_cu_id
		USING ERRCODE = 'P0001', DETAIL = 'CU-ID-NV';
    END IF;

    UPDATE cu_curso
    SET cu_is_valid = FALSE, cu_last_edited = NOW(), cu_edited_by = p_cu_edited_by
    WHERE cu_id = p_cu_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;	
END;
$$ LANGUAGE plpgsql;

-- DROP FUNCTION create_curso(character varying,character varying,integer)
