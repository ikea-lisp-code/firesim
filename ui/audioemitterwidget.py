from PySide import QtCore, QtGui, QtDeclarative

class AudioEmitterWidget(QtDeclarative.QDeclarativeItem):

    def __init__(self, canvas=None, model=None):
        super(AudioEmitterWidget, self).__init__(canvas)
        self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptedMouseButtons(QtCore.Qt.MouseButton.LeftButton |
                                     QtCore.Qt.MouseButton.MiddleButton |
                                     QtCore.Qt.MouseButton.RightButton)
        self.setAcceptsHoverEvents(True)
        self.model = model
        self.about_to_delete = False

        self.setHeight(10)
        self.setWidth(10)

        self.dragging = False
        self.mouse_down = False
        self.setSelected(False)
        self.hovering = False
        self.drag_pos = None

        if canvas:
            self.canvas = canvas
            x, y = canvas.get_next_new_fixture_pos_and_increment()
            self.setPos(x, y)
            #self.canvas.hover_move_event.connect(self.hover_move_handler)

        self.update_geometry()

    def update_geometry(self):
        pos = self.canvas.scene_to_canvas(self.model.pos())
        self.prepareGeometryChange()
        self.update(self.boundingRect())

    def paint(self, painter, options, widget):
        width, height = (self.canvas.coordinate_scale * self.width(),
                         self.canvas.coordinate_scale * self.height())
        painter.setBrush(QtGui.QColor(255, 255, 255, 255))
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 255),
                                  6,
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.drawRect(0, 0, width, height)

    def mousePressEvent(self, event):
        print "mousePressEvent", event
        self.mouse_down = True
        self.drag_pos = event.scenePos()

    def select(self, selected, multi=False):
        print "select", selected, multi

    def mouseMoveEvent(self, event):
        if self.mouse_down:
            self.dragging = True
            npos = (event.scenePos() - self.drag_pos)
            if self.parent().sceneBoundingRect().contains(event.scenePos()):
                self.moveBy(npos.x(), npos.y())
            self.drag_pos = event.scenePos()
            self.model.move_callback(self)

        event.ignore()
        #super(FixtureWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragging:
            self.dragging = False
            self.mouse_down = False
            self.drag_pos = None
            self.model.move_callback(self)
