FROM python:3.10-slim-buster

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt 

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY app .

VOLUME ["/model_cache"]

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]