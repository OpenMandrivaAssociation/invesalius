%define	svnrev		1925
%define name		invesalius
%define vers		3
%define instdir		%{_datadir}/%{name}

# checkout procedure:
# http://svn.softwarepublico.gov.br/trac/invesalius/wiki/InVesalius/DownloadSource
# source build as:
# 	% svn checkout --username anonymous.invesalius@gmail.com http://svn.softwarepublico.gov.br/svn/invesalius/invesalius3/trunk invesalius3
# <<use 'invesalius' password>>
#	% rm -fr `find invesalius3 -type d -name .svn`
# 	% tar jcvf invesalius3.tar.bz2 invesalius3

Name:			%{name}
Group:			Sciences/Other
License:		GPLv2
Summary:		3D medical imaging reconstruction software
Version:		%{vers}.0.%{svnrev}
Release:		%mkrel 2
URL:			http://svn.softwarepublico.gov.br/trac/invesalius/
Source0:		%{name}%{vers}.tar.bz2
Source1:		%{name}.xpm
BuildRoot:		%{_tmppath}/%{name}-%{vers}-%{release}-buildroot

Requires:		pygtk2.0
Requires:		python-cairo
Requires:		python-dicom
Requires:		python-itk
Requires:		python-itkvtk
Requires:		python-itk-numarray
Requires:		python-nibabel
Requires:		python-sigar
Requires:		python-vtk
Requires:		python-gdcm
Requires:		python-imaging
Requires:		python-serial
Requires:		wxPythonGTK

#-----------------------------------------------------------------------
%description
  InVesalius generates 3D anatomical models based on a sequence of 2D DICOM
files acquired using CT or MRI equipments.  InVesalius is internationalized
(currently available in Chinese, English, French,  German, Greek, Portuguese,
Spanish) and provides several tools:
  * DICOM-support including: (a) ACR-NEMA version 1 and 2; (b) DICOM
    version 3.0 (including various encodings of JPEG -lossless and lossy-, RLE)
  * Image manipulation facilities (zoom, pan, rotation, brightness/contrast, etc)
  * Segmentation based on 2D slices
  * Pre-defined threshold ranges according to tissue of interest
  * Edition tools (similar to Paint Brush) based on 2D slices
  * 2D and 3D measurements (distance and angle)
  * 3D surface creation
  * 3D surface connectivity tools
  * 3D surface exportation (including: binary STL, OBJ, VRML, Inventor)
  * High-quality volume rendering
  * Pre-defined volume rendering presets
  * Volume rendering crop plane
  * Picture exportation (including: BMP, TIFF, JPG, PostScript, POV-Ray)

#-----------------------------------------------------------------------
%prep
%setup -q -n %{name}%{vers}

#-----------------------------------------------------------------------
%build
perl -pi -e 's|/usr/local/bin/python|%{__python}|;' invesalius/invesalius.py
perl -pi -e 's|(DOC_DIR = ).*|$1"%{_docdir}/%{name}"|;' invesalius/constants.py
perl -pi -e 's|\bSpacing= |spacing=|;' invesalius/gui/default_tasks.py

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
