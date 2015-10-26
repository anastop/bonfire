#!/usr/bin/env bash

su -p vagrant << EOF
cd /opt

# Install openjdk 1.8_60
wget --no-check-certificate -nc http://www.java.net/download/jdk8u66/archive/b02/binaries/jdk-8u66-ea-bin-b02-linux-x64-28_jul_2015.tar.gz -P /vagrant/files/
cp /vagrant/files/jdk-8u66-ea-bin-b02-linux-x64-28_jul_2015.tar.gz .
mkdir -p /opt/openjdk
tar -xvf jdk-8u66-ea-bin-b02-linux-x64-28_jul_2015.tar.gz -C /opt/openjdk/

# Install Oracle JDK
wget --no-check-certificate --no-cookies -nc --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u60-b27/jdk-8u60-linux-x64.tar.gz -P /vagrant/files/
cp /vagrant/files/jdk-8u60-linux-x64.tar.gz .
mkdir -p /opt/oraclejdk
tar -xvf jdk-8u60-linux-x64.tar.gz -C /opt/oraclejdk/

# Install Maven 3.3.3
wget -nc http://mirrors.myaegean.gr/apache/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz
tar -xvf apache-maven-3.3.3-bin.tar.gz
mv apache-maven-3.3.3 /opt/maven/

EOF

OPENJDK_HOME=/opt/openjdk/jdk1.8.0_66
echo "export OPENJDK_HOME=$OPENJDK_HOME" >> /etc/profile
echo "export OPENJDK_HOME=$OPENJDK_HOME" >> /etc/bash.bashrc

echo "Setup java @ $OPENJDK_HOME"

JAVA_HOME=/opt/oraclejdk/jdk1.8.0_60
echo "export JAVA_HOME=$JAVA_HOME" >> /etc/profile
echo "export JAVA_HOME=$JAVA_HOME" >> /etc/bash.bashrc
ln -sf $JAVA_HOME/bin/java /usr/bin/java
ORACLEJDK_HOME=/opt/oraclejdk/jdk1.8.0_60
echo "export ORACLEJDK_HOME=$ORACLEJDK_HOME" >> /etc/profile
echo "export ORACLEJDK_HOME=$ORACLEJDK_HOME" >> /etc/bash.bashrc

M2_HOME=/opt/maven/
echo "export M2_HOME=$M2_HOME" >> /etc/profile
echo "export M2_HOME=$M2_HOME" >> /etc/bash.bashrc
echo 'export MAVEN_OPTS="-Xms256m -Xmx512m"' >> /etc/bash.bashrc # Very important to put the "m" on the end
ln -sf /opt/maven/bin/mvn /usr/bin/mvn

mkdir -p /home/vagrant/.m2
chown vagrant /home/vagrant/.m2

yes | cp -f /vagrant/config/jmc.ini $ORACLEJDK_HOME/jmc.ini
yes | cp -f /vagrant/config/full_profile.jfc $ORACLEJDK_HOME/jre/lib/jfr/full_profile.jfc

echo vagrant | sudo -S update-alternatives --install /usr/bin/mvn mvn $M2_HOME/bin/mvn 1000
echo vagrant | sudo -S update-alternatives --install /usr/bin/java java $OPENJDK_HOME/bin/java 1100
echo vagrant | sudo -S update-alternatives --install /usr/bin/javac javac $OPENJDK_HOME/bin/javac 1100
echo vagrant | sudo -S update-alternatives --install /usr/bin/java java $ORACLEJDK_HOME/bin/java 1200
echo vagrant | sudo -S update-alternatives --install /usr/bin/javac javac $ORACLEJDK_HOME/bin/javac 1200
echo vagrant | sudo -S update-alternatives --install /usr/bin/jmc jmc $ORACLEJDK_HOME/bin/jmc 1000
