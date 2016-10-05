Name:           iotivity-example
Version:        1.0.0
Release:        0
License:        Apache-2.0
Summary:        Very minimalist example of IoTivity resource
Url:            http://github.com/TizenTeam/iotivity-example
Group:          System/Libraries
#X-Vc-Url:      http://github.com/TizenTeam/iotivity-example
Group:          Contrib
Source:         %{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  fdupes
BuildRequires:  iotivity-devel
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(dlog)
BuildRequires:  systemd
Requires:  iotivity


%description
Mimimal client/server application,
that share a binarry switch value as IoTivity resource.

%prep
%setup -q

%build

%__make %{?_smp_mflags} \
    PLATFORM=TIZEN \
    #eol

%install
%__make install \
    DEST_LIB_DIR=%{buildroot}/opt/%{name}/ \
    PLATFORM=TIZEN \
    #eol

install -d %{buildroot}%{_unitdir}/network.target.wants
install extra/iotivity-example.service \
  %{buildroot}%{_unitdir}/%{name}.service

sed -e "s|ExecStart=.*|ExecStart=/opt/%{name}/server|g" -i \
  %{buildroot}%{_unitdir}/%{name}.service

#ln -s ../%{name}.service \
#  %{buildroot}%{_unitdir}/network.target.wants/%{name}.service
%install_service network.target.wants %{name}.service


%fdupes %{buildroot}

%post -p /sbin/ldconfig
systemctl enable %{name}


%postun -p /sbin/ldconfi
systemctl disable %{name}


%files
%defattr(-,root,root)
/opt/%{name}/*
%{_unitdir}/%{name}.service
%{_unitdir}/network.target.wants/%{name}.service

