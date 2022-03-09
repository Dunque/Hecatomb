class Scene:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo events.")

    def draw(self, screen):
        raise NotImplemented("Tiene que implementar el metodo draw.")
