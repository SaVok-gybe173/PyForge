class InvalidPageError(Exception):

    def __init__(self, message="Произошла ошибка в программе!"):
        self.message = message
        super().__init__(self.message)  # Вызываем конструктор базового класса Exception

    def __str__(self):
        return f"MyCustomError: {self.message}"