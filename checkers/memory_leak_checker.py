import re

class MemoryLeakChecker:
    def __init__(self):
        self.java_patterns = [
            (r'new\s+[A-Za-z]+\s*$[^)]*$\s*(?!.*close$$)', 'Unmanaged resource creation'),
            (r'Runtime\.getRuntime$$\.exec$', 'Potential unclosed Process')
        ]
        self.python_patterns = [
            (r'open$[^)]+$\s*(?!.*with.*$)', 'Unclosed file handle'),
            (r'__del__$self$', 'Destructor usage (potential circular references)'),
            (r'global\s+[A-Za-z_]+', 'Global variable declaration')
        ]

    def check(self, content, file_path):
        findings = []
        ext = file_path.split('.')[-1]

        for i, line in enumerate(content.split('\n')):
            patterns = self.java_patterns if ext == 'java' else self.python_patterns
            for pattern, message in patterns:
                if re.search(pattern, line):
                    findings.append({
                        'severity': 'MEDIUM',
                        'message': f'Potential memory leak: {message}',
                        'file': file_path,
                        'line': i + 1
                    })
        return findings