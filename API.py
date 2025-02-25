from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import autopep8

# 初始化 Flask 应用
app = Flask(__name__)

# 加载 CodeLlama 模型
MODEL_NAME = "/usrhome/xiaoyuchen/Desktop/codellama/CodeLlama-7b-Python-hf"
print(f"Loading model: {MODEL_NAME} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
print("Model loaded successfully!")

# 获取代码上下文
def get_context(code, cursor_position, window_size=512):
    """
    获取光标前后的代码片段，用于构造上下文。
    :param code: 当前完整的代码
    :param cursor_position: 光标位置
    :param window_size: 上下文窗口大小
    :return: 光标前的上下文代码片段，光标后的上下文代码片段
    """
    start = max(0, cursor_position - window_size)
    end = min(len(code), cursor_position + window_size)
    return code[start:cursor_position], code[cursor_position:end]

# 调用 CodeLlama 模型生成补全代码
def generate_completion(context_before_cursor, max_length=100):
    """
    使用 CodeLlama 模型生成补全代码
    :param context_before_cursor: 光标前的代码上下文
    :param max_length: 补全的最大长度
    :return: 生成的代码补全
    """
    inputs = tokenizer(context_before_cursor, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.7  # 调整采样温度
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 格式化代码
def format_code(code):
    """
    使用 autopep8 对生成的代码进行格式化
    :param code: 待格式化的代码
    :return: 格式化后的代码
    """
    return autopep8.fix_code(code)

# 定义 API 路由
@app.route('/complete', methods=['POST'])
def complete():
    """
    补全代码 API
    :请求数据: {"code": 当前代码, "cursor_position": 光标位置}
    :返回数据: {"completion": 补全的代码}
    """
    try:
        data = request.json
        code = data.get("code", "")
        cursor_position = data.get("cursor_position", len(code))

        # 获取上下文
        context_before, context_after = get_context(code, cursor_position)

        # 生成补全代码
        completion = generate_completion(context_before)

        # 格式化代码
        formatted_completion = format_code(completion)

        return jsonify({"completion": formatted_completion})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
