# Class rpmforge
#
# Actions:
#   Configure the proper repositories and import GPG keys
#
# Reqiures:
#   You should probably be on an Enterprise Linux variant. (Centos, RHEL, Scientific, Oracle, Ascendos, et al)
#
# Sample Usage:
#  include rpmrepos::rpmforge
#
class rpmrepos::rpmforge ($testing = '0',
                          $extras  = '0',
                          $proxy   = 'absent') {
    yumrepo { 'rpmforge':
        baseurl     => "http://apt.sw.be/redhat/el${::os_maj_version}/en/${::architecture}/rpmforge/",
        mirrorlist  =>  "http://apt.sw.be/redhat/el${::os_maj_version}/en/mirrors-rpmforge",
        proxy       => $rpmrepos::rpmforge::proxy,
        enabled     => 1,
        gpgcheck    => 1,
        exclude    => ['nagios-plugins-*'],
        gpgkey      => 'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-dag',
        descr       => "Rpmforge - ${::os_maj_version} - ${::architecture} "
    }
    
    yumrepo { 'rpmforge-extras':
        baseurl     => "http://apt.sw.be/redhat/el${::os_maj_version}/en/${::architecture}/extras/",
        mirrorlist  =>  "http://apt.sw.be/redhat/el${::os_maj_version}/en/mirrors-rpmforge-extras",
        proxy       => $rpmrepos::rpmforge::proxy,
        enabled     => $rpmrepos::rpmforge::extras,
        gpgcheck    => 1,
        gpgkey      => 'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-dag',
        descr       => "Rpmforge - ${::os_maj_version} - Extras - ${::architecture}"
    }
    
    yumrepo { 'rpmforge-testing':
        baseurl     => "http://apt.sw.be/redhat/el${::os_maj_version}/en/${::architecture}/testing/",
        mirrorlist  =>  "http://apt.sw.be/redhat/el${::os_maj_version}/en/mirrors-rpmforge-testing",
        proxy       => $rpmrepos::rpmforge::proxy,
        enabled     => $rpmrepos::rpmforge::testing,
        gpgcheck    => 1,
        gpgkey      => 'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-dag',
        descr       => "Rpmforge - ${::os_maj_version} - Testing - ${::architecture}"
    }

    file { "/etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-dag":
        ensure => present,
        owner  => 'root',
        group  => 'root',
        mode   => '0644',
        source => "puppet:///modules/rpmrepos/RPM-GPG-KEY-rpmforge-dag",
    }
    
    rpmrepos::rpm_gpg_key{ "rpmforge-dag":
        path => "/etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-dag",
    }
}
