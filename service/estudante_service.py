import psycopg2
from database import get_db_connection
from utils import get_error_message
class Estudante_Service:
    
    def create_estudante(e_nome, e_code, e_created_by):

        """Create a new estudante in the database."""

        db = get_db_connection()
        try:
            query = "SELECT * FROM create_estudante(%s, %s, %s);"
            db.execute(query, (e_nome, e_code, e_created_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Estudante created successfully", 
                    "success": True,
                    "status": 201,
                    "data": result
                }
        except psycopg2.Error as e:
            message, code = get_error_message(e.diag.message_detail)
            if code == 409:
                try:
                    get_id_query = "SELECT get_estudante(%s);"
                    db.execute(get_id_query, (e_code,))
                    e_id = (db.fetchone()).get('get_estudante')
                    return Estudante_Service.update_estudante(e_id, e_nome, e_code, e_created_by)
                except Exception as ex:
                    print(str(ex))
                    db.connection.rollback()
                    return {
                        "message": "Could not update existing estudante.",
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
        
    def update_estudante(e_id, e_nome, e_code, e_edited_by):
        """Update an existing estudante in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_estudante(%s, %s, %s, %s);"
            db.execute(query, (e_id, e_nome, e_code, e_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Estudante updated successfully", 
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
        
    def delete_estudante(e_id, e_edited_by):
        """Delete an existing estudante in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_estudante(%s, %s);"
            db.execute(query, (e_id, e_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Estudante deleted successfully", 
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