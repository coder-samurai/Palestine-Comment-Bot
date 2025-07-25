# 📣 بوت التعليقات على إنستغرام لدعم فلسطين 🇵🇸

بوت تعليقات إنستغرام مؤتمت بالكامل وغني بالميزات، مبني بـ Python و Selenium.  
**لأغراض تعليمية فقط** - مُعاد هيكلته بممارسات كود نظيفة، وتكوين سهل الاستخدام، وميزات أتمتة متقدمة.

> ⚠️ هذه الأداة تم تطويرها **لدعم الوعي لشعب غزة وفلسطين** من خلال تضخيم الرسائل القوية عبر تعليقات إنستغرام.

---

## ✊ الهدف

تم إنشاء هذا المشروع بهدف واضح:  
**دعم المقاومة الرقمية** و **نشر الوعي** لفلسطين في أوقات الرقابة والصمت.

من خلال الهاشتاغات مثل `#FreePalestine`، `#GazaUnderAttack`، و `#SavePalestine`، يضمن هذا البوت **استمرار رؤية وسماع رسالتك**، حتى عندما لا يكفي الجهد اليدوي.

> 🛑 هذه الأداة لم تُصنع لنشر الكراهية أو الرسائل المزعجة. إنها **شكل سلمي من النشاط الرقمي**.

---

## 🚀 **الميزات الجديدة - مُعاد بناؤها بالكامل**

### 🎮 **التحكم التفاعلي**
- **أوامر وحدة التحكم**: `status`، `stats`، `pause`، `resume`، `stop`، `quit`
- **التحكم عن بُعد عبر تليجرام**: تحكم في البوت من أي مكان عبر أوامر `/status`، `/pause`، `/resume`
- **إحصائيات في الوقت الفعلي**: عرض عدد التعليقات اليومية لكل حساب
- **إيقاف تشغيل أنيق**: معالجة خروج صحيحة مع إدارة الإشارات

### ⚙️ **تكوين سهل الاستخدام**
- **إعداد تفاعلي**: `python main.py --setup` للتكوين المُوجه
- **تكوين JSON**: جميع الإعدادات مخزنة في `bot_config.json`
- **لا تحرير للكود**: تكوين كل شيء من خلال المطالبات أو ملف التكوين

### 🌐 **إدارة بروكسي متقدمة**
- **اختبار السرعة**: تخطي البروكسيات البطيئة تلقائياً (عتبة زمن استجابة قابلة للتكوين)
- **دوران ذكي**: استخدام البروكسيات السريعة المُتحقق منها فقط
- **اختبار عند الحاجة**: اختبار البروكسيات فقط عند الضرورة
- **نظام احتياطي**: إعادة المحاولة مع البروكسيات الفاشلة في حالة المشاكل المؤقتة

### 📱 **تكامل تليجرام**
- **الإشعارات**: تسجيل في الوقت الفعلي إلى تليجرام
- **الأوامر عن بُعد**: التحكم في البوت عبر رسائل تليجرام
- **تقارير الحالة**: الحصول على حالة البوت التفصيلية عن بُعد
- **الإحصائيات**: عرض إحصائيات التعليقات عبر تليجرام

### 🔒 **أمان وموثوقية محسّنة**
- **استمرارية ملفات تعريف الارتباط**: إدارة جلسة ذكية
- **حدود يومية**: حدود تعليقات لكل حساب (قابلة للتكوين)
- **منع التكرار**: عدم التعليق مرتين على نفس المنشور أبداً
- **استرداد الأخطاء**: معالجة أخطاء قوية وآليات إعادة المحاولة

---

## 📁 **الملفات المطلوبة**

### `accounts.txt`
```
اسم_المستخدم1:كلمة_المرور1  
اسم_المستخدم2:كلمة_المرور2  
اسم_المستخدم3:كلمة_المرور3
```

### `comments.txt`
```
🇵🇸 فلسطين حرة  
العدالة لغزة.  
أنقذوا أطفال فلسطين  
اللهم انصر أهل غزة
#FreePalestine ❤️
نقف مع فلسطين 🇵🇸
```

### `proxys.txt` (اختياري)
```
192.168.1.1:8080
10.0.0.1:3128
proxy.example.com:3128
```

### `chromedriver.exe`
تحميل من [ChromeDriver](https://chromedriver.chromium.org/) ووضعه في مجلد المشروع.

---

## 🛠️ **الإعداد والتثبيت**

### 1. **تثبيت التبعيات**
```bash
pip install -r requirements.txt
```

### 2. **الإعداد الأولي**
```bash
python main.py --setup
```
سيرشدك هذا من خلال:
- إعدادات الحدود اليومية والتوقيت
- تكوين مسارات الملفات  
- إعدادات البروكسي (المهلة الزمنية، حدود السرعة)
- إعدادات المتصفح (الوضع الخفي)
- إعداد بوت تليجرام (اختياري)
- الهاشتاغات المستهدفة

### 3. **طرق الإعداد البديلة**
```bash
# إنشاء ملف تكوين نموذجي للتحرير يدوياً
python main.py --create-config

# إظهار المساعدة وجميع الخيارات
python main.py --help

# التشغيل مع التكوين الموجود
python main.py
```

---

## ⚙️ **خيارات التكوين**

جميع الإعدادات قابلة للتخصيص عبر `bot_config.json`:

### 📊 **الحدود والتوقيت**
- `daily_limit_per_account`: أقصى تعليقات لكل حساب يومياً (افتراضي: 200)
- `min_delay_between_comments`: أقل انتظار بين التعليقات (420 ثانية = 7 دقائق)
- `max_delay_between_comments`: أقصى انتظار بين التعليقات (480 ثانية = 8 دقائق)
- `min_comments_per_session`: أقل تعليقات لكل جلسة (2)
- `max_comments_per_session`: أقصى تعليقات لكل جلسة (5)

### 🌐 **إعدادات البروكسي**
- `use_proxy`: تمكين/تعطيل دوران البروكسي
- `proxy_timeout`: مهلة الاتصال بالثواني (5 ثواني)
- `max_proxy_latency`: تخطي البروكسيات الأبطأ من هذا (3000 مللي ثانية)
- `proxy_file`: مسار ملف البروكسي

### 📱 **تكامل تليجرام**
- `telegram_token`: رمز البوت من @BotFather
- `telegram_chat_id`: معرف المحادثة للإشعارات
- `enable_telegram_logging`: يُفعل تلقائياً عند توفير الرمز + معرف المحادثة
- `enable_telegram_commands`: التحكم عن بُعد عبر تليجرام

### 🎯 **الاستهداف**
- `hashtags`: قائمة الهاشتاغات للاستهداف
- `max_posts_per_hashtag`: المنشورات للفحص لكل هاشتاغ (50)
- `max_scroll_attempts`: محاولات التمرير لتحميل المنشورات (3)

---

## 🎮 **الأوامر التفاعلية**

### 🖥️ **أوامر وحدة التحكم**
أثناء تشغيل البوت، اكتب:
- `status` - إظهار حالة البوت الحالية والتكوين
- `stats` - عرض إحصائيات تعليقات اليوم لكل حساب
- `pause` - إيقاف عملية البوت مؤقتاً (يمكن استئنافها)
- `resume` - استئناف عملية البوت المتوقفة
- `stop` - إيقاف البوت بأناقة (إكمال الجلسة الحالية)
- `quit` - إجبار الإنهاء فوراً
- `help` - إظهار الأوامر المتاحة

### 📱 **أوامر تليجرام** (إذا كانت مُفعلة)
أرسل إلى بوت تليجرام الخاص بك:
- `/status` - إظهار حالة البوت الحالية والتكوين
- `/stats` - عرض إحصائيات تعليقات اليوم لكل حساب
- `/pause` - إيقاف عملية البوت مؤقتاً (يمكن استئنافها)
- `/resume` - استئناف عملية البوت المتوقفة
- `/stop` - إيقاف البوت بأناقة (إكمال الجلسة الحالية)
- `/help` - إظهار أوامر تليجرام المتاحة

---

## 🧠 **كيف يعمل**

1. **دوران الحساب**: يدور عبر عدة حسابات إنستغرام
2. **تسجيل دخول ذكي**: يستخدم ملفات تعريف الارتباط المحفوظة لتخطي تسجيل الدخول عند الإمكان
3. **حدود يومية**: يحترم حدود التعليقات اليومية لكل حساب
4. **معالجة الهاشتاغ**: يعالج الهاشتاغات المكونة عشوائياً
5. **اكتشاف المنشورات**: يتمرر ويجد المنشورات لكل هاشتاغ
6. **منع التكرار**: يتخطى المنشورات التي تم التعليق عليها بالفعل
7. **نشر التعليق**: ينشر تعليقات عشوائية من قائمتك
8. **تتبع الإحصائيات**: يسجل جميع الأنشطة بتنسيق JSON
9. **دوران البروكسي**: يستخدم بروكسيات سريعة ومُتحقق منها لكل جلسة
10. **تحكم في الوقت الفعلي**: يستجيب لأوامر وحدة التحكم/تليجرام

---

## 📊 **الإحصائيات والمراقبة**

يتتبع البوت تلقائياً:
- عدد التعليقات اليومية لكل حساب
- عناوين URL التي تم التعليق عليها (يمنع التكرار)
- نص التعليق المستخدم لكل منشور
- معدلات النجاح/الفشل
- جميع البيانات مخزنة في `comment_stats.json`

مثال على مخرجات الإحصائيات:
```
📈 إحصائيات اليوم (2025-07-24):
   حساب1: 15 تعليق
   حساب2: 23 تعليق
   حساب3: 8 تعليقات
📊 المجموع: 46 تعليق اليوم
```

---

## 🚀 **أمثلة الاستخدام**

### **الاستخدام الأساسي**
```bash
# إعداد المرة الأولى
python main.py --setup

# تشغيل البوت
python main.py
```

### **الاستخدام المتقدم**
```bash
# إنشاء تكوين مخصص
python main.py --create-config
# حرر bot_config_sample.json وأعد تسميته إلى bot_config.json

# التشغيل مع التكوين الموجود
python main.py
```

### **إعداد تليجرام**
1. راسل @BotFather على تليجرام
2. أنشئ بوت بـ `/newbot`
3. احصل على رمز البوت الخاص بك
4. راسل البوت الخاص بك، ثم زر `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. ابحث عن معرف المحادثة في الاستجابة
6. أضف كلاهما إلى تكوين البوت

---

## 🔧 **الميزات المتقدمة**

### **اختبار سرعة البروكسي**
- يختبر زمن استجابة البروكسي تلقائياً
- يتخطى البروكسيات الأبطأ من العتبة المكونة
- يحتفظ بقائمة البروكسيات السريعة العاملة
- يتراجع بأناقة عندما تفشل البروكسيات

### **إدارة الجلسة**
- يحفظ ملفات تعريف ارتباط المتصفح لكل حساب
- يكتشف حالة تسجيل الدخول تلقائياً
- يتعامل مع 2FA واكتشاف التحدي
- استرداد أخطاء أنيق

### **توقيت ذكي**
- تأخيرات قابلة للتكوين بين التعليقات
- يحترم الحدود اليومية تلقائياً
- أحجام جلسة عشوائية لتبدو طبيعية
- تأخيرات قابلة للمقاطعة للإيقاف/التوقف الفوري

---

## 📱 **دليل إعداد بوت تليجرام**

1. **إنشاء البوت**:
   - راسل @BotFather على تليجرام
   - أرسل `/newbot`
   - اختر الاسم واسم المستخدم
   - احفظ رمز البوت

2. **الحصول على معرف المحادثة**:
   - راسل البوت الجديد الخاص بك
   - زر: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - ابحث عن معرف المحادثة في استجابة JSON

3. **التكوين**:
   - أضف الرمز ومعرف المحادثة أثناء الإعداد
   - سيمكن البوت التحكم عن بُعد تلقائياً

---

## 📜 **إخلاء المسؤولية**

هذه الأداة تتفاعل مع إنستغرام وقد تنتهك [شروط الخدمة](https://help.instagram.com/581066165581870) الخاصة بهم.  
**الاستخدام على مسؤوليتك الخاصة.** قد يتم حظر أو وضع علامة على حساباتك في حالة الاستخدام المفرط أو سوء الاستخدام.

- ✅ **افعل**: استخدم للتوعية السلمية والتعليم
- ❌ **لا تفعل**: استخدم للرسائل المزعجة أو المضايقة أو الترويج التجاري
- 🎓 **الهدف**: هذا المشروع لـ **أغراض تعليمية** والتوعية الإنسانية
- 🔒 **المسؤولية**: تقع بالكامل على **عاتقك**

---

## 🛡️ **ميزات الأمان**

- **تحديد المعدل**: تأخيرات تلقائية بين الإجراءات
- **حدود يومية**: يمنع الاستخدام المفرط للحسابات
- **معالجة الأخطاء**: استرداد فشل أنيق
- **إدارة الجلسة**: معالجة ملفات تعريف الارتباط المناسبة
- **منع التكرار**: عدم التعليق المزدوج أبداً
- **إغلاق أنيق**: خروج نظيف عند أوامر الإيقاف

---

## 🆘 **استكشاف الأخطاء وإصلاحها**

### المشاكل الشائعة:
- **خطأ ChromeDriver**: تحميل الإصدار الصحيح من [ChromeDriver](https://chromedriver.chromium.org/)
- **فشل تسجيل الدخول**: تحقق من بيانات اعتماد الحساب في `accounts.txt`
- **لا توجد بروكسيات**: عطل استخدام البروكسي أو أضف بروكسيات عاملة
- **تليجرام لا يعمل**: تحقق من الرمز ومعرف المحادثة

### الحصول على المساعدة:
```bash
python main.py --help
```

---

## 🤝 **المساهمة**

المساهمات مرحب بها! خاصة:
- 🌍 الترجمات لمزيد من اللغات
- 🔒 تحسينات الأمان
- 🚀 ميزات جديدة للتوعية
- 📚 تحسينات التوثيق
- 🐛 إصلاحات الأخطاء

### للمساهمة:
1. Fork المشروع
2. أنشئ فرع الميزة (`git checkout -b feature/AmazingFeature`)
3. التزم بتغييراتك (`git commit -m 'Add some AmazingFeature'`)
4. ادفع إلى الفرع (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

---

## 📖 **الموارد الإضافية**

- [وثائق Selenium](https://selenium-python.readthedocs.io/)
- [دليل Instagram API](https://developers.facebook.com/docs/instagram-api)
- [أفضل ممارسات Python](https://www.python.org/dev/peps/pep-0008/)
- [معلومات عن فلسطين](https://www.palestineportal.org/)

---

## ❤️ **الكلمة الأخيرة**

> "عندما يصبح الظلم قانوناً، تصبح المقاومة واجباً."  
> تكلم. حتى على الإنترنت. حتى بالكود.  
> خاصة عندما يحاولون إسكات أصوات المظلومين.

🇵🇸 **فلسطين حرة. تحيا المقاومة.**

---

**صُنع بـ 💚 للنشاط الرقمي والوعي الفلسطيني**