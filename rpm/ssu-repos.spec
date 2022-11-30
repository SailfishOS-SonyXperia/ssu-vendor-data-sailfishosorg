# Build options
# These build options should be set in the obs project configuration this package
# belongs to like this:
# %%global <option> <value>

# Buildflavour
# On build.sailfishos.org the same build flavour that is used
# for devices that are in rnd is also used on devices that are in release mode.
# This because of the repositories there are usually used as an addition to existing
# repositories and not to replace them.
# Since we can can't use ssu to set the mode for each repository by default we do this:
#
# Set `sailfishosorg_flavour` to one of these below:
# - devel - bleeding edge, latest features straight from source code changes,
#   along with all the new bugs :)
# - testing - cutting edge, less instability
# - stable - currently not used
#
# On device this can be orriden by using:
# ssu set sailfishosorg_flavour <flavour>
#
%if 0%{!?sailfishosorg_flavour:1}
%define sailfishosorg_flavour testing
%endif

# Adaptation Organisation
# Right now Adaptations are build under the nemo Organisation.
# In case the layout differs `sailfishosorg_adaptationOrg` can be set to any organisation.
# For example project foobar with subproject bar this would be 'foobar:/bar'.

%if 0%{!?sailfishosorg_adaptationOrg:1}
%define sailfishosorg_adaptationOrg nemo
%endif

Name: ssu-repos
Version: 0.1
Release: 1
Summary: SSU repositories
BuildArch: noarch
License: GPLv2
Source0: %{name}-%{version}.tar.gz
%define keydir /etc/pki/rpm-gpg


%description
%{summary}.

%package -n ssu-vendor-data-sailfishosorg
Summary: BuildSailfishosorg vendor configuration data
Requires: ssu >= 0.44.7

%description -n ssu-vendor-data-sailfishosorg
%{summary}. A vendor (including Nemo) is supposed to put those configuration on device.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_datadir}/ssu/repos.d/
sed \
    -e "s|@FLAVOUR@|%{sailfishosorg_flavour}|g" \
    -e "s|@sailfishorgAdaptationOrg@|%{sailfishosorg_adaptationOrg}|g" \
    ssu/20-sailfishosorg.ini.in > %{buildroot}%{_datadir}/ssu/repos.d/20-sailfishosorg.ini


%files
%defattr(-,root,root,-)

%files -n ssu-vendor-data-sailfishosorg
%defattr(-,root,root,-)
%verify (not mtime) %{_datadir}/ssu/repos.d/20-sailfishosorg.ini
