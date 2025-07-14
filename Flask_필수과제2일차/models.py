class BookModel:
    def __init__(self):
        self.books = {}
        self.counter = 1

        def get_all(self):
            return list(self.books.values())
        
        def get_by_id(self, book_id: int):
            return self.books.get(book_id)
        
        def create(self, date):
            book_id = self.counter
            self.books[book_id] = { "id": book_id, **date }
            self.counter += 1
            return self.books[book_id]
        
        def update(self, book_id: int, data):
            if book_id in self.books:
                self.books[book_id].update(data)
                return self.books[book_id]
            return None
        
        def delete(self, book_id: int):
            return self.books.pop(book_id, None)
