##Install NGINX to setup Web Server

#Setup Official NGINGX bionic repo
echo deb http://nginx.org/packages/ubuntu/ bionic nginx >> /etc/apt/sources.list
#change to /tmp to store temporary files
cd /tmp
#pull nginx signing key
wget https://nginx.org/keys/nginx_signing.key
#install nginx signing key
sudo apt-key add /tmp/nginx_signing.key
#update dependencies
sudo apt-get update -y
#install nginx (currently at 16.1)
sudo apt-get install nginx -y
#clone my repo in order to grab the nginx.conf file inside.
git clone https://github.com/redislabsdemo/acldemo.git
#remove existing nginx.conf file
sudo rm -f /etc/nginx/nginx.conf
#remove index.html
sudo rm -f /usr/share/nginx/html/index.html
#remove server error message
sudo rm -f /usr/share/nginx/html/50x.html
#Move nginx.conf file to correct location
mv ./acldemo/nginx.conf /etc/nginx/
#install aws cli tools to obtain public network info in automated fashion
sudo apt-get install awscli -y
#use aws cli tools to get public ip address
publicip=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
#use aws cli tools to get public ip dns name
publicdns=$(curl http://169.254.169.254/latest/meta-data/public-hostname)
#add the public dns and public ip address to the server name directive to ensure you can only access NGINX when the host header is that name.
sed -i "s/server_name[^;]*;/server_name $publicip $publicdns;/" /etc/nginx/nginx.conf
#AWS public DNS names are too long for NGINX to handle. 
#The following line is not required if your hostname and ipaddres are shorter. This line configures the size the server_name directive can be
sed -i "s/http {/http {\n    server_names_hash_bucket_size 128;/g" /etc/nginx/nginx.conf
#change directories to the directory we want the certificate to be installed in.
cd /etc/nginx
#create a self-signed certificate
sudo openssl req -x509 -nodes -days 365 -subj "/C=US/ST=CA/L=MountainView/O=Redislabs/OU=ProductDemos/CN=ACLDemoSelf-Signed" -newkey rsa:2048 -keyout /etc/nginx/nginx-selfsigned.key -out /etc/nginx/nginx-selfsigned.crt
#recycle nginx to make changes take effect.
service nginx restart

#Install Redis as a local host cache in protected-mode so that it can't be accessed externally.
sudo apt install build-essential tcl -y
sudo apt install tcl-tls -y
sudo apt install redis-tools -y
git clone https://github.com/antirez/redis.git
cd ./redis
make
./src/redis-server

#TODO Install Website for Demos
git clone https://github.com/redislabsdemo/acldemo.git
mv acldemo/index.html /usr/share/nginx/html/index.html
mv acldemo/redis-logo.png /usr/share/nginx/html/
mv acldemo/app.py /usr/share/nginx/html
mkdir /usr/share/nginx/html/static
mv acldemo/static/style.css /usr/share/nginx/html/static
