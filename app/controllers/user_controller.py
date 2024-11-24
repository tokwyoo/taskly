from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
from app.db import db
from app.models.user import User

user_bp = Blueprint("user", __name__)

UPLOAD_FOLDER = 'app/static/uploads/profile_photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))
        
    return render_template(
        "settings.html",
        user=user  # Pasamos el objeto user completo
    )

@user_bp.route("/api/update-profile", methods=["POST"])
def update_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        user = User.query.get(session["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Handle name update
        name = request.form.get('name')
        if name and len(name.strip()) > 0:
            if len(name) > 50:  # Validación según el modelo
                return jsonify({"error": "Name too long. Maximum 50 characters."}), 400
            user.name = name.strip()

        # Handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                if not allowed_file(file.filename):
                    return jsonify({"error": "Invalid file type. Allowed types: png, jpg, jpeg, gif"}), 400
                
                # Check file size
                file.seek(0, os.SEEK_END)
                size = file.tell()
                file.seek(0)
                if size > MAX_FILE_SIZE:
                    return jsonify({"error": "File too large. Maximum size is 5MB"}), 400

                filename = secure_filename(f"user_{user.id}_{file.filename}")
                
                # Create upload directory if it doesn't exist
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Delete old profile picture if exists
                if user.profile_picture:
                    old_path = os.path.join('app', user.profile_picture.lstrip('/'))
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                # Save the file
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Update database with new photo path
                user.profile_picture = f"/static/uploads/profile_photos/{filename}"

        # Handle bio update
        bio = request.form.get('bio')
        if bio is not None:  # Permitimos bio vacía
            if len(bio) > 255:  # Validación según el modelo
                return jsonify({"error": "Bio too long. Maximum 255 characters."}), 400
            user.bio = bio.strip()

        db.session.commit()
        return jsonify({
            "message": "Profile updated successfully",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route("/api/update-security", methods=["POST"])
def update_security():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        user = User.query.get(session["user_id"])
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update email
        new_email = data.get('email')
        if new_email:
            new_email = new_email.strip().lower()
            if '@' not in new_email or '.' not in new_email:
                return jsonify({"error": "Invalid email format"}), 400
            if len(new_email) > 255:  # Validación según el modelo
                return jsonify({"error": "Email too long. Maximum 255 characters."}), 400
            
            # Check if email is already in use
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({"error": "Email already in use"}), 400
                
            user.email = new_email
            user.email_verified = False  # Requiere nueva verificación

        # Update password
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if new_password:
            if not current_password:
                return jsonify({"error": "Current password is required"}), 400
            
            if not user.check_password(current_password):
                return jsonify({"error": "Current password is incorrect"}), 400
                
            if len(new_password) < 8:
                return jsonify({"error": "Password must be at least 8 characters long"}), 400
                
            user.set_password(new_password)

        db.session.commit()
        return jsonify({
            "message": "Security settings updated successfully",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route("/api/delete-account", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        user = User.query.get(session["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Verify password before deletion
        password = data.get('password')
        if not password or not user.check_password(password):
            return jsonify({"error": "Invalid password"}), 400

        # Delete profile picture if it exists
        if user.profile_picture:
            photo_path = os.path.join('app', user.profile_picture.lstrip('/'))
            if os.path.exists(photo_path):
                os.remove(photo_path)

        # Delete user from database
        db.session.delete(user)
        db.session.commit()
        
        # Clear session
        session.clear()
        
        return jsonify({"message": "Account deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500