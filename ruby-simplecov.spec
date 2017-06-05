#
# Conditional build:
%bcond_without	doc	# ri/rdoc documentation

%define pkgname simplecov
Summary:	Code coverage for Ruby 1.9+
Summary(pl.UTF-8):	Pokrycie kodu dla języka Ruby 1.9+
Name:		ruby-%{pkgname}
Version:	0.14.1
Release:	1
License:	MIT
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	dc307ae2de2bd70c9c64ca3fd5ae61a5
Group:		Development/Languages
URL:		https://rubygems.org/gems/simplecov
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby >= 1:1.8.7
BuildRequires:	ruby-rdoc
Requires:	ruby >= 1:1.8.7
Requires:	ruby-docile >= 1.1.0
Requires:	ruby-json >= 1.8
Requires:	ruby-json < 3
Requires:	ruby-simplecov-html >= 0.10.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Code coverage for Ruby 1.9+ with a powerful configuration library
and automatic merging of coverage across test suites.

%description -l pl.UTF-8
Pokrycie kodu dla języka Ruby 1.9+ z potężną biblioteką konfiguracyjną
oraz automatycznym łączeniem pokrycia z różnych zbiorów testów.

%package rdoc
Summary:	HTML documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla moduły języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla moduły języka Ruby %{pkgname}.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} -r ri/created.rid ri/{Coverage,Rails}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_ridir},%{ruby_rdocdir}/%{name}-%{version}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}

cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

# install gemspec
install -d $RPM_BUILD_ROOT%{ruby_specdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md MIT-LICENSE README.md
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/SimpleCov
%{ruby_ridir}/lib/simplecov
%endif
