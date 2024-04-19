
sudo apt-get update
pip install --upgrade build setuptools

# # Install prerequisites
sudo apt-get install -y python-software-properties software-properties-common
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get install gcc-4.9
sudo apt-get upgrade libstdc++6

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

exho "-------------------------------------------------"
echo "NIX_ENV"
exho "-------------------------------------------------"
nix-env -iA iconv -f https://github.com/NixOS/nixpkgs/archive/9957cd48326fe8dbd52fdc50dd2502307f188b0d.tar.gz
exho "-------------------------------------------------"
echo "NIX_SHELL"
exho "-------------------------------------------------"
nix-shell -p iconv -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/9957cd48326fe8dbd52fdc50dd2502307f188b0d.tar.gz

mkdir converted_images
ls
echo "Everything OK"
tesseract --version
