oauth2_proxy copr repository
============================

This repository provides unofficial packages of oauth2_proxy (previously Google
Auth Proxy) for CentOS 7+ and Fedora 25+. They are available at:

https://copr.fedorainfracloud.org/coprs/adrienverge/oauth2_proxy/

Install
-------

Fedora:

.. code:: shell

 sudo dnf copr enable adrienverge/oauth2_proxy
 sudo dnf install oauth2-proxy

CentOS:

.. code:: shell

 sudo yum install yum-plugin-copr
 sudo yum copr enable adrienverge/oauth2_proxy
 sudo yum install oauth2-proxy

Build RPM locally
-----------------

.. code:: shell

 rpmbuild -bs oauth2-proxy.spec
 # enable config_opts['rpmbuild_networking'] in /etc/mock/site-defaults.cfg
 mock -r epel-7-x86_64 rebuild ~/rpmbuild/SRPMS/oauth2-proxy-2.*.src.rpm
