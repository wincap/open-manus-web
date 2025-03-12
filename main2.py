import sys
import asyncio
import threading


from loguru import logger
import gradio as gr
from app.agent.manus import Manus
from app.logger import logger
from io import StringIO
from pathlib import Path

prompt = ""
prompt_label = None
result_box= None


agent = Manus()

text_value = ""

state = ""
state1 = StringIO()

sys.stdout = state1 
sys.stderr = state1 


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




logger.configure(handlers=[
    {
        "sink": sys.stderr,
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} |<lvl>{level:8}</>| {name} : {module}:{line:4} | <cyan>mymodule</> | - <lvl>{message}</>",
        "colorize": True
    },
])


def sync_values(text,state):
    global state1
    return  state1.getvalue() 

async def greet(name,history):
    global state1
    global state
    global agent

    prompt = name
    print(prompt)

    prompt_lower = prompt.lower()
    if prompt_lower in ["exit", "quit"]:
         logger.info("Goodbye!")
         return "good bye"+state1.getvalue()

    if not prompt.strip():
         logger.warning("Skipping empty prompt.")
         return "good bye" + state1.getvalue()
      
    logger.warning("Processing your request...")
    await  agent.run(prompt)
    state = name+"\n"+state1.getvalue()
    return state

async def main():
    with gr.Blocks() as demo:
        result_box = gr.Textbox(label="推理过程",value=text_value)

        tr = gr.Timer(2)
        tr.tick(sync_values,inputs=[result_box],outputs=[result_box])

        #t = threading.Timer(13, task)  # 3秒后首次执行 
        #t.start()

        search_box = gr.Textbox(label="你想做什么啊")

        search_btn = gr.Button("搜索")
        search_btn.click(fn=greet, inputs=[search_box,result_box],outputs=[result_box])  # 按钮触发‌:ml-citation{ref="1,2" data="citationList"}
        # 指定IP为0.0.0.0（允许外部访问），端口为8000



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


        demo.launch(server_name="0.0.0.0", server_port=8000)

if __name__ == "__main__":
    asyncio.run(main())
