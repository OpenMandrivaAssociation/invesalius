Name:			invesalius
Group:			Sciences/Other
License:		GPLv2
Summary:		3D medical imaging reconstruction software
Version:		3.1.99994
Release:		2
URL:			http://svn.softwarepublico.gov.br/trac/invesalius/
Source0:		https://github.com/invesalius/invesalius3/archive/v%{version}.tar.gz
Source1:		%{name}.xpm

Requires:              pygtk2.0
Requires:              python-cairo
Requires:              python-dicom
#Requires:              python-itk
#Requires:              python-itk-numarray
#Requires:              python-nibabel
#Requires:              python-sigar
#Requires:              python-vtk
#Requires:              python-gdcm
#Requires:              python-imaging
Requires:              python-pillow
Requires:              python-serial
Requires:              wxPythonGTK
BuildRequires:         python-cython
BuildRequires:         python-numpy
BuildArch:             noarch

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

%prep
%autosetup -n %{name}3-%{version}
sed -i '127i\
        pass' invesalius/data/styles.py

%build
#perl -pi -e 's|/usr/local/bin/python|%{__python}|;' invesalius/invesalius.py
perl -pi -e 's|(DOC_DIR = ).*|$1"%{_docdir}/%{name}"|;' invesalius/constants.py
perl -pi -e 's|\bSpacing= |spacing=|;' invesalius/gui/default_tasks.py
%py_build

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
for dir in icons invesalius locale presets samples; do
    cp -far $dir %{buildroot}%{_datadir}/%{name}
done

mkdir -p %{buildroot}%{_docdir}/%{name}
for arg in *.txt docs/*; do
    cp -far $arg %{buildroot}%{_docdir}/%{name}
done

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh
export INVESALIUS_LIBRARY_PATH="%{_datadir}/%{name}/%{name}"
cd \$INVESALIUS_LIBRARY_PATH
python2 invesalius.py "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

install -m644 -D %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=InVesalius
Comment=Medical Imaging Public Software
Exec=invesalius
Icon=invesalius
Terminal=false
Type=Application
Categories=Application;Graphics;Medical;
EOF

sed -i 's|/usr/bin/env python$|/usr/bin/python2|' %{buildroot}%{_datadir}/invesalius/invesalius/*/*.py %{buildroot}%{_datadir}/invesalius/invesalius/*/*/*.py

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_docdir}/%{name}
%{_datadir}/applications/*
%{_datadir}/pixmaps/%{name}.xpm
