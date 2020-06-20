lost_words = ['забр']

def get_is_lost(text):
    processed_text = text.lower()

    for lost_word in lost_words:
        if lost_word in processed_text:
            return True

    return False