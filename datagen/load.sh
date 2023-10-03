mkdir -p data/zipped
python datagen/download.py
mkdir data/unzipped
for f in data/zipped/*.tgz; do tar zxvf "$f" -C data/unzipped; done
mkdir data/combined
python datagen/combine.py