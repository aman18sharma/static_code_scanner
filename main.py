import argparse
import os
import chardet  # Add this import
from checkers.secret_checker import SecretChecker
from checkers.memory_leak_checker import MemoryLeakChecker
from checkers.code_standard_checker import CodeStandardChecker

class CodeAnalyzer:
    def analyze_file(self, file_path):
        findings = []
        try:
            # Detect file encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            # Read with detected encoding
            with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                content = file.read()
                for checker in [SecretChecker(), MemoryLeakChecker(), CodeStandardChecker()]:
                    findings.extend(checker.check(content, file_path))
        except UnicodeDecodeError:
            print(f"Skipping non-text file: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
        return findings

def main():
    parser = argparse.ArgumentParser(description='Static Code Analyzer')
    parser.add_argument('path', help='Path to directory or file to analyze')
    args = parser.parse_args()
    analyzer = CodeAnalyzer()
    findings = []
    if os.path.isfile(args.path):
        findings = analyzer.analyze_file(args.path)
    elif os.path.isdir(args.path):
        for root, dirs, files in os.walk(args.path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(('.py', '.java')):
                    findings.extend(analyzer.analyze_file(file_path))
    else:
        print("Invalid path provided.")

    print("\nAnalysis Results:")
    for finding in findings:
        print(f"[{finding['severity']}] {finding['message']} in {finding['file']} at line {finding['line']}")

if __name__ == "__main__":
    main()