from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1. Model untuk Pengguna (User)
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    sessions = db.relationship('ChatSession', backref='owner', lazy=True)

# 2. Model untuk Sesi Percakapan (Baru)
class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), default="Percakapan Baru")
    
    is_pinned = db.Column(db.Boolean, default=False)
    

    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade="all, delete-orphan")

# 3. Model untuk Pesan Chat
class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
  
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    
    sender = db.Column(db.String(10), nullable=False) # 'user' atau 'bot'
    message = db.Column(db.Text, nullable=False)