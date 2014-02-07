# History

Michael Stahnke wrote [puppet-module-epel](https://github.com/stahnma/puppet-module-epel).
Lee Boynton followed up with [puppet-rpmforge](https://github.com/lboynton/puppet-rpmforge)
which has a dependancy on `puppet-module-epel` for a fact and rpm key
importing.

It seems like managing third party repos is a common task. If we're going to
have a cross module dependancy we might as well merge the modules.

# Why?

EPEL and RepoForge are two common third party RPM repositories. To parrot
Michael Stahnke,  "I just got sick of coding Puppet modules and basically
having an assumption that EPEL was setup or installed.  I can now depend on
this module instead."

There are also some packages which don't play nicely between the two
(nagios-plugins comes to mind) and when possible that has been captured here.

# Configure EPEL (Extra Repository for Enterprise Linux)

`include rpmrepos::epel`

## About
This module basically just mimics the epel-release rpm. The same
repos are enabled/disabled and the GPG key is imported.  In the end you will
end up with the EPEL repos configured.

The following Repos will be setup and enabled by default:

  * epel

Other repositories that will setup but disabled (as per the epel-release
setup)

  * epel-debuginfo
  * epel-source
  * epel-testing
  * epel-testing-debuginfo
  * epel-testing-source

You can enable them using class parameters (`testing => true`).

## Proxy
If you have an http proxy required to access the internet, you can
use the $proxy variable in the class parameters. If it is set to a value other
than 'absent' a proxy will be setup with each repository.  Note that otherwise
each of the repos will fall back to settings in the /etc/yum.conf file.

# Configure RepoForge

`include rpmrepos::rpmforge`

## About
This module basically just mimics the rpmforge-release rpm. The same
repos are enabled/disabled and the GPG key is imported.  In the end you will
end up with the RepoForge (aka RPMForge) repos configured.

The following Repos will be setup and enabled by default:

  * rpmforge

Other repositories that will setup but disabled (as per the rpmforge-release
setup)

  * rpmforge-extras
  * rpmforge-testing

You can enable them using class parameters (`testing => '1'`).

## Proxy
If you have an http proxy required to access the internet, you can
use the $proxy variable in the class parameters. If it is set to a value other
than 'absent' a proxy will be setup with each repository.  Note that otherwise
each of the repos will fall back to settings in the /etc/yum.conf file.

# Futher Information

* [EPEL Wiki](http://fedoraproject.org/wiki/EPEL)
* [epel-release package information](http://mirrors.servercentral.net/fedora/epel/6/i386/repoview/epel-release.html)
* [RepoForge](http://repoforge.org/use/)

# Testing

* This was tested using Puppet 2.7.x on Centos5/6 I assume it will work on any
* RHEL variant Also, I think this should work with earlier versions of Puppet
* (2.6.x at least)

# License Apache Software License 2.0
