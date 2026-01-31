import re
from urllib.parse import urlparse

def extract_features(url: str) -> list[float]:
    parsed = urlparse(url)

    features = []

    # 1️⃣ Length of URL
    features.append(len(url))

    # 2️⃣ Length of hostname
    features.append(len(parsed.netloc))

    # 3️⃣ Count of dots
    features.append(url.count('.'))

    # 4️⃣ HTTPS present
    features.append(1 if parsed.scheme == "https" else 0)

    # 5️⃣ Suspicious characters
    features.append(1 if re.search(r"[@\-]", url) else 0)

    # ⚠️ أكمل باقي الـ features بنفس ترتيب التدريب
    # يجب أن يكون العدد النهائي = عدد Features في الموديل

    return features
