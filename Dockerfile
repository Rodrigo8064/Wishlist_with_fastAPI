FROM python:3.13.9-alpine3.22

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

ARG USERNAME=wishlist
ENV POETRY_VERSION=2.2.1 \
    PATH="/home/${USERNAME}/.local/bin:$PATH"


RUN apk add curl=8.14.1-r2 \
      --no-cache && \
    rm -rf /var/cache/apk/* && \
		adduser -s /bin/sh -D ${USERNAME}

USER ${USERNAME}
  
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /home/${USERNAME}

COPY --chown=wishlist:wishlist pyproject.toml poetry.lock ./
RUN poetry install \
      --no-root \
      --no-ansi \
      --without dev

COPY --chown=wishlist:wishlist . .

CMD ["poetry", "run", "gunicorn", "fastapi_wishlist:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "2"]
