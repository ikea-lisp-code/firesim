import liblo

from ui.audioemitterwidget import AudioEmitterWidget

class AudioEmitter:
    def __init__(self, data=None, controller=None):
        self._type = "emitter"
        self._pos = (0, 0)
        self._velocity = (0, 0)
        self._orientation = (0, 0)
        self._group = 'none'
        self._controller = controller

        if data is not None:
            self.unpack(data)

        self._widget = None

    def __repr__(self):
        return "AudioEmitter:%s,%s,%s" % (self._type, self._pos, self._velocity, self._orientation)

    def pack(self):
        return {
                'type': self._type,
                'pos': self._pos,
                'velocity': self._velocity,
                'orientation': self._orientation,
                'group': self._group
                }

    def unpack(self, data):
        self._type = data.get("type", "")
        self._group = data.get('group', 'none')
        self._pos = data.get("pos", (0, 0))
        self._velocity = data.get("pos", (0, 0))
        self._orientation = data.get("pos", (0, 0))

    def pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos

        mixxx_addr = liblo.Address(2448)
        liblo.send(mixxx_addr, '/control/set',
                   ('s', '%s,position_x' % self._group),
                   ('d', self._pos[0]))
        liblo.send(mixxx_addr, '/control/set',
                   ('s', '%s,position_y' % self._group),
                   ('d', self._pos[1]))

    def destroy(self):
        self._widget.deleteLater()

    def get_widget(self):
        if self._widget is None:
            self._widget = AudioEmitterWidget(self._controller.get_canvas(), model=self)
            x, y = self._pos[0], self._pos[1]
            self._widget.setPos(x, y)
            #self._widget.setRotation(self.angle)
        return self._widget

    def move_callback(self, widget):
        print "AudioEmitter.move_callback", widget
        self.set_pos((widget.x(), widget.y()))
