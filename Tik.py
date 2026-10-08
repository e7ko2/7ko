import string
import random
import requests
import time

def check_single_username(username, domain_template):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    full_url = domain_template.format(username)
    
    try:
        response = requests.get(full_url, headers=headers, timeout=5)
        
        # إذا كانت الاستجابة 404 فالحساب غالباً متاح
        if response.status_code == 404:
            return username, "متاح"
        else:
            return username, "غير متاح"
            
    except requests.exceptions.RequestException:
        return username, "خطأ في الاتصال"

def generate_and_check():
    # 1. طلب عدد اليوزرات من المستخدم عند التشغيل
    try:
        total_count = int(input("أدخل عدد اليوزرات الرباعية المراد فحصها: "))
    except ValueError:
        print("خطأ: يرجى كتابة رقم صحيح.")
        return

    print(f"\n--- جاري توليد وفحص {total_count} يوزر رباعي ---\n")
    
    # الأحرف المسموح بها لتوليد يوزر رباعي
    chars = string.ascii_lowercase + string.digits
    
    # 2. توليد قائمة يوزرات رباعية عشوائية
    pool = []
    for _ in range(total_count):
        quad_name = ''.join(random.choice(chars) for _ in range(4))
        pool.append(quad_name)

    # 3. المواقع المراد الفحص بها (يمكنك إضافة أو تعديل الروابط)
    domain_templates = [
        "https://www.github.com/{}"
    ]

    # 4. بدء الفحص
    for i, name in enumerate(pool):
        print(f"[{i+1}] فحص اليوزر: {name}")
        for template in domain_templates:
            site_name = template.split("/")[2]
            username, status = check_single_username(name, template)
            print(f"   └─ النتيجة: {status}")
        
        # مهلة زمنية بسيطة لحماية الاتصال من التوقف
        time.sleep(0.5)
        print("-" * 30)

if __name__ == "__main__":
    generate_and_check()
