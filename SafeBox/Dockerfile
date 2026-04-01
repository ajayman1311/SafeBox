# File: Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tcpdump bandit curl && rm -rf /var/lib/apt/lists/*

RUN useradd -m developer
WORKDIR /home/developer/workspace

# Persistence setup
ENV PYTHONUSERBASE=/home/developer/env_storage
# We have placed '/usr/local/bin' first in the path.
ENV PATH="/usr/local/bin:/home/developer/env_storage/bin:${PATH}"
ENV PIP_USER=true

# --- ROBUST SMART PIP SCRIPT ---
# We will overwrite this script at '/usr/local/bin/pip'.
RUN echo '#!/bin/bash\n\
# Check if command is "install"\n\
if [[ "$1" == "install" ]]; then\n\
    # Find the package name (skipping flags like -U or --no-cache)\n\
    for arg in "${@:2}"; do\n\
        if [[ ! $arg == -* ]]; then\n\
            PACKAGE=$arg\n\
            break\n\
        fi\n\
    done\n\
    \n\
    if [[ ! -z "$PACKAGE" ]]; then\n\
        echo "--------------------------------------------------"\n\
        echo "🔍 [SECURITY SCAN] Analyzing: $PACKAGE"\n\
        echo "--------------------------------------------------"\n\
        mkdir -p /tmp/scan\n\
        # Download only source code for scanning\n\
        python3 -m pip download $PACKAGE --no-binary :all: -d /tmp/scan > /dev/null 2>&1\n\
        \n\
        # Run Bandit scan\n\
        bandit -r /tmp/scan\n\
        EXIT_CODE=$?\n\
        rm -rf /tmp/scan\n\
        \n\
        if [ $EXIT_CODE -ne 0 ]; then\n\
            echo "⚠️  MALICIOUS PATTERN DETECTED in $PACKAGE!"\n\
            read -p "Risk detected. Proceed anyway? (y/n): " confirm\n\
            if [[ $confirm != "y" ]]; then echo "❌ Installation Aborted."; exit 1; fi\n\
        else\n\
            echo "✅ [SCAN CLEAN] No high-risk patterns found."\n\
        fi\n\
    fi\n\
fi\n\
# Execute the real pip\n\
python3 -m pip "$@"' > /usr/local/bin/pip && \
chmod +x /usr/local/bin/pip

RUN chown -R developer:developer /home/developer
USER developer

CMD ["/bin/bash"]
