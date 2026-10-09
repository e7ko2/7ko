import string
import random
import requests
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "Accept": "text/html,application/xhtml+xml,application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

def check_username(username, session):
    url = f"https://www.tiktok.com/@{username}"
    try:
        response = session.get(url, headers=HEADERS, timeout=10, allow_redirects=True)

        if response.status_code in (403, 429):
            return "محظور", True        # النتيجة الثانية = يحتاج استراحة

        if response.status_code == 404:
            return "متاح", False

        if response.status_code == 200:
            page = response.text.lower()
            # صفحة "الحساب غير موجود" => متاح
            if "couldn't find this account" in page or "could not find this account" in page:
                return "متاح", False
            # صفحة بروفايل حقيقية تحتوي بيانات اليوزر => محجوز
            if f'"uniqueid":"{username}"' in page or f"@{username}" in page.lower():
                return "غير متاح", False
            # 200 لكن بدون أي علامة تعريف => كابتشا/صفحة تحقق => لا نصنف
            return "تعذر التحقق", True

        return "تعذر التحقق", False

    except requests.exceptions.RequestException:
        return "تعذر التحقق", False


def main():
    print("=" * 40)
    print("TikTok Username Checker")
    print("=" * 40)

    try:
        total = int(input("عدد اليوزرات: ").strip())
        if total <= 0:
            print("أدخل رقمًا أكبر من صفر.")
            return

        delay_text = input("التأخير بالثواني (Enter = 2): ").strip()
        delay = max(0.5, float(delay_text) if delay_text else 2.0)
    except ValueError:
        print("أدخل أرقامًا صحيحة.")
        return

    chars = string.ascii_lowercase + string.digits + "_"
    checked = set()
    counts = {}
    available = []
    filename = f"results_{int(time.time())}.txt"

    with requests.Session() as session:
        try:
            session.get("https://www.tiktok.com/", headers=HEADERS, timeout=10)
        except requests.exceptions.RequestException:
            pass

        for i in range(1, total + 1):
            username = "".join(random.choices(chars, k=4))
            while username in checked:
                username = "".join(random.choices(chars, k=4))
            checked.add(username)

            status, need_break = check_username(username, session)
            counts[status] = counts.get(status, 0) + 1

            mark = "  <---" if status == "متاح" else ""
            print(f"[{i}/{total}] @{username} : {status}{mark}")

            if status == "متاح":
                available.append(username)

            with open(filename, "a", encoding="utf-8") as file:
                file.write(f"{username} : {status}\n")

            if need_break:
                # استراحة واحدة بدل المزدوجة
                time.sleep(delay * 3)
                continue

            time.sleep(delay)

    print("=" * 40)
    print("الإحصائيات:")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    if available:
        print("المتاح:")
        for u in available:
            print(f"  @{u}")
    print(f"النتائج محفوظة في {filename}")

if __name__ == "__main__":
    main()
