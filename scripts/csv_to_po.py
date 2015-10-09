# -*- coding: utf-8 -*-
'''
    use:
        python scripts/csv_to_po.py oec/translations/zh_cn/LC_MESSAGES/messages.po path/to/file.csv
'''
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

@click.command()
@click.argument('popath', type=click.Path(exists=True))
@click.argument('csvfile', type=click.File())
def write_po(popath, csvfile):
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    csvreader.next()
    new_trans = {}
    
    for row in csvreader:
        (english, foreign) = row
        if english:
            new_trans[english] = foreign
    
    po_eng_regex = re.compile('msgid "(.*)"')
    new_lines = []
    commented_out = False
    with open(popath, "r") as pofile:
        found = False
        for line in pofile:
            if found:
                comment_char = "#~ " if commented_out else ""
                new_lines.append('{}msgstr "{}"\n'.format(comment_char, found))
                found = False
                continue
            if "msgid " in line:
                commented_out = line[0] == "#"
                eng_txt = filter(None, po_eng_regex.findall(line))
                if eng_txt:
                    eng_txt = eng_txt[0]
                    if eng_txt in new_trans:
                        found = new_trans[eng_txt]
            new_lines.append(line)

    with open(popath, "w") as outputfile:
        outputfile.writelines(new_lines)

if __name__ == '__main__':
    write_po()
