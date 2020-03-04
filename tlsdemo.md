# Pre-reqs

## Build Redis with TLS

### Note: Its very important that you make BUILD_TLS=yes rather than just use the standard make. Redis will not function with TLS otherwise.

```bash
sudo sudo apt update -y
sudo apt install build-essential tcl -y
sudo apt install tcl-tls -y
sudo apt install redis-tools -y
sudo apt install libssl-dev -y
git clone https://github.com/antirez/redis.git
cd ./redis
make BUILD_TLS=yes
./utils/gen-test-certs.sh
./runtest --tls
./src/redis-server --tls-port 6379 --port 0 \
        --tls-cert-file ./tests/tls/redis.crt \
        --tls-key-file ./tests/tls/redis.key \
        --tls-ca-cert-file ./tests/tls/ca.crt
```


# TLS Demo


```bash
#create key without password
openssl genrsa -out server.key 4098
#create csr
openssl req -new -key redis.key -out server.csr
#create certificate
openssl x509 -req -days 366 -in server.csr -signkey redis.key -out redis.crt
#create ca file because this is self-signed and the issuer is the actual certificate.
cp redis.crt ca.crt 
#move all files to the redis directory for simple config
mv redis.crt ./redis-6.0-rc1 ; mv redis.key ./redis-6.0-rc1 ; mv ca.crt ./redis-6.0-rc1
#Move to Redis Directory
cd ./redis-6.0-rc1
#Start Redis Server
/src/redis-server redis.conf
#Connect to Redis Server on the Server
./src/redis-cli --tls --cert ./redis.crt --key ./redis.key --cacert ./ca.crt
#Disable Protected Mode
./src/redis-cli --tls --cert ./redis.crt --key ./redis.key --cacert ./ca.crt config set protected-mode no
#Copy Files from redis.crt, ca.crt and redis.key to your remote host.
redis-cli --tls --cert ./redis.crt --key ./redis.key --cacert ./ca.crt -h "inserthostname"
#Demonstrate that you are reset by peer if not using TLS
redis-cli -h "inserthostname"
#Demonstrate that certificate verification is required.
./src/redis-cli --tls --cert ./redis.crt --key ./redis.key  -h "inserthostname"
```



### Demonstrate how to change TLS configuration in Redis.conf by ensure the following variables are set

- tls-prefer-server-ciphers yes #Ensures that server ciphers are enforced and client is not able to downgrade.

- tls-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384 

The above configuration leverages the mozilla moderate for TLS 1.2 found at https://ssl-config.mozilla.org/

- tls-ciphersuites TLS_CHACHA20_POLY1305_SHA256 #For TLS 1.3 only

- tls-ciphersuites "TLSv1.2 TLSv1.3"


