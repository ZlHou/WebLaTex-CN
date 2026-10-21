# syntax=docker/dockerfile:1
ARG NODE_IMAGE=node:24-trixie-slim
FROM ${NODE_IMAGE}

USER root
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    NPM_CONFIG_PREFIX=/opt/npm-global \
    PATH=/opt/npm-global/bin:$PATH

# Keep TeX Live and Biber on the same Debian release; do not mix with tlmgr.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bash ca-certificates curl git openssh-client ripgrep less make \
        python3 bubblewrap fontconfig fonts-noto-cjk fonts-texgyre \
        texlive-xetex texlive-luatex texlive-lang-chinese texlive-lang-japanese \
        texlive-latex-recommended texlive-latex-extra texlive-science \
        texlive-pictures texlive-publishers texlive-bibtex-extra \
        texlive-fonts-recommended texlive-fonts-extra texlive-extra-utils \
        latexmk biber poppler-utils \
        libyaml-tiny-perl libfile-homedir-perl libunicode-linebreak-perl \
    && printf '%s\n' '<?xml version="1.0"?>' '<!DOCTYPE fontconfig SYSTEM "fonts.dtd">' '<fontconfig><dir>/usr/share/texlive/texmf-dist/fonts/opentype</dir><dir>/usr/share/texlive/texmf-dist/fonts/truetype</dir></fontconfig>' > /etc/fonts/conf.d/09-texlive.conf \
    && fc-cache -f \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /opt/npm-global /workspaces \
    && chown -R node:node /opt/npm-global /workspaces

ARG INSTALL_CODEX=true
ARG CODEX_VERSION=latest
# The optional CA secret is for builds behind an HTTPS inspection proxy.
RUN --mount=type=secret,id=proxy_ca \
    if [ "$INSTALL_CODEX" = true ]; then \
        if [ -f /run/secrets/proxy_ca ]; then export NODE_EXTRA_CA_CERTS=/run/secrets/proxy_ca; fi; \
        npm install --global "@openai/codex@${CODEX_VERSION}" \
        && codex --version; \
    elif [ "$INSTALL_CODEX" != false ]; then \
        echo 'INSTALL_CODEX must be true or false' >&2; exit 1; \
    fi \
    && chown -R node:node /opt/npm-global

COPY --chmod=755 scripts/check-environment.sh /usr/local/bin/check-latex-environment
USER node
WORKDIR /workspaces
# Run real compilations as the same non-root user used at runtime.
RUN check-latex-environment
LABEL org.opencontainers.image.title="WebLaTeX CN" \
      org.opencontainers.image.source="https://github.com/ZlHou/WebLaTex-CN" \
      org.opencontainers.image.description="Chinese LaTeX, scientific typesetting, Node.js and optional Codex CLI"
CMD ["bash"]
