from project import PNGcoin as pg
from PIL import Image
import pickle

# Create PNGCoin
my_coin = pg.PNGCoin([
    Image.open("./images/alice.png"),
    Image.open("./images/alice-to-bob.png")])

# Check that it works
my_coin.transfers[1].show()

# Test coin validation
pg.validate(my_coin)

# Check serialization
filename = "./bob.pngcoin"
pg.to_disk(my_coin, filename)
my_coin_2 = pg.from_disk(filename)
my_coin.transfers == my_coin_2.transfers
