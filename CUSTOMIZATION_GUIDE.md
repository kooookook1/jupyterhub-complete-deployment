# دليل التخصيص المسموح لـ JupyterHub

## 🎨 التخصيصات المسموحة قانونياً

### 1. تخصيص الواجهة
```python
# في ملف التكوين
c.JupyterHub.template_paths = ['/path/to/custom/templates']
c.JupyterHub.extra_static_paths = ['/path/to/custom/static']
```

### 2. تغيير الشعار
```python
# إضافة شعار مخصص
c.JupyterHub.logo_file = '/path/to/your/logo.png'
```

### 3. تخصيص الألوان والتصميم
```css
/* ملف CSS مخصص */
.navbar-brand {
    /* تخصيص الشعار */
}
```

### 4. إضافة معلومات التخصيص
```python
# في ملف التكوين
c.JupyterHub.template_vars = {
    'custom_message': 'Customized by ZERO (@c4ccz)',
    'deployment_info': 'Custom deployment'
}
```

## ⚖️ الرخصة والحقوق

### BSD License (الرخصة الأصلية)
- ✅ يمكن الاستخدام التجاري
- ✅ يمكن التعديل
- ✅ يمكن التوزيع
- ❌ لا يمكن تغيير حقوق الملكية الأصلية
- ❌ يجب الإشارة للمصدر الأصلي

### الاستخدام المسموح
```
Powered by JupyterHub
Customized by ZERO (@c4ccz)
Original project: https://github.com/jupyterhub/jupyterhub
```

## 🛠️ خطوات التخصيص الآمن

### 1. إنشاء fork
```bash
git fork https://github.com/jupyterhub/jupyterhub
```

### 2. إضافة التخصيصات
```bash
# إضافة ملفات التخصيص الخاصة بك
mkdir custom_templates
mkdir custom_static
```

### 3. الحفاظ على الرخصة
```bash
# عدم حذف ملفات الرخصة الأصلية
# LICENSE
# COPYING.md
```

## 📞 للاستفسارات
- Telegram: @c4ccz
- التخصيص: ZERO

---
**ملاحظة**: هذا التخصيص يحترم حقوق المطورين الأصليين ويتبع القوانين المعمول بها.