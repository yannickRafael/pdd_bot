import psycopg2
from database import get_db_connection
from utils import get_error_message

class Avaliacao_Service:

    def create_avaliacao(a_nome, a_code, a_caid, a_nota_max, a_created_by):
        a_code = a_code.strip().upper()
        """Create new assessment in the database."""
        db = get_db_connection()
        try:
            query = "SELECT * FROM create_avaliacao(CAST(%s AS VARCHAR), CAST(%s AS VARCHAR), %s, CAST(%s AS INTEGER), %s);"
            db.execute(query, (a_nome, a_code, a_caid, a_nota_max, a_created_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Avaliacao created successfully", 
                    "success": True,
                    "status": 201,
                    "data": result
                }
        except psycopg2.Error as e:
            db.connection.rollback()
            message, code = get_error_message(e.diag.message_detail)
            if code == 409:
                try:
                    db.connection.rollback()
                    get_id_query = "SELECT get_avaliacao(%s, %s);"
                    db.execute(get_id_query, (a_code, a_caid))
                    a_id = (db.fetchone()).get('get_avaliacao')
                    return Avaliacao_Service.update_avaliacao(a_id, a_nome, a_code, a_caid, a_nota_max, a_created_by)
                except Exception as ex:
                    print(str(ex))
                    db.connection.rollback()
                    return {
                        "message": "Could not update existing avaliacao.",
                        "success": False,
                        "status": 500,
                        "data": None
                    }
            else:
                db.connection.rollback()
                return {
                    "message": message,
                    "success": False,
                    "status": code,
                    "data": None
                }
        except Exception as e:
            print("error: "+str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }

    def update_avaliacao(a_id, a_nome, a_code, a_caid, a_nota_max, a_edited_by):
        """Update existing assessment in the database."""
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_avaliacao(%s, %s, %s, %s, %s, %s);"
            db.execute(query, (a_id, a_nome, a_code, a_caid, a_nota_max, a_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Avaliacao created successfully", 
                    "success": True,
                    "status": 201,
                    "data": result
                }
        except psycopg2.Error as e:
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }
        except Exception as e:
            print(str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }

    def delete_avaliacao(a_id, a_edited_by):
        """Delete existing assessment in the database."""
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_avaliacao(%s, %s);"
            db.execute(query, (a_id, a_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Avaliacao deleted successfully", 
                    "success": True,
                    "status": 201,
                    "data": result
                }
        except psycopg2.Error as e:
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }
        except Exception as e:
            print(str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }
           


