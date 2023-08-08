import random
import pythonbible as bible
# https://docs.python.bible/technical_reference.html

bible_reference_ids = [9006019, 5025011, 60002018, 2021007, 2021008, 3009010, 3015025, 3015033, 23013016, \
                    28013016, 5023001, 12006028, 1019035, 1019035, 1019036, 40005028, 12013009, 1038007, \
                    1038008, 1038009, 1038010, 14021014, 14021015, 66021008, 10013011, 10013012, 10013014, \
                    23003016, 3026029, 4005019, 4005024, 4005028, 26023020, 5028035, 3019027, 2023019, \
                    3015019, 3015020, 5025011, 5025012, 12002024, 40021019, 4031017, 4031018, 12023020, \
                    12023024, 3025044, 3025045, 49006005, 5021020, 5021021, 3020015, 5023001, 3021018, \
                    3021023, 4016048, 7019024, 1009027, 1009021, 1009022, 1009023, 1009024, 54002012, \
                    2004024, 2004025, 2009009, 2009011, 11020036, 10006007, 2021004, 2021006, 2021020, \
                    2021021, 42012047, 42012048, 3012002, 3012003, 3012004, 3012005, 3012007, 3012008, \
                    18014001, 18014004, 2022017, 3020013, 2021015, 20020020, 3020009, 3020010, 3021009, \
                    2022019, 14015013, 38013003, 5013015, 5013016, 4016035, 4021003, 4021006, 4025004, \
                    4025008, 4025009, 4031009, 5020016, 6011006, 7001017, 7004021, 7007021, 7009005, \
                    7009045, 7011037, 7011038, 7015015, 7018027, 9004010, 9011011, 9015033, 10002023]

def get_selected_bible_verse():
    # Get a random bible_reference_id
    bible_reference_id = random.choice(bible_reference_ids)
    try:
        text = bible.get_verse_text(bible_reference_id)
    except:
        print(f"Error: {bible_reference_id} not found")
        return "In the beginning God created the heavens and the earth. - Genesis 1:1"
    reference = bible.convert_verse_ids_to_references([bible_reference_id])[0]
    verse = bible.format_single_reference(reference)

    return f"{text} - {verse}"


def check_reference(text):
    try:
        ref = bible.get_references(text)
        if len(ref) == 0:
            return False
        else:
            ref = ref[0]
        
        verse_text = '"'
        if bible.is_valid_reference(ref):
            verse_id_list = bible.convert_reference_to_verse_ids(ref)
            for verse_id in verse_id_list:
                if len(verse_text) + len(bible.get_verse_text(verse_id)) < 1950:
                    verse_text += bible.get_verse_text(verse_id) 
            verse_text += '"'
            verse = bible.format_single_reference(ref)

            return f"{verse_text} - {verse}"
        else:
            return False
    except Exception as e:
        return False
    

def get_random_verse():
    dice_roll = random.randint(1, 3)
    
    if dice_roll == 1:
        return get_selected_bible_verse()
    else:
        num_of_books = 72
        # get a random book
        selected_book_num = random.randint(1, num_of_books)
        book = bible.Book(selected_book_num)

        # get a random chapter
        num_of_chapters = bible.get_number_of_chapters(book)
        selected_chapter_num = random.randint(1, num_of_chapters)

        # get a random verse
        num_of_verses = bible.get_number_of_verses(book, selected_chapter_num)
        selected_verse_num = random.randint(1, num_of_verses)

        reference = bible.NormalizedReference(book, selected_chapter_num, selected_verse_num, selected_chapter_num, selected_verse_num)
        if bible.is_valid_reference(reference):
            verse_id_list = bible.convert_reference_to_verse_ids(reference)
            for verse_id in verse_id_list:
                verse_text = bible.get_verse_text(verse_id)
            verse = bible.format_single_reference(reference)

            return f"{verse_text} - {verse}"

        