
echo "Everything OK"
tesseract --version


  'sudo apt-get install -y devscripts build-essential gawk bison texinfo',
  'echo "Everything OK ----------------------------------"',
  'mkdir $HOME/glibc/ && cd $HOME/glibc',
  'wget http://ftp.gnu.org/gnu/libc/glibc-2.36.tar.gz',
  'tar -xvzf glibc-2.36.tar.gz',
  'mkdir build',
  'mkdir glibc-2.36-install',
  'ls',
  'cd build',
  './glibc-2.36/configure --prefix=/glibc-2.36-install',
  'make',
  'make install',
