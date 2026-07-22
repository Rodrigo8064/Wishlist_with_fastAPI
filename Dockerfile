FROM python:3.13.9-alpine3.22

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

ARG USERNAME=wishlist
ENV POETRY_VERSION=2.4.1 \
    PATH="/home/${USERNAME}/.local/bin:$PATH"


RUN apk add curl \
      --no-cache && \
    rm -rf /var/cache/apk/* && \
    adduser -s /bin/sh -D ${USERNAME}

USER ${USERNAME}

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /home/${USERNAME}

COPY --chown=w${USERNAME}:${USERNAME} pyproject.toml poetry.lock ./
RUN poetry install \
      --no-root \
      --no-ansi \
      --without dev

COPY --chown=${USERNAME}:${USERNAME} . .

RUN chmod +x entrypoint.sh
EXPOSE 8001
CMD ["./entrypoint.sh"]
