from flask import jsonify
import psycopg2
from database import get_db_connection
from utils import get_error_message

class Avaliacao_Service:

    def create_avaliacao(a_nome, a_code, a_caid, a_nota_max, a_created_by):
        """Create new assessment in the database."""
        db = get_db_connection()
        try:
            query = "SELECT * FROM create_avaliacao(%s, %s, %s, %s, %s);"
            db.execute(query, (a_nome, a_code, a_caid, a_nota_max, a_created_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Avaliacao created successfully", 
                    "success": True,
                    "status": 201,
                    "data": result
                }), 201
        except psycopg2.Error as e:
            print(str(e))
            message, code = get_error_message(e.diag.message_detail)
            if code == 409:
                try:
                    get_id_query = "SELECT get_avaliacao(%s);"
                    db.execute(get_id_query, (a_code,))
                    a_id = db.fetchone()[0]
                    return Avaliacao_Service.update_avaliacao(a_id, a_nome, a_code, a_caid, a_nota_max, a_created_by)
                except Exception as ex:
                    print(str(ex))
                    db.connection.rollback()
                    return jsonify({
                        "message": "Could not update existing avaliacao.",
                        "success": False,
                        "status": 500,
                        "data": None
                    }), 500
            else:
                db.connection.rollback()
                return jsonify({
                    "message": message,
                    "success": False,
                    "status": code,
                    "data": None
                }), code
        except Exception as e:
            print("error: "+str(e))
            message, code = get_error_message("")
            db.connection.rollback()
            return jsonify({
                "message": message,
                "success": False,
                "status": code,
                "data": None
            }), code

    def update_avaliacao(a_id, a_nome, a_code, a_caid, a_nota_max, a_edited_by):
        """Update existing assessment in the database."""
        db = get_db_connection()
        try:
            query = "SELECT * FROM update_avaliacao(%s, %s, %s, %s, %s, %s);"
            db.execute(query, (a_id, a_nome, a_code, a_caid, a_nota_max, a_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Avaliacao created successfully", 
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

    def delete_avaliacao(a_id, a_edited_by):
        """Delete existing assessment in the database."""
        db = get_db_connection()
        try:
            query = "SELECT * FROM delete_avaliacao(%s, %s);"
            db.execute(query, (a_id, a_edited_by))
            result = db.fetchone()
            print(result)
            db.connection.commit()
            return jsonify({
                    "message": "Avaliacao deleted successfully", 
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
           


