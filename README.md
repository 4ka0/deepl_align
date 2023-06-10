## DeepL Align

A command line script for translating a docx file using the DeepL API.<br>
The translation is output as a tmx file or as a docx file table with the source and target text segments ***fully aligned***.

### Built using:

* Python 3.10
* python-docx 0.8.11
* deepl 1.9.0
* environs 9.5.0
* pytest 7.1.2

<br>

### Tmx output example:

https://github.com/4ka0/kikai_to_tmx/assets/39420293/86a301c5-a26d-47fa-880f-f849790998cd

<br>

### Docx output example:

https://github.com/4ka0/kikai_to_tmx/assets/39420293/8fb08af7-5962-4c20-8e86-e25a5064b4ac

<br>

### To download and run:

1. Go to the DeepL website and sign up to use the DeepL API.
At the time of writing, it is possible to sign up and use the API to translate up to 500,000 characters a month for free.
You will receive an authentication key. Keep this safe as you will need it later.

Then, using the terminal:

2. Clone this repo.<br>
`git clone https://github.com/4ka0/deepl_align.git`

3. Move into the project folder.<br>
`cd deepl_align`

4. Create and activate a virtual environment.<br>
(Example using venv:)<br>
`python3 -m venv venv`
`source venv/bin/activate`

5. Update pip (package manager).<br>
`python -m pip install --upgrade pip`

6. Install the dependencies.<br>
`python -m pip install -r requirements.txt`

7. In the root directory of the project, create a file called `.env`.<br>
In the `.env` file, write the following line.<br>
`export AUTH_KEY=(your DeepL authentication key)`<br>
Note there should be no space after the equals sign.<br>
And replace "(your DeepL authentication key)" with your actual key

6. Run the script.<br>
To output a docx file:<br>
`python translate docx source-text.docx`<br>
To output a tmx file:<br>
`python translate tmx source-text.docx`<br>
To provide DeepL with a glossary of preferred terms to be used in the translation:<br>
`python translate tmx source-text.docx glossary.txt`<br>
Note that the glossary should be a tab-delimited text file having the following format on each line.<br>
`source-term<tab>target-term`<br>
(Replace `<tab>` with an actual tab character.)
