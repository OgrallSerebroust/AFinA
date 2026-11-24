ARG APP_DIRECTORY="/app"

# STAGE 1 --> Builder
FROM python:3.13-slim AS builder
ARG APP_DIRECTORY
SHELL ["/bin/bash", "-e", "-u", "-o", "pipefail", "-x", "-c"]
ENV PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=0 \
    #TODO: In the future, it will be possible to use 1 for optimize app running in production. But it brings more size of final image;
    UV_LINK_MODE=copy
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt/lists \
    rm -f /etc/apt/apt.conf.d/docker-clean
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
#TODO: Version;
#TODO: Users rights;
#TODO: Maybe don't add uv.lock and pyproject.toml to the image. To do this, you need change COPY . . to COPY only necessary files.
WORKDIR ${APP_DIRECTORY}
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,sharing=locked,target=/root/.cache/uv \
    uv sync --frozen --no-editable --no-dev --no-install-project

#STAGE 2 --> Application
FROM python:3.13-slim AS application
ARG APP_DIRECTORY
ARG GID="2514"
ARG UID="2514"
ARG USER_NAME="ograll"
SHELL ["/bin/bash", "-e", "-u", "-o", "pipefail", "-x", "-c"]
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt/lists \
<<EOF
rm -f /etc/apt/apt.conf.d/docker-clean
groupadd --gid=${GID} --system ${USER_NAME}
useradd --uid=${UID} --gid=${GID} --system --no-log-init --no-create-home --shell /usr/sbin/nologin ${USER_NAME}
EOF

# COPY --from=builder --chown=${UID}:${GID} /opt/venv /opt/venv
COPY --from=builder /opt/venv /opt/venv
WORKDIR ${APP_DIRECTORY}
COPY --chown=${UID}:${GID} . .
RUN find . -type d -exec chmod 755 {} + \
    && find . -type f -exec chmod 644 {} + \
    && chmod 755 ./entrypoint.sh
USER ${USER_NAME}
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["dev"]