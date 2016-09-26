import re

from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

def get_bible_verse_model():
    model_name = htk_setting('HTK_BIBLE_VERSE_MODEL')
    bible_verse_model = resolve_model_dynamically(model_name)
    return bible_verse_model

def lookup_bible_verse(book, chapter, verse):
    BibleVerse = get_bible_verse_model()
    try:
        verse = BibleVerse.objects.get(
            book=book,
            chapter=chapter,
            verse=verse,
        )
    except BibleVerse.DoesNotExist:
        verse = None
    return verse

def resolve_bible_verse_reference(reference):
    pattern = r'^(?P<book>.*) (?P<chapter>\d+):(?P<verse>\d+)$'
    m = re.match(pattern, reference.strip())
    (book, chapter, verse,) = (
        m.group('book'),
        m.group('chapter'),
        m.group('verse'),
    )
    v = lookup_bible_verse(book, chapter, verse)
    return v

def get_bible_chapter_data(book, chapter):
    BibleVerse = get_bible_verse_model()
    data = {
        'num_verses' : BibleVerse.objects.filter(book=book, chapter=chapter).count(),
    }
    return data
