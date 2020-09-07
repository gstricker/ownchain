# Example of PNG Coin validation
validate_PNG("./images/alice.png")

# Create PNGCoin
my_coin = PNGCoin([
    Image.open("./images/alice.png"),
    Image.open("./images/alice-to-bob.png")])
my_coin.transfers[1].show()
