'''Board class module'''
import pygame
import pygame.font

class Board:
    '''Board class'''
    def __init__(self, life, box=8):

        self.life = life
        self.info_panel_width = 320
        self.columns = life.columns
        self.rows = life.rows
        self.box = box
        self.life_width = self.columns*self.box
        self.width = self.life_width+self.info_panel_width
        self.height = self.rows*self.box

        self.col_bck = (0, 0, 0)
        self.col_box = ((0, 0, 0),(64, 0, 0),(0, 255, 0),(255, 0, 0))
        self.col_axis = (0, 32, 0)
        self.col_text = (0, 128, 0)
        self.fps = 25

        pygame.init()
        self.board = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('LIFE')
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.SysFont('Consolas', 32)
        self.font_big = pygame.font.SysFont('Consolas', 64)
        self.v_offset = 40
        self.h_offset = 20
        self.text_v_offset = 40
        self.text_v_big_offset = 80

        self.quit = False
        self.pause = True
        self.step = False
        self.reset = False

        self.surf_pop = self.get_rendered_text_surface('POPULATION:')
        self.surf_cycles = self.get_rendered_text_surface('CYCLES:')
        self.surf_stabilized = self.get_rendered_text_surface('STABILIZED AT:')
        self.surf_pause = self.get_rendered_text_surface('P: PAUSE')
        self.surf_reset = self.get_rendered_text_surface('R: RESET')
        self.surf_step = self.get_rendered_text_surface('S: STEP')
        self.surf_plus = self.get_rendered_text_surface('+: INC POPUL.')
        self.surf_minus = self.get_rendered_text_surface('-: DEC POPUL.')
        self.surf_quit = self.get_rendered_text_surface('Q: QUIT')

    def get_rendered_text_surface(self, text, args=tuple(), big_font=False):
        '''returns text surface to blit'''
        if big_font:
            return self.font_big.render(text.format(*args), True, self.col_text)
        else:
            return self.font.render(text.format(*args), True, self.col_text)

    def blit_text(self):
        '''draws osd'''
        x = self.life_width+self.h_offset
        y = self.v_offset

        self.board.blit(self.surf_pop, (x, y))
        y += self.text_v_offset
        text_surf = self.get_rendered_text_surface('{}%', args=[self.life.population], big_font=True)
        self.board.blit(text_surf, (x, y))

        y += self.text_v_big_offset
        self.board.blit(self.surf_cycles, (x, y))
        y += self.text_v_offset
        text_surf = self.get_rendered_text_surface('{}', args=[self.life.cycles], big_font=True)
        self.board.blit(text_surf, (x, y))

        y += self.text_v_big_offset
        self.board.blit(self.surf_stabilized, (x, y))
        y += self.text_v_offset
        text_surf = self.get_rendered_text_surface('{}', args=[self.life.stabilized_at], big_font=True)
        self.board.blit(text_surf, (x, y))

        y += self.text_v_big_offset*2
        self.board.blit(self.surf_pause, (x, y))
        y += self.text_v_offset
        self.board.blit(self.surf_step, (x, y))
        y += self.text_v_offset
        self.board.blit(self.surf_reset, (x, y))
        y += self.text_v_offset
        self.board.blit(self.surf_plus, (x, y))
        y += self.text_v_offset
        self.board.blit(self.surf_minus, (x, y))
        y += self.text_v_offset
        self.board.blit(self.surf_quit, (x, y))

        self.surf_state = self.font.render('WORKING...', True, (255, 128, 0))
        if self.pause:
            self.surf_state = self.font.render('PAUSED', True, (255, 128, 0))
        if self.life.stabilized:
            self.surf_state = self.font.render('STABILIZED', True, (255, 128, 0))
        y += self.text_v_offset*2
        self.board.blit(self.surf_state, (x, y))

    def get_inputs(self):
        '''check for user inputs'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.quit = True

                if event.key == pygame.K_r:
                    self.life.reset()
                    self.pause = True

                if event.key == pygame.K_p:
                    self.pause = not self.pause

                if event.key == pygame.K_s:
                    if self.pause and not self.life.stabilized:
                        self.step = True

                if event.key == pygame.K_KP_PLUS:
                    if self.pause:
                        self.life.increase_population()

                if event.key == pygame.K_KP_MINUS:
                    if self.pause:
                        self.life.decrease_population()

    def update(self):
        '''redraws board'''
        self.get_inputs()

        self.board.fill(self.col_bck)

        box = self.box - 1
        for c in range(self.columns):
            for r in range(self.rows):
                if self.life.A[c, r]:
                    rect = pygame.Rect(c*self.box+1, r*self.box+1, box, box)
                    pygame.draw.rect(self.board, self.col_box[self.life.A[c, r]], rect, 0)

        # vertical axes
        for v in range(self.columns + 1):
            x = self.box * v
            pygame.draw.line(self.board, self.col_axis,[x, 0],[x, self.height])

        # horizontal axes
        for h in range(self.rows + 1):
            y = self.box * h
            pygame.draw.line(self.board, self.col_axis,[0, y],[self.life_width, y])

        self.blit_text()

        pygame.display.update() # pygame.display.flip()
        self.clock.tick(self.fps)
