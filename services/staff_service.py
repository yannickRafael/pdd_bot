from database import get_db_connection

def create_staff(data):
    try:
        conn = get_db_connection()
        conn.execute("""
                SELECT create_staff(
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::INTEGER,
                    %s::BOOLEAN,
                    %s::INTEGER,
                    %s::INTEGER,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR,
                    %s::VARCHAR
                )
            """,(
                data["pn_operator"],
                data["pn_phone"],
                data["p_name"],
                data["s_role"],
                data.get("p_first_name"),
                data.get("p_middle_name"),
                data.get("p_last_name"),
                data.get("p_email"),
                data.get("p_address"),
                data.get("p_age"),
                data.get("pn_has_whatsapp", False),
                data.get("s_created_by", 0),
                data.get("s_prid"),
                data.get("pr_name"),
                data.get("pr_email"),
                data.get("pr_nuit"),
                data.get("pr_address")
            )
        )
        result = conn.fetchone()
        conn.connection.commit()
        conn.close()
        return {"status": "success", "message": result["create_staff"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def view_staff_service(searcher_id, promoter_id, target_staff_id=None):
    try:
        conn = get_db_connection()
        conn.execute("SELECT * FROM view_staff(%s, %s, %s)", (searcher_id, promoter_id, target_staff_id))
        result = conn.fetchall()
        conn.close()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
