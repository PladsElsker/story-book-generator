install_requirements() {
    local arg1=$1
    shift
    echo Installing dependencies for $arg1
    venv/bin/pip install -r $arg1/requirements.txt $@ || { echo Failed to install requirements; exit 1; }
}


if [ ! -d venv ]; then
    echo Creating a new virtual environment
    python3 -m venv venv || { echo Failed to create virtual environment; exit 1; }
fi


install_requirements scraper
install_requirements scenes
install_requirements audio
