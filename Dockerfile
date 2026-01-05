FROM python:3.10-slim

WORKDIR /app

COPY flask_app/ /app/

COPY models/vectorizer.pkl /app/models/vectorizer.pkl

RUN pip install -r requirements.txt


# 3. Set a fixed NLTK data directory
ENV NLTK_DATA=/usr/local/nltk_data

# RUN python3 -m nltk.downloader stopwords wordnet
RUN python3 - <<EOF
import nltk
nltk.download("stopwords", download_dir="/usr/local/nltk_data")
nltk.download("wordnet", download_dir="/usr/local/nltk_data")
EOF

EXPOSE 5002

#local
# CMD ["python", "app.py"]  

#Prod
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--timeout", "120", "app:app"]