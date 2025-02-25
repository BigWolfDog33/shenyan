import gradio as gr
import traceback


def hello_world_fn(username: str) -> tuple[str, str]:
    try:
        return f"HELLO WORLD\n{username.upper()}", "SUCCESS"
    except Exception as e:
        return f"opus! some exception {e}\n{traceback.format_exc()}", "FAILED"
def extract_p_tags(html: str) -> tuple[str, str]:
    try:
        start_tag = "<p>"
        extracted_text = []

        while True:
            # 查找 <p> 标签的开始
            start_idx = html.find(start_tag)
            if start_idx == -1:
                break  # 如果没有找到 <p> 标签，结束循环

            # 提取从 <p> 后开始到下一个 < 的内容
            start_idx += len(start_tag)  # 跳过 <p> 标签本身
            end_idx = html.find('<', start_idx)  # 查找下一个标签的开始位置

            # 如果没有找到下一个标签，提取直到字符串末尾
            if end_idx == -1:
                p_content = html[start_idx:]
            else:
                p_content = html[start_idx:end_idx]

            extracted_text.append(p_content.strip())  # 去掉多余的空格

            # 删除已提取的部分，继续查找下一个 <p> 标签
            html = html[end_idx:]

        if extracted_text:
            return "\n".join(extracted_text), "SUCCESS"
        else:
            return "没有找到 <p> 标签内容", "FAILED"
    
    except Exception as e:
        return f"出现异常：{e}\n{traceback.format_exc()}", "FAILED"

def main() -> None:
    with gr.Blocks(title="DeepLang Data test project") as demo:
        with gr.Tab("hello world 0"):
            raw_input = gr.Textbox(lines=1, placeholder="输入你的名字(英文)", label="")
            pack_output = gr.Textbox(label="输出")
            status_output = gr.Textbox(label="状态信息")

            btn = gr.Button("开始转换")
            btn.click(
                fn=hello_world_fn,
                inputs=raw_input,
                outputs=[pack_output, status_output],
            )

        with gr.Tab("hello world 1"):
            raw_input = gr.Textbox(lines=1, placeholder="输入你的名字(英文)", label="")
            pack_output = gr.Textbox(label="输出")
            status_output = gr.Textbox(label="状态信息")

            btn = gr.Button("开始转换")
            btn.click(
                fn=hello_world_fn,
                inputs=raw_input,
                outputs=[pack_output, status_output],
            )

        with gr.Tab("extract_p_tags"):
            raw_input = gr.Textbox(lines=1, placeholder="输入你的名字(英文)", label="")
            pack_output = gr.Textbox(label="输出")
            status_output = gr.Textbox(label="状态信息")

            btn = gr.Button("开始转换")
            btn.click(
                fn=extract_p_tags,
                inputs=raw_input,
                outputs=[pack_output, status_output],
            )
    demo.queue(default_concurrency_limit=100).launch(
        inline=False,
        debug=False,
        server_name="127.0.0.1",
        server_port=8081,
        show_error=True,
    )


if __name__ == "__main__":
    main()
