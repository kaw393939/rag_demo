#!/bin/bash
# Run the Streamlit application

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
  source venv/Scripts/activate
fi

# Ensure src package is in PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# Run streamlit application
streamlit run app.py "$@"
