# Copyright 2017-2022 Adrien Vergé

%define debug_package %{nil}

Name:           oauth2-proxy
Version:        7.4.0
Release:        1%{?dist}
Summary:        A reverse proxy that provides authentication with Google, Github or other provider
License:        MIT
URL:            https://github.com/oauth2-proxy/oauth2-proxy
Source0:        oauth2-proxy-v7.4.0.linux-amd64.tar.gz
Source1:        oauth2-proxy.cfg.example
Source2:        oauth2-proxy.service.example

BuildRequires: systemd

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd

%description
A reverse proxy and static file server that provides authentication using
Providers (Google, GitHub, and others) to validate accounts by email, domain or
group.

%prep
%setup -q -n oauth2-proxy-v%{version}.linux-amd64

%build
echo "For simplicity I use the official pre-built binary from the GitHub repo"
sed -i 's|/usr/local/bin/oauth2-proxy|/usr/bin/oauth2-proxy|g' %{SOURCE2}

%install
install -D -p -m 755 oauth2-proxy %{buildroot}%{_bindir}/oauth2-proxy
install -D -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/oauth2-proxy.cfg
install -D -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/oauth2-proxy.service

%pre
getent group www-data >/dev/null || groupadd -r www-data
getent passwd www-data >/dev/null || \
  useradd -r -g www-data -s /sbin/nologin www-data

%post
%systemd_post oauth2-proxy.service

%preun
%systemd_preun oauth2-proxy.service

%postun
%systemd_postun_with_restart oauth2-proxy.service

%files
%defattr(-,root,root,-)
%{_bindir}/oauth2-proxy
%config(noreplace) %{_sysconfdir}/oauth2-proxy.cfg
%{_unitdir}/oauth2-proxy.service

%changelog
* Mon Nov 14 2022 Adrien Vergé - 7.4.0-1
- Update to latest upstream version

* Wed Sep 6 2017 Adrien Vergé - 2.2-1
- Update to latest upstream version

* Mon Feb 6 2017 Adrien Vergé - 2.1-1
- Initial RPM release
