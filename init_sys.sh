#!/bin/bash
#description: add CentOS system init script

#安装常用软件
#安装系统后首先装这个epel源
yum -y install epel-release
yum -y install ntpd dstat mlocate perf gprof perl cpio lrzsz
yum -y install traceroute subversion git
yum -y install tree ftp
#安装sar
yum -y install sysstat
#安装htop
yum -y install htop
yum -y install rpm-build

#同步时间
ntpdate time.windows.com
/sbin/hwclock -w

#永久关闭防火墙
service iptables status
chkconfig iptables off

#安装Telnet
yum -y install xinetd telnet telnet-server
#配置telnet，设置开机启动，默认是关闭的
chkconfig telnet on

#简单配置vim
cd ~
git clone https://github.com/taoyunxing/github_test.git
cp -f github_test/vimrc ~/.vimrc
