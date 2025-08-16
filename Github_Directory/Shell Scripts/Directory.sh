#!/bin/bash

# Change this to your actual path
BASE_DIR="/Users/gitansh/Developer/GitHub_Directory"

# Create base directory
mkdir -p $BASE_DIR

# Define projects
PROJECTS=("ExpensePlanner" "SecondProject")

# Loop through projects and create structure
for PROJECT in "${PROJECTS[@]}"; do
  mkdir -p $BASE_DIR/$PROJECT/assets
  mkdir -p $BASE_DIR/$PROJECT/docs
  
  # Create files inside project
  touch $BASE_DIR/$PROJECT/README.md
  touch $BASE_DIR/$PROJECT/requirements.txt
  touch $BASE_DIR/$PROJECT/index.html
  touch $BASE_DIR/$PROJECT/style.css
  touch $BASE_DIR/$PROJECT/script.js
  touch $BASE_DIR/$PROJECT/app.py
  touch $BASE_DIR/$PROJECT/database.db
done

echo "✅ Project structure created under $BASE_DIR"