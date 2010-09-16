%define modname gmagick
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B01_%{modname}.ini

Summary:	Provides a wrapper to the GraphicsMagick library
Name:		php-%{modname}
Version:	1.0.8
Release:	%mkrel 0.0.b1.1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/gmagick/
Source0:	http://pecl.php.net/get/%{modname}-%{version}b1.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	graphicsmagick-devel >= 1.0.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gmagick is a php extension to create, modify and obtain meta information of
images using the GraphicsMagick API. This extension requires GraphicsMagick
version 1.2.6+ and PHP 5.1.3+.

%prep

%setup -q -n %{modname}-%{version}b1
[ "../package*.xml" != "/" ] && mv ../package*.xml .

find -type f | xargs chmod 644

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

