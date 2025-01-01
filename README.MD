SQLite Manager SQLite Manager هو أداة بسيطة وفعالة لإدارة قواعد البيانات باستخدام SQLite. تم تطوير هذا المشروع بلغة Python، ويوفر واجهة سهلة الاستخدام لإنشاء قواعد البيانات، وإدارة الجداول، وتنفيذ الاستعلامات، وعرض النتائج.

الميزات الرئيسية إنشاء قاعدة بيانات: يمكنك بسهولة إنشاء قواعد بيانات جديدة باستخدام SQLite.

إدارة الجداول: إنشاء، تعديل، وحذف الجداول داخل قاعدة البيانات.

تنفيذ الاستعلامات: يدعم المشروع تنفيذ استعلامات SQL مثل SELECT, INSERT, UPDATE, DELETE.

عرض النتائج: عرض نتائج الاستعلامات في شكل جدول أو نص.

واجهة بسيطة: واجهة سهلة الاستخدام للمبتدئين والمتخصصين.

كيفية الاستخدام المتطلبات Python 3.x

المكتبات المذكورة في requirements.txt

خطوات التشغيل تنزيل المشروع من GitHub:

bash Copy git clone https://github.com/hmada2024/sqlite_manager.git الانتقال إلى مجلد المشروع:

bash Copy cd sqlite_manager تثبيت المتطلبات:

bash Copy pip install -r requirements.txt تشغيل الملف الرئيسي:

bash Copy python main.py أمثلة على الاستخدام إنشاء قاعدة بيانات جديدة:

python Copy import sqlite3 conn = sqlite3.connect('example.db') إنشاء جدول جديد:

python Copy cursor = conn.cursor() cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''') إدراج بيانات:

python Copy cursor.execute("INSERT INTO users (name, age) VALUES ('Ahmed', 30)") conn.commit() استعلام البيانات:

python Copy cursor.execute("SELECT * FROM users") rows = cursor.fetchall() for row in rows: print(row) المساهمة نرحب بجميع المساهمات لتحسين هذا المشروع. إذا كنت ترغب في المساهمة، يرجى اتباع الخطوات التالية:

عمل Fork للمشروع.

إنشاء فرع جديد (git checkout -b feature/YourFeatureName).

إجراء التغييرات المطلوبة.

عمل Commit للتغييرات (git commit -m 'Add some feature').

Push إلى الفرع (git push origin feature/YourFeatureName).

فتح طلب Pull.

الترخيص هذا المشروع مرخص تحت MIT License.

الاتصال إذا كان لديك أي أسئلة أو استفسارات، يمكنك التواصل معي عبر البريد الإلكتروني. alasuity881991@gmail.com