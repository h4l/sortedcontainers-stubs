ARG PYTHON_VER

FROM python:${PYTHON_VER:?} AS python-base


FROM python-base AS poetry
RUN pip install poetry
WORKDIR /workspace
COPY pyproject.toml poetry.lock /workspace/

# Poetry needs these to exist to setup the editable install
RUN mkdir sortedcontainers-stubs && touch README.md
RUN poetry install


FROM poetry AS test
RUN --mount=source=.,target=/workspace,rw \
    --mount=type=cache,uid=1000,target=.pytest_cache \
    poetry run pytest


FROM poetry AS lint-flake8
RUN --mount=source=.,target=/workspace,rw \
    poetry run flake8


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
