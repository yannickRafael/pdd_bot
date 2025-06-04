import psycopg2
from database import get_db_connection
from flask import jsonify
from utils.utils import get_error_message

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
            return jsonify({
                    "message": "Cadeira created successfully", 
                    "success": True,
                    "status": 201,
                    "data": result
                }), 201
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
        
    def update_cadeira(ca_id, ca_nome, ca_code, ca_cuid, ca_link, ca_edited_by):

        """Update an existing curso in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_cadeira(%s, %s, %s, %s, %s, %s);"
            db.execute(query, (ca_id, ca_nome, ca_code, ca_cuid, ca_link, ca_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Cadeira updated successfully", 
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
        
    def delete_cadeira(ca_id, ca_edited_by):
        """Delete an existing curso in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_cadeira(%s, %s);"
            db.execute(query, (ca_id, ca_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Cadeira deleted successfully", 
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
        
  