import feedforwardNN

if __name__ == '__main__':
    fnn = feedforwardNN.FNN()
    fnn.load_sets("train-images", True)
    fnn.load_sets("test-images", False)
    fnn.train()
    predictions = fnn.predict(-1, "test-images")
