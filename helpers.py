import cherrypy
from cherrypy import HTTPRedirect, HTTPError
import os.path
from tempfile import NamedTemporaryFile
from subprocess import call, PIPE

def add_flash(msg_type,msg=None):
    if not msg:
        msg = msg_type
        msg_type = 'info'

    cherrypy.session.setdefault(msg_type,[]).append(msg)

def redirect(*args,**kwargs):
    raise HTTPRedirect(*args,**kwargs)

class Validation(Exception):
    pass


def save_form_data(form_file,save_root,
                        prefix=''):
    """ save form file to random file under root,
        returning the path """

    file_data = form_file.file.read()
    file_name = os.path.basename(form_file.filename)
    file_ext = file_name.rsplit('.',1)[-1]
    file_name = file_name[:-(len(file_ext)+1)]
    return _save_form_data(file_data,save_root,file_ext,prefix)

def _save_form_data(file_data,save_root,file_ext=None,prefix=''):
    t = NamedTemporaryFile(delete=False,
                           dir=save_root,
                           suffix='.%s'%file_ext,
                           prefix=prefix)
    fh = t.file
    path = os.path.abspath(t.name)
    fh.write(file_data)
    fh.close()
    return path

def create_thumbnail(img_path,out_root,w,h='',
                          overwrite=False):
    """ creats a thumbnail of the image @ the given size,
        writes the thumbnail to the drive w/ size as
        the prefix """

    w,h = map(str,(w,h))
    if not h:
        h = w
    if 'x' in w:
        size = w
    else:
        size = '%sx%s' % (w,h)
    file_name = os.path.basename(img_path)
    out_path = os.path.join(out_root,
                            '%s_%s' % (size,file_name))
    if os.path.exists(out_path) and not overwrite:
        return out_path

    cmd = ['convert','-thumbnail',size,img_path,out_path]
    cherrypy.log('cmd: %s' % cmd)
    r = call(cmd) # TODO check return code
    cherrypy.log('out path: %s' % out_path)
    return out_path

