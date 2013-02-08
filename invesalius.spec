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
Release:		4
URL:			http://svn.softwarepublico.gov.br/trac/invesalius/
Source0:		%{name}%{vers}.tar.bz2
Source1:		%{name}.xpm
BuildRoot:		%{_tmppath}/%{name}-%{vers}-%{release}-buildroot

Requires:		pygtk2.0
Requires:		python-cairo
Requires:		python-dicom
Requires:		python-itk
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
  * Image manipulation facilities (zoom, pan, rotation, brightness/contrast, ..)
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


%changelog
* Thu Nov 17 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.0.1925-3mdv2012.0
+ Revision: 731313
- Remove dependency on wrapitk.

* Tue May 17 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.0.1925-2
+ Revision: 675930
- Add workaround for argument name change in wxPythonGTK-2.8.12.

* Fri Nov 12 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.0.1925-1mdv2011.0
+ Revision: 596961
- Update to new stable svn snapshot revision 1925

* Mon Aug 16 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.0.1912-1mdv2011.0
+ Revision: 570660
- Update requires and svn snapshot.
- Update to a newer svn snapshot.

* Tue May 18 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.0.1886-2mdv2010.1
+ Revision: 545264
- Avoid /tmp possible exploit or race condition

* Fri Apr 23 2010 Paulo Andrade <pcpa@mandriva.com.br> 3.0.1886-1mdv2010.1
+ Revision: 538371
- Update to a newer svn snapshot
- Enable itk and wrapitk were updated in cooker

* Mon Apr 05 2010 Paulo Andrade <pcpa@mandriva.com.br> 3-4mdv2010.1
+ Revision: 531858
- o Update license, summary and description as requested by upstream

* Thu Apr 01 2010 Paulo Andrade <pcpa@mandriva.com.br> 3-3mdv2010.1
+ Revision: 530740
+ rebuild (emptylog)

* Wed Mar 31 2010 Paulo Andrade <pcpa@mandriva.com.br> 3-2mdv2010.1
+ Revision: 530088
- Correct documentation search path

* Tue Mar 30 2010 Paulo Andrade <pcpa@mandriva.com.br> 3-1mdv2010.1
+ Revision: 529998
- Import invesalius 3.
- invesalius

