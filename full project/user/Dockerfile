FROM python:3.12

#
WORKDIR /user

#
COPY ./requirements.txt /user/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /user/requirements.txt

#
COPY ./proga /user/proga

#
CMD ["uvicorn", "proga.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "81"]