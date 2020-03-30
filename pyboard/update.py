import urequests
import io
import uzlib
import utarfile
import os
import sys

import etc.github

def root_dir():
  return "" if "linux" == sys.platform else "/"

def read_content(url):
  response = urequests.get(url, headers={"User-Agent":"micropython urequests"})
  retval = response.content
  response.close()
  return retval

def read_json(url):
  response = urequests.get(url, headers={"User-Agent":"micropython urequests"})
  retval = response.json()
  response.close()
  return retval

def mkdir(name):
  if "" != name:
    try:
      os.mkdir(name)
    except:
      pass

def get_local_sha():
  shafile = root_dir() + "var/github.py"
  try:
    with open(shafile, "r") as f:
      pass
  except:
    mkdir(root_dir() + "var")
    with open(shafile, "w") as f:
      f.write('repo = {"sha":""}')

  import var.github
  return var.github.repo["sha"]

def get_remote_sha():
  url = "https://api.github.com/repos/%s/%s/commits/%s" % (etc.github.repo['user'], etc.github.repo['repo'], etc.github.repo['branch'])
  return read_json(url)['sha']

def save_file(fname, subf):
  file_buf = bytearray(256)
  with open(fname, "wb") as outf:
    while True:
      sz = subf.readinto(file_buf)
      if not sz:
        break
      outf.write(file_buf, sz)

def perform_update():
  url = "https://codeload.github.com/%s/%s/legacy.tar.gz/%s" % (etc.github.repo['user'], etc.github.repo['repo'], etc.github.repo['branch'])
  tarball_gz = io.BytesIO(read_content(url))
  tarball_gz.seek(0)
  tarball = uzlib.DecompIO(tarball_gz, 31)
  tar = utarfile.TarFile(fileobj=tarball)
  for info in tar:
    if 'pyboard/' in info.name:
      target = "/" + info.name.split('pyboard/')[1]
      if "linux" == sys.platform:
        target = target.lstrip("/")
      if utarfile.DIRTYPE == info.type:
        mkdir(target)
      elif utarfile.REGTYPE == info.type:
        save_file(target, tar.extractfile(info))
      else:
        print("Unknown type: " + target)

def set_local_sha(sha):
  shafile = "var/github.py" if "linux" == sys.platform else "/var/github.py"
  with open(shafile, "w") as outf:
    outf.write('repo = {"sha":"%s"}' % (sha))


local_sha = get_local_sha()
remote_sha = get_remote_sha()

if local_sha != remote_sha:
  print("local sha  : %s" % (local_sha))
  print("remote sha : %s" % (remote_sha))
  print("Updating...")

  perform_update()
  set_local_sha(remote_sha)
