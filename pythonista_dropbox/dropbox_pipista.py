"""
This code was cloned from https://gist.github.com/pudquick/4116558
and then modified. Instead of downloading files from the
Cheese Shop, it downloads files from Dropbox.
pypi_download accepts a dictionary with keys 'url', 'filename'
where 'url' is the complete path to an installable file and 'filename'
is the name only, e.g.:
    source_dict = {
        'url': '/PyPi-tarballs/hello_world-0.1.0.tar.gz', 
        'filename': 'hello_world-0.1.0.tar.gz',
    }

"""
import os, os.path, sys, urllib2, requests, tempfile, zipfile, shutil, gzip, tarfile
from pythonista_dropbox.client import get_client
from pythonista_dropbox.adapters import Platform

platform = Platform()


__pypi_base__ = os.path.abspath(os.path.dirname(__file__))

class PyPiError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def _chunk_report(bytes_so_far, chunk_size, total_size):
    if (total_size != None):
        percent = float(bytes_so_far) / total_size
        percent = round(percent*100, 2)
        print 'Downloaded %d of %d bytes (%0.2f%%)' % (bytes_so_far, total_size, percent)
        if bytes_so_far >= total_size:
            print ''
    else:
        print 'Downloaded %d bytes' % (bytes_so_far)

def _chunk_read(response, chunk_size=32768, report_hook=None, filename=None):
    file_data = []
    if response.info().has_key('Content-Length'):
        total_size = response.info().getheader('Content-Length').strip()
        total_size = int(total_size)
    else:
        # No size
        total_size = None
        if report_hook:
            print '* Warning: No total file size available.'
    if (filename == None) and (response.info().has_key('Content-Disposition')):
        # If the response has Content-Disposition, we take file name from it
        try:
            filename = response.info()['Content-Disposition'].split('filename=')[1]
            if filename[0] == '"' or filename[0] == "'":
                filename = filename[1:-1]
        except Exception:
            sys.exc_clear()
            filename = 'output'
    if (filename == None):
        if report_hook:
            print "* No detected filename, using 'output'"
        filename = 'output'
    bytes_so_far = 0
    while True:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)
        if not chunk:
            break
        else:
            file_data.append(chunk)
        report_hook(bytes_so_far, chunk_size, total_size)
    return (file_data, filename)

def _download(src_dict, print_progress=True):
    if print_progress:
        print '* Downloading:', src_dict['url']
    client = get_client()
    data = client.get_file(src_dict['url'])
    filename = src_dict['filename']
    if data:
        if os.path.exists(filename):
            os.remove(filename)
        try:
            with open(filename, 'wb') as f:
                f.write(data.read()) 
            if print_progress:
                print '* Saved to:', filename
            return os.path.abspath(filename)
        except Exception:
            if print_progress:
                print '! Error:', sys.exc_info()[1]
            raise
    else:
        if print_progress:
            print '* Error: 0 bytes downloaded, not saved'

def pypi_download(src_dict, print_progress=True):
    return _download(src_dict, print_progress)

def pypi_versions(pkg_name, limit=10, show_hidden=True):
    if not pkg_name:
        return []
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    hits = pypi.package_releases(pkg_name, show_hidden)
    if not hits:
        return []
    if len(hits) > limit:
        hits = hits[:limit]
    return hits

def pypi_search(search_str, limit=5):
    if not search_str:
        return []
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    hits = pypi.search({'name': search_str}, 'and')
    if not hits:
        return []
    hits = sorted(hits, key=lambda pkg: pkg['_pypi_ordering'], reverse=True)
    if len(hits) > limit:
        hits = hits[:limit]
    return hits

def _install_ConfigParser(path='.'):
    # Grab the 2.7.3 version of ConfigParser - even though Pythonista 1.2 is 2.7.0
    r = requests.get('http://hg.python.org/cpython/raw-file/70274d53c1dd/Lib/ConfigParser.py')
    lib_file = os.path.join(path, 'ConfigParser.py')
    with open(lib_file, 'w') as f:
        f.write(r.text)

def _install_xmlrpclib(path='.'):
    # Grab the 2.7.3 version of xmlrpclib - even though Pythonista 1.2 is 2.7.0
    r = requests.get('http://hg.python.org/cpython/raw-file/70274d53c1dd/Lib/xmlrpclib.py')
    lib_file = os.path.join(path, 'xmlrpclib.py')
    with open(lib_file, 'w') as f:
        f.write(r.text)

def _unzip(a_zip=None, path='.'):
    if a_zip is None:
        return
    filename = os.path.abspath(a_zip)
    if not os.path.isfile(filename):
        return
    # PK magic marker check
    f = open(filename)
    try:
        pk_check = f.read(2)
    except Exception:
        pk_check = ''
    finally:
        f.close()
    if pk_check != 'PK':
        print "unzip: %s: does not appear to be a zip file" % a_zip
    else:
        if (os.path.basename(filename).lower().endswith('.zip')):
            altpath = os.path.splitext(os.path.basename(filename))[0]
        else:
            altpath = os.path.basename(filename) + '_unzipped'
        altpath = os.path.join(os.path.dirname(filename), altpath)
        location = os.path.abspath(path)
        if not os.path.exists(location):
            os.makedirs(location)
        zipfp = open(filename, 'rb')
        try:
            zipf = zipfile.ZipFile(zipfp)
            # check for a leading directory common to all files and remove it
            dirnames = [os.path.join(os.path.dirname(x), '') for x in zipf.namelist()]
            common_dir = os.path.commonprefix(dirnames or ['/'])
            # Check to make sure there aren't 2 or more sub directories with the same prefix
            if not common_dir.endswith('/'):
                common_dir = os.path.join(os.path.dirname(common_dir), '')
            for name in zipf.namelist():
                data = zipf.read(name)
                fn = name
                if common_dir:
                    if fn.startswith(common_dir):
                        fn = fn.split(common_dir, 1)[-1]
                    elif fn.startswith('/' + common_dir):
                        fn = fn.split('/' + common_dir, 1)[-1]
                fn = fn.lstrip('/')
                fn = os.path.join(location, fn)
                dirf = os.path.dirname(fn)
                if not os.path.exists(dirf):
                    os.makedirs(dirf)
                if fn.endswith('/'):
                    # A directory
                    if not os.path.exists(fn):
                        os.makedirs(fn)
                else:
                    fp = open(fn, 'wb')
                    try:
                        fp.write(data)
                    finally:
                        fp.close()
        except Exception:
            zipfp.close()
            print "unzip: %s: zip file is corrupt" % a_zip
            return
        zipfp.close()
        return os.path.abspath(location)

def _ungzip(a_gz=None, path='.'):
    fname = 'ungzip'
    if a_gz is None:
        return
    filename = os.path.abspath(a_gz)
    if not os.path.isfile(filename):
        return
    else:
        # '\x1f\x8b\x08' magic marker check
        f = open(filename, 'rb')
        try:
            gz_check = f.read(3)
        except Exception:
            gz_check = ''
        finally:
            f.close()
        if gz_check != '\x1f\x8b\x08':
            print "%s: %s: does not appear to be a gzip file" % (fname,a_gz)
            return
        else:
            if (os.path.basename(filename).lower().endswith('.gz') or os.path.basename(filename).lower().endswith('.gzip')):
                altpath = os.path.splitext(os.path.basename(filename))[0]
            elif os.path.basename(filename).lower().endswith('.tgz'):
                altpath = os.path.splitext(os.path.basename(filename))[0] + '.tar'
            else:
                altpath = os.path.basename(filename) + '_ungzipped'
            location = os.path.join(os.path.abspath(path), altpath)
            if os.path.exists(location):
                # Older file exists somehow, get rid of it
                os.remove(location)
            dirf = os.path.dirname(os.path.dirname(os.path.abspath(location)))
            try:
                if not os.path.exists(dirf):
                    os.makedirs(dirf)
                with open(location, 'wb') as outfile:
                    with gzip.open(filename, 'rb') as gzfile:
                        outfile.write(gzfile.read())
            except Exception:
                print "%s: %s: gzip file is corrupt" % (fname, a_gz)
                return
    return os.path.abspath(location)

def _untar(a_tar=None, path='.'):
    if a_tar is None:
        return
    filename = os.path.abspath(a_tar)
    if not os.path.isfile(filename):
        return
    # 'ustar' magic marker check
    f = open(filename)
    try:
        f.seek(257)
        ustar_check = f.read(5)
    except Exception:
        ustar_check = ''
    finally:
        f.close()
    if ustar_check != 'ustar':
        print "untar: %s: does not appear to be a tar file" % a_tar
        return
    else:
        if (os.path.basename(filename).lower().endswith('.tar')):
            altpath = os.path.splitext(os.path.basename(filename))[0]
        else:
            altpath = os.path.basename(filename) + '_untarred'
        altpath = os.path.join(os.path.dirname(filename), altpath)
        location = os.path.abspath(path)
        if not os.path.exists(location):
            os.makedirs(location)
        try:
            tar = tarfile.open(filename, 'r')
            # check for a leading directory common to all files and remove it
            dirnames = [os.path.join(os.path.dirname(x.name), '') for x in tar.getmembers() if x.name != 'pax_global_header']
            common_dir = os.path.commonprefix(dirnames or ['/'])
            if not common_dir.endswith('/'):
                common_dir = os.path.join(os.path.dirname(common_dir), '')
            for member in tar.getmembers():
                fn = member.name
                if fn == 'pax_global_header':
                    continue
                if common_dir:
                    if fn.startswith(common_dir):
                        fn = fn.split(common_dir, 1)[-1]
                    elif fn.startswith('/' + common_dir):
                        fn = fn.split('/' + common_dir, 1)[-1]
                fn = fn.lstrip('/')
                fn = os.path.join(location, fn)
                dirf = os.path.dirname(fn)
                if member.isdir():
                    # A directory
                    if not os.path.exists(fn):
                        os.makedirs(fn)
                elif member.issym():
                    # skip symlinks
                    continue
                else:
                    try:
                        fp = tar.extractfile(member)
                    except (KeyError, AttributeError):
                        # invalid member, not necessarily a bad tar file
                        continue
                    if not os.path.exists(dirf):
                        os.makedirs(dirf)
                    with open(fn, 'wb') as destfp:
                        shutil.copyfileobj(fp, destfp)
                    fp.close()
        except Exception:
            tar.close()
            print "untar: %s: tar file is corrupt" % a_tar
            return
        tar.close()
        return os.path.abspath(location)

def _install_setuptools(path='.'):
    # Can't use requests - need https access and it's not availabe in Pythonista 1.2
    r = urllib2.urlopen('https://raw.github.com/pudquick/pipista/master/st-lite.zip')
    temp_zip = tempfile.TemporaryFile()
    temp_zip.write(r.read())
    r.close()
    temp_zip.seek(0)
    unzipped = zipfile.ZipFile(temp_zip)
    for name in unzipped.namelist():
        data = unzipped.read(name)
        fn = os.path.abspath(os.path.join(path, name))
        dirn = os.path.dirname(fn)
        if not os.path.exists(dirn):
            os.makedirs(dirn)
        if fn.endswith('/') or fn.endswith('\\'):
            if not os.path.exists(fn):
                os.makedirs(fn)
        else:
            fp = open(fn, 'wb')
            try:
                fp.write(data)
            finally:
                fp.close()
    temp_zip.close()

def _rm(path=None):
        if path is None:
            return
        full_file = os.path.abspath(path).rstrip('/')
        if not os.path.exists(path):
            return
        if (os.path.isdir(full_file)):
            try:
                shutil.rmtree(full_file, True)
                if (os.path.exists(full_file)):
                    return
            except Exception:
                sys.exc_clear()
                return
        else:
            try:
                os.remove(full_file)
            except Exception:
                sys.exc_clear()
                return

if platform.pythonista:
    import pipista
    pipista._prep_pipista()

def _reset_and_enter_tmp(alt_dir=None):
    lib_dir  = os.path.join(__pypi_base__, 'pypi-modules')
    tmp_dir  = os.path.join(lib_dir, '.tmp')
    # Nuke the existing .tmp folder
    _rm(tmp_dir)
    # Prep .tmp folders: archive, unpack
    os.makedirs(tmp_dir)
    os.makedirs(os.path.join(tmp_dir, 'archive'))
    os.makedirs(os.path.join(tmp_dir, 'unpack'))
    if alt_dir is None:
        os.chdir(tmp_dir)
    else:
        # Cleaning up after ourselves, time to return
        os.chdir(alt_dir)

def _py_build(path=None):
    if path is None:
        return
    import distutils.core
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = tempfile.TemporaryFile()
    sys.stderr = tempfile.TemporaryFile()
    os.chdir(path)
    try:
        result = distutils.core.run_setup('setup.py', ['build_py', '--force'])
    except Exception:
        result = None
    finally:
        sys.stderr = old_stderr
        sys.stdout = old_stdout
    return result

def pypi_install(src_dict, print_progress=True):
    ## EXPERIMENTAL - not guaranteed to work! ##
    # Remeber where we were
    cwd = os.getcwd()
    # Reset build environment and enter it
    _reset_and_enter_tmp()
    # Download the specified package to the archive directory
    os.chdir('archive')
    fn = pypi_download(src_dict, print_progress)
    if not fn:
        _reset_and_enter_tmp(cwd)
        return False
    # Successfully downloaded, move back to .tmp
    os.chdir('..')
    res = None
    if fn.lower().endswith('.zip'):
        res = _unzip(os.path.abspath(fn), 'unpack')
    elif (fn.lower().endswith('.tar.gz') or fn.lower().endswith('.tgz')):
        res_tar = _ungzip(os.path.abspath(fn), 'archive')
        if res_tar:
            # Got the tar file, now to unpack it
            res = _untar(os.path.abspath(res_tar), 'unpack')
    elif fn.lower().endswith('.tar'):
        res = _untar(os.path.abspath(fn), 'unpack')
    if res:
        # Assuming we got to this point, we now have a directory, with possible sub-dirs, with a setup.py
        # Have to find that setup.py, search top down for first one
        # Pick a sane default
        setup_dir = res
        for (path, dirs, files) in os.walk(res):
            if 'setup.py' in set([x.lower() for x in files]):
                setup_dir = path
                break
        setup_dir = os.path.abspath(setup_dir)
        print "* setup.py found here:", setup_dir
        # Attempt a pure python build
        print "* Compiling pure python modules ..."
        result = _py_build(setup_dir)
        if result:
            # Should be contents inside setup_dir/build/lib - merge them into pypi-modules
            if platform.pythonista:
                build_dir = os.path.join(setup_dir, 'build/lib')
            else:
                build_dir = os.path.join(setup_dir, 'build/lib.linux-x86_64-2.7')
            build_dir_exists = os.path.exists(build_dir)
            if not build_dir_exists:
                """If the same tar ball is installed again on iOS, the build_dir
                does not exist. Restarting Pythonista resolves the problem."""
                message = "The build directory does not exist: '{}'".format(
                    build_dir)
                raise ValueError(message)
            if os.path.exists(build_dir):
                # Get the files and directories in it
                os.chdir(build_dir)
                (path, dirs, files) = os.walk(build_dir).next()
                lib_dir = os.path.abspath(os.path.join(__pypi_base__, 'pypi-modules'))
                for a_file in files:
                    print "* Installing module: %s ..." % a_file
                    target = os.path.join(lib_dir, a_file)
                    if os.path.exists(target):
                        _rm(target)
                    shutil.copyfile(a_file, target)
                for a_dir in dirs:
                    print "* Installing module: %s ..." % a_dir
                    target = os.path.join(lib_dir, a_dir)
                    if os.path.exists(target):
                        _rm(target)
                    shutil.copytree(a_dir, target)

        _reset_and_enter_tmp(cwd)
        return True
    else:
        print "* ERROR: Something went wrong"
    _reset_and_enter_tmp(cwd)
    return False
