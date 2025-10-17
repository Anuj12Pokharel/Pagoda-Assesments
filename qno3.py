def even_squares_list(n=1_000_000):

    return [i * i for i in range(0, n, 2)]


if __name__ == "__main__":

    squares = even_squares_list(1_000_000)
    print(len(squares))
    print(squares[:5])
