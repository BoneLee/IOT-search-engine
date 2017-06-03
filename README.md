# IOT-search-engine
full text search engine for IOT based on influxdb

usage:
    searcher = IotSearcher()

    searcher.index(1, {"name": "bone lee", "age": 23, "cats": "ao da miao and ao er miao", "title": "this is a good title"})
    searcher.index(2, {"name": "jack lee", "age": 33, "cats": "unknown", "title": "hello world, this is from jack"})
    searcher.index(3, {"kaka": "how are you?"})

    searcher.search("lee")
    
    searcher.search("hello lee")
    
    searcher.search("this is a good miao")
    
    searcher.search("cats='da miao'")
    
