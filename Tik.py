import string
import random
import requests

# الاسم الأساسي الذي سيتم التوليد بناءً عليه
base_name = "YOUR_NAME" 

def check_single_username(username, domain_template):
    """
    دالة للتحقق من اسم واحد عبر رابط محدد مفصل
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # دمج اسم المستخدم في المكان المخصص داخل الرابط {}
    full_url = domain_template.format(username)
    
    try:
        response = requests.get(full_url, headers=headers, timeout=5)
        
        # الاعتماد على رمز استجابة HTTP لتحديد الحالة
        if response.status_code == 404:
            return username, "Available", "404"
        elif response.status_code == 200:
            return username, "Taken", "200"
        else:
            return username, "Status Unknown", str(response.status_code)
            
    except requests.exceptions.RequestException:
        return username, "Connection Error", "500"

def generate_and_check(master_name):
    print(f"--- جاري توليد وفحص الأسماء بناءً على: {master_name} ---\n")
    
    # 1. توليد قائمة بالأسماء
    pool = []
    suffixes = ["y", "ie", "hq", "x", "io", "me"]
    
    for _ in range(5):
        part = random.choice([master_name, master_name[0], master_name + random.choice(suffixes)])
        if random.random() > 0.5:
            final_name = part + str(random.randint(1, 99))
        else:
            final_name = part.lower()
        pool.append(final_name)

    # 2. المواقع المراد الفحص بها مع تحديد مكان الاسم بـ {}
    domain_templates = [
        "https://www.github.com/{}",
        "https://www.pinterest.com/{}/"
    ]

    # 3. الفحص
    for i, name in enumerate(pool):
        print(f"[{i+1}] فحص الاسم: {name}")
        for template in domain_templates:
            site_name = template.split("/")[2] # استخراج اسم الموقع
            username, status, code = check_single_username(name, template)
            print(f"   ├─ [{site_name}]: {status} (HTTP: {code})")
        print("-" * 40)

if __name__ == "__main__":
    generate_and_check(base_name)
