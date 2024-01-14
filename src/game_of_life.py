import numpy as np


######################################## test ##################################################
def test_grid(grid: np.ndarray[bool],) -> None:
    # this tests if the grid has the good format and shape
    assert type(grid) == np.ndarray  # work with numpy array
    assert grid.shape[0] == grid.shape[1]  # work with squared grid only
    assert len(grid.shape) == 2
    assert grid.dtype == bool  # grid contains boolean only


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


if __name__ == "__main__":
    print("hello")
    size = 10
    grid_empty = create_grid(size=size)
    test_grid(grid_empty)
    cond_init = [(5, 5), (6, 5), (7, 5)]
    grid_init = initialize_grid(grid=grid_empty,
                                cond_init=cond_init)
    test_grid(grid_init)
