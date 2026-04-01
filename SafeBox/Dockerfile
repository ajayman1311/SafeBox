# File: Dockerfile
FROM python:3.11-slim

# Install system tools, security scanners, and network loggers
RUN apt-get update && apt-get install -y \
    tcpdump \
    bandit \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Setup a non-root user for better security
RUN useradd -m developer
WORKDIR /home/developer/workspace

# PERSISTENCE CONFIG: These environment variables ensure libraries are stored in the mounted volume
ENV PYTHONUSERBASE=/home/developer/env_storage
ENV PATH="/home/developer/env_storage/bin:${PATH}"
ENV PIP_USER=true

# Create the storage directory and fix ownership permissions
RUN mkdir -p /home/developer/env_storage && \
    chown -R developer:developer /home/developer

# Switch to the non-root user
USER developer

# Start the bash terminal
CMD ["/bin/bash"]