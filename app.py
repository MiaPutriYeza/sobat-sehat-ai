from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, ChatMessage, ChatSession, User 
from chatbot import get_chat_response

app = Flask(__name__)
CORS(app) 

# KONFIGURASI
app.config['SECRET_KEY'] = 'kunci_rahasia_sobat_sehat_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sobatsehat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# --- RUTE FRONTEND ---
@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/chat')
def chat_ui():
    return render_template('chat.html')

# --- RUTE API AUTENTIKASI ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email sudah terdaftar"}), 400
    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registrasi berhasil"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({"message": "Login berhasil", "email": user.email})
    return jsonify({"error": "Email atau password salah"}), 401

@app.route('/api/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout berhasil"})

# --- RUTE API HISTORY MANAGEMENT ---
@app.route('/api/history', methods=['GET'])
def get_history():
    u_id = session.get('user_id')
    if not u_id:
        return jsonify({"history": []})
    
    user_sessions = ChatSession.query.filter_by(user_id=u_id)\
        .order_by(ChatSession.is_pinned.desc(), ChatSession.id.desc()).all()
    
    results = [
        {"title": s.title, "id": s.id, "is_pinned": s.is_pinned} 
        for s in user_sessions
    ]
    return jsonify({"history": results})

@app.route('/api/history/update', methods=['POST'])
def update_history():
    u_id = session.get('user_id')
    if not u_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    session_id = data.get('id')
    action = data.get('action') # 'rename', 'delete', 'pin'
    
    chat_session = ChatSession.query.filter_by(id=session_id, user_id=u_id).first()
    if not chat_session:
        return jsonify({"error": "Data tidak ditemukan"}), 404

    try:
        if action == 'rename':
            chat_session.title = data.get('title')
        elif action == 'delete':
            db.session.delete(chat_session)
        elif action == 'pin':
            chat_session.is_pinned = not chat_session.is_pinned
        
        db.session.commit()
        return jsonify({"message": "Update berhasil"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/messages/<int:session_id>', methods=['GET'])
def get_session_messages(session_id):
    u_id = session.get('user_id')
    if not u_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    chat_session = ChatSession.query.filter_by(id=session_id, user_id=u_id).first()
    if not chat_session:
        return jsonify({"error": "Sesi tidak ditemukan"}), 404
        
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.id.asc()).all()
    res = [{"sender": m.sender, "message": m.message} for m in messages]
    
    return jsonify({"messages": res, "title": chat_session.title})

# --- RUTE API CHAT ---
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    user_message = data.get('message')
    model_type = data.get('model_type', 'groq')
    session_id = data.get('session_id') # Ambil session_id jika ada
    u_id = session.get('user_id')

    if not u_id:
        return jsonify({"response": "LOGIN_REQUIRED"}), 401

    try:
        if not session_id:
            new_title = user_message[:30] + '...' if len(user_message) > 30 else user_message
            new_session = ChatSession(user_id=u_id, title=new_title)
            db.session.add(new_session)
            db.session.commit()
            session_id = new_session.id

        new_user_msg = ChatMessage(session_id=session_id, sender='user', message=user_message)
        db.session.add(new_user_msg)
        
        history = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.id.desc()).limit(6).all()
        history.reverse() 

        bot_response = get_chat_response(user_message, history[:-1], model_type)

        new_bot_msg = ChatMessage(session_id=session_id, sender='bot', message=bot_response)
        db.session.add(new_bot_msg)
        db.session.commit()
        
        return jsonify({"response": bot_response, "session_id": session_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"response": "Gangguan sistem: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)