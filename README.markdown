# A Recipe for a Redis RPM on CentOS

Perform the following on a build box as a regular user.

## Create an RPM Build Environment

Install rpmdevtools from the [EPEL][epel] repository:

    sudo yum install rpmdevtools
    rpmdev-setuptree

## Install Prerequisites for RPM Creation

    sudo yum groupinstall 'Development Tools'

## Download Redis

    wget http://redis.googlecode.com/files/redis-2.6.8.tar.gz
    mv redis-2.6.8.tar.gz ~/rpmbuild/SOURCES/

## Get Necessary System-specific Configs

    git clone git://github.com/bluerail/redis-centos.git
    cp redis-centos/conf/* ~/rpmbuild/SOURCES/
    cp redis-centos/spec/* ~/rpmbuild/SPECS/

## Build the RPM

    cd ~/rpmbuild/
    rpmbuild -ba SPECS/redis.spec

The resulting RPM will be:

    ~/rpmbuild/RPMS/x86_64/redis-2.6.8-1.{arch}.rpm

## Credits

Based on the `redis.spec` file from Jason Priebe.

Maintained by [Martijn Storck](martijn@bluerail.nl)

[EPEL]: http://fedoraproject.org/wiki/EPEL#How_can_I_use_these_extra_packages.3F
