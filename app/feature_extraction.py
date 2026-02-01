# feature_extractor.py
import re
import urllib.parse

def extract_features(url: str):
    features = []

    parsed = urllib.parse.urlparse(url)

    features.append(len(url))                              # 1
    features.append(len(parsed.netloc))                    # 2
    features.append(len(parsed.path))                      # 3
    features.append(url.count('.'))                        # 4
    features.append(url.count('-'))                        # 5
    features.append(url.count('@'))                        # 6
    features.append(url.count('?'))                        # 7
    features.append(url.count('%'))                        # 8
    features.append(url.count('='))                        # 9
    features.append(url.count('http'))                     # 10
    features.append(url.count('https'))                    # 11
    features.append(url.count('www'))                      # 12
    features.append(1 if parsed.scheme == "https" else 0) # 13
    features.append(len(re.findall(r'\d', url)))           # 14
    features.append(1 if '@' in url else 0)                # 15
    features.append(1 if '-' in parsed.netloc else 0)      # 16
    features.append(1 if url.startswith("https") else 0)  # 17
    features.append(len(parsed.query))                     # 18
    features.append(len(parsed.fragment))                  # 19
    features.append(1 if parsed.fragment else 0)           # 20
    features.append(len(parsed.params))                    # 21
    features.append(1 if parsed.params else 0)             # 22
    features.append(url.count('/'))                        # 23
    features.append(len(parsed.netloc.split('.')))         # 24

    return features
