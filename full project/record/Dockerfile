FROM python:3.12

#
WORKDIR /record

#
COPY ./requirements.txt /record/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /record/requirements.txt

#
COPY ./myrecord /record/myrecord

#
CMD ["uvicorn", "myrecord.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]