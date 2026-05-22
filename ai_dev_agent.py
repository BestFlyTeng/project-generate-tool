# ai_dev_agent.py
# 真正可运行的多文件 AI 项目生成工具
#
# 功能：
# 1. AI 自动生成多文件项目
# 2. 自动创建目录结构
# 3. 自动写入代码
# 4. 自动生成 README
# 5. 自动 Git 初始化
# 6. 自动上传 GitHub
#
# 支持：
# - FastAPI
# - Flask
# - Next.js
# - React
# - Python工具项目
#
# 安装：
# pip install openai
#
# 使用：
# python ai_dev_agent.py

import os
import json
import subprocess
from openai import OpenAI

# 配置
OPENAI_API_KEY = "OpenAIKey"
GITHUB_USERNAME = "Github用户名"
GITHUB_REPO = "仓库名"
GITHUB_TOKEN = "GithubToken"
MODEL_NAME = "gpt-4.1-mini"

# OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY
)

# 项目目录
PROJECT_DIR = "generated_project"

# 创建文件
def write_file(path, content):

    full_path = os.path.join(PROJECT_DIR, path)

    os.makedirs(
        os.path.dirname(full_path),
        exist_ok=True
    )

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

# AI 生成项目结构
def generate_project(prompt):

    system_prompt = """
你是专业全栈开发工程师。

根据用户需求：

1. 自动设计项目结构
2. 返回完整JSON
3. 包含多个文件
4. 每个文件都必须有完整代码

返回格式：

{
  "files": [
    {
      "path": "main.py",
      "content": "代码"
    }
  ]
}

不要返回markdown。
不要解释。
只返回JSON。
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    return json.loads(content)

# 写入项目
def build_project(project_json):

    files = project_json["files"]

    for file in files:

        path = file["path"]
        content = file["content"]

        print(f"创建文件: {path}")

        write_file(path, content)

# Git 初始化
def git_init():

    subprocess.run(
        ["git", "init"],
        cwd=PROJECT_DIR
    )

    subprocess.run(
        ["git", "add", "."],
        cwd=PROJECT_DIR
    )

    subprocess.run(
        ["git", "commit", "-m", "Initial Commit"],
        cwd=PROJECT_DIR
    )

# 上传 GitHub
def push_github():

    repo_url = (
        f"https://{GITHUB_TOKEN}"
        f"@github.com/"
        f"{GITHUB_USERNAME}/"
        f"{GITHUB_REPO}.git"
    )

    subprocess.run(
        ["git", "branch", "-M", "main"],
        cwd=PROJECT_DIR
    )

    subprocess.run(
        ["git", "remote", "add", "origin", repo_url],
        cwd=PROJECT_DIR
    )

    subprocess.run(
        ["git", "push", "-u", "origin", "main"],
        cwd=PROJECT_DIR
    )

# 主流程
def main():

    print("=" * 50)
    print("AI Multi File Dev Agent")
    print("=" * 50)

    prompt = input("请输入项目需求:\n")

    print("\nAI 正在生成项目...\n")

    project_json = generate_project(prompt)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    build_project(project_json)

    print("\n项目生成完成")

    git_init()

    upload = input("\n是否上传 GitHub？(y/n): ")

    if upload.lower() == "y":

        push_github()

        print("\nGitHub 上传完成")

    print("\n全部完成")

# 启动
if __name__ == "__main__":
    main()