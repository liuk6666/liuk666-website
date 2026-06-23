"""
团湘网络 - 统一主站
整合：AI Agent + 技术外包 + 量化交易
"""
from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# 数据库配置
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'main.db')

def init_db():
    """初始化数据库"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 产品表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            features TEXT,
            image TEXT,
            status TEXT DEFAULT 'active',
            sales_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 服务表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price_range TEXT,
            features TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 订单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            product_id INTEGER,
            service_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 初始化产品数据
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        products = [
            ('科研助手 Agent', 'AI Agent', '文献检索/论文润色/格式调整/摘要生成', 699, '文献检索|论文润色|格式调整|摘要生成', '', 0),
            ('客服 Agent', 'AI Agent', '智能客服自动回复系统', 499, '自动回复|知识库|问题分类', '', 0),
            ('量化交易 Agent', 'AI Agent', '行情分析/交易信号/风险控制', 1999, '行情分析|信号生成|风险控制', '', 0),
            ('量化交易系统', '量化交易', '完整量化交易平台（Dream3）', 5000, '实时行情|自动交易|风险控制|飞书通知', '', 0),
        ]
        cursor.executemany('''
            INSERT INTO products (name, category, description, price, features, image, sales_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', products)
    
    # 初始化服务数据
    cursor.execute('SELECT COUNT(*) FROM services')
    if cursor.fetchone()[0] == 0:
        services = [
            ('网站开发', '技术外包', '企业官网/响应式网页/后台管理系统', '3000-20000 元', 'HTML/CSS/JS|Python/Flask|MySQL'),
            ('数据爬虫', '技术外包', '网站数据采集/批量抓取/定时采集', '1000-5000 元', 'Python|Scrapy|Selenium'),
            ('API 对接', '技术外包', '第三方 API 集成/支付接口/数据同步', '2000-10000 元', 'REST API|WebSocket|OAuth'),
            ('Python 开发', '技术外包', '自动化脚本/工具开发/系统定制', '500-3000 元', 'Python|自动化|数据处理'),
        ]
        cursor.executemany('''
            INSERT INTO services (name, category, description, price_range, features)
            VALUES (?, ?, ?, ?, ?)
        ''', services)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """首页"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE status="active" ORDER BY sales_count DESC LIMIT 6')
    products = cursor.fetchall()
    cursor.execute('SELECT * FROM services WHERE status="active" LIMIT 4')
    services = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products, services=services)

@app.route('/mall')
def mall():
    return render_template('mall.html')


@app.route('/products')
def products():
    return render_template('mall.html')  # 复用 mall.html

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """产品详情"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('product_detail.html', product=product)

@app.route('/services')
def services():
    """服务列表"""
    category = request.args.get('category', '')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if category:
        cursor.execute('SELECT * FROM services WHERE category = ? AND status="active"', (category,))
    else:
        cursor.execute('SELECT * FROM services WHERE status="active"')
    services = cursor.fetchall()
    conn.close()
    return render_template('services.html', services=services, current_category=category)

@app.route('/service/<int:service_id>')
def service_detail(service_id):
    """服务详情"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM services WHERE id = ?', (service_id,))
    service = cursor.fetchone()
    conn.close()
    return render_template('service_detail.html', service=service)

@app.route('/tutorials')
def tutorials():
    """教程/博客"""
    return render_template('tutorials.html')

@app.route('/about')
def about():
    """关于"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """联系"""
    return render_template('contact.html')

@app.route('/create_order', methods=['POST'])
def create_order():
    """创建订单 (JSON API)"""
    try:
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO orders (user_name, contact, product_id, amount, status) VALUES (?, ?, ?, ?, ?)',
            (data.get('name',''), data.get('contact',''), data.get('product_id',''), data.get('amount',''), 'pending')
        )
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'order_id': order_id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/pay/<int:order_id>')
def pay(order_id):
    return render_template('pay.html', order_id=order_id)


@app.route('/buy/<int:product_id>', methods=['GET', 'POST'])
def buy_product(product_id):
    """购买产品"""
    if request.method == 'POST':
        data = request.form
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (user_name, contact, product_id, amount, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (
            data.get('name', ''),
            data.get('contact', ''),
            product_id,
            data.get('amount', 0)
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '订单提交成功！请联系支付'})
    return render_template('buy.html', product_id=product_id)

@app.route('/admin')
def admin():
    """后台管理"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = cursor.fetchall()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.execute('SELECT * FROM services')
    services = cursor.fetchall()
    conn.close()
    return render_template('admin.html', orders=orders, products=products, services=services)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# 模块加载时初始化数据库 (Gunicorn 也走这里)
try:
    init_db()
except Exception as e:
    import sys
    print(f"init_db warning: {e}", file=sys.stderr)
