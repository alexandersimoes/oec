import os, MySQLdb
import urllib
import csv
import flickr
import _flickr_short
import click

FILE_PATH = os.path.join( os.path.dirname(os.path.realpath(__file__)) , '../../dataviva/static/img/profiles/unformatted')
SHORT_URL = u'http://flic.kr/p/%s'

''' Connect to DB '''
db = MySQLdb.connect(host=os.environ.get("DATAVIVA2_DB_HOST", "localhost"),
                     user=os.environ.get("DATAVIVA2_DB_USER", "root"),
                     passwd=os.environ.get("DATAVIVA2_DB_PW", ""),
                     db=os.environ.get("DATAVIVA2_DB_NAME", "dataviva2"))
db.autocommit(1)
cursor = db.cursor()
badImages = []

def process(pid, uid):
    photo = flickr.Photo(pid)
    photo._load_properties()

    if photo._Photo__license in ["0", "7", "8"]:
        print " *** Bad license:", photo._Photo__license
        badImages.append(uid)
        return None

    author = photo._Photo__owner.realname
    if not author:
        author = photo._Photo__owner.username

    url = max(photo.getSizes(), key=lambda item: item["width"])["source"]

    return {"author": author.replace("'", "\\'"), "url": url}

def db_is_old(uid, url, mode):
    q = "SELECT image_link, image_author FROM attrs_{} WHERE image_link=%s AND id=%s;".format(mode)
    cursor.execute(q, [url, uid])
    res = cursor.fetchone()
    return res is None

def download(uid, data, mode):
    # -- todo update database
    img_dir = FILE_PATH + "/" + mode + "/"
    path = img_dir + uid + ".jpg"
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    urllib.urlretrieve(data["url"], path)
    print " *** Image downloaded!", path

def update_db(uid, data, mode):
    q = "UPDATE attrs_{} SET image_link=%s, image_author=%s, palette=NULL WHERE id = %s;".format(mode)
    cursor.execute(q, [data["short_url"], data["author"], uid])
    print " *** Updated DB with data %s" % data

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('-m', '--mode', prompt='Mode', help='bra, hs, cnae, cbo', required=True)
def read_csv(file_path, mode='bra'):
    input_file = csv.DictReader(open(file_path))

    for row in input_file:

        if row["should_use"] and int(row["should_use"]) != 1:
            print "skipping row ... "; continue

        url = row['image_link']
        uid = row['id']
        print "Checking %s image: %s" % (mode, uid)

        if row["image_link"]:
            # -- assumes the url ends in /flickrId. manipulate photolist url to match the form
            if "photolist" in url:
                url = url.split("/in/photolist")[0]
            pid = url.split("/")[-1]
            if "flic.kr" in url:
                short_url = url
            else:
                short_url = SHORT_URL % (_flickr_short.encode(pid),)
            if db_is_old(uid, short_url, mode):
                data = process(pid, uid)
                if data:
                    data['short_url'] = short_url
                    download(uid, data, mode)
                    update_db(uid, data, mode)
            else:
                print " *** No change"
        else:
            q = "SELECT image_link FROM attrs_{} WHERE id=%s;".format(mode)
            cursor.execute(q, [uid])
            res = cursor.fetchone()[0]
            if res:
                q = "UPDATE attrs_{} SET image_link=NULL, image_author=NULL, palette=NULL WHERE id = %s;".format(mode)
                cursor.execute(q, [uid])
                print " *** Removed image from DB"
            else:
                print " *** No change"

    if len(badImages):
        print "Images with incorrect licensing: %s" % (", ".join(badImages))

if __name__ == '__main__':
    read_csv()
