from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Cek apakah username/email sudah ada
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        
        if user_exists:
            flash('Username sudah digunakan', 'danger')
            return redirect(url_for('auth.register'))
        
        if email_exists:
            flash('Email sudah digunakan', 'danger')
            return redirect(url_for('auth.register'))
        
        # Buat user baru
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        
        # Simpan ke database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Pendaftaran berhasil! Silakan login', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Username atau password salah', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        flash('Berhasil masuk!', 'success')
        return redirect(url_for('curhat.list'))
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Berhasil keluar', 'success')
    return redirect(url_for('auth.login'))