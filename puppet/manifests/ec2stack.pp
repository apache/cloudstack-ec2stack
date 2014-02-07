group {
    "puppet": ensure => "present"
}

Exec {
    path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/",
    "/usr/local/bin"]
}

stage { 'pre':
    before => Stage['main']
}

class { 'baseconfig':
    stage => 'pre'
}

class baseconfig {
    exec { "Update the system":
        command => "/usr/bin/yum -y update"
    }

    $packages = [ "zlib-devel", "bzip2-devel", "openssl-devel", "ncurses-devel", "mysql-devel", "libxml2-devel", "libxslt-devel", "unixODBC-devel", "sqlite", "sqlite-devel", "wget", "git" ]

    package {
        $packages: ensure => "installed"
    }

    exec { "Install Development Tools":
      unless  => "yum grouplist 'Development tools' | /bin/grep '^Installed Groups'",
      command => "yum -y groupinstall 'Development tools'",
    }
}

class ec2stack {
    exec { "Install Python 2.7":
        command => "rm -rf Python-2.7.4* && wget --no-check-certificate http://www.python.org/ftp/python/2.7.4/Python-2.7.4.tar.bz2 && tar xf Python-2.7.4.tar.bz2 && cd Python-2.7.4 && ./configure --prefix=/usr/local && make && make altinstall",
        cwd => "/tmp",
        unless => "which python2.7",
        timeout => 60 * 20,
        tries => 5,
        try_sleep => 30
    }

    exec { "Install distribute 0.6.10 for Python 2.6":
        command => "rm -rf distribute-* && wget --no-check-certificate http://pypi.python.org/packages/source/d/distribute/distribute-0.6.10.tar.gz && tar -xvzf distribute-0.6.10.tar.gz && cd distribute-0.6.10 && python2.6 setup.py install",
        cwd => "/tmp",
        unless => "which easy_install-2.6",
        timeout => 60 * 10,
        tries => 5,
        try_sleep => 30
    }

    exec { "Install distribute 0.6.10 for Python 2.7":
        command => "rm -rf distribute-* && wget --no-check-certificate http://pypi.python.org/packages/source/d/distribute/distribute-0.6.10.tar.gz && tar -xvzf distribute-0.6.10.tar.gz && cd distribute-0.6.10 && python2.7 setup.py install",
        cwd => "/tmp",
        require => [ Exec["Install Python 2.7"] ],
        unless => "which easy_install-2.7",
        timeout => 60 * 10,
        tries => 5,
        try_sleep => 30
    }

    exec { "Install virtualenv 1.9.1 for Python 2.6":
        command => "rm -rf virtualenv-* && wget --no-check-certificate https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.1.tar.gz#md5=07e09df0adfca0b2d487e39a4bf2270a && tar -xvzf virtualenv-1.9.1.tar.gz && cd virtualenv-1.9.1 && python2.6 setup.py install",
        cwd => "/tmp",
        require => [ Exec["Install distribute 0.6.10 for Python 2.6"] ],
        unless => "which virtualenv-2.6",
        timeout => 60 * 10,
        tries => 5,
        try_sleep => 30
    }

    exec { "Install virtualenvwrapper 4.0 for Python 2.6":
        command => "rm -rf virtualenvwrapper-* && wget --no-check-certificate https://pypi.python.org/packages/source/v/virtualenvwrapper/virtualenvwrapper-4.0.tar.gz#md5=78df3b40735e959479d9de34e4b8ba15 && tar -xvzf virtualenvwrapper-4.0.tar.gz && cd virtualenvwrapper-4.0 && python2.6 setup.py install",
        cwd => "/tmp",
        require => [ Exec["Install virtualenv 1.9.1 for Python 2.6"] ],
        unless => "which virtualenvwrapper.sh",
        timeout => 60 * 10,
        tries => 5,
        try_sleep => 30
    }

    exec { "Install pep8 for Python 2.6":
        command => "easy_install pep8",
        cwd => "/tmp",
        require => [ Exec["Install distribute 0.6.10 for Python 2.6"] ],
        unless => "which pep8",
        timeout => 60 * 10,
        tries => 5,
        try_sleep => 30
    }

    exec { "Install pylint for Python 2.6":
        command => "easy_install pylint",
        require => [ Exec["Install distribute 0.6.10 for Python 2.6"] ],
        unless => "which pylint",
        timeout => 60 * 10,
        tries => 5,
        try_sleep => 30
    }

    exec { "Install awscli for Python2.6":
    ####command => "easy_install awscli",
    ####require => [ Exec["Install distribute 0.6.10 for Python 2.6"] ],
    ####unless => "which aws",
    ####timeout => 60 * 10,
    ####tries => 5,
    ####try_sleep => 30
    }

    file {
        "/etc/profile.d/virtualenv.sh":
            ensure => present,
            source => "file:///vagrant/puppet/files/virtualenv.sh"
        ;
        "/etc/profile.d/alias.sh":
            ensure => present,
            source => "file:///vagrant/puppet/files/alias.sh"
        ;
    }
}

include baseconfig
include ec2stack
include rpmrepos::epel
include rpmrepos::rpmforge
