import re

class CodeStandardChecker:
    def __init__(self):
        self.java_standards = [
            (r'void\s+[a-z][A-Za-z0-9]*\s*$', 'Method naming should be camelCase'),
            (r'class\s+[A-Z][a-zA-Z0-9]*', 'Class name should be PascalCase')
        ]
        self.python_standards = [
            (r'def\s+[A-Z][A-Za-z0-9_]*\s*$', 'Function name should be snake_case'),
            (r'class\s+[a-z][a-z0-9_]*', 'Class name should be PascalCase'),
            (r'print\s*$', 'Avoid direct print statements in production code')
        ]

    def check(self, content, file_path):
        findings = []
        ext = file_path.split('.')[-1]

        for i, line in enumerate(content.split('\n')):
            standards = self.java_standards if ext == 'java' else self.python_standards
            for pattern, message in standards:
                if re.search(pattern, line):
                    findings.append({
                        'severity': 'LOW',
                        'message': f'Code standard violation: {message}',
                        'file': file_path,
                        'line': i + 1
                    })
        return findings