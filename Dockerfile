FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 5000

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--log-level=DEBUG", "-w", "4", "--timeout", "300", "--preload", "run:app"]
