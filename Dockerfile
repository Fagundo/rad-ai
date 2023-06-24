FROM python:3.9

# Set env for protobuf
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Set a working dir path
ARG WORKING_PATH=/home/radai
WORKDIR $WORKING_PATH

# Copy app
COPY app $WORKING_PATH/app

# Install dependencies, specifically torch cpu from whl
RUN pip install torch torchvision torchaudio \ 
    --index-url https://download.pytorch.org/whl/cpu && \
    pip install -r app/requirements.txt

# Expose port
EXPOSE 8000

# Download model here so its available at runtime
RUN sh app/scripts/download.sh

CMD ["uvicorn", "app.run:app", "--host=0.0.0.0", "--port=8000"]
