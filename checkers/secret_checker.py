import re
import json

class SecretChecker:
    def __init__(self):
        self.secret_patterns = [
            (r'password\s*=\s*[\'"].+?[\'"]', 'Hardcoded password'),
            (r'api_key\s*=\s*[\'"].+?[\'"]', 'Exposed API key'),
            (r'(aws_access_key_id|aws_secret_access_key)\s*=', 'AWS credentials'),
            (r'sqlite:///(.+?)\.db', 'Local database reference'),
            (r'[A-Za-z0-9/+]{40}', 'Potential base64 secret'),
            (r'sk_[a-zA-Z0-9]{24}', 'Stripe secret key'),
            # JSON patterns
            (r'\{.*?(password|api_key|secret|token|secret_key).*?\}', 'Potential sensitive data in JSON', True),
            # Hash patterns
            (r'\{.*?(password|api_key|secret|token|secret_key).*?\}', 'Potential sensitive data in hash', True)
        ]

    def check(self, content, file_path):
        findings = []
        for i, line in enumerate(content.split('\n')):
            for pattern, message, is_json in self.secret_patterns[-2:]:
                print(pattern, line)
                if re.search(pattern, line):
                    # For JSON, attempt to parse and validate
                    if is_json:
                        try:
                            json_data = json.loads(line.strip())
                            print(json_data)
                            if any(key in json_data for key in ['password', 'api_key', 'secret', 'token']):
                                findings.append({
                                    'severity': 'HIGH',
                                    'message': f'{message}',
                                    'file': file_path,
                                    'line': i + 1
                                })
                        except json.JSONDecodeError:
                            # Not valid JSON, treat as text
                            pass
                    else:
                        findings.append({
                            'severity': 'HIGH',
                            'message': f'{message}',
                            'file': file_path,
                            'line': i + 1
                        })
        return findings