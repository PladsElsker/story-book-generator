cd scraper

if [ ! -d venv ]; then
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
fi

cd ..

scraper/venv/bin/python scraper/scraping.py "$@"
