FROM python:3.12

WORKDIR /project

COPY requirements .

RUN pip install --no-cache-dir -r requirements

COPY . .

CMD ["bash"]