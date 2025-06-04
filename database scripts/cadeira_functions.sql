CREATE OR REPLACE FUNCTION create_cadeira(
    p_ca_nome VARCHAR,
    p_ca_code VARCHAR,
    p_ca_cuid INTEGER,
    p_ca_link VARCHAR DEFAULT NULL,
    p_ca_created_by INTEGER DEFAULT 0
)
RETURNS SETOF ca_cadeira AS $$
DECLARE
    v_ca_id INTEGER;
BEGIN
    IF p_ca_nome IS NULL THEN
        RAISE EXCEPTION 'ca_nome not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CA-NOME-MP';
    END IF;
    IF p_ca_code IS NULL THEN
        RAISE EXCEPTION 'ca_code not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CA-CODE-MP';
    END IF;
    IF p_ca_cuid IS NULL THEN
        RAISE EXCEPTION 'ca_cuid not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CU-ID-MP';
    END IF;

	IF EXISTS(
		SELECT 1 FROM ca_cadeira
		WHERE ca_code = p_ca_code AND ca_is_valid IS TRUE
	) THEN
		RAISE EXCEPTION 'A Subject with code: %, already exists', p_ca_code
	    USING ERRCODE = 'P0001', DETAIL = 'CA-AE';
	END IF;

	IF NOT EXISTS(
		SELECT 1 FROM cu_curso
		WHERE cu_id = p_ca_cuid AND cu_is_valid IS TRUE
	) THEN
		RAISE EXCEPTION 'cu_id not found or not valid: %', p_ca_cuid
		USING ERRCODE = 'P0001', DETAIL = 'CU-ID-NV';
	END IF;

    INSERT INTO ca_cadeira(ca_nome, ca_code, ca_cuid, ca_link, ca_created_by)
    VALUES(p_ca_nome, p_ca_code, p_ca_cuid, p_ca_link, p_ca_created_by)
    RETURNING ca_id INTO v_ca_id;

    RETURN QUERY SELECT * FROM ca_cadeira WHERE ca_id = v_ca_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_cadeira(
    p_ca_id INTEGER,
    p_ca_nome VARCHAR DEFAULT NULL,
    p_ca_code VARCHAR DEFAULT NULL,
    p_ca_cuid INTEGER DEFAULT NULL,
    p_ca_link VARCHAR DEFAULT NULL,
    p_ca_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF ca_cadeira AS $$
DECLARE
    v_ca_nome VARCHAR;
    v_ca_code VARCHAR;
    v_ca_cuid INTEGER;
    v_ca_link VARCHAR;
BEGIN
    IF p_ca_id IS NULL THEN
        RAISE EXCEPTION 'ca_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CA-ID-MP';
    END IF;


    IF NOT EXISTS(
        SELECT 1 FROM ca_cadeira
        WHERE ca_id = p_ca_id AND ca_is_valid IS TRUE
    ) THEN
        RAISE EXCEPTION 'ca_id not found or not valid: %', p_ca_id
		USING ERRCODE = 'P0001', DETAIL = 'CA-ID-NV';
    END IF;

	IF p_ca_cuid IS NOT NULL AND NOT EXISTS(SELECT 1 FROM cu_curso WHERE cu_id = p_ca_cuid AND cu_is_valid IS TRUE) THEN
		RAISE EXCEPTION 'cu_id not found or not valid: %', p_ca_cuid
		USING ERRCODE = 'P0001', DETAIL = 'CU-ID-NV';
	END IF;

	

    UPDATE ca_cadeira
    SET ca_is_valid = FALSE, ca_last_edited = NOW(), ca_edited_by = p_ca_edited_by
    WHERE ca_id = p_ca_id AND ca_is_valid IS TRUE
    RETURNING ca_nome, ca_code, ca_cuid, ca_link INTO v_ca_nome, v_ca_code, v_ca_cuid, v_ca_link;

    INSERT INTO ca_cadeira(ca_id, ca_nome, ca_code, ca_cuid, ca_link)
    VALUES(
		p_ca_id, 
		COALESCE(p_ca_nome, v_ca_nome), 
		COALESCE(p_ca_code, v_ca_code), 
		COALESCE(p_ca_cuid, v_ca_cuid), 
		COALESCE(p_ca_link, v_ca_link)
	);

    RETURN QUERY SELECT * FROM ca_cadeira
    WHERE ca_id = p_ca_id AND ca_is_valid IS TRUE;

EXCEPTION WHEN OTHERS THEN
	RAISE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_cadeira(
    p_ca_id INTEGER,
    p_ca_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF ca_cadeira AS $$
BEGIN
    IF p_ca_id IS NULL THEN
        RAISE EXCEPTION 'ca_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'CA-ID-MP';
    END IF;

    IF NOT EXISTS(
        SELECT 1 FROM ca_cadeira
        WHERE ca_id = p_ca_id AND ca_is_valid IS TRUE
    ) THEN
        RAISE EXCEPTION 'ca_id not found or not valid: %', p_ca_id
		USING ERRCODE = 'P0001', DETAIL = 'CA-ID-NV';
    END IF;

    UPDATE ca_cadeira
    SET ca_is_valid = FALSE, ca_last_edited = NOW(), ca_edited_by = p_ca_edited_by
    WHERE ca_id = p_ca_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;
END;
$$ LANGUAGE plpgsql;
