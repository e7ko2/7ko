import string
import random
import requests
import time

def check_tiktok_username(username):
    # رابط الملف الشخصي المباشر على تيك توك
    url = f"https://www.tiktok.com/@{username}"
    
    # متصفح وهمي لتفادي حظر الطلبات البسيطة
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        # رمز 404 يعني أن الصفحة غير موجودة (اليوزر قد يكون متاحاً)
        if response.status_code == 404:
            return "متاح"
        else:
            return "غير متاح"
            
    except requests.exceptions.RequestException:
        return "خطأ في الاتصال"

def main():
    print("=" * 45)
    print("   فحص متاحية يوزرات تيك توك الرباعية")
    print("=" * 45)
    
    try:
        total_checks = int(input("أدخل عدد اليوزرات المراد فحصها: "))
    except ValueError:
        print("يرجى كتابة رقم صحيح!")
        return

    print(f"\nجاري بدء فحص {total_checks} يوزر على تيك توك...\n")
    
    # الحروف والأرقام والشرطة السفلية المقبولة في يوزرات تيك توك
    chars = string.ascii_lowercase + string.digits + "_"
    
    available_list = []

    for i in range(1, total_checks + 1):
        # توليد يوزر رباعي
        quad_user = ''.join(random.choice(chars) for _ in range(4))
        
        status = check_tiktok_username(quad_user)
        
        if status == "متاح":
            print(f"[{i}] {quad_user} : متاح  <---")
            available_list.append(quad_user)
        else:
            print(f"[{i}] {quad_user} : غير متاح")
            
        # مهلة ثانية واحدة بين كل فحص لتجنب الحظر السريع للـ IP
        time.sleep(1)

    print("\n" + "=" * 45)
    print("الأسماء المتاحة في هذه الجولة:")
    if available_list:
        for user in available_list:
            print(f"- {user}")
    else:
        print("لم يتم العثور على يوزرات متاحة (أغلب الرباعيات محجوزة).")
    print("=" * 45)

if __name__ == "__main__":
    main()
