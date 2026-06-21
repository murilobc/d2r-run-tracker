FROM python:3.12-slim

WORKDIR /app

COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ .

ENV API_URL="https://d2r-run-tracker-api.fly.dev"

EXPOSE 8501

CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --browser.gatherUsageStats=false"]
