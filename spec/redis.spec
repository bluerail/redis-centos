%define pid_dir %{_localstatedir}/run/redis
%define pid_file %{pid_dir}/redis.pid
%define redis_ver 2.4.17
%define redis_rel 2

Summary: Redis is an open source, advanced key-value store
Name: redis
Version: %{redis_ver}
Release: %{redis_rel}
License: BSD
Group: Applications/Databases
URL: http://redis.io

Source0: redis-%{redis_ver}.tar.gz
Source2: redis.init
Source3: redis.logrotate
Patch0: redis-conf.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc, make
Requires(post): /sbin/chkconfig /usr/sbin/useradd
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Provides: redis

%description
Redis is an open source, advanced key-value store. It is often referred to as a
data structure server since keys can contain strings, hashes, lists, sets and
sorted sets.

You can run atomic operations on these types, like appending to a string;
incrementing the value in a hash; pushing to a list; computing set intersection,
union and difference; or getting the member with highest ranking in a sorted
set.

In order to achieve its outstanding performance, Redis works with an in-memory
dataset. Depending on your use case, you can persist it either by dumping the
dataset to disk every once in a while, or by appending each command to a log.

Redis also supports trivial-to-setup master-slave replication, with very fast
non-blocking first synchronization, auto-reconnection on net split and so forth.

Other features include a simple check-and-set mechanism, pub/sub and
configuration settings to make Redis behave like a cache.

You can use Redis from most programming languages out there.

Redis is written in ANSI C and works in most POSIX systems like Linux, *BSD,
OS X and Solaris without external dependencies. There is no official support
for Windows builds, although you may have some options.

%prep
%setup -n %{name}-%{redis_ver}
%patch0 -p1

%build
%{__make}

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%{__install} -Dp -m 0755 src/redis-server %{buildroot}%{_sbindir}/redis-server
%{__install} -Dp -m 0755 src/redis-benchmark %{buildroot}%{_bindir}/redis-benchmark
%{__install} -Dp -m 0755 src/redis-cli %{buildroot}%{_bindir}/redis-cli

%{__install} -Dp -m 0755 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/redis
%{__install} -Dp -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/redis
%{__install} -Dp -m 0644 redis.conf %{buildroot}%{_sysconfdir}/redis.conf
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/lib/redis
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/log/redis
%{__install} -p -d -m 0755 %{buildroot}%{pid_dir}

%pre
getent group redis >/dev/null  || groupadd -r redis -g 496
getent passwd redis >/dev/null || \
    useradd -r -u 496 -g redis -d %{_localstatedir}/lib/redis -s /sbin/nologin \
    -c "User for redis database" redis


%preun
if [ $1 = 0 ]; then
    # make sure redis service is not running before uninstalling

    # when the preun section is run, we've got stdin attached.  If we
    # call stop() in the redis init script, it will pass stdin along to
    # the redis-cli script; this will cause redis-cli to read an extraneous
    # argument, and the redis-cli shutdown will fail due to the wrong number
    # of arguments.  So we do this little bit of magic to reconnect stdin
    # to the terminal
    term="/dev/$(ps -p$$ --no-heading | awk '{print $2}')"
    exec < $term

    /sbin/service redis stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del redis
fi

%post
/sbin/chkconfig --add redis

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_sbindir}/redis-server
%{_bindir}/redis-benchmark
%{_bindir}/redis-cli
%{_sysconfdir}/init.d/redis
%config(noreplace) %{_sysconfdir}/redis.conf
%{_sysconfdir}/logrotate.d/redis
%dir %attr(0770,redis,redis) %{_localstatedir}/lib/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/log/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/run/redis

%changelog
* Fri Feb 27 2012 Martijn Storck <martijn@bluerail.nl> 2.4.8-2
- Change uid for CentOS 6 compatibility
- Don't suppress useradd warnings

* Fri Feb 27 2012 Martijn Storck <martijn@bluerail.nl> 2.4.8-1
- Upgrade to 2.4.8
- Update description
- Update redis.conf patch
- Removed documentation as it's no longer included in the source

* Fri Sep 23 2011 Martijn Storck <martijn@bluerail.nl> 2.2.14-1
- Upgrade to 2.2.14
- Update website URL

* Thu Aug 21 2011 Alex Simenduev <shamil.si@gmail.com> 2.2.12-1
- Upgrade to 2.2.12

* Thu Feb 24 2011 SHIBATA Hiroshi <h-shibata@esm.co.jp> 2.2.1-0
- Upgrade to 2.2.1

* Tue Nov  9 2010 SHIBATA Hiroshi <h-shibata@esm.co.jp> 2.0.4-1
- Upgrade to 2.0.4

* Tue Aug  3 2010 Karanbir Singh <kbsingh@karan.org> 2.0.0-rc4..el5.kb.1
- Upgrade to 2.0.0rc4
- Move init script to its own file, expand the rpm macros into static values
- Move logrotate script to its own file
- bring in the conf file into the same dir as spec file
- Remove Packager tag from spec ( should be set in the .rpmmacros )
- Add a Dist tag to Release
- Use the redis.conf included in the tarball
- Patch redis.conf included in tarball to make it behave like a server

* Tue Jul 13 2010 - jay at causes dot com 2.0.0-rc2
- upped to 2.0.0-rc2

* Mon May 24 2010 - jay at causes dot com 1.3.9-2
- moved pidfile back to /var/run/redis/redis.pid, so the redis
  user can write to the pidfile.
- Factored it out into %{pid_dir} (/var/run/redis), and
  %{pid_file} (%{pid_dir}/redis.pid)


* Wed May 05 2010 - brad at causes dot com 1.3.9-1
- redis updated to version 1.3.9 (development release from GitHub)
- extract config file from spec file
- move pid file from /var/run/redis/redis.pid to just /var/run/redis.pid
- move init file to /etc/init.d/ instead of /etc/rc.d/init.d/

* Fri Sep 11 2009 - jpriebe at cbcnewmedia dot com 1.0-1
- redis updated to version 1.0 stable

* Mon Jun 01 2009 - jpriebe at cbcnewmedia dot com 0.100-1
- Massive redis changes in moving from 0.09x to 0.100
- removed log timestamp patch; this feature is now part of standard release

* Tue May 12 2009 - jpriebe at cbcnewmedia dot com 0.096-1
- A memory leak when passing more than 16 arguments to a command (including
  itself).
- A memory leak when loading compressed objects from disk is now fixed.

* Mon May 04 2009 - jpriebe at cbcnewmedia dot com 0.094-2
- Patch: applied patch to add timestamp to the log messages
- moved redis-server to /usr/sbin
- set %config(noreplace) on redis.conf to prevent config file overwrites
  on upgrade

* Fri May 01 2009 - jpriebe at cbcnewmedia dot com 0.094-1
- Bugfix: 32bit integer overflow bug; there was a problem with datasets
  consisting of more than 20,000,000 keys resulting in a lot of CPU usage
  for iterated hash table resizing.

* Wed Apr 29 2009 - jpriebe at cbcnewmedia dot com 0.093-2
- added message to init.d script to warn user that shutdown may take a while

* Wed Apr 29 2009 - jpriebe at cbcnewmedia dot com 0.093-1
- version 0.093: fixed bug in save that would cause a crash
- version 0.092: fix for bug in RANDOMKEY command

* Fri Apr 24 2009 - jpriebe at cbcnewmedia dot com 0.091-3
- change permissions on /var/log/redis and /var/run/redis to 755; this allows
  non-root users to check the service status and to read the logs

* Wed Apr 22 2009 - jpriebe at cbcnewmedia dot com 0.091-2
- cleanup of temp*rdb files in /var/lib/redis after shutdown
- better handling of pid file, especially with status

* Tue Apr 14 2009 - jpriebe at cbcnewmedia dot com 0.091-1
- Initial release.
