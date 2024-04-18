
# sudo apt-get update

# # Remove old package lists (optional)
# sudo rm -fR /var/lib/apt/lists/*

# # Update again to refresh package lists after removal (optional)
sudo apt-get update

# # Install prerequisites
sudo apt-get install -y python-software-properties software-properties-common

# Remove the specific repository
sudo add-apt-repository -y ppa:alex-p/tesseract-ocr5

# Update package lists after repository removal
sudo apt-get update

# Install Tesseract OCR
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng

# Install Poppler utils without user interaction
sudo apt-get install -y poppler-utils
sudo apt install libgl1-mesa-glx
echo "Everything OK"

# Display Tesseract version
tesseract --version
