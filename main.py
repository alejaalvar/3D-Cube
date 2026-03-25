"""
File: main.py
Author: Alejandro Alvarado
Brief: A 3D interactive cube PyGame application.
"""

import pygame
from math import *
from typing import List

ROTATE_SPEED: float = 0.02
WINDOW_SIZE: int = 800
clock: pygame.time.Clock = pygame.time.Clock()  # control the fps
window: pygame.Surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

# We use this to convert a 3D point -> 2D point
projection_matrix: List[List[int]] = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]

cube_points: List[List[int]] = [n for n in range(8)]
cube_points[0] = [[-1], [-1], [1]]
cube_points[1] = [[1], [-1], [1]]
cube_points[2] = [[1], [1], [1]]
cube_points[3] = [[-1], [1], [1]]
cube_points[4] = [[-1], [-1], [-1]]
cube_points[5] = [[1], [-1], [-1]]
cube_points[6] = [[1], [1], [-1]]
cube_points[7] = [[-1], [1], [-1]]


def multiply_m(
    a: list[list[float]], b: list[list[float]]
) -> list[list[float]]:
    """Multiply two matrices a and b. O(n^3) time complexity.

    Args:
        a (list[list[float]]): the first matrix
        b (list[list[float]]): the second matrix

    Returns:
        list[list[float]]: the resulting matrix
    """
    a_rows: int = len(a)
    a_cols: int = len(a[0])

    b_rows: int = len(b)
    b_cols: int = len(b[0])
    # Dot product matrix dimensions = a_rows x b_cols
    product: list[list[float]] = [
        [0 for _ in range(b_cols)] for _ in range(a_rows)
    ]

    # O(n^3), this is pretty bad - I should use numpy instead
    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product[i][j] += a[i][k] * b[k][j]
    else:
        print("Error: Incompatible matrix sizes")

    return product


def connect_points(i: int, j: int, points: list[tuple[float, float]]) -> None:
    """Draw a line between a pair of points on the cube

    Args:
        i (int): the i'th point to connect
        j (int): the j'th point to connect
        points (list[tuple[float, float]]): the list of points to connect
    """
    pygame.draw.line(window, (255, 255, 255), (points[i]), (points[j]))


def main() -> None:
    scale: int = 100  # we need this to draw the cube in the center
    # These are how we rotate the cube itself
    angle_x: float = 0.0
    angle_y: float = 0.0
    angle_z: float = 0.0

    # ===== Game Loop =====
    while True:
        clock.tick(60)  # 60 fps
        window.fill((0, 0, 0))  # clear the frame

        # Our rotation matrices
        rotation_x: List[List[int | float]] = [
            [1, 0, 0],
            [0, cos(angle_x), -sin(angle_x)],
            [0, sin(angle_x), cos(angle_x)],
        ]

        rotation_y: List[List[int | float]] = [
            [cos(angle_y), 0, sin(angle_y)],
            [0, 1, 0],
            [-sin(angle_y), 0, cos(angle_y)],
        ]

        rotation_z: List[List[int | float]] = [
            [cos(angle_z), -sin(angle_z), 0],
            [sin(angle_z), cos(angle_z), 0],
            [0, 0, 1],
        ]
        points = []  # our 2D points

        # Rotate points & convert 3D points -> 2D points
        for point in cube_points:
            rotate_x = multiply_m(rotation_x, point)
            rotate_y = multiply_m(rotation_y, rotate_x)
            rotate_z = multiply_m(rotation_z, rotate_y)

            point_2d: List[List[int]] = multiply_m(projection_matrix, rotate_z)

            # This drags the cube out of the top left cortner -> center
            x = (point_2d[0][0] * scale) + WINDOW_SIZE / 2
            y = (point_2d[1][0] * scale) + WINDOW_SIZE / 2

            points.append((x, y))
            pygame.draw.circle(
                window, (255, 0, 0), (x, y), 5
            )  # each red dot, thats why circle

        connect_points(0, 1, points)
        connect_points(1, 2, points)
        connect_points(2, 3, points)
        connect_points(3, 0, points)

        connect_points(4, 5, points)
        connect_points(5, 6, points)
        connect_points(6, 7, points)
        connect_points(7, 4, points)

        connect_points(0, 4, points)
        connect_points(1, 5, points)
        connect_points(2, 6, points)
        connect_points(3, 7, points)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                angle_y = angle_x = angle_z = 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                angle_y += ROTATE_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                angle_y -= ROTATE_SPEED
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                angle_x += ROTATE_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                angle_x -= ROTATE_SPEED
            if keys[pygame.K_q]:
                angle_z -= ROTATE_SPEED
            if keys[pygame.K_e]:
                angle_z += ROTATE_SPEED
            if keys[pygame.K_LCTRL] and keys[pygame.K_c]:
                pygame.quit()
                return

        pygame.display.update()


if __name__ == "__main__":
    main()
