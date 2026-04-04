# File: Dockerfile
FROM python:3.11-slim

# Install core tools
RUN apt-get update && apt-get install -y \
    tcpdump bandit curl && rm -rf /var/lib/apt/lists/*

RUN useradd -m developer
WORKDIR /home/developer/workspace

# Persistence configuration
ENV PYTHONUSERBASE=/home/developer/env_storage
ENV PATH="/usr/local/bin:/home/developer/env_storage/bin:${PATH}"
ENV PIP_USER=true

# --- OPTIMIZED SMART PIP WRAPPER ---
RUN echo '#!/bin/bash \n\
if [[ "$1" == "install" ]]; then \n\
    for arg in "${@:2}"; do \n\
        if [[ ! $arg == -* ]]; then \n\
            PACKAGE=$arg \n\
            break \n\
        fi \n\
    done \n\
    if [[ ! -z "$PACKAGE" ]]; then \n\
        echo "--------------------------------------------------" \n\
        echo "📥 [1/2] DOWNLOADING: $PACKAGE" \n\
        echo "--------------------------------------------------" \n\
        mkdir -p /tmp/scan \n\
        # Removed --no-binary for speed and > /dev/null for visibility \n\
        python3 -m pip download $PACKAGE -d /tmp/scan --progress-bar on \n\
        \n\
        echo "--------------------------------------------------" \n\
        echo "🔍 [2/2] SECURITY SCANNING (Bandit)..." \n\
        echo "--------------------------------------------------" \n\
        # Added -ll to skip low-severity warnings and speed up analysis \n\
        bandit -r /tmp/scan -ll \n\
        EXIT_CODE=$? \n\
        rm -rf /tmp/scan \n\
        if [ $EXIT_CODE -ne 0 ]; then \n\
            echo "⚠️  CRITICAL RISK DETECTED!" \n\
            read -p "Security issues found. Install anyway? (y/n): " confirm \n\
            if [[ $confirm != "y" ]]; then echo "❌ Aborted."; exit 1; fi \n\
        else \n\
            echo "✅ [CLEAN] No major threats found. Proceeding..." \n\
        fi \n\
    fi \n\
fi \n\
# Run the actual pip installation \n\
python3 -m pip "$@"' > /usr/local/bin/pip && \
chmod +x /usr/local/bin/pip

RUN chown -R developer:developer /home/developer
USER developer

CMD ["/bin/bash"]
