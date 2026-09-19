Name:           linux-id
Version:        0.2.4
Release:        2%{?dist}
Summary:        FIDO token implementation for Linux using TPM

%global debug_package %{nil}

License:        MIT
URL:            https://github.com/matejsmycka/linux-id
Source0:        https://github.com/matejsmycka/linux-id/archive/refs/tags/v%{version}.tar.gz
Source1:        linux-id.service
Source2:        60-linux-id-fido-tpm.rules
Source3:        uhid.conf

BuildRequires:  golang >= 1.21
BuildRequires:  systemd-rpm-macros
BuildRequires:  go-rpm-macros
BuildRequires:  tpm2-tss-devel

Requires:       pinentry
Requires:       tpm2-tools

Recommends:     fprintd
Recommends:     fprintd-pam

%description
linux-id is a FIDO2/WebAuthn software token for Linux that stores private
keys inside the system TPM 2.0 chip. It emulates a USB HID device via the
kernel's uhid facility so that browsers detect it like a hardware key.

By default, linux-id uses pinentry for presence confirmation. To use fingerprint
authentication via fprintd instead:

  1. Ensure a fingerprint is enrolled:
     $ fprintd-enroll

  2. Override the systemd service command:
     $ systemctl --user edit linux-id.service

  3. Add the following lines:
     [Service]
     ExecStart=
     ExecStart=/usr/bin/linux-id --auth fprintd

  4. Restart the service:
     $ systemctl --user restart linux-id.service

%prep
%autosetup -n %{name}-%{version}

%build
export CGO_ENABLED=0
go build -v -ldflags="-s -w" -o %{name} .

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_userunitdir}/%{name}.service
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_udevrulesdir}/60-%{name}-fido-tpm.rules
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_modulesloaddir}/uhid.conf

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service
%{_udevrulesdir}/60-%{name}-fido-tpm.rules
%{_modulesloaddir}/uhid.conf

%changelog
* Sun Sep 20 2026 Hamish West <hamish@hamishwest.xyz> - 0.2.4-2
- Fix DNF error
* Sun Sep 20 2026 Hamish West <hamish@hamishwest.xyz> - 0.2.4-1
- Bump deps
* Tue Aug 04 2026 Hamish West <hamish@hamishwest.xyz> - 0.2.3-1
- Initial RPM packaging for Fedora COPR
