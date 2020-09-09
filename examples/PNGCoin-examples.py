from project import PNGcoin as pg
from PIL import Image

# Create PNGCoin
my_coin = pg.PNGCoin([
    Image.open("./images/alice.png"),
    Image.open("./images/alice-to-bob.png")])

# Check that it works
my_coin.transfers[1].show()

# Test coin validation
my_coin.validate()

# Check serialization
filename = "./bob.pngcoin"
my_coin.to_disk(filename)
my_coin_2 = pg.PNGCoin.from_disk(filename)
my_coin.transfers == my_coin_2.transfers

# Chek visually
my_coin_2.transfers[1].show()
