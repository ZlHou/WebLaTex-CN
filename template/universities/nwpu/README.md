<div align="center">

**西北工业大学本硕博论文 LaTeX 模板**

***NwpuThesis***

[![Test](https://github.com/1195343015/nwputhesis/actions/workflows/test.yml/badge.svg)](https://github.com/1195343015/nwputhesis/actions/workflows/test.yml)
[![TeX Live](https://img.shields.io/badge/TeX%20Live-2025%20%7C%202026-yellow)](https://www.tug.org/texlive/)
[![Nightly Built PDF](https://img.shields.io/badge/Preview-预览PDF_-C9CBFF?style=flat&logo=view&logoColor=D9E0EE&labelColor=302D41)](https://nightly.link/1195343015/nwputhesis/workflows/test/main/nwputhesis-pdf-tl2026.zip)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

</div>

> 强烈推荐使用 Typst 模板 **[modern-npu-thesis](https://github.com/1195343015/modern-npu-thesis)**，语法更简洁，编译更快。

硕博格式符合 [研究生学位论文写作指南](https://gs.nwpu.edu.cn/info/2283/30467.htm)，本科格式符合 [本科毕业设计（论文）撰写规范](https://jiaowu.nwpu.edu.cn/info/1160/24598.htm)。

> **近期更新**：编译产物统一输出到 `build/` 目录，根目录不再产生中间文件；`master.tex` 和 `phd.tex` 已合并为 `graduate.tex`；原根目录 `thesis-body.tex` 已拆分至 `content/thesis/undergraduate/` 和 `content/thesis/graduate/` 下。

## 使用说明

Fork 仓库后 Clone 到本地获取模板。字体自动检测，Windows 用户无需额外操作；非 Windows 用户需克隆字体子模块（`git submodule update --init`）。

### 编译方式

推荐搭配 VS Code 的 LaTeX Workshop 插件：
- **Recipe: xelatex + biber + xelatex x 2**：编译参考文献时使用
- **Recipe: xelatex (fast)**：日常编辑时使用

编译产物统一输出到 `build/` 目录，根目录保持干净。PDF 位于 `build/bachelor.pdf` 或 `build/graduate.pdf`。

![[编译方式]](infra/assets/example.png)

### 入口文件

- `bachelor.tex`：本科毕业设计论文
- `graduate.tex`：硕博学位论文（默认硕士，改 `degree = phd` 编译博士）

### 文件修改说明

用户只需修改 `content/` 下的文件：
- `content/thesis/graduate/`：研究生论文内容（个人信息、摘要、正文、附录、致谢等）
- `content/thesis/undergraduate/`：本科论文内容
- `content/figures/`：论文插图，可直接用文件名引用，如 `\includegraphics{example.png}`

硕博提交最终版时，可将签字版声明扫描为 PDF 替换 [研究生学位论文使用授权声明.pdf](content/figures/研究生学位论文使用授权声明.pdf)。

## QQ交流群

<img src="content/figures/QQ交流群.png" width="200">

## 推荐项目

[awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) | [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)

## 许可证

本项目的硕博格式基于 [Yet-Another-LaTeX-Template-for-NPU-Thesis](https://github.com/NWPUMetaphysicsOffice/Yet-Another-LaTeX-Template-for-NPU-Thesis) 修改，本科格式参考了 [LaTeX-Template-For-NPU-Thesis](https://github.com/polossk/LaTeX-Template-For-NPU-Thesis)、[LaTeX-NewTemplate-For-NPU-undergraduate-Thesis](https://github.com/jialinlvcn/LaTeX-NewTemplate-For-NPU-undergraduate-Thesis) 和 [NWPU-Thesis-Template](https://github.com/lihanshu/NWPU-Thesis-Template)，整体实现参考了 [thuthesis](https://github.com/tuna/thuthesis)。

本项目采用 [GNU General Public License v3.0](LICENSE) 许可证发布。

Copyright (c) 2016-2022 NWPU Metaphysics Office https://github.com/NWPUMetaphysicsOffice

Modified (c) 2026 by Jiayi Yan https://github.com/1195343015
