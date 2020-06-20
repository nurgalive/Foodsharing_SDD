book_words = ['бронь', 'спасу', 'забронированно']

def get_is_booked(text):
    processed_text = text.lower()

    for book_word in book_words:
        if book_word in processed_text:
            return True

    return False