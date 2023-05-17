## A simple program that converts text into audiobook.

This program converts given text file into mp3-audiobook using Google Translate's or Microsoft Edge's online text-to-speech service.

#### Running the program:

At first convert your f2-book to plain text:

`./fb2_to_txt.py <you_book_path>.fb2`

For example:
`./fb2_to_txt.py Morning\ on\ the\ Wissahiccon.fb2`

You can also create a text file on your own from any other format, such as PDF. However, it is important to remember that the file name should include the author's name, book name, and publication year separated with " - ". If you wish to divide an audiobook into multiple files by chapters, the text file format should be written in the following manner:

>Chapter 1 name.
>
> Chapter 1 content goes here.
> Next part of the first Chapter.
> The end of Chapter one.
>
>===
>Chapter 3 name.
>
> Chapter 2 content goes here.
> Next part of thesecond Chapter.
> The end of Chapter two.
>
>===
>Chapter 3 name.
>
> Chapter 1 content goes here.
> Next part of the third Chapter.
> The end of Chapter three.
>
>===
>,,,

Then run:

`./convert_book.py --book <book_author - book_title - publish_year>.txt --tts gtts`

For example:

`./convert_book.py -b Edgar\ Allan\ Poe\ -\ Morning\ on\ the\ Wissahiccon\ -\ 2023.txt -s edge -g male`
