"""
The content of this module was adapted and mostly taken verbatim from the gutenbergypy project:
https://github.com/raduangelescu/gutenbergpy/blob/master/gutenbergpy/textget.py
which was itself taken from the gutenberg project:
https://github.com/c-w/Gutenberg
in which the strip_headers function was ported from a C++ version by Johannes Krugel which no longer appears to be available.
I have added a line to TEXT_END_MARKERS and changed the return value of strip_headers to encode the output text
"""

import os
import requests
import ipdb


TEXT_START_MARKERS = frozenset(
    (
        "*END*THE SMALL PRINT",
        "*** START OF THE PROJECT GUTENBERG",
        "*** START OF THIS PROJECT GUTENBERG",
        "This etext was prepared by",
        "E-text prepared by",
        "Produced by",
        "Distributed Proofreading Team",
        "Proofreading Team at http://www.pgdp.net",
        "http://gallica.bnf.fr)",
        "      http://archive.org/details/",
        "http://www.pgdp.net",
        "by The Internet Archive)",
        "by The Internet Archive/Canadian Libraries",
        "by The Internet Archive/American Libraries",
        "public domain material from the Internet Archive",
        "Internet Archive)",
        "Internet Archive/Canadian Libraries",
        "Internet Archive/American Libraries",
        "material from the Google Print project",
        "*END THE SMALL PRINT",
        "***START OF THE PROJECT GUTENBERG",
        "This etext was produced by",
        "*** START OF THE COPYRIGHTED",
        "The Project Gutenberg",
        "http://gutenberg.spiegel.de/ erreichbar.",
        "Project Runeberg publishes",
        "Beginning of this Project Gutenberg",
        "Project Gutenberg Online Distributed",
        "Gutenberg Online Distributed",
        "the Project Gutenberg Online Distributed",
        "Project Gutenberg TEI",
        "This eBook was prepared by",
        "http://gutenberg2000.de erreichbar.",
        "This Etext was prepared by",
        "This Project Gutenberg Etext was prepared by",
        "Gutenberg Distributed Proofreaders",
        "Project Gutenberg Distributed Proofreaders",
        "the Project Gutenberg Online Distributed Proofreading Team",
        "**The Project Gutenberg",
        "*SMALL PRINT!",
        "More information about this book is at the top of this file.",
        "tells you about restrictions in how the file may be used.",
        "l'authorization à les utilizer pour preparer ce texte.",
        "of the etext through OCR.",
        "*****These eBooks Were Prepared By Thousands of Volunteers!*****",
        "We need your donations more than ever!",
        " *** START OF THIS PROJECT GUTENBERG",
        "****     SMALL PRINT!",
        '["Small Print" V.',
        "      (http://www.ibiblio.org/gutenberg/",
        "and the Project Gutenberg Online Distributed Proofreading Team",
        "Mary Meehan, and the Project Gutenberg Online Distributed Proofreading",
        "                this Project Gutenberg edition.",
    )
)

TEXT_END_MARKERS = frozenset(
    (
        "*** END OF THE PROJECT GUTENBERG",
        "*** END OF THIS PROJECT GUTENBERG",
        "***END OF THE PROJECT GUTENBERG",
        "End of the Project Gutenberg",
        "End of The Project Gutenberg",
        "Ende dieses Project Gutenberg",
        "by Project Gutenberg",
        "End of Project Gutenberg",
        "End of this Project Gutenberg",
        "Ende dieses Projekt Gutenberg",
        "        ***END OF THE PROJECT GUTENBERG",
        "*** END OF THE COPYRIGHTED",
        "End of this is COPYRIGHTED",
        "Ende dieses Etextes ",
        "Ende dieses Project Gutenber",
        "Ende diese Project Gutenberg",
        "**This is a COPYRIGHTED Project Gutenberg Etext, Details Above**",
        "Fin de Project Gutenberg",
        "The Project Gutenberg Etext of ",
        "Ce document fut presente en lecture",
        "Ce document fut présenté en lecture",
        "More information about this book is at the top of this file.",
        "We need your donations more than ever!",
        "END OF PROJECT GUTENBERG",
        " End of the Project Gutenberg",
        " *** END OF THIS PROJECT GUTENBERG",
        "            *** END OF THE PROJECT GUTENBERG",
    )
)

LEGALESE_START_MARKERS = frozenset(("<<THIS ELECTRONIC VERSION OF",))
LEGALESE_END_MARKERS = frozenset(("SERVICE THAT CHARGES FOR DOWNLOAD",))


# def is_valid_utf8(byte_sequence):
#     try:
#         byte_sequence.decode("utf-8")
#         return True
#     except UnicodeDecodeError:
#         return False

def is_valid_utf8(byte_sequence):
    try:
        return isinstance(byte_sequence, str)
    except Exception as e:
        print(e)
        return False

def strip_headers(text):
    lines = text.splitlines()
    sep = os.linesep
    sep = sep.encode("utf-8")
    out = []
    i = 0
    footer_found = False
    ignore_section = False

    for line in lines:
        reset = False

        if i <= 600:
            # Check if the header ends here
            if any(line.startswith(token.encode("utf-8")) for token in TEXT_START_MARKERS):
                reset = True

            # If it's the end of the header, delete the output produced so far.
            # May be done several times, if multiple lines occur indicating the
            # end of the header
            if reset:
                out = []
                continue

        if i >= 100:
            # Check if the footer begins here
            if any(line.startswith(token.encode("utf-8")) for token in TEXT_END_MARKERS):
                footer_found = True

            # If it's the beginning of the footer, stop output
            if footer_found:
                break

        if any(line.startswith(token.encode("utf-8")) for token in LEGALESE_START_MARKERS):
            ignore_section = True
            continue
        elif any(line.startswith(token.encode("utf-8")) for token in LEGALESE_END_MARKERS):
            ignore_section = False
            continue

        if not ignore_section:
            stripline = line.rstrip(sep)
            out.append(stripline)
            i += 1

    return str(sep.join(out), encoding="utf-8")


def write_text_to_file(url, file_path):
    text_request = requests.get(url, stream=True)

    ipdb.set_trace()

    if text_request.status_code != 200:
        raise Exception("Book not found...")

    with open(file_path, "wb") as file:
        chunks = {}
        bad_chunks = {}
        bad_idx = []
        idx = 1

        for chunk in text_request.iter_content(chunk_size=8192):
            if is_valid_utf8(chunk):
                stripped_chunk = strip_headers(chunk)
                chunks[idx] = stripped_chunk
            else:
                print(f"Chunk {idx} invalid")
                bad_chunks[idx] = chunk
                bad_idx.append(idx)
            idx += 1
        # ipdb.set_trace()
        if bad_chunks and len(bad_chunks) % 2 == 0:
            countdown = len(bad_idx)
            idx = 0
            while countdown:
                bad_chunks[bad_idx[idx]] = str(
                    bad_chunks[bad_idx[idx]] + bad_chunks[bad_idx[idx + 1]]
                )
                del bad_chunks[bad_idx[idx + 1]]
                countdown -= 2
                idx += 2
            chunks = chunks | bad_chunks
        elif bad_chunks:
            raise Exception("Bad book data :(")

        for key in range(1, idx):
            if chunks.get(key):
                file.write(chunks[key].encode("utf-8"))

    return file_path


# write_text_to_file("https://gutenberg.org/cache/epub/84/pg84.txt", "./test.txt")


# def write_text_to_book(url):
#     text_request = requests.get(url, stream=True)

#     if text_request.status_code != 200:
#         raise Exception("Book not found...")

#     chunks = {}
#     bad_chunks = {}
#     bad_idx = []
#     bad_flag = False
#     idx = 1

#     for chunk in text_request.iter_content(chunk_size=8192):
#         if is_valid_utf8(chunk):
#             stripped_chunk = strip_headers(chunk)
#             chunks[idx] = stripped_chunk
#         else:
#             if not bad_flag:
#                 print("Bad chunks detected.")
#                 bad_flag = True
#             bad_chunks[idx] = chunk
#             bad_idx.append(idx)
#         idx += 1
#     # ipdb.set_trace()
#     if bad_chunks and len(bad_chunks) % 2 == 0:
#         print("Attempting bad chunk repair.")
#         countdown = len(bad_idx)
#         idx = 0
#         while countdown:
#             bad_chunks[bad_idx[idx]] = str(bad_chunks[bad_idx[idx]] + bad_chunks[bad_idx[idx + 1]])
#             del bad_chunks[bad_idx[idx + 1]]
#             countdown -= 2
#             idx += 2
#         chunks = chunks | bad_chunks
#     elif bad_chunks:
#         print("Chunks irreparable. The text may contain gaps.")

#     return chunks

# def write_text_to_book(url):
#     # Check the content-type first
#     headers = requests.head(url).headers
#     # if 'Content-Type' not in headers:
#         # raise Exception("No Content-Type header found.")
#     # elif 'text/plain' not in headers['Content-Type']:
#         # raise Exception(f"Unexpected Content-Type: {headers['Content-Type']}")

#     text_request = requests.get(url, stream=True)

#     if text_request.status_code != 200:
#         raise Exception("Book not found...")

#     chunks = {}
#     idx = 0

#     for chunk in text_request.iter_content(chunk_size=8192):
#         stripped_chunk = strip_headers(chunk)
        
#         # Try to decode each chunk individually and skip over any bytes that fail.
#         valid_chars = ''
#         for char in stripped_chunk.encode('utf-8', errors='replace'):
#             if ord(char) < 65536:
#                 valid_chars += char
        
#         chunks[idx] = valid_chars
#         idx += 1
#     ipdb.set_trace()
#     return chunks

def write_text_to_book(url):
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise Exception("Book not found...")

    chunks = []
    bad_chunks = []

    for chunk in response.iter_content(chunk_size=8192):
        stripped_chunk = strip_headers(chunk)
        
        # Try to combine consecutive bad chunks
        while not is_valid_utf8(stripped_chunk) and len(bad_chunks) > 0:
            prev_bad_chunk = bad_chunks.pop()
            combined_chunk = str(prev_bad_chunk + stripped_chunk)
            
            if is_valid_utf8(combined_chunk):
                stripped_chunk = combined_chunk
                break
            
            bad_chunks.append(stripped_chunk)
            continue
        
        if is_valid_utf8(stripped_chunk):
            chunks.append(stripped_chunk)
        else:
            bad_chunks.append(stripped_chunk)

    if len(bad_chunks) > 0:
        print("Chunks irreparable. The text may contain gaps.")
    
    return ''.join(chunks)

write_text_to_book("https://www.gutenberg.org/ebooks/100.txt.utf-8")