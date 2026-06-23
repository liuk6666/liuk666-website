# 团湘网络 - 统一主站

## 🎯 网站定位

**计算机博士创立的技术服务公司**

整合业务：
- AI Agent 产品（科研助手/客服/量化交易）
- 技术服务外包（网站/爬虫/API）
- 量化交易系统

---

## 📦 文件结构

```
liuk666-main/
├── app.py                      # Flask 主程序
├── requirements.txt            # Python 依赖
├── data/
│   └── main.db                # SQLite 数据库（自动创建）
├── templates/
│   ├── index.html             # 首页（统一品牌）
│   ├── products.html          # 产品列表
│   ├── product_detail.html    # 产品详情
│   ├── services.html          # 服务列表
│   ├── service_detail.html    # 服务详情
│   ├── tutorials.html         # 教程/博客
│   ├── about.html             # 关于
│   ├── contact.html           # 联系
│   ├── buy.html               # 购买
│   └── admin.html             # 后台管理
└── static/
    └── css/
        └── style.css          # 样式文件
```

---

## 🚀 部署步骤

### 1. 上传到服务器

```bash
# 本地 PowerShell
cd C:\Users\ysuli\.openclaw\workspace\liuk666-main
scp -r * root@108.61.161.189:/root/liuk666-main/
```

### 2. SSH 登录并部署

```bash
# SSH 登录
ssh root@108.61.161.189

# 进入目录
cd /root/liuk666-main

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install flask

# 启动应用
python3 app.py
```

### 3. 配置 Nginx

```bash
# 备份旧配置
cp /etc/nginx/sites-available/liuk666 /etc/nginx/sites-available/liuk666.bak

# 创建新配置
cat > /etc/nginx/sites-available/liuk666 << 'EOF'
server {
    listen 80;
    server_name liuk666.com www.liuk666.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# 启用配置
ln -sf /etc/nginx/sites-available/liuk666 /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx
```

### 4. 配置 systemd 服务

```bash
cat > /etc/systemd/system/liuk666-main.service << 'EOF'
[Unit]
Description=团湘网络主站
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/liuk666-main
Environment="PATH=/root/liuk666-main/venv/bin"
ExecStart=/root/liuk666-main/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable liuk666-main
systemctl start liuk666-main
```

---

## 📊 数据库说明

### 数据表

| 表名 | 说明 |
|------|------|
| products | 产品（AI Agent/量化系统） |
| services | 服务（技术外包） |
| orders | 订单 |

### 初始数据

**产品**：
1. 科研助手 Agent - 699 元
2. 客服 Agent - 499 元
3. 量化交易 Agent - 1999 元
4. 量化交易系统 - 5000 元

**服务**：
1. 网站开发 - 3000-20000 元
2. 数据爬虫 - 1000-5000 元
3. API 对接 - 2000-10000 元
4. Python 开发 - 500-3000 元

---

## 🎯 网站架构

```
liuk666.com（主站）
│
├── 首页（品牌 + 产品展示）
│
├── /products（AI 产品）
│   ├── 科研助手 Agent
│   ├── 客服 Agent
│   └── 量化交易 Agent
│
├── /services（技术服务）
│   ├── 网站开发
│   ├── 数据爬虫
│   ├── API 对接
│   └── Python 开发
│
├── /tutorials（教程/博客）
│
├── /about（关于）
│
└── /contact（联系）
```

---

## 💰 盈利模式

| 来源 | 产品/服务 | 价格 | 预期 |
|------|---------|------|------|
| **AI 产品销售** | 科研助手/客服/量化 | 499-1999 元 | 月 10000-30000 元 |
| **技术服务** | 网站/爬虫/API | 500-20000 元 | 月 20000-50000 元 |
| **量化系统** | Dream3 完整系统 | 5000 元 | 月 5000-20000 元 |
| **培训课程** | AI/量化教程 | 299-2999 元 | 月 5000-15000 元 |

---

## 📝 关于页内容

```
关于团湘网络

团湘网络是由计算机博士创立的技术服务公司，专注于：
- AI Agent 研发与销售
- 量化交易系统开发
- 技术外包服务

创始人背景:
- 计算机科学与技术博士
- 研究方向：AI Agent、自动化系统
- 多年量化交易系统开发经验

我们的使命:
用 AI 技术提升工作效率，帮助客户成功。

联系方式:
微信：HMWK_001
邮箱：ysuliukang2021@163.com
QQ: 1403698747
```

---

## 🚀 下一步

### 1. 部署上线
- [ ] 上传代码
- [ ] 配置 Nginx
- [ ] 配置 systemd
- [ ] 测试访问

### 2. 完善页面
- [ ] products.html
- [ ] product_detail.html
- [ ] services.html
- [ ] service_detail.html
- [ ] about.html
- [ ] contact.html

### 3. 整合产品
- [ ] 科研助手 Agent 集成
- [ ] 客服 Agent 集成
- [ ] 量化交易 Agent 集成

### 4. 配置支付
- [ ] 微信收款码
- [ ] 支付宝收款码
- [ ] 订单系统

---

**开始部署吧！** 🚀
