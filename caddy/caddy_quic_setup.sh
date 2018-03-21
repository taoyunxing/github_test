#!/bin/sh
#description: 给出在CentOS 6.9上caddy服务器开启QUIC功能的自动化过程，假定root用户执行
#date： 2018-03-21
#author： tao_627@aliyun.com

#install Go 1.10+ env
#......

#download, compile and install caddy
cd $GOPATH/src
go get -v github.com/mholt/caddy/caddy
go get -v github.com/caddyserver/builds
cd github.com/mholt/caddy/caddy
go run build.go
mv ./caddy /usr/local/bin

#apply for valid domain in Aliyun.com and pay money
#make this domain point to the specified IP in A Record in DNS (also must buy)
#for example, my site is www.812506.xyz whose free ssl cert and key coming from Let's Encrypt
#......

#prepare ssl certifcate and key
#prepare caddy confile
#......

#setup caddy related directory
#confile file
sudo mkdir -p /etc/caddy
sudo touch /etc/caddy/Caddyfile

#ssl cert & key
sudo mkdir -p /etc/ssl/caddy
sudo chmod 0770 /etc/ssl/caddy

#website Root dir
sudo mkdir -p /var/www

#vim /etc/init.d/caddy
#https://github.com/mholt/caddy/blob/master/dist/init/linux-sysvinit/caddy
touch /etc/init.d/caddy
chmod +x /etc/init.d/caddy

#open some ports (tcp 80,443,2015, udp 80,443) in VPS
#vim /etc/sysconfig/iptables
#-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT-
#-A INPUT -p tcp -m state --state NEW -m tcp --dport 443 -j ACCEPT-
#-A INPUT -p tcp -m state --state NEW -m tcp --dport 2015 -j ACCEPT-
#-A INPUT -p tcp -m state --state NEW -m tcp --dport 2048 -j ACCEPT-
#-A INPUT -p udp -m state --state NEW -m udp --dport 443 -j ACCEPT
#/etc/init.d/iptables restart
#/etc/init.d/iptables status

#install start-stop-daemon in CentOS, need by /etc/init.d/caddy script
yum -y install gcc gcc-c++
wget http://developer.axis.com/download/distribution/apps-sys-utils-start-stop-daemon-IR1_9_18-2.tar.gz
tar -xzvf apps-sys-utils-start-stop-daemon-IR1_9_18-2.tar.gz
gcc start-stop-daemon.c -o start-stop-daemon
cp start-stop-daemon /usr/bin/start-stop-daemon

#start
#service caddy start

#open Chrome 64 and enable QUIC
#......

