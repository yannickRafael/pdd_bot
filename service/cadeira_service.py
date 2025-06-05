import psycopg2
from database import get_db_connection
from utils import get_error_message

class Cadeira_Service:

    def create_cadeira(ca_nome, ca_code, ca_cuid, ca_link, ca_created_by):
        """Create new cadeira in the database"""
        db = get_db_connection()
        try:
            query = "SELECT * FROM create_cadeira(%s, %s, %s, %s, %s);"
            db.execute(query, (ca_nome, ca_code, ca_cuid, ca_link, ca_created_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Cadeira created successfully", 
                    "success": True,
                    "status": 201,
                    "data": result
                }
        except psycopg2.Error as e:
            db.connection.rollback()
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            if code == 409:
                try:
                    db.connection.rollback()
                    get_id_query = "SELECT get_cadeira(%s);"
                    db.execute(get_id_query, (ca_code,))
                    ca_id = (db.fetchone()).get('get_cadeira')
                    print('DEBUG: Cadeira ID:', ca_id)
                    return Cadeira_Service.update_cadeira(ca_id, ca_nome, ca_code, ca_cuid, ca_link, ca_created_by)
                except Exception as ex:
                    print("DEBUG: EXCEPTION:", str(ex))
                    db.connection.rollback()
                    return {
                        "message": "Could not update existing curso.",
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
            print(str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }
        
    def update_cadeira(ca_id, ca_nome, ca_code, ca_cuid, ca_link, ca_edited_by):

        """Update an existing curso in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_cadeira(%s, %s, %s, %s, %s, %s);"
            db.execute(query, (ca_id, ca_nome, ca_code, ca_cuid, ca_link, ca_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Cadeira updated successfully", 
                    "success": True,
                    "status": 200,
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
        
    def delete_cadeira(ca_id, ca_edited_by):
        """Delete an existing curso in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_cadeira(%s, %s);"
            db.execute(query, (ca_id, ca_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Cadeira deleted successfully", 
                    "success": True,
                    "status": 200,
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
        

