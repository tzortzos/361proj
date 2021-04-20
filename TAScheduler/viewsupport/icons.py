class IconItem:
    """Represents a single icon of the set built into bootstrap"""

    def __init__(self, iconname: str):
        """Create a new icon item with a specific name
        see names here: https://getbootstrap.com/docs/3.4/components/#glyphicons-glyphs"""
        self.name = iconname

    def take(self) -> str:
        """get the bootstrap name of a specific icon"""
        return self.name

    def classes(self) -> str:
        return f'bi bi-{self.name}'
