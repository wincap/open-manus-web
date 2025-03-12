import gradio as gr

def append_text(new_input, history=""):
    updated_history = history + new_input + "\n"
    return updated_history, updated_history  # 更新输出框和状态存储

with  gr.Blocks() as app:
    with gr.Row():
        input_box = gr.Textbox(label="输入内容", placeholder="输入内容后点击按钮叠加")
        submit_btn = gr.Button("叠加内容", variant="primary")
    
    output_box = gr.Textbox(label="叠加结果", interactive=False, lines=8)
    history = gr.State(value="")  # 初始化空状态

    submit_btn.click(
        fn=append_text,
        inputs=[input_box, history],
        outputs=[output_box, history]
    )

app.launch(server_name='0.0.0.0', server_port=8080)

