import os
from pyppeteer import launch
import asyncio
import markdown

html_template = """
<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
<meta http-equiv="Content-type" content="text/html;charset=UTF-8">
{style}
</head>
<body>
{content}
</body>
</html>
""".strip()


def convert_markdown_to_pdf(markdown_str, file_name, output_path=None):
    if output_path is None:
        output_path = os.getcwd()
    content = markdown_str
    html_content = markdown.markdown(content, extensions=['pymdownx.superfences', 'codehilite'])
    title = "test html"
    style = ""
    style_dir = "./styles/"
    style_list = ["markdown-pdf.css", "markdown.css", "tomorrow.css"]
    for style_file in style_list:
        filename = style_dir + style_file
        with open(filename, 'r') as f:
            css = f.read()
        style += '\n<style>\n' + css + '\n</style>\n'
    complete_html = html_template.format(title=title, style=style, content=html_content)

    html_file_path = f"{output_path}/{file_name}.html"
    with open(html_file_path, 'w') as f:
        f.write(complete_html)

    async def html_to_pdf(url, output_path):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url, {'timeout': 0})
        pdf_options = {
            'path': output_path,  # PDF文件保存路径
            'format': 'A4',       # 纸张大小
            'printBackground': True  # 包括背景颜色和图片
        }
        await page.pdf(pdf_options)
        await browser.close()

    # 注意这里的路径要么是文件的本地绝对路径，如 file:///absolute/path/to/file.html
    pdf_file_path = f"{output_path}/{file_name}.pdf"
    asyncio.run(html_to_pdf(f'file://{html_file_path}', pdf_file_path))
