# Class epel
#
# Actions:
#   Configure the proper repositories and import GPG keys
#
# Reqiures:
#   You should probably be on an Enterprise Linux variant. (Centos, RHEL, Scientific, Oracle, Ascendos, et al)
#
# Sample Usage:
#  include rpmrepos::epel
#
class rpmrepos::epel ($testing           = '0',
                      $testing_debuginfo = '0',
                      $testing_source    = '0',
                      $debuginfo         = '0',
                      $source            = '0',
                      $proxy             = 'absent') {

  if $::osfamily == 'RedHat' and $::operatingsystem != 'Fedora' {

    yumrepo { 'epel-testing':
      baseurl        => "http://download.fedora.redhat.com/pub/epel/testing/${::os_maj_version}/${::architecture}",
      failovermethod => 'priority',
      proxy          => $rpmrepos::epel::proxy,
      enabled        => $rpmrepos::epel::testing,
      gpgcheck       => '1',
      gpgkey         => "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-${::os_maj_version}",
      descr          => "Extra Packages for Enterprise Linux ${::os_maj_version} - Testing - ${::architecture} "
    }

    yumrepo { 'epel-testing-debuginfo':
      baseurl        => "http://download.fedora.redhat.com/pub/epel/testing/${::os_maj_version}/${::architecture}/debug",
      failovermethod => 'priority',
      proxy          => $rpmrepos::epel::proxy,
      enabled        => $rpmrepos::epel::testing_debuginfo,
      gpgcheck       => '1',
      gpgkey         => "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-${::os_maj_version}",
      descr          => "Extra Packages for Enterprise Linux ${::os_maj_version} - Testing - ${::architecture} - Debug"
    }

    yumrepo { 'epel-testing-source':
      baseurl        => "http://download.fedora.redhat.com/pub/epel/testing/${::os_maj_version}/SRPMS",
      failovermethod => 'priority',
      proxy          => $rpmrepos::epel::proxy,
      enabled        => $rpmrepos::epel::testing_source,
      gpgcheck       => '1',
      gpgkey         => "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-${::os_maj_version}",
      descr          => "Extra Packages for Enterprise Linux ${::os_maj_version} - Testing - ${::architecture} - Source"
    }

    yumrepo { 'epel':
      mirrorlist     => "http://mirrors.fedoraproject.org/mirrorlist?repo=epel-${::os_maj_version}&arch=${::architecture}",
      failovermethod => 'priority',
      proxy          => $rpmrepos::epel::proxy,
      enabled        => '1',
      gpgcheck       => '1',
      gpgkey         => "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-${::os_maj_version}",
      descr          => "Extra Packages for Enterprise Linux ${::os_maj_version} - ${::architecture}"
    }

    yumrepo { 'epel-debuginfo':
      mirrorlist     => "http://mirrors.fedoraproject.org/mirrorlist?repo=epel-debug-${::os_maj_version}&arch=${::architecture}",
      failovermethod => 'priority',
      proxy          => $rpmrepos::epel::proxy,
      enabled        => $rpmrepos::epel::debuginfo,
      gpgcheck       => '1',
      gpgkey         => "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-${::os_maj_version}",
      descr          => "Extra Packages for Enterprise Linux ${::os_maj_version} - ${::architecture} - Debug"
    }

    yumrepo { 'epel-source':
      mirrorlist     => "http://mirrors.fedoraproject.org/mirrorlist?repo=epel-source-${::os_maj_version}&arch=${::architecture}",
      proxy          => $rpmrepos::epel::proxy,
      failovermethod => 'priority',
      enabled        => $rpmrepos::epel::source,
      gpgcheck       => '1',
      gpgkey         => "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-${::os_maj_version}",
      descr          => "Extra Packages for Enterprise Linux ${::os_maj_version} - ${::architecture} - Source"
    }

    file { "/etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-${::os_maj_version}":
      ensure => present,
      owner  => 'root',
      group  => 'root',
      mode   => '0644',
      source => "puppet:///modules/rpmrepos/RPM-GPG-KEY-EPEL-${::os_maj_version}",
    }

    rpmrepos::rpm_gpg_key{ "EPEL-${::os_maj_version}":
      path => "/etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-${::os_maj_version}"
    }
  } else {
      notice ("Your operating system ${::operatingsystem} will not have the EPEL repository applied")
  }

}
