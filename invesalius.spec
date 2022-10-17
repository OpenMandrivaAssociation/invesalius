# FIXME debugsource should not be empty
#define	debug_package	%{nil}

# FIXME actually OM texlive and doxygen are broken!
%bcond_with _build_doc

Name:		invesalius
Group:		Sciences/Other
License:	GPLv2
Summary:	3D medical imaging reconstruction software
Version:	3.1.99997
Release:	3
URL:		http://svn.softwarepublico.gov.br/trac/invesalius/
Source0:	https://github.com/invesalius/invesalius3/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.xpm

BuildRequires:	imagemagick
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(cython)
BuildRequires:	python3dist(numpy)
%if %{with _build_doc}
BuildRequires:	texlive
%endif

Requires:	python3dist(cython)
Requires:	python-gdcm
Requires:	python3dist(h5py)
Requires:	python3dist(keras)
Requires:	python3dist(imageio)
Requires:	python3dist(nibabel)
Requires:	python3dist(numpy)
Requires:	python3dist(pillow)
Requires:	python3dist(psutil)
Requires:	python3dist(pyacvd)
Requires:	python3dist(pypubsub)
Requires:	python3dist(scipy)
Requires:	python3dist(pyserial)
Requires:	python3dist(scikit-image)
Requires:	python3dist(theano)
Requires:	python3dist(wxpython)
Requires:	python-vtk

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
%license LICENSE.txt
%doc AUTHORS.md changelog.md HEADER.txt README.md docs/user_guide_en.pdf docs/user_guide_pt_BR.pdf
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/openmandriva-%{name}.desktop
%{_datadir}/pixmaps/%{name}.xpm
%{_iconsdir}/hicolor/*/apps/%{name}.png

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}3-%{version}

%build
%{__python} setup.py build build_ext --inplace

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
#%%py_install

# data
mkdir -p %{buildroot}%{_datadir}/%{name}
for dir in ai icons invesalius locale presets samples
do
	cp -far $dir %{buildroot}%{_datadir}/%{name}
done

# fix plugins path
mkdir -p %{buildroot}%{_libdir}/%{name}/%{name}_cy
cp -far %{name}_cy/*{py,so} %{buildroot}%{_libdir}/%{name}/%{name}_cy


# add app
cp -far app.py %{buildroot}%{_datadir}/%{name}/

# launcher
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh
#export INV_SAMPLE_DIR="%{_datadir}/%{name}/samples/"
#export GDK_BACKEND=x11
export PYTHONPATH=\$PYTHONPATH:"%{_libdir}/%{name}"
export INVESALIUS_LIBRARY_PATH="%{_datadir}/%{name}"
cd \$INVESALIUS_LIBRARY_PATH
%{__python} app.py "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

# .desktop
install -dm 0755 %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/openmandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=InVesalius
Comment=Medical Imaging Public Software
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Application;Graphics;Medical;
X-Vendor=OpenMandriva
EOF

# icon
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -size "${d}x${d}" "%{SOURCE1}" \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -m644 -D %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

