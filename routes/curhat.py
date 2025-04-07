from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from models import db, Curhat, Komentar

curhat_bp = Blueprint('curhat', __name__)

@curhat_bp.route('/')
def list():
    # Ambil semua curhatan publik dan milik user yang login
    if current_user.is_authenticated:
        curhatan = Curhat.query.filter(
            (Curhat.is_public == True) | (Curhat.user_id == current_user.id)
        ).order_by(Curhat.created_at.desc()).all()
    else:
        curhatan = Curhat.query.filter_by(is_public=True).order_by(Curhat.created_at.desc()).all()
    
    return render_template('curhat/list.html', curhatan=curhatan)

@curhat_bp.route('/buat', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        judul = request.form.get('judul')
        isi = request.form.get('isi')
        is_public = True if request.form.get('is_public') else False
        
        if not judul or not isi:
            flash('Judul dan isi curhatan tidak boleh kosong', 'danger')
            return redirect(url_for('curhat.create'))
        
        new_curhat = Curhat(
            judul=judul,
            isi=isi,
            is_public=is_public,
            user_id=current_user.id
        )
        
        db.session.add(new_curhat)
        db.session.commit()
        
        flash('Curhatan berhasil dibuat!', 'success')
        return redirect(url_for('curhat.detail', id=new_curhat.id))
    
    return render_template('curhat/create.html')

@curhat_bp.route('/detail/<int:id>', methods=['GET', 'POST'])
def detail(id):
    curhat = Curhat.query.get_or_404(id)
    
    # Cek apakah user bisa melihat curhat private
    if not curhat.is_public and (not current_user.is_authenticated or current_user.id != curhat.user_id):
        abort(403)  # Forbidden
    
    if request.method == 'POST' and current_user.is_authenticated:
        isi_komentar = request.form.get('komentar')
        
        if isi_komentar:
            new_komentar = Komentar(
                isi=isi_komentar,
                user_id=current_user.id,
                curhat_id=id
            )
            
            db.session.add(new_komentar)
            db.session.commit()
            
            flash('Komentar berhasil ditambahkan', 'success')
            return redirect(url_for('curhat.detail', id=id))
    
    return render_template('curhat/detail.html', curhat=curhat)

@curhat_bp.route('/milik-saya')
@login_required
def my_curhats():
    curhatan = Curhat.query.filter_by(user_id=current_user.id).order_by(Curhat.created_at.desc()).all()
    return render_template('curhat/list.html', curhatan=curhatan, title='Curhatan Saya')