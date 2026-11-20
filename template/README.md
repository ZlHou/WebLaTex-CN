# 中文期刊、基金项目与各高校学位论文 LaTeX 模板汇总

本目录汇总了 **11 个中文期刊 / 通用框架模板**、**19 个基金项目模板**（含中国基金 9 个与国际可申请基金 10 个）以及 **45 所高校的 53 个学位论文模板**（均直接存放精简后的模板源码，保留各上游仓库的原始 `LICENSE` 与说明文档）。

## 目录组织规范

- `journals/<期刊简称>/`：中文期刊与通用期刊框架模板。
- `grants/china/<项目简称>/`：中国内地及中国香港地区科研基金与博士后报告模板（如国家自然科学基金 NSFC、香港 RGC GRF/ECS 等）。
- `grants/international/<地区-项目简称>/`：中国学者/学生可申请的国际科研基金模板（如欧盟 MSCA / ERC / Horizon Europe、德国 DFG、美国 NSF / NIH、英国 UKRI/EPSRC、加拿大 NSERC 等）。
- `universities/<高校简称>/`：若同一上游模板同时覆盖 **本科 / 硕士 / 博士** 全部三个学位层次，则直接置于该高校目录下。
- `universities/<高校简称>/<bachelor|master|doctor|master-doctor>/`：若同一高校的模板未包含全部学位层次，则在学校目录下按学位层次分设子目录，便于后续补充与区分。

## 使用说明

1. 在 WebLaTeX CN（Codespaces 或本地 Dev Container）中打开目标模板目录，阅读该目录下的 `README.md` 确认主入口 `.tex` 文件（如 `main.tex`、`thesis.tex`、`example.tex`）及编译方式。
2. 中文模板默认推荐使用 **XeLaTeX** 配合 `latexmk` 编译；英文国际基金模板可使用 **XeLaTeX** 或 **pdfLaTeX**，部分模板提供 `Makefile` 或 `latexmkrc`，可直接按其文档执行。
3. **字体与体积说明**：为遵守开源合规并控制仓库体积，收录时已移除各上游仓库中附带的商业/大体积字体文件（`.ttf` / `.otf` / `.ttc`）及非 LaTeX 的 Word/PSD 附件。请优先使用镜像预装的 **Fandol / Noto CJK / TeX Gyre** 字体（多数现代模板支持 `fontset=fandol` 或 `fontset=ubuntu`），或在需要商业字体时自行按上游仓库说明配置。
4. **版本核对**：下表标注的「更新时间」为收录时上游仓库默认分支最近一次提交日期（`YYYY-MM-DD`）。正式投稿、申报基金或提交学位论文前，请务必对照对应机构/期刊/学校当年的最新官方通知与 Word/PDF 规范核对格式细节。

## 中文期刊模板（11 个）

| 期刊名称 | 英文名称 | 模板目录 | 来源仓库 | 更新时间 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 计算机学报 | Chinese Journal of Computers | [`journals/cjc`](journals/cjc) | [DaozeTang/CHINESE-JOURNAL-OF-COMPUTERS--Overleaf-Latex-Template](https://github.com/DaozeTang/CHINESE-JOURNAL-OF-COMPUTERS--Overleaf-Latex-Template) | 2026-04-24 | 未声明 |
| 软件学报 | Journal of Software | [`journals/jos`](journals/jos) | [VansWaston/software-journal-LaTex-Template](https://github.com/VansWaston/software-journal-LaTex-Template) | 2024-12-30 | 未声明 |
| 自动化学报 | Acta Automatica Sinica | [`journals/aas`](journals/aas) | [Passer-montanus/AAS_Template_LaTeX](https://github.com/Passer-montanus/AAS_Template_LaTeX) | 2023-11-09 | MIT |
| 物理学报 | Acta Physica Sinica | [`journals/aps`](journals/aps) | [ddddavid-he/LaTeXTemplate_ActaPhysicaSinica](https://github.com/ddddavid-he/LaTeXTemplate_ActaPhysicaSinica) | 2023-01-21 | MIT |
| 中国科学：信息科学 | Scientia Sinica Informationis | [`journals/ssi`](journals/ssi) | [ProgramFan/ssi-template](https://github.com/ProgramFan/ssi-template) | 2023-04-21 | 未声明 |
| 测绘学报 | Acta Geodaetica et Cartographica Sinica | [`journals/agcs`](journals/agcs) | [WHULS/LaTeX-AGCS-thesis](https://github.com/WHULS/LaTeX-AGCS-thesis) | 2020-11-25 | 未声明 |
| 机械工程学报 | Chinese Journal of Mechanical Engineering | [`journals/cjome`](journals/cjome) | [LittleYe233/CJOME-latex-template](https://github.com/LittleYe233/CJOME-latex-template) | 2025-02-28 | 未声明 |
| 航空学报 | Acta Aeronautica et Astronautica Sinica | [`journals/aaas`](journals/aaas) | [Htallone/AAAS](https://github.com/Htallone/AAAS) | 2019-01-09 | 未声明 |
| 北京航空航天大学学报 | Journal of Beijing University of Aeronautics and Astronautics | [`journals/jbuaa`](journals/jbuaa) | [Htallone/JBUAA](https://github.com/Htallone/JBUAA) | 2018-08-21 | 未声明 |
| 中国电机工程学报 | Proceedings of the CSEE | [`journals/csee`](journals/csee) | [SUEPaper/CSEE-LaTeX-template](https://github.com/SUEPaper/CSEE-LaTeX-template) | 2026-10-08 | 未声明 |
| 中文期刊通用模板框架 | General Chinese Journal LaTeX Framework | [`journals/chinesejournal`](journals/chinesejournal) | [latexstudio/chinesejournal](https://github.com/latexstudio/chinesejournal) | 2019-05-15 | LPPL-1.3c |

## 基金项目模板（19 个）

### 中国基金项目（9 个）

| 基金项目 | 适用范围 / 资助机构 | 模板目录 | 来源仓库 | 更新时间 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 国家自然科学基金（面地青 A/B/C 类） | 中国内地 · NSFC | [`grants/china/nsfc-general`](grants/china/nsfc-general) | [fylimas/nsfc](https://github.com/fylimas/nsfc) | 2026-03-05 | 未声明 |
| 国家自然科学基金（面上项目正文） | 中国内地 · NSFC | [`grants/china/nsfc-surface`](grants/china/nsfc-surface) | [Ruzim/NSFC-application-template-latex](https://github.com/Ruzim/NSFC-application-template-latex) | 2026-01-24 | MIT |
| 国家自然科学基金（青年科学基金 A 类） | 中国内地 · NSFC | [`grants/china/nsfc-youth-a`](grants/china/nsfc-youth-a) | [Ruzim/NSFC-QA-template-latex](https://github.com/Ruzim/NSFC-QA-template-latex) | 2026-01-25 | MIT |
| 国家自然科学基金（iNSFC 模板） | 中国内地 · NSFC | [`grants/china/nsfc-insfc`](grants/china/nsfc-insfc) | [YimianDai/iNSFC](https://github.com/YimianDai/iNSFC) | 2026-03-16 | 未声明 |
| 国家自然科学基金（2026 模块化模板） | 中国内地 · NSFC | [`grants/china/nsfc-2026`](grants/china/nsfc-2026) | [tsingke/NSFC-LaTeX-2026](https://github.com/tsingke/NSFC-LaTeX-2026) | 2026-05-05 | MIT |
| 国家自然科学基金（MCG-NKU 版） | 中国内地 · NSFC | [`grants/china/nsfc-nku`](grants/china/nsfc-nku) | [MCG-NKU/NSFC-LaTex](https://github.com/MCG-NKU/NSFC-LaTex) | 2026-03-19 | 未声明 |
| 中国科研常用模板集（含国自然等） | 中国内地 · 综合科研基金 | [`grants/china/chinese-research-latex`](grants/china/chinese-research-latex) | [huangwb8/ChineseResearchLaTeX](https://github.com/huangwb8/ChineseResearchLaTeX) | 2026-11-15 | MIT |
| 博士后研究工作报告（北京大学版） | 中国内地 · 博士后 | [`grants/china/postdoc-pku`](grants/china/postdoc-pku) | [Jiayin-Gu/PKUreport](https://github.com/Jiayin-Gu/PKUreport) | 2023-03-14 | GPL-3.0 |
| 香港研究资助局 RGC（GRF / ECS） | 中国香港 · RGC | [`grants/china/hk-rgc-grf`](grants/china/hk-rgc-grf) | [zhiyzuo/HK-RGC-Grant-Proposal-Template](https://github.com/zhiyzuo/HK-RGC-Grant-Proposal-Template) | 2020-10-29 | 未声明 |

### 国际基金项目（中国学者 / 学生可申请，10 个）

| 基金项目 | 适用范围 / 资助机构 | 模板目录 | 来源仓库 | 更新时间 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 欧盟玛丽·居里博士后基金（MSCA-PF） | 欧盟 · 全球无国籍限制 | [`grants/international/eu-msca-pf`](grants/international/eu-msca-pf) | [alexfikl/msca-pf](https://github.com/alexfikl/msca-pf) | 2026-11-09 | CC-BY-4.0 |
| 欧盟玛丽·居里博士生网络（MSCA-DN） | 欧盟 · 全球无国籍限制 | [`grants/international/eu-msca-dn`](grants/international/eu-msca-dn) | [pgarner/msca-dn](https://github.com/pgarner/msca-dn) | 2022-08-01 | 未声明 |
| 欧洲研究理事会启动基金（ERC StG） | 欧盟 · 全球无国籍限制 | [`grants/international/eu-erc-stg`](grants/international/eu-erc-stg) | [alexfikl/erc-stg](https://github.com/alexfikl/erc-stg) | 2026-11-16 | CC-BY-4.0 |
| 欧盟地平线计划（Horizon Europe RIA/IA） | 欧盟 · 国际合作可申请 | [`grants/international/eu-horizon-heria`](grants/international/eu-horizon-heria) | [logological/heria](https://github.com/logological/heria) | 2026-08-16 | 未声明 |
| 德国科学基金会项目（DFG Proposal） | 德国 · 赴德/在德学者可申请 | [`grants/international/de-dfg`](grants/international/de-dfg) | [emtpb/proposal_dfg](https://github.com/emtpb/proposal_dfg) | 2026-02-26 | See LICENSE |
| 美国国家科学基金会（NSF Proposal） | 美国 · 在美机构/合作可申请 | [`grants/international/us-nsf`](grants/international/us-nsf) | [nsf-open/nsf-proposal-latex-samples](https://github.com/nsf-open/nsf-proposal-latex-samples) | 2026-07-28 | See LICENSE |
| 美国国立卫生研究院（NIH Grant） | 美国 · 在美机构/合作可申请 | [`grants/international/us-nih`](grants/international/us-nih) | [Noble-Lab/nih-latex](https://github.com/Noble-Lab/nih-latex) | 2023-02-07 | MIT |
| 美国 NIH 博士后奖学金（NIH F32） | 美国 · 博士后项目 | [`grants/international/us-nih-f32`](grants/international/us-nih-f32) | [c-bun/latex-F32](https://github.com/c-bun/latex-F32) | 2019-02-27 | GPL-3.0 |
| 英国工程与物理科学研究理事会（UKRI/EPSRC） | 英国 · 在英机构/合作可申请 | [`grants/international/uk-epsrc`](grants/international/uk-epsrc) | [DilhanM/epsrc_latex](https://github.com/DilhanM/epsrc_latex) | 2024-10-25 | MIT |
| 加拿大自然科学与工程研究理事会（NSERC DG） | 加拿大 · 在加机构学者可申请 | [`grants/international/ca-nserc`](grants/international/ca-nserc) | [aasgreen/NSERC-Application-Latex-Template](https://github.com/aasgreen/NSERC-Application-Latex-Template) | 2011-10-03 | 未声明 |

## 各高校学位论文模板（45 所高校 / 53 个模板）

| 高校 | 学位层次 | 模板目录 | 来源仓库 | 更新时间 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| 清华大学 | 本科 / 硕士 / 博士 | [`universities/tsinghua`](universities/tsinghua) | [tuna/thuthesis](https://github.com/tuna/thuthesis) | 2026-06-18 | LPPL-1.3c |
| 北京大学 | 本科 / 硕士 / 博士 | [`universities/peking`](universities/peking) | [CasperVector/pkuthss](https://github.com/CasperVector/pkuthss) | 2024-04-20 | 未声明 |
| 上海交通大学 | 本科 / 硕士 / 博士 | [`universities/sjtu`](universities/sjtu) | [sjtug/SJTUThesis](https://github.com/sjtug/SJTUThesis) | 2026-03-12 | Apache-2.0 |
| 浙江大学 | 本科 / 硕士 / 博士 | [`universities/zju`](universities/zju) | [TheNetAdmin/zjuthesis](https://github.com/TheNetAdmin/zjuthesis) | 2025-12-07 | MIT |
| 哈尔滨工业大学 | 本科 / 硕士 / 博士 | [`universities/hit`](universities/hit) | [hithesis/hithesis](https://github.com/hithesis/hithesis) | 2026-10-26 | 未声明 |
| 中国科学技术大学 | 本科 / 硕士 / 博士 | [`universities/ustc`](universities/ustc) | [ustctug/ustcthesis](https://github.com/ustctug/ustcthesis) | 2026-11-16 | LPPL-1.3c |
| 复旦大学 | 本科 / 硕士 / 博士 | [`universities/fudan`](universities/fudan) | [stone-zeng/fduthesis](https://github.com/stone-zeng/fduthesis) | 2024-05-06 | LPPL-1.3c |
| 南京大学 | 本科 / 硕士 / 博士 | [`universities/nju`](universities/nju) | [nju-lug/NJUThesis](https://github.com/nju-lug/NJUThesis) | 2026-06-11 | LPPL-1.3c |
| 武汉大学 | 本科 / 硕士 / 博士 | [`universities/whu`](universities/whu) | [whutug/whu-thesis](https://github.com/whutug/whu-thesis) | 2025-05-27 | LPPL-1.3c |
| 北京理工大学 | 本科 / 硕士 / 博士 | [`universities/bit`](universities/bit) | [BITNP/BIThesis](https://github.com/BITNP/BIThesis) | 2026-10-03 | LPPL-1.3c |
| 西安电子科技大学 | 本科 / 硕士 / 博士 | [`universities/xdu`](universities/xdu) | [note286/xduts](https://github.com/note286/xduts) | 2025-05-04 | LPPL-1.3c |
| 西北工业大学 | 本科 / 硕士 / 博士 | [`universities/nwpu`](universities/nwpu) | [1195343015/nwputhesis](https://github.com/1195343015/nwputhesis) | 2026-10-04 | GPL-3.0 |
| 东北大学 | 本科 / 硕士 / 博士 | [`universities/neu`](universities/neu) | [sci-m-wang/NEU-Thesis](https://github.com/sci-m-wang/NEU-Thesis) | 2026-11-16 | Apache-2.0 |
| 南京航空航天大学 | 本科 / 硕士 / 博士 | [`universities/nuaa`](universities/nuaa) | [nuaatug/nuaathesis](https://github.com/nuaatug/nuaathesis) | 2026-05-31 | Apache-2.0 |
| 重庆大学 | 本科 / 硕士 / 博士 | [`universities/cqu`](universities/cqu) | [nanmu42/CQUThesis](https://github.com/nanmu42/CQUThesis) | 2026-06-22 | LPPL-1.3c |
| 合肥工业大学 | 本科 / 硕士 / 博士 | [`universities/hfut`](universities/hfut) | [HFUTTUG/HFUT_Thesis](https://github.com/HFUTTUG/HFUT_Thesis) | 2026-05-22 | LPPL-1.3c |
| 兰州大学 | 本科 / 硕士 / 博士 | [`universities/lzu`](universities/lzu) | [yuhldr/LZUThesis2020](https://github.com/yuhldr/LZUThesis2020) | 2026-03-11 | See LICENSE |
| 中国人民大学 | 本科 / 硕士 / 博士 | [`universities/ruc`](universities/ruc) | [ZebinWang/ructhesis](https://github.com/ZebinWang/ructhesis) | 2016-12-21 | 未声明 |
| 广东工业大学 | 本科 / 硕士 / 博士 | [`universities/gdut`](universities/gdut) | [sikouhjw/gdutthesis](https://github.com/sikouhjw/gdutthesis) | 2024-03-26 | LPPL-1.3c |
| 山东大学 | 本科 / 硕士 / 博士 | [`universities/sdu`](universities/sdu) | [Liam0205/sduthesis](https://github.com/Liam0205/sduthesis) | 2026-05-04 | LPPL-1.3c |
| 北京师范大学 | 本科 / 硕士 / 博士 | [`universities/bnu`](universities/bnu) | [jinyiliu/bnu-thesis-template](https://github.com/jinyiliu/bnu-thesis-template) | 2025-03-03 | 未声明 |
| 东南大学 | 本科 / 硕士 / 博士 | [`universities/seu`](universities/seu) | [zhimengfan1990/seuthesix](https://github.com/zhimengfan1990/seuthesix) | 2023-03-19 | 未声明 |
| 中国科学院大学 | 硕士 / 博士 | [`universities/ucas/master-doctor`](universities/ucas/master-doctor) | [mohuangrui/ucasthesis](https://github.com/mohuangrui/ucasthesis) | 2021-10-29 | 未声明 |
| 北京航空航天大学 | 本科 | [`universities/buaa/bachelor`](universities/buaa/bachelor) | [BHOSC/BUAAthesis](https://github.com/BHOSC/BUAAthesis) | 2025-01-12 | LPPL-1.3c |
| 北京航空航天大学 | 硕士 / 博士 | [`universities/buaa/master-doctor`](universities/buaa/master-doctor) | [CheckBoxStudio/BUAAThesis](https://github.com/CheckBoxStudio/BUAAThesis) | 2024-02-01 | MIT |
| 电子科技大学 | 硕士 / 博士 | [`universities/uestc/master-doctor`](universities/uestc/master-doctor) | [bdebye/thesisuestc](https://github.com/bdebye/thesisuestc) | 2026-06-17 | 未声明 |
| 中山大学 | 本科 | [`universities/sysu/bachelor`](universities/sysu/bachelor) | [SYSU-SCC/sysu-thesis](https://github.com/SYSU-SCC/sysu-thesis) | 2026-09-04 | GPL-3.0 |
| 华南理工大学 | 硕士 / 博士 | [`universities/scut/master-doctor`](universities/scut/master-doctor) | [mengchaoheng/SCUT_thesis](https://github.com/mengchaoheng/SCUT_thesis) | 2026-08-03 | GPL-3.0 |
| 同济大学 | 本科 | [`universities/tongji/bachelor`](universities/tongji/bachelor) | [TJ-CSCCG/TongjiThesis](https://github.com/TJ-CSCCG/TongjiThesis) | 2026-10-30 | LPPL-1.3c |
| 同济大学 | 硕士 / 博士 | [`universities/tongji/master-doctor`](universities/tongji/master-doctor) | [wyqy/TongjiThesis_Proto](https://github.com/wyqy/TongjiThesis_Proto) | 2025-03-06 | 未声明 |
| 西安交通大学 | 硕士 / 博士 | [`universities/xjtu/master-doctor`](universities/xjtu/master-doctor) | [obster-y/XJTU-thesis](https://github.com/obster-y/XJTU-thesis) | 2026-02-03 | LPPL-1.3c |
| 中南大学 | 硕士 / 博士 | [`universities/csu/master-doctor`](universities/csu/master-doctor) | [CSUcse/CSUthesis](https://github.com/CSUcse/CSUthesis) | 2025-04-02 | 未声明 |
| 北京邮电大学 | 本科 | [`universities/bupt/bachelor`](universities/bupt/bachelor) | [sheng-qiang/BUPTBachelorThesis](https://github.com/sheng-qiang/BUPTBachelorThesis) | 2021-05-02 | MIT |
| 北京邮电大学 | 硕士 / 博士 | [`universities/bupt/master-doctor`](universities/bupt/master-doctor) | [jjfu99/BUPTGraduateThesisLatexTemplate](https://github.com/jjfu99/BUPTGraduateThesisLatexTemplate) | 2026-06-02 | GPL-3.0 |
| 天津大学 | 硕士 / 博士 | [`universities/tju/master-doctor`](universities/tju/master-doctor) | [xnth97/TJUThesisLatexTemplate](https://github.com/xnth97/TJUThesisLatexTemplate) | 2024-05-29 | GPL-3.0 |
| 国防科技大学 | 硕士 / 博士 | [`universities/nudt/master-doctor`](universities/nudt/master-doctor) | [liubenyuan/nudtpaper](https://github.com/liubenyuan/nudtpaper) | 2026-10-13 | 未声明 |
| 南方科技大学 | 本科 | [`universities/sustech/bachelor`](universities/sustech/bachelor) | [iydon/sustechthesis](https://github.com/iydon/sustechthesis) | 2026-08-15 | LPPL-1.3c |
| 南方科技大学 | 硕士 / 博士 | [`universities/sustech/master-doctor`](universities/sustech/master-doctor) | [SUSTech-CRA/sustech-master-thesis](https://github.com/SUSTech-CRA/sustech-master-thesis) | 2026-11-15 | LPPL-1.3c |
| 华中科技大学 | 本科 | [`universities/hust/bachelor`](universities/hust/bachelor) | [skinaze/HUSTPaperTemp](https://github.com/skinaze/HUSTPaperTemp) | 2022-04-11 | MIT |
| 华中科技大学 | 博士 | [`universities/hust/doctor`](universities/hust/doctor) | [XinzeZhang/HUST-PhD-Thesis-Latex](https://github.com/XinzeZhang/HUST-PhD-Thesis-Latex) | 2026-09-06 | 未声明 |
| 华南师范大学 | 硕士 / 博士 | [`universities/scnu/master-doctor`](universities/scnu/master-doctor) | [scnu/scnuthesis](https://github.com/scnu/scnuthesis) | 2024-12-30 | 未声明 |
| 厦门大学 | 硕士 / 博士 | [`universities/xmu/master-doctor`](universities/xmu/master-doctor) | [zoam/xmu-thesis-grd](https://github.com/zoam/xmu-thesis-grd) | 2025-06-28 | 未声明 |
| 四川大学 | 硕士 / 博士 | [`universities/scu/master-doctor`](universities/scu/master-doctor) | [kevinleeex/scu_thesis_2020](https://github.com/kevinleeex/scu_thesis_2020) | 2022-06-08 | 未声明 |
| 上海大学 | 本科 | [`universities/shu/bachelor`](universities/shu/bachelor) | [shuosc/SHU-Bachelor-Thesis-OSC](https://github.com/shuosc/SHU-Bachelor-Thesis-OSC) | 2026-01-19 | 未声明 |
| 南开大学 | 硕士 / 博士 | [`universities/nku/master-doctor`](universities/nku/master-doctor) | [NewFuture/NKThesis](https://github.com/NewFuture/NKThesis) | 2025-05-06 | MIT |
| 吉林大学 | 本科 | [`universities/jlu/bachelor`](universities/jlu/bachelor) | [Jackknifer/jluthesis-template](https://github.com/Jackknifer/jluthesis-template) | 2026-04-24 | MIT |
| 吉林大学 | 硕士 / 博士 | [`universities/jlu/master-doctor`](universities/jlu/master-doctor) | [maxuewei2/JLUThesis2020](https://github.com/maxuewei2/JLUThesis2020) | 2026-07-24 | 未声明 |
| 大连理工大学 | 本科 | [`universities/dlut/bachelor`](universities/dlut/bachelor) | [Anplus/DUT-Bachelor-Thesis-Latex-Template](https://github.com/Anplus/DUT-Bachelor-Thesis-Latex-Template) | 2017-06-26 | 未声明 |
| 大连理工大学 | 硕士 | [`universities/dlut/master`](universities/dlut/master) | [01xz/dlut-thesis](https://github.com/01xz/dlut-thesis) | 2025-03-14 | LPPL-1.3c |
| 湖南大学 | 本科 | [`universities/hnu/bachelor`](universities/hnu/bachelor) | [leaf-hsiao/HNUThesisTemplate](https://github.com/leaf-hsiao/HNUThesisTemplate) | 2019-12-11 | 未声明 |
| 湖南大学 | 硕士 | [`universities/hnu/master`](universities/hnu/master) | [WhiteByeBye/HNUThesisTemplate-Master](https://github.com/WhiteByeBye/HNUThesisTemplate-Master) | 2022-09-20 | 未声明 |
| 台湾大学 | 硕士 / 博士 | [`universities/ntu-tw/master-doctor`](universities/ntu-tw/master-doctor) | [Hsins/NTU-Thesis-LaTeX-Template](https://github.com/Hsins/NTU-Thesis-LaTeX-Template) | 2024-08-13 | MIT |
| 台湾成功大学 | 硕士 / 博士 | [`universities/ncku-tw/master-doctor`](universities/ncku-tw/master-doctor) | [wengan-li/ncku-thesis-template-latex](https://github.com/wengan-li/ncku-thesis-template-latex) | 2026-11-15 | CC-BY-4.0 |

## 致谢与许可

衷心感谢上述所有中文期刊、科研基金与高校学位论文 LaTeX 模板的原作者、高校 TeX 用户组（TUG）及开源社区维护者。目录整理亦参考了以下开源索引项目：

- [1195343015/cn-university-latex-thesis-templates](https://github.com/1195343015/cn-university-latex-thesis-templates)
- [hantang/latex-templates](https://github.com/hantang/latex-templates)

各模板子目录中的源码与资源均遵循其来源仓库各自的开源许可证（已保留各仓库原始 `LICENSE` 文件）；若某模板未显式声明许可证，请在使用前联系原作者或参阅来源仓库说明。
