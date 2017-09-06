# Copyright 2017 Adrien Vergé

%define debug_package %{nil}

Name:           oauth2-proxy
Version:        2.2
Release:        1%{?dist}
Summary:        A reverse proxy that provides authentication with Google, Github or other provider
License:        MIT
URL:            https://github.com/bitly/oauth2_proxy
Source0:        oauth2_proxy-v%{version}.tar.gz

BuildRequires: git
BuildRequires: golang
BuildRequires: systemd

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd

%description
A reverse proxy and static file server that provides authentication using
Providers (Google, GitHub, and others) to validate accounts by email, domain or
group.

%prep
%setup -q -n oauth2_proxy-%{version}

%build
export GOPATH=$(pwd)/_build
export GOBIN=$(pwd)/_build/bin
go get .
go build -o oauth2_proxy .
sed -i 's|/usr/local/bin/oauth2_proxy|/usr/bin/oauth2_proxy|g' \
  contrib/oauth2_proxy.service.example

%install
install -D -p -m 755 oauth2_proxy %{buildroot}%{_bindir}/oauth2_proxy
install -D -p -m 644 contrib/oauth2_proxy.cfg.example \
  %{buildroot}%{_sysconfdir}/oauth2_proxy.cfg
install -D -p -m 644 contrib/oauth2_proxy.service.example \
  %{buildroot}%{_unitdir}/oauth2_proxy.service

%pre
getent group www-data >/dev/null || groupadd -r www-data
getent passwd www-data >/dev/null || \
  useradd -r -g www-data -s /sbin/nologin www-data

%post
%systemd_post oauth2_proxy.service

%preun
%systemd_preun oauth2_proxy.service

%postun
%systemd_postun_with_restart oauth2_proxy.service

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/oauth2_proxy
%config(noreplace) %{_sysconfdir}/oauth2_proxy.cfg
%{_unitdir}/oauth2_proxy.service

%changelog
* Wed Sep 6 2017 Adrien Vergé - 2.2-1
- Update to latest upstream version

* Mon Feb 6 2017 Adrien Vergé - 2.1-1
- Initial RPM release
