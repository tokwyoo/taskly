from flask import Blueprint, redirect, render_template, session, url_for, request, jsonify
from app.models.user import User
from app.models.list import List
from app.db import db

lists_bp = Blueprint("lists", __name__)

@lists_bp.route("/lists")
def lists():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])
    active_lists = List.query.filter_by(user_id=user.id, is_deleted=False).all()
    return render_template("lists.html", user=user, lists=active_lists)

@lists_bp.route("/lists/create", methods=["POST"])
def create_list():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    title = data.get("title")
    
    if not title:
        return jsonify({"error": "Title is required"}), 400
        
    new_list = List(
        user_id=session["user_id"],
        title=title
    )
    
    db.session.add(new_list)
    db.session.commit()
    
    return jsonify(new_list.to_dict()), 201

@lists_bp.route("/lists/<int:list_id>", methods=["PUT"])
def update_list(list_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    list_item = List.query.get_or_404(list_id)
    
    if list_item.user_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403
        
    data = request.json
    title = data.get("title")
    
    if not title:
        return jsonify({"error": "Title is required"}), 400
        
    list_item.title = title
    db.session.commit()
    
    return jsonify(list_item.to_dict())

@lists_bp.route("/lists/<int:list_id>", methods=["DELETE"])
def delete_list(list_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    list_item = List.query.get_or_404(list_id)
    
    if list_item.user_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403
        
    list_item.soft_delete()
    db.session.commit()
    
    return jsonify({"message": "List deleted successfully"})

@lists_bp.route("/lists/<int:list_id>/restore", methods=["POST"])
def restore_list(list_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    list_item = List.query.get_or_404(list_id)
    
    if list_item.user_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403
        
    list_item.restore()
    db.session.commit()
    
    return jsonify(list_item.to_dict())