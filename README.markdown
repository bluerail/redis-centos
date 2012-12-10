# A Recipe for a Redis RPM on CentOS

Perform the following on a build box as a regular user.

## Create an RPM Build Environment

    sudo rpm -Uvh http://download.fedora.redhat.com/pub/epel/5/i386/epel-release-5-4.noarch.rpm 
    sudo yum install rpmdevtools
    rpmdev-setuptree

## Install Prerequisites for RPM Creation

    sudo yum groupinstall 'Development Tools'

## Download Redis

    wget http://redis.googlecode.com/files/redis-2.6.4.tar.gz
    cp redis-2.6.4.tar.gz ~/rpmbuild/SOURCES/

## Get Necessary System-specific Configs

    https://github.com/fauria/redis-centos
    cp redis-centos/conf/* ~/rpmbuild/SOURCES/
    cp redis-centos/spec/* ~/rpmbuild/SPECS/

## Build the RPM

    cd ~/rpmbuild/
    rpmbuild -ba SPECS/redis.spec

The resulting RPM will be:

    ~/rpmbuild/RPMS/x86_64/redis-2.6.4-1.{arch}.rpm

## Credits

Based on the `redis.spec` file from Jason Priebe, found on [Google Code][gc].

 [gc]: http://groups.google.com/group/redis-db/files
