book_words = ['бронь', 'спасу', 'забронированно']

def is_booked(text):
    processed_text = text.lower()

    for book_word in book_words:
        if book_word in text:
            return True

    return False