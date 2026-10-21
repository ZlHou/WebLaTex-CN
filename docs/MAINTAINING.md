# WebLaTeX CN 构建与维护

日常写作从 [README](../README.md) 开始。本文供需要定制或发布镜像的维护者使用。

## 本地构建

在环境源码根目录执行：

```bash
docker build --pull -t weblatex-cn:local .
docker run --rm weblatex-cn:local check-latex-environment
```

基础环境为官方 `node:24-trixie-slim`（Debian 13）。TeX Live、Biber 和字体统一通过 APT 安装，不混用 `tlmgr install/update`。TeX Live 使用 Debian 提供的版本；学校模板若要求更新版本，应先检查兼容性。

Dockerfile 会以非 root 用户实际编译 XeLaTeX / LuaLaTeX 中文文档，检查数学公式、字体、算法、绘图及 GB/T 7714 Biber 文献，并验证 PDF 可提取的中文正文和文献题名。测试在临时目录中生成并清理，不调用 OpenAI 服务，也不需要 API key。

## 定制与版本固定

```bash
# 跳过 Codex CLI，保留 Node.js 和 npm
docker build --build-arg INSTALL_CODEX=false -t weblatex-cn:base .

# 固定 CLI 版本：将占位符替换为实际 npm 版本号
docker build --build-arg CODEX_VERSION=<版本号> -t weblatex-cn:pinned .

# 固定基础镜像：将占位符替换为实际 digest
docker build --build-arg NODE_IMAGE=node:24-trixie-slim@sha256:<digest> \
  -t weblatex-cn:pinned .
```

默认基础镜像补丁、APT 包和 Codex CLI 会随重建更新，不保证逐字节可复现。CI 发布以下标签：

- `ghcr.io/zlhou/weblatex-cn:latest`：最近一次成功发布的环境。
- `ghcr.io/zlhou/weblatex-cn:sha-<完整提交 SHA>`：对应提交的镜像，请勿手动覆盖。

需要固定写作环境时，在 devcontainer 的 `image` 字段使用 SHA 标签或已发布镜像的 digest。

当前 CI 验证 `linux/amd64`。默认用户为 `node`，UID/GID 为 1000；Dev Containers 可自动调整 UID。npm 全局目录 `/opt/npm-global` 对该用户可写。手动覆盖 UID 后，不保证该目录仍可写。

## 代理与凭据

HTTPS 检查代理环境中，可为 npm 通过 BuildKit secret 注入 CA：

```bash
docker build --secret id=proxy_ca,src=/path/to/proxy-ca.pem -t weblatex-cn:local .
```

CA 不写入镜像。APT 等工具如也需要代理 CA，应按平台配置受信证书，保留 TLS 和软件源签名校验。

使用者在自己的运行容器中登录 Codex，不将 API key、登录文件或 `.env` 烘焙进镜像。`docker run --rm` 会丢弃容器内后续安装和登录状态；需要保留时使用持久卷。

## Codex 沙箱

镜像包含 bubblewrap。若出现 `bwrap: No permissions to create a new namespace`，检查宿主机或托管平台的用户命名空间策略。

仅在受信环境并接受 Docker 外层权限扩大时，可为本地 `docker run` 添加：

```text
--cap-add=SYS_ADMIN
--security-opt=seccomp=unconfined
--security-opt=apparmor=unconfined
```

Dev Containers 可在 `runArgs` 数组中设置这些参数，然后重建容器。它们不能解除宿主机禁令，也不应通过关闭 Codex 自身沙箱来解决问题。

## 发布镜像

工作流 [container.yml](../.github/workflows/container.yml) 对 `main` 分支的 push、PR 和手动执行进行构建与验证。PR 只检查；本分支 push 或在本分支手动执行通过后，使用 GitHub 自动提供的 `GITHUB_TOKEN` 发布 GHCR，无需额外 registry secret。

仓库或组织需要允许 Actions 运行及写入 Packages。若已有同名包，需要授予本仓库 Actions 写入权限。需要匿名拉取时，在 **GitHub Packages → weblatex-cn → Package settings** 中将可见性设为 **Public**。

在仓库的 **Actions → Build, test and publish WebLaTeX CN → Run workflow** 中可手动触发发布，选择 `main` 分支。环境更新提交并普通推送到本仓库的 `origin/main`，也会自动触发构建。仓库仅维护构建配置、文档与检查脚本，不加入论文正文或业务代码。
