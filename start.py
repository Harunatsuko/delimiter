import pygame
from delimiter import Delimiter


def main():
    '''
    Manage:
    1) To choose part of image: click on left mouse button and drag to choose image part -
       it will be saved as new image when mouse button will be upped
    2) When all good parts of image will be saved, delete the source image with
       one click on right mouse button
    3) To save the source image just click on 's' key - and crop the part of next image
    '''
    delimit = Delimiter()
    is_running = True
    print('Delimiter process starting...')
    while is_running: # Основной цикл 
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == pygame.QUIT:
                a = False
            elif e.type ==pygame.MOUSEBUTTONDOWN:
                if e.button == 1:  #  левая кнопка мыши
                    delimit.handle_left_mbt(e.pos, 'down')
                    print('left mb down')
                if e.button == 3:  #  правая кнопка мыши
                    delimit.delete_img()
                    delimit.next_image()
            elif e.type ==pygame.MOUSEBUTTONUP:
                if e.button == 1:  #  левая кнопка мыши
                    delimit.handle_left_mbt(e.pos, 'up')
                    print('left mb up')
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_s: # s button key
                    delimit.next_image()

        delimit.update()
        pygame.time.wait(10)
        pygame.display.update()

if __name__ == "__main__":
    main()