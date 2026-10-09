import string
import random
import requests
import time

def check_username(username):
    # رابط فحص حسابات العامة
    url = f"https://www.github.com/{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        # إذا كان رمز الاستجابة 404 فهذا يعني أن الاسم متاح
        if response.status_code == 404:
            return "متاح"
        else:
            return "غير متاح"
            
    except requests.exceptions.RequestException:
        return "خطأ في الاتصال"

def main():
    print("=" * 40)
    print("      برنامج فحص اليوزرات الرباعية")
    print("=" * 40)
    
    # تحديد عدد محاولات الفحص
    try:
        total_checks = int(input("أدخل عدد اليوزرات المراد فحصها: "))
    except ValueError:
        print("يرجى كتابة رقم صحيح!")
        return

    print(f"\nجاري بدء فحص {total_checks} يوزر رباعي...\n")
    
    # عناصر اليوزر الرباعي (حروف إنجليزية صغيرة + أرقام + شرطة سفلية)
    chars = string.ascii_lowercase + string.digits + "_"
    
    # القائمة لحفظ المتاح فقط
    available_list = []

    for i in range(1, total_checks + 1):
        # توليد يوزر رباعي فقط (4 أحرف)
        quad_user = ''.join(random.choice(chars) for _ in range(4))
        
        # فحص الحالة
        status = check_username(quad_user)
        
        # طباعة النتيجة بتنسيق واضح
        if status == "متاح":
            print(f"[{i}] {quad_user} : متاح  <---")
            available_list.append(quad_user)
        else:
            print(f"[{i}] {quad_user} : غير متاح")
            
        # مهلة بسيطة بين كل فحص لضمان ثبات الاتصال
        time.sleep(0.3)

    # ملخص النتائج في النهاية
    print("\n" + "=" * 40)
    print("النتائج النهائية للليوزرات المتاحة:")
    if available_list:
        for user in available_list:
            print(f"- {user}")
    else:
        print("لم يتم العثور على يوزرات متاحة في هذه الجولة.")
    print("=" * 40)

if __name__ == "__main__":
    main()
