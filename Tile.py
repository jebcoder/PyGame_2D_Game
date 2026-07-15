import pygame
from utilities import load_image

# Tile type to image mapping
TILE_IMAGES = {
    'grass': 'tile_grass.jpg',
    'hole': 'tile_hole.png',
    'water': 'tile_water.gif'
}

TILE_BORDER_COLOR = (250, 0, 0)


class Tile:
    def __init__(self, column, row, tile_type, image_name=None, parent=None):
        self.column = column
        self.row = row
        self.type = tile_type
        self.parent = parent
        self.transparent = False
        
        # Set image name
        self.image_name = image_name or TILE_IMAGES.get(tile_type, image_name)
        
        # Load images
        self.image = load_image(self.image_name, path='Images/Tiles')
        self.transparent_image = load_image('transparent_tile.png', path='Images', alpha_channel=True)
        
        # Set rect position
        self.rect = self.image.get_rect()
        self.rect.x = column * self.rect.w
        self.rect.y = row * self.rect.h

    def __repr__(self):
        return f"Tile {self.column}|{self.row} type:{self.type}, coord({self.rect.x},{self.rect.y})"

    def get_type(self):
        return self.type

    def get_size(self):
        return self.rect.size

    def get_coord(self):
        return self.rect.x, self.rect.y

    def check_mouse_coords(self, xy):
        return self.rect.collidepoint(xy)

    def change_image(self, status):
        if status == 'on' and not self.transparent:
            self.image.blit(self.transparent_image, (0, 0))
            self.transparent = True
        elif status == 'off':
            self.image = load_image(self.image_name, path='Images/Tiles', alpha_channel=True)
            self.transparent = False

    def is_walkable(self):
        return self.type == 'grass'

    def render(self, surf, coord=None):
        x = self.column * self.rect.w
        y = self.row * self.rect.h
        
        if coord:
            x, y = coord
        
        surf.blit(self.image, (x, y))
        
        # Draw tile border
        self._draw_border(surf, x, y)

    def _draw_border(self, surf, x, y):
        w, h = self.rect.w, self.rect.h
        pygame.draw.lines(surf, TILE_BORDER_COLOR, True, [
            (x, y),
            (x + w, y),
            (x + w, y + h),
            (x, y + h)
        ])


class TileBrush(Tile):
    def __init__(self, column, row, tile_type, image_name, parent=None):
        super().__init__(column, row, tile_type, image_name, parent)
        self.brush = False

    def check_mouse_coords(self, xy):
        return self.rect.collidepoint(xy)

    def event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and self.check_mouse_coords(self.parent.cursor_coord):
            self.brush = True

    def get_brush(self):
        return 'tile', self.type
