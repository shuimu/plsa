import plsa

a = plsa.PLSA(4, "sample1", 5000)
a.load_data()
a.init_model()
a.run_model()
a.print_model()
