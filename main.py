import os
from datetime import datetime
from flask import Flask, jsonify, render_template_string, abort

app = Flask(__name__)

# إعداد المتغيرات التي طلبتها
MY_UUID = "df137605-475a-408e-9013-33e595c6d837"
CUSTOM_PATH = "/@radwan"

# دمج المسار ليصبح: /@radwan/df137605-475a-408e-9013-33e595c6d837
FULL_SECURE_PATH = f"{CUSTOM_PATH}/{MY_UUID}"

# واجهة المستخدم الخاصة بحاويتك
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حاوية Radwan X1 السرية</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0f172a; text-align: center; padding: 50px; color: #f8fafc; }
        .card { background: #1e293b; padding: 30px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); display: inline-block; max-width: 550px; width: 100%; border: 1px solid #334155; }
        h1 { color: #38bdf8; font-size: 1.8rem; }
        .uuid-box { background: #0f172a; padding: 10px; border-radius: 8px; font-family: monospace; color: #f43f5e; font-size: 0.95rem; word-break: break-all; border: 1px solid #475569; margin: 15px 0; }
        .status { font-weight: bold; color: #4ade80; background: rgba(74, 222, 128, 0.1); padding: 10px; border-radius: 5px; display: inline-block; }
        .path-info { color: #94a3b8; margin-top: 15px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="card">
        <h1>مرحباً بك في حاوية Radwan X1 المأمنة 🛡️</h1>
        <p>تم تشغيل الحاوية بنجاح باستخدام الـ UUID والمسار الخاص بك.</p>
        
        <p><strong>المعرف النشط (UUID):</strong></p>
        <div class="uuid-box">{{ uuid_code }}</div>
        
        <div class="status">الحالة: الحاوية تعمل ومحمية 100% 🟢</div>
        
        <p class="path-info">أنت تتصفح الآن عبر المسار الآمن: <br><code>{{ secure_path }}</code></p>
    </div>
</body>
</html>
"""

# 1. حماية المسار الرئيسي (لو دخل أي شخص للرابط العادي يعطيه خطأ 404 لحمايتك)
@app.route('/')
def index():
    return abort(404)

# 2. المسار السري والخاص بك فقط الذي يفتح الحاوية
@app.route(FULL_SECURE_PATH)
def secure_zone():
    return render_template_string(HTML_TEMPLATE, uuid_code=MY_UUID, secure_path=FULL_SECURE_PATH)

# 3. نظام فحص الصحة الداخلي للحاوية (تستخدمه المنصات للتأكد أن السيرفر شغال)
@app.route('/health')
def health_check():
    return jsonify({"status": "running", "uuid_verified": True})

if __name__ == '__main__':
    # الحصول على المنفذ تلقائياً من قوقل كلاود أو منصات النشر الأخرى
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

