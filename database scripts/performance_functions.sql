CREATE OR REPLACE FUNCTION create_performance(
    p_p_nota INTEGER,
    p_p_eid INTEGER,
    p_p_aid INTEGER,
    p_p_created_by INTEGER DEFAULT 0
)
RETURNS SETOF p_performance AS $$
DECLARE
    v_p_id INTEGER;
BEGIN
    IF p_p_nota IS NULL THEN
        RAISE EXCEPTION 'p_nota not provided'
		USING ERRCODE = 'P0001', DETAIL = 'P-NOTA-MP';
    END IF;
    IF p_p_eid IS NULL THEN
        RAISE EXCEPTION 'p_eid not provided'
		USING ERRCODE = 'P0001', DETAIL = 'E-ID-MP';
    END IF;
    IF p_p_aid IS NULL THEN
        RAISE EXCEPTION 'p_aid not provided'
		USING ERRCODE = 'P0001', DETAIL = 'A-ID-MP';
    END IF;

    IF NOT EXISTS (
		SELECT 1 FROM e_estudante 
		WHERE e_id = p_p_eid AND e_is_valid IS TRUE
	) THEN
        RAISE EXCEPTION 'e_id % not found or not valid', p_eid
		USING ERRCODE = 'P0001', DETAIL = 'E-ID-NV';
    END IF;

    IF NOT EXISTS (
		SELECT 1 FROM a_avaliacao 
		WHERE a_id = p_p_aid AND a_is_valid IS TRUE
	) THEN
        RAISE EXCEPTION 'a_id % not found or not valid', p_aid
		USING ERRCODE = 'P0001', DETAIL = 'A-ID-NV';
    END IF;

	IF (
		SELECT a_nota_max FROM a_avaliacao 
		WHERE a_id = p_p_aid AND a_is_valid
	) < p_p_nota THEN
		RAISE EXCEPTION 'The provided score(%) is higher than the assesment max score',p_p_nota
		USING ERRCODE = 'P0001', DETAIL = 'P-NOTA-NV';
	END IF;

    INSERT INTO p_performance(p_nota, p_eid, p_aid, p_created_by)
    VALUES(p_p_nota, p_p_eid, p_p_aid, p_p_created_by)
    RETURNING p_id INTO v_p_id;

    RETURN QUERY SELECT * FROM p_performance WHERE p_id = v_p_id;

EXCEPTION WHEN OTHERS THEN
	RAISE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_performance(
    p_p_id INTEGER,
    p_p_nota INTEGER,
    p_p_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF p_performance AS $$
DECLARE
	v_a_id INTEGER;
	V_a_nota_max INTEGER;
DECLARE
	v_p_eid INTEGER; 
	v_p_aid INTEGER;
BEGIN
    IF p_p_id IS NULL THEN
        RAISE EXCEPTION 'p_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'P-ID-MP';
    END IF;
    IF p_p_nota IS NULL THEN
        RAISE EXCEPTION 'p_nota not provided'
		USING ERRCODE = 'P0001', DETAIL = 'P-NOTA-MP';
    END IF;

    IF NOT EXISTS (
		SELECT 1 FROM p_performance 
		WHERE p_id = p_p_id AND p_is_valid IS TRUE
	) THEN
        RAISE EXCEPTION 'p_id % not found or not valid', p_p_id
		USING ERRCODE = 'P0001', DETAIL = 'P-ID-NV';
    END IF;

	SELECT a_id, a_nota_max INTO v_a_id, v_a_nota_max FROM p_performance
	JOIN a_avaliacao ON a_id = p_aid;
	

    IF v_a_nota_max < p_p_nota THEN
		RAISE EXCEPTION 'The provided score(%) is higher than the assesment max score',p_p_nota
		USING ERRCODE = 'P0001', DETAIL = 'P-NOTA-NV';
	END IF;

    UPDATE p_performance
    SET p_is_valid = FALSE, p_last_edited = NOW(), p_edited_by = p_p_edited_by
    WHERE p_id = p_p_id AND p_is_valid IS TRUE
	RETURNING p_eid, p_aid INTO v_p_eid, v_p_aid;

    INSERT INTO p_performance(p_id, p_nota, p_eid, p_aid)
    VALUES(p_p_id, p_p_nota, v_p_eid, v_p_aid);

    RETURN QUERY SELECT * FROM p_performance
    WHERE p_id = p_p_id AND p_is_valid IS TRUE;

EXCEPTION WHEN OTHERS THEN
	RAISE;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_performance(
    p_p_id INTEGER,
    p_p_edited_by INTEGER DEFAULT 0
)
RETURNS SETOF p_performance AS $$
BEGIN
    IF p_p_id IS NULL THEN
        RAISE EXCEPTION 'p_id not provided'
		USING ERRCODE = 'P0001', DETAIL = 'P-ID-MP';
    END IF;

    IF NOT EXISTS (
		SELECT 1 FROM p_performance 
		WHERE p_id = p_p_id AND p_is_valid IS TRUE
	) THEN
        RAISE EXCEPTION 'p_id % not found or not valid', p_p_id
		USING ERRCODE = 'P0001', DETAIL = 'P-ID-NV';
    END IF;

    UPDATE p_performance
    SET p_is_valid = FALSE, p_last_edited = NOW(), p_edited_by = p_p_edited_by
    WHERE p_id = p_p_id;


EXCEPTION WHEN OTHERS THEN
	 RAISE;
END;
$$ LANGUAGE plpgsql;

--DROP FUNCTION create_performance(integer,integer,integer,integer)