class Scene:

    def __init__(self, sceneManager):
        self.sceneManager = sceneManager

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def draw(self, screen):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
