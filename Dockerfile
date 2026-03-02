FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install flask
# Create a non-root user for banking security
RUN useradd -m bankuser
USER bankuser
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1
CMD ["python", "app.py"]