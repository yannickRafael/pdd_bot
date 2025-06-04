import psycopg2
from database import get_db_connection
from flask import jsonify
from utils.utils import get_error_message

class Curso_Service:
    
    def create_curso(cu_nome, cu_code, cu_created_by):

        """Create a new curso in the database."""

        db = get_db_connection()
        try:
            query = "SELECT * FROM create_curso(%s, %s, %s);"
            db.execute(query, (cu_nome, cu_code, cu_created_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Curso created successfully", 
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
        
    def update_curso(cu_id, cu_nome, cu_code, cu_edited_by):
        """Update an existing curso in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_curso(%s, %s, %s, %s);"
            db.execute(query, (cu_id, cu_nome, cu_code, cu_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Curso updated successfully", 
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
        
    def delete_curso(cu_id, cu_edited_by):
        """Delete an existing curso in the database."""
        
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_curso(%s, %s);"
            db.execute(query, (cu_id, cu_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Curso deleted successfully", 
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