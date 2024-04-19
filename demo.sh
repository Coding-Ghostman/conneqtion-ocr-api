
sudo apt-get update
pip install --upgrade build setuptools

# # Install prerequisites
sudo apt-get install -y python-software-properties software-properties-common

# Remove the specific repository
sudo add-apt-repository -y ppa:alex-p/tesseract-ocr5

# Update package lists after repository removal
sudo apt-get update
sudo apt-get install -y ffmpeg libsm6 libxext6
sudo apt-get install -y libgl1
sudo apt-get install -y opencv-python-headless
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
sudo apt-get install -y poppler-utils
sudo apt-get install -y libgl1-mesa-glx
sudo apt-get install -y libc6
sudo apt-get install -y GLIBC-2.36
nix-shell -p GLIBC-2.36
mkdir converted_images
ls
echo "Everything OK"
tesseract --version
