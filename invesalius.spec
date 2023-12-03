# FIXME debugsource should not be empty
#define	debug_package	%{nil}

# FIXME actually OM texlive and doxygen are broken!
%bcond_with _build_doc

Name:		invesalius
Group:		Sciences/Other
License:	GPLv2
Summary:	3D medical imaging reconstruction software
Version:	3.1.99998
Release:	7
URL:		https://invesalius.github.io
Source0:	https://github.com/invesalius/invesalius3/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.xpm
Patch0:		invesalius3-3.1.99998-python3.11.patch
# Make it work with the version of gdcm we ship
Patch1:		https://github.com/invesalius/invesalius3/commit/89d6c18e223935a89526362c45c9ca424d1f5d1c.patch
Patch2:		https://github.com/invesalius/invesalius3/commit/22a0da312891c9dd2d4fbbdd3a838fd8dba4ee06.patch
Patch3:		https://github.com/invesalius/invesalius3/commit/f8af93cc22ad3867cecc2973ebd3c8c995903237.patch

BuildRequires:	imagemagick
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(cython)
BuildRequires:	python3dist(numpy)
%if %{with _build_doc}
BuildRequires:	texlive
%endif

Requires:	python-gdcm
Requires:	python%{pyver}dist(cython)
Requires:	python%{pyver}dist(h5py)
Requires:	python%{pyver}dist(keras)
Requires:	python%{pyver}dist(imageio)
Requires:	python%{pyver}dist(nibabel)
Requires:	python%{pyver}dist(numpy)
Requires:	python%{pyver}dist(pillow)
Requires:	python%{pyver}dist(psutil)
Requires:	python%{pyver}dist(pyacvd)
Requires:	python%{pyver}dist(pypubsub)
Requires:	python%{pyver}dist(scipy)
Requires:	python%{pyver}dist(pyserial)
Requires:	python%{pyver}dist(scikit-image)
Requires:	python%{pyver}dist(theano)
Requires:	python%{pyver}dist(wxpython)
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

