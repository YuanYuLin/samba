import ops
import iopc

TARBALL_FILE="samba-4.8.4.tar.gz"
TARBALL_DIR="samba-4.8.4"
INSTALL_DIR="samba-bin"
pkg_path = ""
output_dir = ""
tarball_pkg = ""
tarball_dir = ""
install_dir = ""
install_tmp_dir = ""
cc_host = ""
tmp_include_dir = ""
dst_include_dir = ""
dst_lib_dir = ""
dst_usr_local_lib_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global tarball_pkg
    global install_dir
    global install_tmp_dir
    global tarball_dir
    global cc_host
    global tmp_include_dir
    global dst_include_dir
    global dst_lib_dir
    global dst_usr_local_lib_dir
    global dst_usr_local_libexec_dir
    global dst_usr_local_share_dir
    global dst_usr_local_dir
    global src_pkgconfig_dir
    global dst_pkgconfig_dir
    global dst_bin_dir
    global dst_etc_dir
    global install_test_utils
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    tarball_pkg = ops.path_join(pkg_path, TARBALL_FILE)
    install_dir = ops.path_join(output_dir, INSTALL_DIR)
    install_tmp_dir = ops.path_join(output_dir, INSTALL_DIR + "-tmp")
    tarball_dir = ops.path_join(output_dir, TARBALL_DIR)
    cc_host_str = ops.getEnv("CROSS_COMPILE")
    cc_host = cc_host_str[:len(cc_host_str) - 1]
    tmp_include_dir = ops.path_join(output_dir, ops.path_join("include",args["pkg_name"]))
    dst_include_dir = ops.path_join("include",args["pkg_name"])
    dst_lib_dir = ops.path_join(install_dir, "lib")
    dst_bin_dir = ops.path_join(install_dir, "bin")
    dst_etc_dir = ops.path_join(install_dir, "etc")
    dst_usr_local_lib_dir = ops.path_join(install_dir, "usr/local/lib")
    dst_usr_local_dir = ops.path_join(install_dir, "usr/local")
    dst_usr_local_libexec_dir = ops.path_join(install_dir, "usr/local/libexec")
    dst_usr_local_share_dir = ops.path_join(install_dir, "usr/local/share")
    src_pkgconfig_dir = ops.path_join(pkg_path, "pkgconfig")
    dst_pkgconfig_dir = ops.path_join(install_dir, "pkgconfig")
    if ops.getEnv("INSTALL_TEST_UTILS") == 'y':
        install_test_utils = True
    else:
        install_test_utils = False


def MAIN_ENV(args):
    set_global(args)

    ops.exportEnv(ops.setEnv("CC", ops.getEnv("CROSS_COMPILE") + "gcc"))
    '''
    ops.exportEnv(ops.setEnv("CXX", ops.getEnv("CROSS_COMPILE") + "g++"))
    ops.exportEnv(ops.setEnv("CPP", ops.getEnv("CROSS_COMPILE") + "g++"))
    ops.exportEnv(ops.setEnv("AR", ops.getEnv("CROSS_COMPILE") + "ar"))
    ops.exportEnv(ops.setEnv("RANLIB", ops.getEnv("CROSS_COMPILE") + "ranlib"))
    ops.exportEnv(ops.setEnv("CROSS", ops.getEnv("CROSS_COMPILE")))
    '''
    ops.exportEnv(ops.setEnv("DESTDIR", install_tmp_dir))

    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.unTarGz(tarball_pkg, output_dir)

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(tarball_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    job_count = ops.getEnv("BUILD_JOBS_COUNT")

    extra_conf = []
    '''
    #extra_conf.append("--cross-compile")
    #extra_conf.append("-C -V")
    #extra_conf.append("--cross-answers=cc.txt")
    #extra_conf.append("--hostcc=" + cc_host)
    extra_conf.append("--abi-check-disable")
    extra_conf.append("--disable-rpath")
    extra_conf.append("--bundled-libraries=NONE")
    #extra_conf.append("--cross-execute='qemu-arm-static -L /usr/arm-linux-gnu'")
    extra_conf.append("--jobs=" + job_count)
    extra_conf.append("--disable-gnutls")
    #extra_conf.append("--private-libraries=NONE")

    extra_conf.append("--without-gettext")
    extra_conf.append("--without-systemd")
    extra_conf.append("--without-ad-dc")
    extra_conf.append("--without-ads")
    extra_conf.append("--without-winbind")
    extra_conf.append("--without-ldap")
    extra_conf.append("--without-pam")
    extra_conf.append("--without-pie")
    extra_conf.append("--without-fam")
    extra_conf.append("--without-dmapi")
    extra_conf.append("--without-automount")
    extra_conf.append("--without-utmp")
    extra_conf.append("--without-dnsupdate")
    extra_conf.append("--without-acl-support")
    extra_conf.append("--without-quotas")
    extra_conf.append("--without-cluster-support")
    extra_conf.append("--disable-glusterfs")
    extra_conf.append("--without-profiling-data")
    extra_conf.append("--without-libarchive")
    extra_conf.append("--without-regedit")
    extra_conf.append("--without-ntvfs-fileserver")
    extra_conf.append("--disable-python")
    extra_conf.append("--disable-cups")
    extra_conf.append("--disable-iprint")
    extra_conf.append("--disable-avahi")
    '''
    extra_conf.append("--disable-python") 
    extra_conf.append("--without-ad-dc")
    extra_conf.append("--without-acl-support")
    extra_conf.append("--without-ldap") 
    extra_conf.append("--without-ads") 
    extra_conf.append("--without-pam")
    extra_conf.append("--without-gettext")

    extra_conf.append("--jobs=" + job_count)
    extra_conf.append("--without-systemd")
    extra_conf.append("--without-regedit")
    extra_conf.append("--without-cluster-support")
    extra_conf.append("--without-ntvfs-fileserver")
    extra_conf.append("--without-winbind")
    extra_conf.append("--disable-glusterfs")
    extra_conf.append("--disable-cups")
    extra_conf.append("--disable-iprint")
    extra_conf.append("--disable-avahi")
    extra_conf.append("--without-automount")
    extra_conf.append("--without-dnsupdate")
    extra_conf.append("--without-fam")
    extra_conf.append("--without-dmapi")
    extra_conf.append("--without-quotas")
    extra_conf.append("--without-profiling-data")
    extra_conf.append("--without-utmp")
    extra_conf.append("--without-libarchive")
    #extra_conf.append("--enable-developer")

    print extra_conf
    #iopc.waf(tarball_dir, extra_conf)
    iopc.configure(tarball_dir, extra_conf)

    return True

def MAIN_BUILD(args):
    set_global(args)

    ops.mkdir(install_dir)
    ops.mkdir(install_tmp_dir)
    iopc.make(tarball_dir)
    iopc.make_install(tarball_dir)

    ops.mkdir(install_dir)
    ops.mkdir(dst_lib_dir)
    ops.mkdir(dst_bin_dir)
    ops.mkdir(dst_usr_local_dir)

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/sbin/nmbd"), dst_bin_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/sbin/smbd"), dst_bin_dir)

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libdcerpc-binding.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libdcerpc-binding.so.0.0.1", "libdcerpc-binding.so.0.0")
    ops.ln(dst_lib_dir, "libdcerpc-binding.so.0.0.1", "libdcerpc-binding.so.0")
    ops.ln(dst_lib_dir, "libdcerpc-binding.so.0.0.1", "libdcerpc-binding.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libdcerpc-samr.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libdcerpc-samr.so.0.0.1", "libdcerpc-samr.so.0.0")
    ops.ln(dst_lib_dir, "libdcerpc-samr.so.0.0.1", "libdcerpc-samr.so.0")
    ops.ln(dst_lib_dir, "libdcerpc-samr.so.0.0.1", "libdcerpc-samr.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libdcerpc.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libdcerpc.so.0.0.1", "libdcerpc.so.0.0")
    ops.ln(dst_lib_dir, "libdcerpc.so.0.0.1", "libdcerpc.so.0")
    ops.ln(dst_lib_dir, "libdcerpc.so.0.0.1", "libdcerpc.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libndr-krb5pac.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libndr-krb5pac.so.0.0.1", "libndr-krb5pac.so.0.0")
    ops.ln(dst_lib_dir, "libndr-krb5pac.so.0.0.1", "libndr-krb5pac.so.0")
    ops.ln(dst_lib_dir, "libndr-krb5pac.so.0.0.1", "libndr-krb5pac.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libndr-nbt.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libndr-nbt.so.0.0.1", "libndr-nbt.so.0.0")
    ops.ln(dst_lib_dir, "libndr-nbt.so.0.0.1", "libndr-nbt.so.0")
    ops.ln(dst_lib_dir, "libndr-nbt.so.0.0.1", "libndr-nbt.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libndr.so.0.1.0"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libndr.so.0.1.0", "libndr.so.0.1")
    ops.ln(dst_lib_dir, "libndr.so.0.1.0", "libndr.so.0")
    ops.ln(dst_lib_dir, "libndr.so.0.1.0", "libndr.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libndr-standard.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libndr-standard.so.0.0.1", "libndr-standard.so.0.0")
    ops.ln(dst_lib_dir, "libndr-standard.so.0.0.1", "libndr-standard.so.0")
    ops.ln(dst_lib_dir, "libndr-standard.so.0.0.1", "libndr-standard.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libnetapi.so.0"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libnetapi.so.0", "libnetapi.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libnss_winbind.so.2"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libnss_winbind.so.2", "libnss_winbind.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libnss_wins.so.2"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libnss_wins.so.2", "libnss_wins.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libsamba-credentials.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libsamba-credentials.so.0.0.1", "libsamba-credentials.so.0.0")
    ops.ln(dst_lib_dir, "libsamba-credentials.so.0.0.1", "libsamba-credentials.so.0")
    ops.ln(dst_lib_dir, "libsamba-credentials.so.0.0.1", "libsamba-credentials.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libsamba-errors.so.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libsamba-errors.so.1", "libsamba-errors.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libsamba-hostconfig.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libsamba-hostconfig.so.0.0.1", "libsamba-hostconfig.so.0.0")
    ops.ln(dst_lib_dir, "libsamba-hostconfig.so.0.0.1", "libsamba-hostconfig.so.0")
    ops.ln(dst_lib_dir, "libsamba-hostconfig.so.0.0.1", "libsamba-hostconfig.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libsamba-passdb.so.0.27.0"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libsamba-passdb.so.0.27.0", "libsamba-passdb.so.0.27")
    ops.ln(dst_lib_dir, "libsamba-passdb.so.0.27.0", "libsamba-passdb.so.0")
    ops.ln(dst_lib_dir, "libsamba-passdb.so.0.27.0", "libsamba-passdb.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libsamba-util.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libsamba-util.so.0.0.1", "libsamba-util.so.0.0")
    ops.ln(dst_lib_dir, "libsamba-util.so.0.0.1", "libsamba-util.so.0")
    ops.ln(dst_lib_dir, "libsamba-util.so.0.0.1", "libsamba-util.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libsamdb.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libsamdb.so.0.0.1", "libsamdb.so.0.0")
    ops.ln(dst_lib_dir, "libsamdb.so.0.0.1", "libsamdb.so.0")
    ops.ln(dst_lib_dir, "libsamdb.so.0.0.1", "libsamdb.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libsmbclient.so.0.3.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libsmbclient.so.0.3.1", "libsmbclient.so.0.3")
    ops.ln(dst_lib_dir, "libsmbclient.so.0.3.1", "libsmbclient.so.0")
    ops.ln(dst_lib_dir, "libsmbclient.so.0.3.1", "libsmbclient.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libsmbconf.so.0"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libsmbconf.so.0", "libsmbconf.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libtevent-util.so.0.0.1"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libtevent-util.so.0.0.1", "libtevent-util.so.0.0")
    ops.ln(dst_lib_dir, "libtevent-util.so.0.0.1", "libtevent-util.so.0")
    ops.ln(dst_lib_dir, "libtevent-util.so.0.0.1", "libtevent-util.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/libwbclient.so.0.14"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libwbclient.so.0.14", "libwbclient.so.0")
    ops.ln(dst_lib_dir, "libwbclient.so.0.14", "libwbclient.so")

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/winbind_krb5_locator.so"), dst_lib_dir)

    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/private/."), dst_lib_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/auth"), dst_lib_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/idmap"), dst_lib_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/ldb"), dst_lib_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/nss_info"), dst_lib_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/samba/lib/vfs"), dst_lib_dir)

    ops.ln(dst_usr_local_dir, "/tmp/samba", "samba")

    return True

def MAIN_INSTALL(args):
    set_global(args)

    iopc.installBin(args["pkg_name"], ops.path_join(dst_lib_dir, "."), "lib")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_bin_dir, "."), "usr/sbin")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_local_dir, "."), "usr/local")
    #iopc.installBin(args["pkg_name"], ops.path_join(tmp_include_dir, "."), dst_include_dir)
    #iopc.installBin(args["pkg_name"], ops.path_join(dst_pkgconfig_dir, '.'), "pkgconfig")

    return False

def MAIN_SDKENV(args):
    set_global(args)

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)

