import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


######################################## test ##################################################
def test_grid(grid: np.ndarray[bool],) -> None:
    # this tests if the grid has the good format and shape
    assert type(grid) == np.ndarray  # work with numpy array
    assert grid.shape[0] == grid.shape[1]  # work with squared grid only
    assert len(grid.shape) == 2
    assert grid.dtype == bool  # grid contains boolean only


def test_update():
    # test the update function on 1 case (blinker)
    # rules:
    # -1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    # -2. Any live cell with two or three live neighbours lives on to the next generation.
    # -3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    # -4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
    size = 10
    grid_empty = create_grid(size=size)
    cond_init_1 = [(5, 5), (6, 5), (7, 5)]
    grid_init = initialize_grid(grid=grid_empty,
                                cond_init=cond_init_1)
    grid = update(grid=grid_init)
    grid_empty = create_grid(size=size)
    cond_init_2 = [(6, 6), (6, 5), (6, 4)]
    grid_ok = initialize_grid(grid=grid_empty,
                              cond_init=cond_init_2)
    assert (grid == grid_ok).all()


######################################## functions #############################################
def create_grid(size: int,) -> np.ndarray[bool]:
    return np.zeros((size, size), dtype=bool)


def initialize_grid(
        grid: np.ndarray[bool],
        cond_init: list[tuple[int, int]],
) -> np.ndarray[bool]:
    if len(cond_init) > 0:
        grid[cond_init[0][0], cond_init[0][1]] = True
        cond_init.pop(0)
        initialize_grid(grid=grid, cond_init=cond_init)
    return grid


def apply_periodicity(x: int, size: int,) -> int:
    if x < 0:
        return size - 1
    elif x == size:
        return 0
    else:
        return x


def count_live_neigbours(
    grid: np.ndarray[bool],
    i: int,
    j: int,
) -> int:
    size = len(grid)
    # count the number of live neighbours of the cell i, j in grid
    n_neighbours = -int(grid[i, j])
    for n_i in range(i-1, i+2):
        for n_j in range(j-1, j+2):
            # periodic boundary condition
            n_i = apply_periodicity(x=n_i, size=size)
            n_j = apply_periodicity(x=n_j, size=size)
            n_neighbours += grid[n_i, n_j]
    return n_neighbours


def update(grid: np.ndarray[bool],) -> np.ndarray[bool]:
    # update the grid according to the rules:
    # -1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    # -2. Any live cell with two or three live neighbours lives on to the next generation.
    # -3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    # -4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction

    # for all cells, I need a function that counts the number of live neighbours
    # if the cell is alive, then apply rule 1, 2 & 3
    # else: apply rule 4
    size = len(grid)
    new_grid = create_grid(size=size)  # rule 1 and 3 already satisfied
    for i in range(size):
        for j in range(size):
            n_ij = count_live_neigbours(grid=grid, i=i, j=j)
            if grid[i, j]:
                if n_ij == 2 or n_ij == 3:  # rule 2
                    new_grid[i, j] = True
            else:
                if n_ij == 3:  # rule 4
                    new_grid[i, j] = True
    return new_grid


def vizualize(
        size: int,
        cond_init: list[tuple[int, int]],
        n_times: int,
) -> None:
    grid_empty = create_grid(size=size)
    grid_init = initialize_grid(grid=grid_empty,
                                cond_init=cond_init)
    grid = grid_init
    ims = []
    fig, ax = plt.subplots()
    for t in range(n_times):
        # ax.set_title("timestamp t = " + str(t))
        ax.imshow(grid, cmap='gray')
        im = plt.imshow(grid, animated=True)
        if t == 0:
            ax.imshow(grid)
        ims.append([im])
        grid = update(grid=grid)
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=1000)
    plt.show()


if __name__ == "__main__":
    print("hello")
    size = 10
    grid_empty = create_grid(size=size)
    test_grid(grid_empty)
    cond_init = [(5, 5), (6, 5), (7, 5)]
    grid_init = initialize_grid(grid=grid_empty,
                                cond_init=cond_init)
    test_grid(grid_init)
    test_update()
    cond_init = [(50, 50), (50, 49), (50, 51), (49, 50), (51, 51)]
    vizualize(size=100, cond_init=cond_init, n_times=60)
