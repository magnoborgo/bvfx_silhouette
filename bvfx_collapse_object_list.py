from fx import *
from PySide2 import QtWidgets, QtCore
import shiboken2

class bvfx_CollapseObjectList(Action):
    """Collapses (close) all the object list main layers """

    def __init__(self):
        Action.__init__(self, "BoundaryVFX|Collapse Object List Layers")

    def available(self):
        node = activeNode()
        session = activeSession()
        assert session, "Select a Session"
        rotoNode = session.node(type="RotoNode")
        assert rotoNode, "The session does not contain a Roto Node"

    def execute(self):
        app = QtWidgets.QApplication.instance()

        # Find the Object List dock and act on its tree widget immediately --
        # no storing references across call boundaries, no re-checking after
        # returning. Everything happens in one pass while the reference is live.
        for dock in app.allWidgets():
            if not isinstance(dock, QtWidgets.QDockWidget):
                continue
            if not shiboken2.isValid(dock):
                continue
            try:
                if dock.windowTitle().strip().lower() != "object list":
                    continue
            except RuntimeError:
                continue

            # Found the dock -- find its tree and act immediately
            trees = [
                w for w in dock.findChildren(QtWidgets.QTreeWidget)
                if shiboken2.isValid(w) and w.isVisible()
            ]
            if not trees:
                print("Dock found but no visible QTreeWidget inside it.")
                return

            tree = max(trees, key=lambda w: w.geometry().width() * w.geometry().height())

            # Act on it right now, no returning or re-fetching
            collapsed = 0
            for i in range(tree.topLevelItemCount()):
                item = tree.topLevelItem(i)
                if item.childCount() > 0 and item.isExpanded():
                    item.setExpanded(False)
                    collapsed += 1

            print("Collapsed %d top-level layer(s)." % collapsed)
            return

        print("Could not find the 'Object List' dock widget.")

        

if __name__ == "__main__":
    bvfx_CollapseObjectList().execute()
else:
    addAction(bvfx_CollapseObjectList())