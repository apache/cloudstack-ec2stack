# Class rpmrepos
#
# Actions:
#   Configure the proper repositories and import GPG keys
#
# Requires:
#   You should probably be on an Enterprise Linux variant. (Centos, RHEL, 
#    Scientific, Oracle, Ascendos, et al)
#
# Sample Usage:
#  include rpmrepos
#
# Basic usage doesn't allow for specific repository selection or proxies.
# If you need them use the classes directly.
class rpmrepos {

    require rpmrepos::epel
    require rpmrepos::rpmforge

}
