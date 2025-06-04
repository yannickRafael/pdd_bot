from flask import jsonify
import psycopg2
from database import get_db_connection
from utils import get_error_message

class Performance_Service:

    def create_performance(p_nota, p_eid, p_aid, p_created_by):
        """Create new performance in the database."""

        db = get_db_connection()
        try:
            query = "SELECT * FROM create_performance(%s, %s, %s, %s);"
            db.execute(query, (p_nota, p_eid, p_aid, p_created_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Performance created successfully", 
                    "success": True,
                    "status": 201,
                    "data": result
                }), 201
        except psycopg2.Error as e:
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            if code == 409:
                return Performance_Service.update_performance(None, p_nota, p_created_by)
            else:
                db.connection.rollback()
                return jsonify({
                    "message": message,
                    "success": False,
                    "status": code,
                    "data": None
                }), code
        except Exception as e:
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            db.connection.rollback()
            return jsonify({
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }), code
        
    def update_performance(p_id, p_nota, p_edited_by):
        """Update existing performance in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_performance(%s, %s, %s);"
            db.execute(query, (p_id, p_nota, p_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Performance updated successfully", 
                    "success": True,
                    "status": 200,
                    "data": result
                }), 200
        except psycopg2.Error as e:
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            db.connection.rollback()
            return jsonify({
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }), code
        except Exception as e:
            print(str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return jsonify({
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }), code
    
    def delete_performance(p_id, p_edited_by):
        """Delete existing performance in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_performance(%s, %s);"
            db.execute(query, (p_id, p_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Performance deleted successfully", 
                    "success": True,
                    "status": 200,
                    "data": result
                }), 200
        except psycopg2.Error as e:
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            db.connection.rollback()
            return jsonify({
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }), code
        except Exception as e:
            print(str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return jsonify({
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }), code