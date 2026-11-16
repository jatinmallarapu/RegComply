# Ship the regcomply CLI and its reproducible example as a nonroot image.
FROM python:3.11-slim
WORKDIR /app
COPY README.md pyproject.toml regcomply.py ./
COPY examples/ examples/
RUN python -m pip install --no-cache-dir .
USER 10001
CMD ["python","regcomply.py","ask","What does FINRA say about misleading advertising?"]
