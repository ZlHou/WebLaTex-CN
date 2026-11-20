# WebLaTeX CN

**打开 VS Code 或浏览器，就能开始写中文 LaTeX。**

中文字体、公式、参考文献和编译工具已经配好，无需在自己的电脑上安装 TeX Live。支持保存后自动编译、PDF 预览和 Live Share 协作，也预装了 Node.js 与 Codex CLI。

[快速开始](#快速开始) · [编译第一份中文文档](#编译第一份中文文档) · [模板汇总](#模板汇总) · [使用已有论文](#使用已有论文) · [常见问题](#常见问题) · [构建与维护](.github/MAINTAINING.md)

## 快速开始

选择一种方式即可。**不想安装本地软件，选浏览器；已经使用 VS Code，选本地开发容器。**

### 方式一：浏览器中使用

1. 登录 GitHub，打开 [WebLaTeX CN 仓库](https://github.com/ZlHou/WebLaTex-CN)，使用默认的 **`main`** 分支。
2. 点击 **Code → Codespaces → Create codespace on main**。
3. 等待环境准备完成，浏览器会打开 VS Code，LaTeX Workshop 扩展会自动安装。
4. 打开自带的 [`example.tex`](example.tex)，保存并查看 PDF。

第一次启动需要下载依赖并构建环境，请耐心等待。Codespaces 的可用额度和费用以你的 GitHub 账户为准。

### 方式二：本地 VS Code

准备好 [VS Code](https://code.visualstudio.com/)、正在运行的 [Docker](https://www.docker.com/products/docker-desktop/) 和 [Dev Containers 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)。

1. 打开 [WebLaTeX CN 仓库](https://github.com/ZlHou/WebLaTex-CN)，通过 **Code → Download ZIP** 下载默认的 `main` 分支并解压。
2. 用 VS Code 打开解压后的文件夹。
3. 按 `F1`，执行 **Dev Containers: Reopen in Container**。
4. 等待环境准备完成，打开 [`example.tex`](example.tex) 并保存。

这两种方式都会使用仓库自带的开发容器配置。首次创建会从源码构建；希望直接使用预构建镜像，可按[使用已有论文](#使用已有论文)中的方法配置。

## 编译第一份中文文档

仓库自带 [`example.tex`](example.tex)，涵盖中文摘要、数学公式、科学单位、表格和参考文献，无需额外文件。

1. 打开 `example.tex`。
2. **保存文件**（`Ctrl+S` / `⌘S`），自动使用 XeLaTeX 编译。
3. 完成后，打开 `PDF/example.pdf` 查看结果。

可以直接修改示例开始写作，也可以复制为 `main.tex` 作为自己的入口。在容器终端手动编译示例：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=PDF example.tex
```

| 想做什么 | 操作 |
| --- | --- |
| 查看 PDF | 打开生成的 PDF，或执行 **LaTeX Workshop: View LaTeX PDF file** |
| 手动编译 | 按 `F1`，执行 **LaTeX Workshop: Build LaTeX project** |
| 查看报错 | 打开 **Output / 输出** 面板，选择 **LaTeX Compiler** |
| 切换 LuaLaTeX | 执行 **LaTeX Workshop: Build with recipe**，选择 **latexmk (LuaLaTeX)** |
| 邀请协作 | 点击 **Live Share**，登录并分享会话链接 |

默认使用 **XeLaTeX**。PDF 保存在入口 `.tex` 文件旁的 `PDF/` 文件夹中；例如 `chapters/main.tex` 对应 `chapters/PDF/main.pdf`。

## 目录结构

```text
.
├── example.tex          # 打开、保存，即可编译的中文示例
├── template/            # 中文期刊、基金项目与各高校学位论文 LaTeX 模板汇总
│   ├── README.md        # 模板目录索引与使用说明
│   ├── journals/        # 中文期刊与通用期刊框架模板
│   ├── grants/          # 中国及国际可申请基金项目模板（china/、international/）
│   └── universities/    # 各高校本科/硕士/博士学位论文模板
├── README.md            # 使用指南与模板来源致谢
├── LICENSE              # MIT 许可证
├── .devcontainer/       # 开发容器、Dockerfile、构建白名单和检查脚本
├── .github/             # Actions、维护文档和工作约定
└── .gitignore           # 忽略 PDF 和编译中间文件
```

## 模板汇总

[`template/`](template/README.md) 目录汇总了 **11 个中文期刊 / 通用框架模板**、**19 个基金项目模板**（中国基金 9 个 + 国际可申请基金 10 个）以及 **45 所高校的 53 个学位论文模板**（均直接存放精简后的模板源码并保留各自原始 `LICENSE`，已移除商业/大体积字体文件与非 LaTeX 办公附件）。

- 基金项目分为 `template/grants/china/`（中国内地及香港基金）与 `template/grants/international/`（中国学者/学生可申请的国际基金）。

- 同一高校若单个模板已覆盖 **本科 / 硕士 / 博士** 全部学位层次，直接置于 `template/universities/<高校简称>/`。
- 若模板仅覆盖部分学位层次，则在学校目录下按 `bachelor/`、`master/`、`doctor/`、`master-doctor/` 分设子目录。
- 表中「更新时间」为收录时上游仓库默认分支最近一次提交日期，正式提交前建议对照来源仓库核对最新格式规范。

### 中文期刊模板（11 个）

| 期刊名称 | 英文名称 | 模板目录 | 来源仓库 | 更新时间 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 计算机学报 | Chinese Journal of Computers | [`template/journals/cjc`](template/journals/cjc) | [DaozeTang/CHINESE-JOURNAL-OF-COMPUTERS--Overleaf-Latex-Template](https://github.com/DaozeTang/CHINESE-JOURNAL-OF-COMPUTERS--Overleaf-Latex-Template) | 2026-04-24 | 未声明 |
| 软件学报 | Journal of Software | [`template/journals/jos`](template/journals/jos) | [VansWaston/software-journal-LaTex-Template](https://github.com/VansWaston/software-journal-LaTex-Template) | 2024-12-30 | 未声明 |
| 自动化学报 | Acta Automatica Sinica | [`template/journals/aas`](template/journals/aas) | [Passer-montanus/AAS_Template_LaTeX](https://github.com/Passer-montanus/AAS_Template_LaTeX) | 2023-11-09 | MIT |
| 物理学报 | Acta Physica Sinica | [`template/journals/aps`](template/journals/aps) | [ddddavid-he/LaTeXTemplate_ActaPhysicaSinica](https://github.com/ddddavid-he/LaTeXTemplate_ActaPhysicaSinica) | 2023-01-21 | MIT |
| 中国科学：信息科学 | Scientia Sinica Informationis | [`template/journals/ssi`](template/journals/ssi) | [ProgramFan/ssi-template](https://github.com/ProgramFan/ssi-template) | 2023-04-21 | 未声明 |
| 测绘学报 | Acta Geodaetica et Cartographica Sinica | [`template/journals/agcs`](template/journals/agcs) | [WHULS/LaTeX-AGCS-thesis](https://github.com/WHULS/LaTeX-AGCS-thesis) | 2020-11-25 | 未声明 |
| 机械工程学报 | Chinese Journal of Mechanical Engineering | [`template/journals/cjome`](template/journals/cjome) | [LittleYe233/CJOME-latex-template](https://github.com/LittleYe233/CJOME-latex-template) | 2025-02-28 | 未声明 |
| 航空学报 | Acta Aeronautica et Astronautica Sinica | [`template/journals/aaas`](template/journals/aaas) | [Htallone/AAAS](https://github.com/Htallone/AAAS) | 2019-01-09 | 未声明 |
| 北京航空航天大学学报 | Journal of Beijing University of Aeronautics and Astronautics | [`template/journals/jbuaa`](template/journals/jbuaa) | [Htallone/JBUAA](https://github.com/Htallone/JBUAA) | 2018-08-21 | 未声明 |
| 中国电机工程学报 | Proceedings of the CSEE | [`template/journals/csee`](template/journals/csee) | [SUEPaper/CSEE-LaTeX-template](https://github.com/SUEPaper/CSEE-LaTeX-template) | 2026-10-08 | 未声明 |
| 中文期刊通用模板框架 | General Chinese Journal LaTeX Framework | [`template/journals/chinesejournal`](template/journals/chinesejournal) | [latexstudio/chinesejournal](https://github.com/latexstudio/chinesejournal) | 2019-05-15 | LPPL-1.3c |

### 基金项目模板（19 个）

#### 中国基金项目（9 个）

| 基金项目 | 适用范围 / 资助机构 | 模板目录 | 来源仓库 | 更新时间 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 国家自然科学基金（面地青 A/B/C 类） | 中国内地 · NSFC | [`template/grants/china/nsfc-general`](template/grants/china/nsfc-general) | [fylimas/nsfc](https://github.com/fylimas/nsfc) | 2026-03-05 | 未声明 |
| 国家自然科学基金（面上项目正文） | 中国内地 · NSFC | [`template/grants/china/nsfc-surface`](template/grants/china/nsfc-surface) | [Ruzim/NSFC-application-template-latex](https://github.com/Ruzim/NSFC-application-template-latex) | 2026-01-24 | MIT |
| 国家自然科学基金（青年科学基金 A 类） | 中国内地 · NSFC | [`template/grants/china/nsfc-youth-a`](template/grants/china/nsfc-youth-a) | [Ruzim/NSFC-QA-template-latex](https://github.com/Ruzim/NSFC-QA-template-latex) | 2026-01-25 | MIT |
| 国家自然科学基金（iNSFC 模板） | 中国内地 · NSFC | [`template/grants/china/nsfc-insfc`](template/grants/china/nsfc-insfc) | [YimianDai/iNSFC](https://github.com/YimianDai/iNSFC) | 2026-03-16 | 未声明 |
| 国家自然科学基金（2026 模块化模板） | 中国内地 · NSFC | [`template/grants/china/nsfc-2026`](template/grants/china/nsfc-2026) | [tsingke/NSFC-LaTeX-2026](https://github.com/tsingke/NSFC-LaTeX-2026) | 2026-05-05 | MIT |
| 国家自然科学基金（MCG-NKU 版） | 中国内地 · NSFC | [`template/grants/china/nsfc-nku`](template/grants/china/nsfc-nku) | [MCG-NKU/NSFC-LaTex](https://github.com/MCG-NKU/NSFC-LaTex) | 2026-03-19 | 未声明 |
| 中国科研常用模板集（含国自然等） | 中国内地 · 综合科研基金 | [`template/grants/china/chinese-research-latex`](template/grants/china/chinese-research-latex) | [huangwb8/ChineseResearchLaTeX](https://github.com/huangwb8/ChineseResearchLaTeX) | 2026-11-15 | MIT |
| 博士后研究工作报告（北京大学版） | 中国内地 · 博士后 | [`template/grants/china/postdoc-pku`](template/grants/china/postdoc-pku) | [Jiayin-Gu/PKUreport](https://github.com/Jiayin-Gu/PKUreport) | 2023-03-14 | GPL-3.0 |
| 香港研究资助局 RGC（GRF / ECS） | 中国香港 · RGC | [`template/grants/china/hk-rgc-grf`](template/grants/china/hk-rgc-grf) | [zhiyzuo/HK-RGC-Grant-Proposal-Template](https://github.com/zhiyzuo/HK-RGC-Grant-Proposal-Template) | 2020-10-29 | 未声明 |

#### 国际基金项目（中国学者 / 学生可申请，10 个）

| 基金项目 | 适用范围 / 资助机构 | 模板目录 | 来源仓库 | 更新时间 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 欧盟玛丽·居里博士后基金（MSCA-PF） | 欧盟 · 全球无国籍限制 | [`template/grants/international/eu-msca-pf`](template/grants/international/eu-msca-pf) | [alexfikl/msca-pf](https://github.com/alexfikl/msca-pf) | 2026-11-09 | CC-BY-4.0 |
| 欧盟玛丽·居里博士生网络（MSCA-DN） | 欧盟 · 全球无国籍限制 | [`template/grants/international/eu-msca-dn`](template/grants/international/eu-msca-dn) | [pgarner/msca-dn](https://github.com/pgarner/msca-dn) | 2022-08-01 | 未声明 |
| 欧洲研究理事会启动基金（ERC StG） | 欧盟 · 全球无国籍限制 | [`template/grants/international/eu-erc-stg`](template/grants/international/eu-erc-stg) | [alexfikl/erc-stg](https://github.com/alexfikl/erc-stg) | 2026-11-16 | CC-BY-4.0 |
| 欧盟地平线计划（Horizon Europe RIA/IA） | 欧盟 · 国际合作可申请 | [`template/grants/international/eu-horizon-heria`](template/grants/international/eu-horizon-heria) | [logological/heria](https://github.com/logological/heria) | 2026-08-16 | 未声明 |
| 德国科学基金会项目（DFG Proposal） | 德国 · 赴德/在德学者可申请 | [`template/grants/international/de-dfg`](template/grants/international/de-dfg) | [emtpb/proposal_dfg](https://github.com/emtpb/proposal_dfg) | 2026-02-26 | See LICENSE |
| 美国国家科学基金会（NSF Proposal） | 美国 · 在美机构/合作可申请 | [`template/grants/international/us-nsf`](template/grants/international/us-nsf) | [nsf-open/nsf-proposal-latex-samples](https://github.com/nsf-open/nsf-proposal-latex-samples) | 2026-07-28 | See LICENSE |
| 美国国立卫生研究院（NIH Grant） | 美国 · 在美机构/合作可申请 | [`template/grants/international/us-nih`](template/grants/international/us-nih) | [Noble-Lab/nih-latex](https://github.com/Noble-Lab/nih-latex) | 2023-02-07 | MIT |
| 美国 NIH 博士后奖学金（NIH F32） | 美国 · 博士后项目 | [`template/grants/international/us-nih-f32`](template/grants/international/us-nih-f32) | [c-bun/latex-F32](https://github.com/c-bun/latex-F32) | 2019-02-27 | GPL-3.0 |
| 英国工程与物理科学研究理事会（UKRI/EPSRC） | 英国 · 在英机构/合作可申请 | [`template/grants/international/uk-epsrc`](template/grants/international/uk-epsrc) | [DilhanM/epsrc_latex](https://github.com/DilhanM/epsrc_latex) | 2024-10-25 | MIT |
| 加拿大自然科学与工程研究理事会（NSERC DG） | 加拿大 · 在加机构学者可申请 | [`template/grants/international/ca-nserc`](template/grants/international/ca-nserc) | [aasgreen/NSERC-Application-Latex-Template](https://github.com/aasgreen/NSERC-Application-Latex-Template) | 2011-10-03 | 未声明 |

### 各高校学位论文模板（45 所高校 / 53 个模板）

| 高校 | 学位层次 | 模板目录 | 来源仓库 | 更新时间 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 清华大学 | 本科 / 硕士 / 博士 | [`template/universities/tsinghua`](template/universities/tsinghua) | [tuna/thuthesis](https://github.com/tuna/thuthesis) | 2026-06-18 | LPPL-1.3c |
| 北京大学 | 本科 / 硕士 / 博士 | [`template/universities/peking`](template/universities/peking) | [CasperVector/pkuthss](https://github.com/CasperVector/pkuthss) | 2024-04-20 | 未声明 |
| 上海交通大学 | 本科 / 硕士 / 博士 | [`template/universities/sjtu`](template/universities/sjtu) | [sjtug/SJTUThesis](https://github.com/sjtug/SJTUThesis) | 2026-03-12 | Apache-2.0 |
| 浙江大学 | 本科 / 硕士 / 博士 | [`template/universities/zju`](template/universities/zju) | [TheNetAdmin/zjuthesis](https://github.com/TheNetAdmin/zjuthesis) | 2025-12-07 | MIT |
| 哈尔滨工业大学 | 本科 / 硕士 / 博士 | [`template/universities/hit`](template/universities/hit) | [hithesis/hithesis](https://github.com/hithesis/hithesis) | 2026-10-26 | 未声明 |
| 中国科学技术大学 | 本科 / 硕士 / 博士 | [`template/universities/ustc`](template/universities/ustc) | [ustctug/ustcthesis](https://github.com/ustctug/ustcthesis) | 2026-11-16 | LPPL-1.3c |
| 复旦大学 | 本科 / 硕士 / 博士 | [`template/universities/fudan`](template/universities/fudan) | [stone-zeng/fduthesis](https://github.com/stone-zeng/fduthesis) | 2024-05-06 | LPPL-1.3c |
| 南京大学 | 本科 / 硕士 / 博士 | [`template/universities/nju`](template/universities/nju) | [nju-lug/NJUThesis](https://github.com/nju-lug/NJUThesis) | 2026-06-11 | LPPL-1.3c |
| 武汉大学 | 本科 / 硕士 / 博士 | [`template/universities/whu`](template/universities/whu) | [whutug/whu-thesis](https://github.com/whutug/whu-thesis) | 2025-05-27 | LPPL-1.3c |
| 北京理工大学 | 本科 / 硕士 / 博士 | [`template/universities/bit`](template/universities/bit) | [BITNP/BIThesis](https://github.com/BITNP/BIThesis) | 2026-10-03 | LPPL-1.3c |
| 西安电子科技大学 | 本科 / 硕士 / 博士 | [`template/universities/xdu`](template/universities/xdu) | [note286/xduts](https://github.com/note286/xduts) | 2025-05-04 | LPPL-1.3c |
| 西北工业大学 | 本科 / 硕士 / 博士 | [`template/universities/nwpu`](template/universities/nwpu) | [1195343015/nwputhesis](https://github.com/1195343015/nwputhesis) | 2026-10-04 | GPL-3.0 |
| 东北大学 | 本科 / 硕士 / 博士 | [`template/universities/neu`](template/universities/neu) | [sci-m-wang/NEU-Thesis](https://github.com/sci-m-wang/NEU-Thesis) | 2026-11-16 | Apache-2.0 |
| 南京航空航天大学 | 本科 / 硕士 / 博士 | [`template/universities/nuaa`](template/universities/nuaa) | [nuaatug/nuaathesis](https://github.com/nuaatug/nuaathesis) | 2026-05-31 | Apache-2.0 |
| 重庆大学 | 本科 / 硕士 / 博士 | [`template/universities/cqu`](template/universities/cqu) | [nanmu42/CQUThesis](https://github.com/nanmu42/CQUThesis) | 2026-06-22 | LPPL-1.3c |
| 合肥工业大学 | 本科 / 硕士 / 博士 | [`template/universities/hfut`](template/universities/hfut) | [HFUTTUG/HFUT_Thesis](https://github.com/HFUTTUG/HFUT_Thesis) | 2026-05-22 | LPPL-1.3c |
| 兰州大学 | 本科 / 硕士 / 博士 | [`template/universities/lzu`](template/universities/lzu) | [yuhldr/LZUThesis2020](https://github.com/yuhldr/LZUThesis2020) | 2026-03-11 | See LICENSE |
| 中国人民大学 | 本科 / 硕士 / 博士 | [`template/universities/ruc`](template/universities/ruc) | [ZebinWang/ructhesis](https://github.com/ZebinWang/ructhesis) | 2016-12-21 | 未声明 |
| 广东工业大学 | 本科 / 硕士 / 博士 | [`template/universities/gdut`](template/universities/gdut) | [sikouhjw/gdutthesis](https://github.com/sikouhjw/gdutthesis) | 2024-03-26 | LPPL-1.3c |
| 山东大学 | 本科 / 硕士 / 博士 | [`template/universities/sdu`](template/universities/sdu) | [Liam0205/sduthesis](https://github.com/Liam0205/sduthesis) | 2026-05-04 | LPPL-1.3c |
| 北京师范大学 | 本科 / 硕士 / 博士 | [`template/universities/bnu`](template/universities/bnu) | [jinyiliu/bnu-thesis-template](https://github.com/jinyiliu/bnu-thesis-template) | 2025-03-03 | 未声明 |
| 东南大学 | 本科 / 硕士 / 博士 | [`template/universities/seu`](template/universities/seu) | [zhimengfan1990/seuthesix](https://github.com/zhimengfan1990/seuthesix) | 2023-03-19 | 未声明 |
| 中国科学院大学 | 硕士 / 博士 | [`template/universities/ucas/master-doctor`](template/universities/ucas/master-doctor) | [mohuangrui/ucasthesis](https://github.com/mohuangrui/ucasthesis) | 2021-10-29 | 未声明 |
| 北京航空航天大学 | 本科 | [`template/universities/buaa/bachelor`](template/universities/buaa/bachelor) | [BHOSC/BUAAthesis](https://github.com/BHOSC/BUAAthesis) | 2025-01-12 | LPPL-1.3c |
| 北京航空航天大学 | 硕士 / 博士 | [`template/universities/buaa/master-doctor`](template/universities/buaa/master-doctor) | [CheckBoxStudio/BUAAThesis](https://github.com/CheckBoxStudio/BUAAThesis) | 2024-02-01 | MIT |
| 电子科技大学 | 硕士 / 博士 | [`template/universities/uestc/master-doctor`](template/universities/uestc/master-doctor) | [bdebye/thesisuestc](https://github.com/bdebye/thesisuestc) | 2026-06-17 | 未声明 |
| 中山大学 | 本科 | [`template/universities/sysu/bachelor`](template/universities/sysu/bachelor) | [SYSU-SCC/sysu-thesis](https://github.com/SYSU-SCC/sysu-thesis) | 2026-09-04 | GPL-3.0 |
| 华南理工大学 | 硕士 / 博士 | [`template/universities/scut/master-doctor`](template/universities/scut/master-doctor) | [mengchaoheng/SCUT_thesis](https://github.com/mengchaoheng/SCUT_thesis) | 2026-08-03 | GPL-3.0 |
| 同济大学 | 本科 | [`template/universities/tongji/bachelor`](template/universities/tongji/bachelor) | [TJ-CSCCG/TongjiThesis](https://github.com/TJ-CSCCG/TongjiThesis) | 2026-10-30 | LPPL-1.3c |
| 同济大学 | 硕士 / 博士 | [`template/universities/tongji/master-doctor`](template/universities/tongji/master-doctor) | [wyqy/TongjiThesis_Proto](https://github.com/wyqy/TongjiThesis_Proto) | 2025-03-06 | 未声明 |
| 西安交通大学 | 硕士 / 博士 | [`template/universities/xjtu/master-doctor`](template/universities/xjtu/master-doctor) | [obster-y/XJTU-thesis](https://github.com/obster-y/XJTU-thesis) | 2026-02-03 | LPPL-1.3c |
| 中南大学 | 硕士 / 博士 | [`template/universities/csu/master-doctor`](template/universities/csu/master-doctor) | [CSUcse/CSUthesis](https://github.com/CSUcse/CSUthesis) | 2025-04-02 | 未声明 |
| 北京邮电大学 | 本科 | [`template/universities/bupt/bachelor`](template/universities/bupt/bachelor) | [sheng-qiang/BUPTBachelorThesis](https://github.com/sheng-qiang/BUPTBachelorThesis) | 2021-05-02 | MIT |
| 北京邮电大学 | 硕士 / 博士 | [`template/universities/bupt/master-doctor`](template/universities/bupt/master-doctor) | [jjfu99/BUPTGraduateThesisLatexTemplate](https://github.com/jjfu99/BUPTGraduateThesisLatexTemplate) | 2026-06-02 | GPL-3.0 |
| 天津大学 | 硕士 / 博士 | [`template/universities/tju/master-doctor`](template/universities/tju/master-doctor) | [xnth97/TJUThesisLatexTemplate](https://github.com/xnth97/TJUThesisLatexTemplate) | 2024-05-29 | GPL-3.0 |
| 国防科技大学 | 硕士 / 博士 | [`template/universities/nudt/master-doctor`](template/universities/nudt/master-doctor) | [liubenyuan/nudtpaper](https://github.com/liubenyuan/nudtpaper) | 2026-10-13 | 未声明 |
| 南方科技大学 | 本科 | [`template/universities/sustech/bachelor`](template/universities/sustech/bachelor) | [iydon/sustechthesis](https://github.com/iydon/sustechthesis) | 2026-08-15 | LPPL-1.3c |
| 南方科技大学 | 硕士 / 博士 | [`template/universities/sustech/master-doctor`](template/universities/sustech/master-doctor) | [SUSTech-CRA/sustech-master-thesis](https://github.com/SUSTech-CRA/sustech-master-thesis) | 2026-11-15 | LPPL-1.3c |
| 华中科技大学 | 本科 | [`template/universities/hust/bachelor`](template/universities/hust/bachelor) | [skinaze/HUSTPaperTemp](https://github.com/skinaze/HUSTPaperTemp) | 2022-04-11 | MIT |
| 华中科技大学 | 博士 | [`template/universities/hust/doctor`](template/universities/hust/doctor) | [XinzeZhang/HUST-PhD-Thesis-Latex](https://github.com/XinzeZhang/HUST-PhD-Thesis-Latex) | 2026-09-06 | 未声明 |
| 华南师范大学 | 硕士 / 博士 | [`template/universities/scnu/master-doctor`](template/universities/scnu/master-doctor) | [scnu/scnuthesis](https://github.com/scnu/scnuthesis) | 2024-12-30 | 未声明 |
| 厦门大学 | 硕士 / 博士 | [`template/universities/xmu/master-doctor`](template/universities/xmu/master-doctor) | [zoam/xmu-thesis-grd](https://github.com/zoam/xmu-thesis-grd) | 2025-06-28 | 未声明 |
| 四川大学 | 硕士 / 博士 | [`template/universities/scu/master-doctor`](template/universities/scu/master-doctor) | [kevinleeex/scu_thesis_2020](https://github.com/kevinleeex/scu_thesis_2020) | 2022-06-08 | 未声明 |
| 上海大学 | 本科 | [`template/universities/shu/bachelor`](template/universities/shu/bachelor) | [shuosc/SHU-Bachelor-Thesis-OSC](https://github.com/shuosc/SHU-Bachelor-Thesis-OSC) | 2026-01-19 | 未声明 |
| 南开大学 | 硕士 / 博士 | [`template/universities/nku/master-doctor`](template/universities/nku/master-doctor) | [NewFuture/NKThesis](https://github.com/NewFuture/NKThesis) | 2025-05-06 | MIT |
| 吉林大学 | 本科 | [`template/universities/jlu/bachelor`](template/universities/jlu/bachelor) | [Jackknifer/jluthesis-template](https://github.com/Jackknifer/jluthesis-template) | 2026-04-24 | MIT |
| 吉林大学 | 硕士 / 博士 | [`template/universities/jlu/master-doctor`](template/universities/jlu/master-doctor) | [maxuewei2/JLUThesis2020](https://github.com/maxuewei2/JLUThesis2020) | 2026-07-24 | 未声明 |
| 大连理工大学 | 本科 | [`template/universities/dlut/bachelor`](template/universities/dlut/bachelor) | [Anplus/DUT-Bachelor-Thesis-Latex-Template](https://github.com/Anplus/DUT-Bachelor-Thesis-Latex-Template) | 2017-06-26 | 未声明 |
| 大连理工大学 | 硕士 | [`template/universities/dlut/master`](template/universities/dlut/master) | [01xz/dlut-thesis](https://github.com/01xz/dlut-thesis) | 2025-03-14 | LPPL-1.3c |
| 湖南大学 | 本科 | [`template/universities/hnu/bachelor`](template/universities/hnu/bachelor) | [leaf-hsiao/HNUThesisTemplate](https://github.com/leaf-hsiao/HNUThesisTemplate) | 2019-12-11 | 未声明 |
| 湖南大学 | 硕士 | [`template/universities/hnu/master`](template/universities/hnu/master) | [WhiteByeBye/HNUThesisTemplate-Master](https://github.com/WhiteByeBye/HNUThesisTemplate-Master) | 2022-09-20 | 未声明 |
| 台湾大学 | 硕士 / 博士 | [`template/universities/ntu-tw/master-doctor`](template/universities/ntu-tw/master-doctor) | [Hsins/NTU-Thesis-LaTeX-Template](https://github.com/Hsins/NTU-Thesis-LaTeX-Template) | 2024-08-13 | MIT |
| 台湾成功大学 | 硕士 / 博士 | [`template/universities/ncku-tw/master-doctor`](template/universities/ncku-tw/master-doctor) | [wengan-li/ncku-thesis-template-latex](https://github.com/wengan-li/ncku-thesis-template-latex) | 2026-11-15 | CC-BY-4.0 |

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

这是宿主机的沙箱权限限制，处理方法见[构建与维护](.github/MAINTAINING.md#codex-沙箱)。

## 致谢与许可

写作体验参考 [WebLaTeX](https://github.com/sanjib-sen/WebLaTex)，结合 VS Code、Codespaces 和 LaTeX Workshop，为中文科技写作提供预配置环境。

衷心感谢[模板汇总](#模板汇总)中收录的所有中文期刊、科研基金与高校学位论文 LaTeX 模板的原作者、各高校 TeX 用户组（TUG）及开源社区维护者，各模板的来源仓库均已在上表逐一标注。模板清单整理亦参考了以下开源索引项目：

- [1195343015/cn-university-latex-thesis-templates](https://github.com/1195343015/cn-university-latex-thesis-templates)
- [hantang/latex-templates](https://github.com/hantang/latex-templates)

[MIT License](LICENSE) · Copyright (c) 2026 ZlHou

第三方软件、字体、基础镜像以及 `template/` 目录下的各模板源码均遵循其来源仓库各自的许可证。
