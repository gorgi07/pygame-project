class Egor:
    def __init__(self, status=None):
        self.status = status

    def __str__(self):
        return f"Егор со статусом {self.status}"

    def __repr__(self):
        return self.status


if __name__ == '__main__':
    egor2007 = Egor("Разработчик")
    print(egor2007)
    print(egor2007.__repr__())