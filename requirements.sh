install_venv() {
    echo Installing dependencies in $1
    cd $1 || { echo Failed to change directory to $1; exit 1; }
    if [ ! -d venv ]; then
        echo Creating a new virtual environment
        python3 -m venv venv || { echo Failed to create virtual environment; exit 1; }
    fi
    venv/bin/pip install -r requirements.txt || { echo Failed to install requirements; exit 1; }
    venv/bin/pip install -e ../novels || { echo Failed to install the novels package; exit 1; }
    cd .. || { echo Failed to return to the parent directory; exit 1; }
}


install_venv scraper
install_venv scenes
install_venv audio
