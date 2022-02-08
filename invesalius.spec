%bcond_with _build_doc

Name:			invesalius
Group:			Sciences/Other
License:		GPLv2
Summary:		3D medical imaging reconstruction software
Version:		3.1.99997
Release:		1
URL:			http://svn.softwarepublico.gov.br/trac/invesalius/
Source0:		https://github.com/invesalius/invesalius3/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:		%{name}.xpm

BuildRequires:         python-cython
BuildRequires:         python-numpy
%if %{with _build_doc}
BuildRequires:         texlive
%endif

Requires:	python-cython
Requires:	python-gdcm
Requires:	python-h5py
Requires:	python-keras
Requires:	python-imageio
Requires:	python-imaging
Requires:	python-nibabel
Requires:	python-numpy
Requires:	python-psutil
Requires:	python-pypubsub
Requires:	python-scipy
Requires:	python-serial
Requires:	python-skimage
Requires:	python-theano
Requires:	python-vtk
Requires:	wxPythonGTK

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

%files
%license LICENSE.txt LICENSE.pt.txt
%doc AUTHORS.md changelog.md HEADER.txt README.md docs/user_guide_en.pdf docs/user_guide_pt_BR.pdf
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/pixmaps/%{name}.xpm

#-----------------------------------------------------------------------

%prep
%autosetup -n %{name}3-%{version}

%build
%py_build

# build docs
%if %{with _build_doc}
for arg in docs/{user_guide_en_source,user_guide_pt_BR_source}; do
    pushd ${arg}
		make
	popd
done
%endif

%install
# install doesn't work
#py_install

# data
mkdir -p %{buildroot}%{_datadir}/%{name}
for dir in ai icons invesalius locale presets samples; do
    cp -far $dir %{buildroot}%{_datadir}/%{name}
done

# fix plugins path
mv %{buildroot}%{py_platsitedir}/%{name}_cy %{buildroot}%{_datadir}/%{name}/
cp -fa %{name}_cy/*py %{buildroot}%{_datadir}/%{name}/%{name}_cy
rm -fr %{buildroot}%{_libdir}/

# add app
cp -fa app.py %{buildroot}%{_datadir}/%{name}/

# launcher
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh
#export INV_SAMPLE_DIR="%{_datadir}/%{name}/samples/"
#export GDK_BACKEND=x11
export INVESALIUS_LIBRARY_PATH="%{_datadir}/%{name}"
cd \$INVESALIUS_LIBRARY_PATH
%{__python} invesalius.py "\$@"
%{__python} app.py "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

# .desktop
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

# icon
install -m644 -D %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

