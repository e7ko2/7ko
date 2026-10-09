import string
import random
import requests
import time
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.tiktok.com/',
}

def check_tiktok_username(username, session):
    """يعيد: 'متاح' / 'غير متاح' / 'خطأ'"""
    try:
        # endpoint بيانات المستخدم - استجابة JSON مباشرة
        url = "https://www.tiktok.com/api/user/detail/"
        params = {
            "uniqueId": username,
            "aid": "1988",
        }
        r = session.get(url, params=params, headers=HEADERS, timeout=8)
        if r.status_code != 200:
            return "خطأ"
        data = r.json()
        # إذا ما فيه userInfo يعني اليوزر غير موجود = متاح
        if not data.get("userInfo"):
            return "متاح"
        return "غير متاح"
    except (requests.exceptions.RequestException, ValueError):
        return "خطأ"

def main():
    print("=" * 50)
    print("   فاحص يوزرات تيك توك الرباعية - نسخة محسّنة")
    print("=" * 50)

    try:
        total = int(input("عدد اليوزرات المراد فحصها: ").strip())
        if total <= 0:
            raise ValueError
    except ValueError:
        print("يرجى إدخال رقم صحيح أكبر من صفر!")
        return

    delay_input = input("التأخير بين كل فحص بالثواني (اتركه فارغ لـ 1): ").strip()
    delay = float(delay_input) if delay_input else 1.0

    # طلبات متتالية بنفس الجلسة لتسريع الاتصال (keep-alive)
    session = requests.Session()

    chars = string.ascii_lowercase + string.digits + "_"
    available = []
    errors = 0

    out_file = f"available_{int(time.time())}.txt"

    print(f"\nبدء الفحص... النتائج المتاحة تنحفظ في: {out_file}\n")

    for i in range(1, total + 1):
        user = ''.join(random.choice(chars) for _ in range(4))
        status = check_tiktok_username(user, session)

        if status == "متاح":
            print(f"[{i}] {user} : متاح  <---")
            available.append(user)
            with open(out_file, "a", encoding="utf-8") as f:
                f.write(user + "\n")
        elif status == "خطأ":
            errors += 1
            print(f"[{i}] {user} : خطأ في الاتصال")
        else:
            print(f"[{i}] {user} : غير متاح")

        time.sleep(delay)

    print("\n" + "=" * 50)
    print(f"النتيجة: {len(available)} متاح | {errors} خطأ")
    if available:
        print("المتاح في هذه الجولة:")
        for u in available:
            print(f"  - {u}")
    else:
        print("ما تم إيجاد متاح (أغلب الرباعيات محجوزة).")
    print("=" * 50)

if __name__ == "__main__":
    main()
