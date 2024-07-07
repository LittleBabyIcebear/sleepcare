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

# Expose port yang digunakan oleh aplikasi Flask
EXPOSE 5000

# Atur command untuk menjalankan aplikasi Flask saat container dijalankan
CMD ["python", "app.py"]
