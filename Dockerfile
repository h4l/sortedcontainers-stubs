ARG PYTHON_VER

FROM python:${PYTHON_VER:?} AS python-base
SHELL ["bash", "-euo", "pipefail", "-c"]


FROM python-base AS poetry
RUN --mount=type=cache,target=/root/.cache pip install poetry
RUN python -m venv /venv
ENV VIRTUAL_ENV=/venv \
    PATH="/venv/bin:$PATH"
RUN poetry config virtualenvs.create false
WORKDIR /workspace
COPY pyproject.toml poetry.lock /workspace/

# Poetry needs these to exist to setup the editable install
RUN mkdir sortedcontainers-stubs && touch README.md
RUN --mount=type=cache,target=/root/.cache poetry install


FROM poetry AS test
RUN --mount=source=.,target=/workspace,rw \
    --mount=type=cache,uid=1000,target=.pytest_cache \
    pytest | sed -E -e 's|(^\|\s+)/workspace/|\1.\/|'


FROM poetry AS lint-flake8
RUN --mount=source=.,target=/workspace,rw \
    flake8


FROM poetry AS lint-black
RUN --mount=source=.,target=/workspace,rw \
    poetry run black --check --diff .


FROM poetry AS lint-isort
RUN --mount=source=.,target=/workspace,rw \
    poetry run isort --check --diff .


FROM poetry AS lint-mypy
RUN --mount=source=.,target=/workspace,rw \
    --mount=type=cache,target=.mypy_cache \
    poetry run mypy .


FROM python-base AS pyright
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm
RUN npm install -g pyright
WORKDIR /workspace
COPY --link --from=poetry /venv /venv


FROM pyright AS lint-pyright
RUN --mount=source=.,target=/workspace,rw \
    pyright --pythonpath /venv/bin/python . | sed -E -e 's|(^\|\s+)/workspace/|\1.\/|'
