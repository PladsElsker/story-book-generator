if [ ! -d venv ]; then
    cd scraper
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
    cd ..
fi


scraper/venv/bin/python scraper/scraping.py "$@"
