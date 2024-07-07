# Gunakan base image Python
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Salin requirements.txt terlebih dahulu agar dependencies di-cache
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Salin seluruh kode aplikasi Flask ke dalam container
COPY . .

# Salin file kredensial BigQuery ke dalam container
COPY sleepcare-428605-767355c54dde.json /app/sleepcare-428605-767355c54dde.json

# Expose port yang digunakan oleh aplikasi Flask
EXPOSE 8080

# Atur command untuk menjalankan aplikasi Flask saat container dijalankan
CMD ["python", "app.py"]
