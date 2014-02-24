%define modname gmagick
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B01_%{modname}.ini

Summary:	Provides a wrapper to the GraphicsMagick library
Name:		php-%{modname}
Version:	1.1.2
Release:	1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/gmagick/
Source0:	http://pecl.php.net/get/gmagick-1.1.2RC1.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	graphicsmagick-devel >= 1.0.0
BuildRequires:	libsm-devel

%description
Gmagick is a php extension to create, modify and obtain meta information of
images using the GraphicsMagick API. This extension requires GraphicsMagick
version 1.2.6+ and PHP 5.1.3+.

%prep

%setup -qn %{modname}-%{version}RC1
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

%files 
%doc README package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-0.0.RC3.1mdv2012.0
+ Revision: 806385
- 1.1.0RC3

* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-0.0.RC2.1
+ Revision: 796959
- 1.1.0RC2

* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.10-0.0.b1.3
+ Revision: 795442
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.10-0.0.b1.2
+ Revision: 761238
- rebuild

* Wed Dec 07 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.10-0.0.b1.1
+ Revision: 738652
- 1.0.10b1

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.0.b1.8
+ Revision: 696425
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.0.b1.7
+ Revision: 695400
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.0.b1.6
+ Revision: 646641
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.0.b1.5mdv2011.0
+ Revision: 629800
- rebuilt for php-5.3.5

* Tue Jan 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.0.b1.4mdv2011.0
+ Revision: 628554
- fix deps (libsm-devel)
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.0.b1.3mdv2011.0
+ Revision: 600491
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.0.b1.2mdv2011.0
+ Revision: 588811
- rebuild

* Thu Sep 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-0.0.b1.1mdv2011.0
+ Revision: 578870
- 1.0.8b1

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-0.0.b5.1mdv2010.1
+ Revision: 514509
- fix versioning

* Sun Feb 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3b5-1mdv2010.1
+ Revision: 505840
- 1.0.3b5

* Sun Jan 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3b3-1mdv2010.1
+ Revision: 495451
- 1.0.3b3

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3b2-2mdv2010.1
+ Revision: 485363
- rebuilt for php-5.3.2RC1

* Sat Dec 19 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.3b2-1mdv2010.1
+ Revision: 480116
- 1.0.3b2

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.1b1-2mdv2010.1
+ Revision: 468169
- rebuilt against php-5.3.1

* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.1b1-1mdv2010.0
+ Revision: 452908
- import php-gmagick


* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.1b1-1mdv2010.0
- initial Mandriva package

