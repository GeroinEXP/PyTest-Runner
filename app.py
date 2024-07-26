from flask import Flask, render_template, request, send_from_directory
import subprocess
import os
import json
import sys
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    test_results = None
    if request.method == 'POST':
        test_file = request.form['test_file']
        if test_file.endswith('.py'):
            result = run_tests(test_file)
            output = result['output']
            test_results = result['results']
        else:
            output = "Please select a valid Python test file."
    
    test_files = [f for f in os.listdir('.') if f.endswith('.py') and f.startswith('test_')]
    return render_template('index.html', test_files=test_files, output=output, test_results=test_results)

def run_tests(test_file):
    # Создаем уникальное имя для файла отчета
    report_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Запускаем тесты с дополнительными опциями
    result = subprocess.run([
        sys.executable, '-m', 'pytest', 
        test_file, 
        '--json-report',
        f'--json-report-file={report_file}'
    ], capture_output=True, text=True)

    output = result.stdout + result.stderr

    # Проверяем, был ли создан файл отчета
    if os.path.exists(report_file):
        try:
            with open(report_file, 'r') as f:
                report = json.load(f)
        except json.JSONDecodeError:
            return {'output': output, 'results': [{'name': 'Error', 'outcome': 'error', 'message': 'Failed to parse JSON report'}]}
        finally:
            # Удаляем файл отчета после использования
            os.remove(report_file)
    else:
        return {'output': output, 'results': [{'name': 'Error', 'outcome': 'error', 'message': 'JSON report file was not created'}]}

    # Обрабатываем результаты тестов
    test_results = []
    for test in report.get('tests', []):
        test_result = {
            'name': test.get('nodeid', 'Unknown test'),
            'outcome': test.get('outcome', 'unknown'),
            'message': test.get('call', {}).get('longrepr', ''),
            'duration': test.get('duration', 0)
        }
        test_results.append(test_result)

    return {
        'output': output,
        'results': test_results
    }

if __name__ == '__main__':
    app.run(debug=True)