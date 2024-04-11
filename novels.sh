if [ ! -d venv ]; then
    cd novels
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt > ../novels.log
    cd ..
fi


novels/venv/bin/python novels/handler.py "$@"
