sudo apt-get update
sudo rm -fR /var/lib/apt/lists/*
sudo apt update
sudo apt-get install python-software-properties
sudo apt-get install software-properties-common
sudo add-apt-repository --remove ppa:alex-p/tesseract-ocr5
sudo apt-get update
sudo apt install -y tesseract-ocr
sudo apt-get install tesseract-ocr-eng
sudo apt-get update
sudo apt install poppler-utils
echo tesseract --version
tesseract --version
