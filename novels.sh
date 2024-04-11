cd novels

if [ ! -d venv ]; then
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt > ../novels.log
fi

cd ..

novels/venv/bin/python novels/handler.py "$@"
