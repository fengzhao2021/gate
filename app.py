from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime, timedelta
import os
from pathlib import Path

# 获取当前文件所在目录的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 在 app 初始化后添加
# 确保 static/images 文件夹存在
images_dir = Path(app.static_folder) / 'images'
images_dir.mkdir(parents=True, exist_ok=True)

# 打印当前工作目录和图片路径
print("Current working directory:", os.getcwd())
print("Image path:", os.path.join(os.getcwd(), 'static', 'images', 'dark-seraph.jpg'))

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer, default=15)  # 添加积分字段，默认15分

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_enough_points(self):
        return self.points > 0

    def use_point(self):
        if self.has_enough_points():
            self.points -= 1
            db.session.commit()
            return True
        return False

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# 路由
@app.route('/')
def index():
    if current_user.is_authenticated and current_user.points < 5:
        flash('积分即将耗尽，请及时充值')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('邮箱或密码错误')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 验密码
        if password != confirm_password:
            flash('两次输入的密码不一致')
            return redirect(url_for('register'))
            
        # 检查邮箱是否已注册
        if User.query.filter_by(email=email).first():
            flash('该邮箱已被注册')
            return redirect(url_for('register'))
            
        # 创建新用户
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/get_random_number')
@login_required
def get_random_number():
    if not current_user.has_enough_points():
        return 'no_points'  # 返回特殊标识
    
    if current_user.use_point():
        return str(random.randint(1, 8))
    return 'error'

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/subscribe/<plan>', methods=['POST'])
@login_required
def subscribe(plan):
    if plan not in ['basic', 'premium']:
        return redirect(url_for('pricing'))
        
    # 这里添加支付逻辑
    # 支付成功后更新用户会员状态
    current_user.member_type = plan
    current_user.member_until = datetime.utcnow() + timedelta(days=30)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# 添加一个路由来检查图片
@app.route('/check_image')
def check_image():
    image_path = Path(app.static_folder) / 'images' / 'dark-seraph.jpg'
    if image_path.exists():
        return {
            'status': 'success',
            'message': 'Image found',
            'path': str(image_path),
            'size': image_path.stat().st_size
        }
    else:
        return {
            'status': 'error',
            'message': 'Image not found',
            'path': str(image_path),
            'available_files': [str(f) for f in images_dir.glob('*')]
        }

@app.route('/test_image')
def test_image():
    return send_from_directory(app.static_folder, 'images/dark-seraph.jpg')

if __name__ == '__main__':
    with app.app_context():
        # 删除所有表并重新创建
        db.drop_all()
        db.create_all()
        print("数据库已重新创建")
    app.run(debug=True) 