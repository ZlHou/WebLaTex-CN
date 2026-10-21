# WebLaTeX CN

**打开 VS Code 或浏览器，就能开始写中文 LaTeX。**

中文字体、公式、参考文献和编译工具已经配好，无需在自己的电脑上安装 TeX Live。支持保存后自动编译、PDF 预览和 Live Share 协作，也预装了 Node.js 与 Codex CLI。

[快速开始](#快速开始) · [编译第一份中文文档](#编译第一份中文文档) · [使用已有论文](#使用已有论文) · [常见问题](#常见问题) · [构建与维护](docs/MAINTAINING.md)

## 快速开始

选择一种方式即可。**不想安装本地软件，选浏览器；已经使用 VS Code，选本地开发容器。**

### 方式一：浏览器中使用

1. 登录 GitHub，打开 [WebLaTeX CN 仓库](https://github.com/ZlHou/WebLaTex-CN)，使用默认的 **`main`** 分支。
2. 点击 **Code → Codespaces → Create codespace on main**。
3. 等待环境准备完成，浏览器会打开 VS Code，LaTeX Workshop 扩展会自动安装。
4. 按下方示例创建 `main.tex`，开始写作。

第一次启动需要下载依赖并构建环境，请耐心等待。Codespaces 的可用额度和费用以你的 GitHub 账户为准。

### 方式二：本地 VS Code

准备好 [VS Code](https://code.visualstudio.com/)、正在运行的 [Docker](https://www.docker.com/products/docker-desktop/) 和 [Dev Containers 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)。

1. 打开 [WebLaTeX CN 仓库](https://github.com/ZlHou/WebLaTex-CN)，通过 **Code → Download ZIP** 下载默认的 `main` 分支并解压。
2. 用 VS Code 打开解压后的文件夹。
3. 按 `F1`，执行 **Dev Containers: Reopen in Container**。
4. 等待环境准备完成，按下方示例创建 `main.tex`。

这两种方式都会使用仓库自带的开发容器配置。首次创建会从源码构建；希望直接使用预构建镜像，可按[使用已有论文](#使用已有论文)中的方法配置。

## 编译第一份中文文档

在工作区根目录新建 `main.tex`，粘贴以下内容：

```tex
\documentclass[UTF8,fontset=fandol]{ctexart}
\usepackage{amsmath}
\usepackage{siunitx}

\title{我的第一份中文科技文档}
\author{作者}
\date{\today}

\begin{document}
\maketitle

\section{开始写作}
中文、English、数学公式和科学单位可以一起使用。
\[
  E = mc^2, \qquad \int_0^1 x^2\,\mathrm{d}x = \frac{1}{3}.
\]
实验温度为 \qty{300}{\kelvin}。

\end{document}
```

**保存文件**（`Ctrl+S` / `⌘S`）即可自动编译。完成后，打开 `PDF/main.pdf` 查看结果。

| 想做什么 | 操作 |
| --- | --- |
| 查看 PDF | 打开生成的 PDF，或执行 **LaTeX Workshop: View LaTeX PDF file** |
| 手动编译 | 按 `F1`，执行 **LaTeX Workshop: Build LaTeX project** |
| 查看报错 | 打开 **Output / 输出** 面板，选择 **LaTeX Compiler** |
| 切换 LuaLaTeX | 执行 **LaTeX Workshop: Build with recipe**，选择 **latexmk (LuaLaTeX)** |
| 邀请协作 | 点击 **Live Share**，登录并分享会话链接 |

默认使用 **XeLaTeX**。PDF 保存在入口 `.tex` 文件旁的 `PDF/` 文件夹中；例如 `chapters/main.tex` 对应 `chapters/PDF/main.pdf`。

## 使用已有论文

### 给自己的仓库接入写作环境

1. 将本项目的 [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) 复制到自己论文仓库的同一路径。
2. 将文件中的整个 `build` 字段替换为 `image` 字段，其他设置保留：

   ```json
   "image": "ghcr.io/zlhou/weblatex-cn:latest"
   ```

3. 在 VS Code 中执行 **Dev Containers: Reopen in Container**；若已在容器中，执行 **Dev Containers: Rebuild Container**。也可以为自己的仓库创建 Codespace。
4. 打开论文入口文件并保存，等待编译完成。

这样会直接拉取配好的镜像，无需复制 Dockerfile 或自行安装编译工具。若论文有多个 `.tex` 文件，可在章节文件顶部注明入口，例如：

```tex
% !TeX root = ../main.tex
```

### 只想用命令行编译

在自己的论文目录运行以下命令（Linux / macOS shell）：

```bash
docker run --rm -it \
  --mount "type=bind,src=$PWD,dst=/workspaces/paper" \
  --workdir /workspaces/paper \
  ghcr.io/zlhou/weblatex-cn:latest \
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=PDF main.tex
```

把 `main.tex` 换成自己的入口文件；需要 LuaLaTeX 时，将 `-xelatex` 换成 `-lualatex`。生成的 PDF 会保存在自己电脑上当前目录的 `PDF/` 中。

## 环境里有什么

| 用途 | 已安装 |
| --- | --- |
| 中文写作 | UTF-8、CTeX、xeCJK、Fandol、Noto CJK |
| 编译与排版 | XeLaTeX、LuaLaTeX、latexmk、latexindent |
| 数学与绘图 | AMS、unicode-math、siunitx、算法环境、TikZ、PGFPlots |
| 参考文献 | BibTeX、Biber、BibLaTeX、natbib、GB/T 7714-2015 样式 |
| 字体 | TeX Gyre、XITS / XITS Math、TeX Live 扩展字体 |
| 开发与协作 | Node.js 24、npm、Python 3、Git、Live Share、Codex CLI |

在容器终端运行 `codex`，按提示登录后即可使用。也可以用 `npm install --global 包名` 安装其他 CLI，无需 `sudo`。Codex 的安装和使用方式见 [OpenAI 官方文档](https://developers.openai.com/codex/cli)。

## 常见问题

**保存后没有生成 PDF？**

确认 VS Code 已连接到开发容器，LaTeX Workshop 已启用，并打开入口 `.tex` 文件。先手动运行 **Build LaTeX project**，再到 **LaTeX Compiler** 查看错误信息。首次启动或首次加载字体可能较慢。

**提示找不到宋体、黑体或 Times New Roman？**

示例使用镜像自带的 Fandol 字体。已有模板若指定了商业字体，需要改用 Fandol / Noto / TeX Gyre，或自行提供有授权的字体，并按模板要求设置字体路径。

**参考文献没有更新？**

先检查 `.bib` 路径、引用键和编译日志，再用 `latexmk` 重新编译；它会按文档配置调用 BibTeX 或 Biber。不要只运行一次 `xelatex` 就结束编译。

**拉取镜像提示 `denied` 或 `unauthorized`？**

确认地址为 `ghcr.io/zlhou/weblatex-cn:latest`。公开镜像无需登录；私有镜像需要先执行 `docker login ghcr.io`，并拥有读取权限。维护者可在 GitHub Packages 中将镜像可见性设为 Public。

**Docker 提示没有权限写入 PDF？**

优先使用 Dev Containers，它会自动对齐 Linux 用户 UID。手动执行 `docker run` 时，可在镜像名之前添加 `--user "$(id -u):$(id -g)" --env HOME=/tmp`，让编译使用自己的 UID/GID。

**Mac 的 Apple 芯片能用吗？**

当前发布并验证的镜像为 `linux/amd64`。可使用 Docker 的 amd64 模拟运行，速度可能较慢；命令行需在镜像名之前添加 `--platform linux/amd64`。也可以从源码构建 ARM 镜像，但该架构尚未经过本项目 CI 验证。

**Codex 提示无法创建 namespace？**

这是宿主机的沙箱权限限制，处理方法见[构建与维护](docs/MAINTAINING.md#codex-沙箱)。

## 致谢与许可

写作体验参考 [WebLaTeX](https://github.com/sanjib-sen/WebLaTex)，结合 VS Code、Codespaces 和 LaTeX Workshop，为中文科技写作提供预配置环境。

[MIT License](LICENSE) · Copyright (c) 2026 ZlHou

第三方软件、字体和基础镜像遵循各自的许可证。
