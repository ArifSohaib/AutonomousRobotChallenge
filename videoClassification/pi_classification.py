from classify_images import ClassifyImages

clf = ClassifyImages("./models/retrained_graph.pb", "./models/labels.txt")

clf.predict_on__pi_video()
