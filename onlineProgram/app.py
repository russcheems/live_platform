from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/execute', methods=['POST'])
@cross_origin()
def execute_python_code():
    data = request.get_json()
    code = data['code']

    try:
        # 创建一个临时 Python 脚本文件，将用户输入的代码写入其中
        with open('user_code.py', 'w') as f:
            f.write(code)

        # 执行用户代码并捕获输出
        result = subprocess.run(['python', 'user_code.py'], capture_output=True, text=True, check=True)
        output = result.stdout

        return jsonify({'output': output})
    except subprocess.CalledProcessError as e:
        error_output = e.stderr
        return jsonify({'error': error_output})

if __name__ == '__main__':
    app.run(debug=True)
