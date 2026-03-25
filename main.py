import pygame

WINDOW_SIZE: int = 800

def main():
    window = pygame.display.set_mode( (WINDOW_SIZE, WINDOW_SIZE) )

    while True:
        pygame.display.update()

if __name__ == "__main__":
    main()
