import sys, click, re, csv

def clean_str(s):
    return s.strip().replace('\n', '').replace('"', '')

@click.command()
@click.argument('pofile', type=click.File())
@click.option('-l', '--lang', prompt='Language', required=True)
def read_po(pofile, lang):
    all_trans = []
    contents = pofile.read()
    found = re.split('\n\s*\n', contents)
    eng_regex = re.compile('msgid "(.*)msgstr', re.DOTALL)
    foreign_regex = re.compile('msgstr(.*)', re.DOTALL)
    for trans in found[1:]:
        if "msgid_plural" not in trans and "msgctxt" not in trans:

            eng_found = eng_regex.findall(trans)

            if eng_found:
                english_txt = clean_str(eng_found[0])
                for_found = foreign_regex.findall(trans)
                foreign_txt = clean_str(for_found[0])
                all_trans.append([english_txt, foreign_txt])
    
    with open('{}_trans.tsv'.format(lang), 'w') as fp:
        a = csv.writer(fp, delimiter='\t')
        a.writerows(all_trans)

if __name__ == '__main__':
    read_po()
