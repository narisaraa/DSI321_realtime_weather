#!/bin/bash

# ชื่อ environment
ENV_NAME="prefect-env"

echo "✅ Creating conda environment: $ENV_NAME"
conda create -n $ENV_NAME python=3.10 -y

echo "✅ Activating environment"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $ENV_NAME

echo "✅ Installing dependencies from requirements.txt"
pip install -r requirements.txt

echo "🎉 Done! You can now run:"
echo "---------------------------------------"
echo "conda activate $ENV_NAME"
echo "prefect version"
echo "prefect server start"
echo "---------------------------------------"
