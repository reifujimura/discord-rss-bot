FROM python:3.8
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD bot /bot
CMD python -u -m bot