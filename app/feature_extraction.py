# feature_extractor.py
import re
import numpy as np
from urllib.parse import urlparse
import tldextract

class AdvancedURLFeatureExtractor:
    def __init__(self):
        self.suspicious_keywords = [
            'login','secure','verify','account','bank','pay','update','confirm',
            'password','security','signin','validation','authentication','billing',
            'payment','wallet','credit','card','ssn','social','click','here',
            'urgent','important','alert','warning','suspended','limited','locked',
            'crypto','bitcoin','free','bonus','winner','prize','recovery',
            'lottery','reward','claim','offer','discount','limited-time',
            'exclusive','deal','sale','win','congratulations','selected'
        ]

        self.brand_keywords = [
            'paypal','facebook','amazon','microsoft','apple','google','netflix',
            'instagram','whatsapp','twitter','ebay','wellsfargo','chase',
            'bankofamerica','citibank','linkedin','outlook','hotmail','yahoo','dropbox'
        ]

        self.suspicious_tlds = [
            'tk','ml','ga','cf','gq','xyz','top','club','site','online',
            'work','bid','win'
        ]

    def extract(self, url: str):
        try:
            url = str(url).strip()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url

            parsed = urlparse(url)
            ext = tldextract.extract(url)
            domain = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
            url_lower = url.lower()

            special_chars = sum(
                not c.isalnum() and c not in ['-', '.', '/']
                for c in url
            )

            features = {
                'url_length': len(url),
                'domain_length': len(domain),
                'has_https': 1 if url.startswith('https://') else 0,
                'path_length': len(parsed.path),
                'query_length': len(parsed.query),
                'subdomain_count': max(
                    0,
                    len(parsed.netloc.split('.')) -
                    (len(ext.suffix.split('.')) if ext.suffix else 0) - 1
                ),
                'is_ip_address': 1 if re.match(
                    r'^\d+(\.\d+){3}(:\d+)?$', parsed.netloc
                ) else 0,
                'digit_count': sum(c.isdigit() for c in url),
                'digit_ratio': sum(c.isdigit() for c in url) / max(len(url), 1),
                'special_char_count': special_chars,
                'special_char_ratio': special_chars / max(len(url), 1),
                'dot_count': url.count('.'),
                'hyphen_count': url.count('-'),
                'has_query': 1 if parsed.query else 0,
                'has_fragment': 1 if parsed.fragment else 0,
                'is_suspicious_tld': 1 if ext.suffix in self.suspicious_tlds else 0,
                'tld_length': len(ext.suffix) if ext.suffix else 0,
                'vowel_ratio': sum(c in 'aeiou' for c in url_lower) / max(len(url), 1),
                'consonant_ratio': sum(
                    c in 'bcdfghjklmnpqrstvwxyz' for c in url_lower
                ) / max(len(url), 1),
                'url_entropy': self.calculate_entropy(url),
                'domain_entropy': self.calculate_entropy(domain),
                'suspicious_keyword_count': sum(
                    kw in url_lower for kw in self.suspicious_keywords
                ),
                'brand_mention_count': sum(
                    b in url_lower for b in self.brand_keywords
                ),
                'avg_word_length': self.calculate_avg_word_length(url_lower)
            }

        except Exception:
            features = {k: 0 for k in [
                'url_length','domain_length','has_https','path_length','query_length',
                'subdomain_count','is_ip_address','digit_count','digit_ratio',
                'special_char_count','special_char_ratio','dot_count','hyphen_count',
                'has_query','has_fragment','is_suspicious_tld','tld_length',
                'vowel_ratio','consonant_ratio','url_entropy','domain_entropy',
                'suspicious_keyword_count','brand_mention_count','avg_word_length'
            ]}

        return features

    def calculate_entropy(self, text):
        if len(text) <= 1:
            return 0
        entropy = 0
        for ch in set(text):
            p = text.count(ch) / len(text)
            entropy -= p * np.log2(p)
        return entr
