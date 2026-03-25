import pygame

WINDOW_SIZE: int = 800
clock = pygame.time.Clock()  # control the fps

projection_matrix = [[1,0,0],
                     [0,1,0],
                     [0,0,0]]

cube_points = [n for n in range(8)]
cube_points[0] = [ [-1], [-1], [1] ]
cube_points[1] = [ [1], [-1], [1] ]
cube_points[2] = [ [1], [1], [1] ]
cube_points[3] = [ [-1], [1], [1] ]
cube_points[4] = [ [-1], [-1], [-1] ]
cube_points[5] = [ [1], [-1], [-1] ]
cube_points[6] = [ [1], [1], [-1] ]
cube_points[7] = [ [-1], [1], [-1] ]

def multiply_m(a,b):
    a_rows = len(a)
    a_cols = len(a[0])

    b_rows = len(b)
    b_cols = len(b[0])
    # Dot product matrix dimensions = a_rows x b_cols
    product = [[0 for _ in range(b_cols)] for _ in range(a_rows)]

    # O(n^3), this is pretty bad - I should use numpy instead
    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product[i][j] += a[i][k] * b[k][j]
    else:
        print("Error: Incompatible matrix sizes")

    return product

def main():
    window = pygame.display.set_mode( (WINDOW_SIZE, WINDOW_SIZE) )

    while True:
        clock.tick(60)  # 60 fps

        for point in cube_points:
            point_2d = multiply_m(projection_matrix, point)

            x = point_2d[0][0]
            y = point_2d[1][0]

            pygame.draw.circle(window, (255, 0, 0), (x, y), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()

if __name__ == "__main__":
    main()
