%define	svnrev		1833
%define name		invesalius
%define version		3
%define instdir		%{_datadir}/%{name}

# checkout procedure:
# http://svn.softwarepublico.gov.br/trac/invesalius/wiki/InVesalius/DownloadSource
# source build as:
# 	% svn co svn checkout --username anonymous.invesalius@gmail.com http://svn.softwarepublico.gov.br/svn/invesalius/invesalius3/trunk invesalius3
# <<use 'invesalius' password>>
#	% rm -fr `find invesalius3 -type d -name .svn`
# 	% tar jcvf invesalius.tar.bz2 invesalius3

Name:			%{name}
Group:			Sciences/Other
License:		GPL
Summary:		Medical Imaging Public Software
Version:		%{version}
Release:		%mkrel 2
URL:			http://svn.softwarepublico.gov.br/trac/invesalius/
Source0:		%{name}%{version}.tar.bz2
Source1:		%{name}.xpm
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires:		pygtk2.0
Requires:		python-cairo
#Requires:		python-itk
Requires:		python-sigar
Requires:		python-vtk
Requires:		python-gdcm
Requires:		wxPythonGTK

#-----------------------------------------------------------------------
%description
InVesalius is a free software (GNU GPL 2) build in collaboration with the
community. It generates 3D medical imaging reconstruction based on a sequence
of 2D DICOM files acquired with CT or MRI equipments, providing several
visualization tools.

#-----------------------------------------------------------------------
%prep
%setup -q -n %{name}%{version}

#-----------------------------------------------------------------------
%build
perl -pi -e 's|/usr/local/bin/python|%{__python}|;' invesalius/invesalius.py
perl -pi -e 's|^import itk||;' invesalius/reader/analyze_reader.py
perl -pi -e 's|(DOC_DIR = ).*|$1"%{_docdir}/%{name}"|;' invesalius/constants.py

#-----------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-----------------------------------------------------------------------
%install
mkdir -p %{buildroot}%{instdir}
for dir in icons invesalius locale presets samples; do
    cp -far $dir %{buildroot}%{instdir}
done

mkdir -p %{buildroot}%{_docdir}/%{name}
for arg in *.txt TODO docs/*; do
    cp -far $arg %{buildroot}%{_docdir}/%{name}
done

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh
export INVESALIUS_LIBRARY_PATH="%{instdir}/%{name}"
cd \$INVESALIUS_LIBRARY_PATH
python invesalius.py "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

install -m644 -D %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=InVesalius
Comment=Medical Imaging Public Software
Exec=invesalius
Icon=invesalius
Terminal=false
Type=Application
Categories=Application;Graphics;Medical;
EOF

#-----------------------------------------------------------------------
%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{instdir}
%{instdir}/*
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/%{name}.xpm
