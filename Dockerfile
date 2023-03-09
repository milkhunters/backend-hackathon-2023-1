FROM python:3.11

COPY . /code
WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#ENV PYTHONPATH "${PYTHONPATH}:/code/src"

CMD ["uvicorn", "src.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
