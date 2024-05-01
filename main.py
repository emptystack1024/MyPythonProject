import gensim.downloader

model = gensim.downloader.load("glove-wiki-gigaword-50")

print(model["tower"])
