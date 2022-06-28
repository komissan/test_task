# 
FROM python:3.10

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY . /app

WORKDIR /app

EXPOSE 8000
EXPOSE 5432
# 

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
