sudo apt-get update

sudo apt-get install software-properties-common
sudo add-apt-repository --remove ppa:alex-p/tesseract-ocr
sudo apt-get update

sudo apt-get install -y libc6
sudo apt-get install -y ffmpeg libsm6 libxext6 libc6

sudo apt-get install -y tesseract-ocr 
sudo apt-get install libtesseract-dev
sudo apt-get install -y poppler-utils


mkdir converted_images
echo "Everything OK"
tesseract --version