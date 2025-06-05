import psycopg2
from database import get_db_connection
from utils import get_error_message

class Performance_Service:

    def create_performance(p_nota, p_eid, p_aid, p_created_by):
        """Create new performance in the database."""

        db = get_db_connection()
        try:
            print("DEBUG: p_nota", p_nota)
            print("DEBUG: p_eid", p_eid)
            print("DEBUG: p_aid", p_aid)
            print("DEBUG: p_created_by", p_created_by)
            
            query = "SELECT * FROM create_performance(CAST(%s AS INTEGER), CAST(%s AS INTEGER), CAST(%s AS INTEGER), CAST(%s AS INTEGER));"
            db.execute(query, (p_nota, p_eid, p_aid, p_created_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Performance created successfully", 
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
                    get_id_query = "SELECT get_performance(%s, %s);"
                    db.execute(get_id_query, (p_eid, p_aid))
                    p_id = (db.fetchone()).get('get_performance')
                    return Performance_Service.update_performance(p_id, p_nota, p_created_by)
                except Exception as ex:
                    db.connection.rollback()
                    return {
                        "message": "Could not update existing curso.",
                        "success": False,
                        "status": str(ex),
                        "data": str(ex)
                    }
            else:
                db.connection.rollback()
                return {
                    "message": message,
                    "success": False,
                    "status": code,
                    "data": str(e)
                }
        except Exception as e:
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": str(e)
            }
        
    def update_performance(p_id, p_nota, p_edited_by):
        """Update existing performance in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_performance(%s, %s, %s);"
            db.execute(query, (p_id, p_nota, p_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Performance updated successfully", 
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
                "data": str(e)
            }
        except Exception as e:
            print(str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": str(e)
            }
    
    def delete_performance(p_id, p_edited_by):
        """Delete existing performance in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_performance(%s, %s);"
            db.execute(query, (p_id, p_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return {
                    "message": "Performance deleted successfully", 
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
                "data": str(e)
            }
        except Exception as e:
            print(str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return {
                "message": message,
                "success": False,
                "status": code,
                "data": str(e)
            }