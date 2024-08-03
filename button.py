import pygame

class Button:
    TEXT_COLOR = (0,0, 0)
    def __init__(self, text, pos, size, colors, font):
        self.text = text
        self.pos= pos
        self.size = size
        self.colors = colors
        self.font = font
        self.rect = pygame.Rect(self.pos, self.size)
        self.color = colors['normal']
        self.hovered = False
        self.clicked = False
    

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect,border_radius=10)
        text_surface = self.font.render(self.text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center =self.rect.center)
        surface.blit(text_surface,text_rect)

    def handle_event(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            self.color = self.colors['hover'] if self.hovered else self.colors['normal']
        if (event.type == pygame.MOUSEBUTTONDOWN) :
           if self.rect.collidepoint(event.pos):
                self.clicked = True
                self.color = self.colors['click']
        if event.type == pygame.MOUSEBUTTONUP:
            if self.clicked and self.rect.collidepoint(event.pos):
                self.clicked = False
                return True
            self.color = self.colors['hover'] if self.hovered else self.colors['normal']
            self.clicked = False
        return False

