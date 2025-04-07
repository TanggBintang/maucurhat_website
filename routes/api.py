from flask import Blueprint, jsonify, request
from flask_login import current_user
from models import Curhat, Komentar, User
from flask_cors import cross_origin

api = Blueprint('api', __name__)

@api.route('/curhatan', methods=['GET'])
@cross_origin()
def get_curhatan():
    # Ambil semua curhatan publik
    curhatan = Curhat.query.filter_by(is_public=True).order_by(Curhat.created_at.desc()).all()
    
    result = []
    for curhat in curhatan:
        author = User.query.get(curhat.user_id)
        result.append({
            'id': curhat.id,
            'judul': curhat.judul,
            'isi': curhat.isi,
            'author': author.username,
            'created_at': curhat.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'komentar_count': len(curhat.komentar)
        })
    
    return jsonify({
        'status': 'success',
        'data': result
    })

@api.route('/curhatan/<int:id>', methods=['GET'])
@cross_origin()
def get_curhat_detail(id):
    curhat = Curhat.query.get_or_404(id)
    
    # Cek apakah curhatan bersifat publik
    if not curhat.is_public:
        return jsonify({
            'status': 'error',
            'message': 'Curhatan tidak ditemukan atau bersifat privat'
        }), 404
    
    author = User.query.get(curhat.user_id)
    
    komentar_list = []
    for komentar in curhat.komentar:
        komentar_author = User.query.get(komentar.user_id)
        komentar_list.append({
            'id': komentar.id,
            'isi': komentar.isi,
            'author': komentar_author.username,
            'created_at': komentar.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'status': 'success',
        'data': {
            'id': curhat.id,
            'judul': curhat.judul,
            'isi': curhat.isi,
            'author': author.username,
            'created_at': curhat.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'komentar': komentar_list
        }
    })