import sys
import itertools
import hashlib
import random
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine
import models







def process_file(fn, parser):
    global INSERTED_ROWS
    with open(fn) as fh:
        blob = json.load(fh)
        inserts = parser(blob)
        for insert in inserts:
            signature = (insert.table, insert.key)
            if signature not in INSERTED_ROWS:
                yield insert.text
                INSERTED_ROWS.add(signature)

def process_tree(fn, parser=models.Artist.parse):
    for (dirpath, dirnames, filenames) in os.walk(fn):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            for insert in process_file(full, parser):
                yield insert


def gen_data(fh, root='/Volumes/source/hacking/collection'):
    artists_path = os.path.join(root, 'artists')
    fh.writelines(process_tree(artists_path, models.Artist.parse))

    artworks_path = os.path.join(root, 'artworks')
    fh.writelines(process_tree(artworks_path, models.Work.parse))


def gen_schema(fh):
    metadata = models.db.metadata
    def dump(sql, *multiparams, **params):
        print(sql.compile(dialect=engine.dialect), file=fh)
    engine = create_engine('postgresql://', strategy='mock', executor=dump)
    metadata.create_all(engine, checkfirst=False)

    for tname in models.db.metadata.tables:
        print("ALTER TABLE {} OWNER TO {{{{ node['wreck']['db_user'] }}}};".format(tname), file=fh)


def generate(schema="sql/schema.sql", data="sql/data.sql"):
    with open(schema, 'w') as fh:
        gen_schema(fh)

    with open(data, 'w') as fh:
        gen_data(fh)

if __name__ == "__main__":
    generate()
