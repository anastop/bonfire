#!/usr/bin/env bash

# grab settings.xml from odl repos
curl https://raw.githubusercontent.com/opendaylight/odlparent/master/settings.xml --create-dirs -o ./settings.xml

if [[ ! -z $http_proxy && ! -z $https_proxy ]]
then

    # remove the last line to append stuff
    head -n -1 settings.xml > temp.xml
    mv temp.xml settings.xml

    # Grab proxy ip and port from $http_proxy
    read HTTP_PROXY_IP HTTP_PROXY_PORT <<< `echo $http_proxy | sed 's~http[s]*://~~g' | sed -e "s/:/ /"`
    read HTTPS_PROXY_IP HTTPS_PROXY_PORT <<< `echo $https_proxy | sed 's~http[s]*://~~g' | sed -e "s/:/ /"`

    #create the proxies block in a temp file
    echo "" > /tmp/proxy_setup.tmp
    echo "  <proxies>" >> /tmp/proxy_setup.tmp
    echo "    <proxy>" >> /tmp/proxy_setup.tmp
    echo "      <id>http-proxy</id>" >> /tmp/proxy_setup.tmp
    echo "      <active>true</active>" >> /tmp/proxy_setup.tmp
    echo "      <protocol>http</protocol>" >> /tmp/proxy_setup.tmp
    echo "      <host>$HTTP_PROXY_IP</host>" >> /tmp/proxy_setup.tmp
    echo "      <port>$HTTP_PROXY_PORT</port>" >> /tmp/proxy_setup.tmp
    echo "      <nonProxyHosts>127.0.0.1,localhost,*.intracomtel.com</nonProxyHosts>" >> /tmp/proxy_setup.tmp
    echo "    </proxy>" >> /tmp/proxy_setup.tmp
    echo "    <proxy>" >> /tmp/proxy_setup.tmp
    echo "      <id>https-proxy</id>" >> /tmp/proxy_setup.tmp
    echo "      <active>true</active>" >> /tmp/proxy_setup.tmp
    echo "      <protocol>https</protocol>" >> /tmp/proxy_setup.tmp
    echo "      <host>$HTTPS_PROXY_IP</host>" >> /tmp/proxy_setup.tmp
    echo "      <port>$HTTPS_PROXY_PORT</port>" >> /tmp/proxy_setup.tmp
    echo "      <nonProxyHosts>127.0.0.1,localhost,*.intracomtel.com</nonProxyHosts>" >> /tmp/proxy_setup.tmp
    echo "    </proxy>" >> /tmp/proxy_setup.tmp
    echo "  </proxies>" >> /tmp/proxy_setup.tmp
    echo "</settings>" >> /tmp/proxy_setup.tmp

    # append temp file to settings.xml
    cat /tmp/proxy_setup.tmp | tee -a settings.xml
fi

# Creates file locally. Uncomment to have the xml file moved to .m2
mkdir -p $HOME/.m2
mv settings.xml $HOME/.m2/

