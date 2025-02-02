#!/bin/bash

# if the dir doesn't exist, create it
if [ ! -d "$HOME/ABOE" ]; then
  cd "$HOME"
  git clone https://github.com/DHMorse/ABOE
fi

cd "$HOME/ABOE"

# Pull latest changes from GitHub
git pull

rm -rf .venv

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

# Run the bot
python3 main.py