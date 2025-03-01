FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install package
RUN pip install -e .

# Expose the Streamlit port
EXPOSE 8501

# Set entrypoint to run Streamlit
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
