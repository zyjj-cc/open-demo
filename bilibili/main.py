import os
from io import BytesIO
from zyjj_open_sdk import Client
import gradio as gr
import requests
from PIL import Image
from uuid import uuid4

client = Client(os.getenv('sk'))

# 获取链接内容
def get_content(url: str) -> bytes:
    return requests.get(url).content

# byte转图片
def bytes_to_image(bytes_data: bytes) -> Image:
    return Image.open(BytesIO(bytes_data))

def pic_parse(url: str):
    img_url = client.tool.bili_pic_parse(url).execute().img_url
    return bytes_to_image(get_content(img_url))

def sub_download(url: str):
    sub_list = client.tool.bili_subtitle_download(url).execute().subtitle
    return [[sub.name, f"[点击下载]({sub.url})"] for sub in sub_list]

def danmu_download(url: str, _format: str):
    danmu = client.tool.bili_danmu_download(url, _format).execute().danmu
    path = f"{uuid4()}.{_format}"
    with open(path, "wb") as f:
        f.write(get_content(danmu))
    return path

def video_summary(url: str):
    return client.tool.bili_video_summary(url).execute().text

def comment_cloud(url: str):
    img_url = client.tool.bili_comment_cloud(url).execute().img_url
    return bytes_to_image(get_content(img_url))


def ui_build():
    with gr.Blocks() as demo:
        demo.title = '智游剪辑-B站demo演示'
        with gr.Tab("封面解析"):
            with gr.Row():
                with gr.Column():
                    url = gr.Text(label="视频链接", placeholder="输入B站视频链接")
                    pic_parse_btn = gr.Button(value="立即解析")
                with gr.Column():
                    pic = gr.Image(label="封面信息", sources=None)
                pic_parse_btn.click(pic_parse, inputs=url, outputs=pic)
        with gr.Tab("字幕下载"):
            with gr.Row():
                with gr.Column():
                    url2 = gr.Text(label="视频链接", placeholder="输入B站视频链接")
                    sub_download_btn = gr.Button(value="立即解析")
                with gr.Column():
                    sub_view = gr.Dataframe(
                        label="字幕列表",
                        headers=["字幕名称", "下载链接"],
                        datatype=["str", "markdown"],
                    )
                sub_download_btn.click(sub_download, inputs=url2, outputs=sub_view)
        with gr.Tab("弹幕下载"):
            with gr.Row():
                with gr.Column():
                    url3 = gr.Text(label="视频链接", placeholder="输入B站视频链接")
                    _format = gr.Dropdown(label="字幕格式", choices=[
                        ("xml(原始格式)", "xml"),
                        ("txt(文本格式)", "txt"),
                        ("str(字幕格式)", "str"),
                        ("json(json格式)", "json")
                    ])
                    danmu_download_btn = gr.Button(value="立即解析")
                with gr.Column():
                    danmu_view = gr.File(label="弹幕文件")
                danmu_download_btn.click(danmu_download, inputs=[url3, _format], outputs=danmu_view)
        with gr.Tab("视频总结"):
            with gr.Row():
                with gr.Column():
                    url4 = gr.Text(label="视频链接", placeholder="输入B站视频链接")
                    video_summary_btn = gr.Button(value="立即总结")
                with gr.Column():
                    summary_text = gr.Markdown(label="总结结果", container=True, height=300, show_copy_button=True)
                video_summary_btn.click(video_summary, inputs=url4, outputs=summary_text)
        with gr.Tab("评论词云"):
            with gr.Row():
                with gr.Column():
                    url5 = gr.Text(label="视频链接", placeholder="输入B站视频链接")
                    comment_cloud_btn = gr.Button(value="立即生成")
                with gr.Column():
                    pic = gr.Image(label="词云数据", sources=None)
                comment_cloud_btn.click(comment_cloud, inputs=url5, outputs=pic)
        demo.launch()


import signal
import sys

def signal_handler(sig, frame):
    print("程序正在退出...")
    # 在这里可以添加清理代码
    client.close()
    sys.exit(0)


# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)  # 捕获 Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # 捕获终止信号

if __name__ == '__main__':
    ui_build()

    # demo = gr.Interface(
    #     title="智游剪辑-B站demo",
    #     fn=submit_task,
    #     inputs=[
    #         gr.Text(label="视频链接", placeholder="输入B站视频链接"),
    #         gr.Dropdown([
    #             ("封面解析", 1),
    #             ("字幕下载", 2),
    #             ("弹幕下载", 3),
    #             ("视频总结", 4),
    #         ], label="下载内容")
    #     ],
    #     outputs=["text"],
    # )


