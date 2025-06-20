import psycopg2
from database import get_db_connection
from utils import get_error_message

class Curso_Service:
    
    def create_curso(cu_nome, cu_code, cu_created_by=0):
        cu_code = cu_code.strip().upper()

        """Create a new curso in the database."""

        db = get_db_connection()
        try:
            query = "SELECT * FROM create_curso(%s, %s, %s);"
            db.execute(query, (cu_nome, cu_code, cu_created_by))
            result = db.fetchone()
            db.connection.commit()
            return {
                    "message": "Curso created successfully", 
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
                    get_id_query = "SELECT get_curso(%s);"
                    db.execute(get_id_query, (cu_code,))
                    cu_id = (db.fetchone()).get('get_curso')
                    return Curso_Service.update_curso(cu_id, cu_nome, cu_code, cu_created_by)
                except Exception as ex:
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
            message, code = get_error_message("")
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }
        
    def update_curso(cu_id, cu_nome, cu_code, cu_edited_by):
        """Update an existing curso in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_curso(%s, %s, %s, %s);"
            db.execute(query, (cu_id, cu_nome, cu_code, cu_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Curso updated successfully", 
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
        
    def delete_curso(cu_id, cu_edited_by):
        """Delete an existing curso in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_curso(%s, %s);"
            db.execute(query, (cu_id, cu_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Curso deleted successfully", 
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