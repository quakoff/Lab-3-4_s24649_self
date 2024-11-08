FROM python:3.9
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "doker_model.py", "--server.port=8501"]