import sys
import logging
import dispose_file_error
args = sys.argv

try:
    import maya.standalone
    maya.standalone.initialize()
    import maya.cmds as cmds
except Exception, e:
    print e

def fileErrorDispose(path):
    if os.path.splitext(path)[-1] == '.mb':
        path = path.replace('\\', '/')
        new_path = path.replace('.mb', '.ma')
        cmds.file(new=True, f=True)
        cmds.file(path, o=True)
        cmds.file(rename=new_path)
        unknown_nodes = cmds.ls(type="unknown")
        if unknown_nodes:
            for u_node in unknown_nodes: 
                try:
                    cmds.lockNode(u_node, l=False)
                    cmds.delete(u_node)
                except Exception,e:
                    print e
        cmds.file(save=True, type="mayaAscii", f=1)
        if dispose_file_error.dispose_file_error(new_path):
            cmds.file(new_path, o=True, f=1)
            cmds.file(rename=path)
            cmds.file(save=True, f=True, type="mayaBinary")
            os.remove(new_path)
    if os.path.splitext(path)[-1] == '.ma':
        path = path.replace('\\', '/')
        if dispose_file_error.dispose_file_error(path):
            cmds.file(new=True, f=1)
            cmds.file(path, o=True)
            unknown_nodes = cmds.ls(type="unknown")
            if unknown_nodes:
                for u_node in unknown_nodes: 
                    try:
                        cmds.lockNode(u_node, l=False)
                        cmds.delete(u_node)
                    except Exception,e:
                        print e
            cmds.file(rename=path.replace('.ma', '.mb'))
            cmds.file(save=True, f=True, type="mayaBinary")
            os.remove(path)
fileErrorDispose(args[1])

try:
    maya.standalone.uninitialize()
except: pass

input()