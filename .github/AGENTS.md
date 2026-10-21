# 仓库工作约定

- 本仓库 `ZlHou/WebLaTex-CN` 仅用于容器镜像、开发容器和环境检查，保留可单文件编译的 `example.tex` 作为环境演示，不添加实际论文正文、学校模板或业务代码。
- 完成必要检查后，自动提交本任务相关变更，并普通推送到本仓库的 `origin/main`，无需重复确认；不强制覆盖历史。
- 推送前 fetch 并检查远程更新。Docker 不可用时明确报告未执行本地镜像构建，不能将静态检查描述为编译成功。
- 镜像统一命名为 `ghcr.io/zlhou/weblatex-cn`；文档与镜像元数据使用 WebLaTeX CN，不带宿主仓库的项目名称。
- 不提交凭据、用户登录状态或私有字体。
- 配置、脚本及维护文档放在 `.devcontainer/` 或 `.github/` 中；根目录可见文件仅保留 `README.md`、`LICENSE` 和 `example.tex`。`.gitignore` 保留在根目录以支持 Git 自动识别。
