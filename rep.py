import os
import csv
import math

def load_bigrams(path):
    with open(path, newline='') as f:
        rows = list(csv.reader(f))
    header = rows[0][1:]
    header[0] = ' '  
    table = {}
    for row in rows[1:]:
        if not row: 
            continue
        first = row[0] if row[0] else ' '
        counts = [float(x) if x else 0.0 for x in row[1:]]
        total = sum(counts)
        for ch, c in zip(header, counts):
            prob = (c / total) if total > 0 else 1e-12
            table[(first, ch)] = math.log(max(prob, 1e-12))
    return table

def map_byte(b):
    if b == 32: return ' '
    if 65 <= b <= 90: return chr(b)
    if 97 <= b <= 122: return chr(b - 32)
    return None

def score_text(bs, table):
    chars = [map_byte(b) for b in bs]
    s = 0.0
    for a, b in zip(chars, chars[1:]):
        if a is None or b is None:
            s += math.log(1e-12)
        else:
            s += table.get((a,b), math.log(1e-12))
    return s

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def main():
    with open('source.txt','rb') as f:
        ct = f.read()
    c1, c2 = ct[:1024], ct[1024:]
    x = xor_bytes(c1,c2)
    dbdir = "/project/web-classes/Fall-2025/csci5471/hw1/db/"
    table = load_bigrams('ftable2.csv')
    best = None
    for fn in os.listdir(dbdir):
        with open(os.path.join(dbdir,fn),'rb') as f:
            db = f.read(1024)
        cand1 = xor_bytes(x, db)
        s1 = score_text(cand1, table)
        if best is None or s1 > best[0]:
            best = (s1, db, cand1)
    with open('db.txt','wb') as f:
        f.write(best[1])
    with open('english.txt','wb') as f:
        f.write(best[2])

if __name__ == "__main__":
    main()

