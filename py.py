import gradio as gr
from pathlib import Path
 
def list_files(folder_path):
    """列出指定文件夹下的所有文件"""
    folder_path = Path(folder_path)
    files = ""
    for file in folder_path.rglob('*'):
        files = files + str(file)+"\n"   # rglob 递归地获取所有文件和文件夹
    return files
 
# 指定文件夹路径
folder_path = '/data/OpenManus/code/'  # 替换为你的文件夹路径
 


def get_multiple_files():
    global folder_path
    folder_path = Path(folder_path)
    files = [str(file) for file in folder_path.rglob('*') ]   # rglob 递归地获取所有文件和文件夹
    return files

# 创建 Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("显示本地文件夹下所有文件")
    with gr.Row():
        folder_input = gr.Textbox(label="文件夹路径", value=folder_path)  # 默认值设置为你想要展示的文件夹路径
        show_button = gr.Button("显示文件")
    output = gr.Textbox(label="文件列表")
 
    show_button.click(fn=list_files, inputs=folder_input, outputs=output)
 
    gr.Interface(
        fn=get_multiple_files,
        inputs=None,
        outputs=gr.File(label="批量下载", file_count="multiple"),
        title="多文件下载示例"
    )
demo.launch(server_name="0.0.0.0",server_port = 8000)
