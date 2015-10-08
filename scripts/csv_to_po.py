import sys, click, re, csv

def clean_str(s):
    return s.strip().replace('\n', '').replace('"', '')

def get_all_english(popath):
    all_english = []
    with open(popath, "r") as pofile:
        contents = pofile.read()
        all_trans = re.split('\n\s*\n', contents)
        eng_regex = re.compile('msgid "(.*)msgstr', re.DOTALL)
        all_english = [eng_regex.findall(trans, re.DOTALL) for trans in all_trans]
        all_english = [clean_str(t[0]) for t in all_english if t]
    return all_english    

def write_new_trans(english, foreign, popath):
    with open(popath, "r") as pofile:
        for line in pofile:
            if english in line:
                raw_input(line)

@click.command()
@click.argument('popath', type=click.Path(exists=True))
@click.argument('csvfile', type=click.File())
def write_po(popath, csvfile):
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    csvreader.next()
    
    for row in csvreader:
        (english, foreign) = row
        if english:
            all_english = get_all_english(popath)
            if english in all_english:
                write_new_trans(english, foreign, popath)

if __name__ == '__main__':
    write_po()
