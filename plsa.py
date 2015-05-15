#coding=UTF-8

import random

class PLSA:
    def __init__(self, K, infile, MAX_step):
        self.MINX = 0.000000001  ## avoid divide by 0
        self.Pz_dw = {}
        self.Pw_z = {}
        self.Pz_d = {}
        self.Pw_d = {}
        self.Nd = {}
        self.Ndw = {}
        self.K = K
        self.Sd = set()
        self.Sw = set()
        self.infile = infile
        self.MAX_step = MAX_step

    def init_model(self):
        """ init self.Pz_dw """
        for d_i in self.Sd:
            for w_j in self.Sw:
                for z_k in range(0, self.K):
                    self.Pz_dw.setdefault(d_i, {})
                    self.Pz_dw[d_i].setdefault(w_j, {})
                    self.Pz_dw[d_i][w_j].setdefault(z_k, 0)
                    self.Pz_dw[d_i][w_j][z_k] = random.random()
        """ init self.Pw_z """
        for z_k in range(0, self.K):
            for w_j in self.Sw:
                self.Pw_z.setdefault(z_k, {})
                self.Pw_z[z_k].setdefault(w_j, 0)
                self.Pw_z[z_k][w_j] = random.random()
        """ init self.Pz_d """
        for d_i in self.Sd:
            for z_k in range(0, self.K):
                self.Pz_d.setdefault(d_i, {})
                self.Pz_d[d_i].setdefault(z_k, 0)
                self.Pz_d[d_i][z_k] = random.random()
    
    def load_data(self):
        inFp = open(self.infile, 'r')
        while True:
            line = inFp.readline()
            if not line:
                break
            doc,word = line.strip().split(' ')
            """ update self.Nd """
            self.Nd.setdefault(doc, 0)
            self.Nd[doc] += 1
            """ update self.Ndw """
            self.Ndw.setdefault(doc, {})
            self.Ndw[doc].setdefault(word, 0)
            self.Ndw[doc][word] += 1
            """ update self.Sd """
            self.Sd.add(doc)
            """ update self.Sw """
            self.Sw.add(word)
            """ update self.Ndw again """
            for d_i in self.Sd:
                for w_j in self.Sw:
                    self.Ndw.setdefault(d_i, {})
                    self.Ndw[d_i].setdefault(w_j, 0) 
        inFp.close()

    def E_step(self):
        """ update Pz_dw """
        for d_i in self.Sd:
            for w_j in self.Sw:
                sum = self.MINX
                for z_k in range(0, self.K):
                    sum += self.Pw_z[z_k][w_j] * self.Pz_d[d_i][z_k]
                for z_k in range(0, self.K):
                    self.Pz_dw[d_i][w_j][z_k] = self.Pw_z[z_k][w_j] * self.Pz_d[d_i][z_k] / sum

    def M_step(self):
        """ update Pw_z """
        for z_k in range(self.K):
            sum_dw = self.MINX
            for d_i in self.Sd:
                for w_j in self.Sw:
                    sum_dw += self.Ndw[d_i][w_j] * self.Pz_dw[d_i][w_j][z_k]
            for w_j in self.Sw:
                sum_d = self.MINX
                for d_i in self.Sd:
                    sum_d += self.Ndw[d_i][w_j] * self.Pz_dw[d_i][w_j][z_k]
                self.Pw_z[z_k][w_j] = sum_d / sum_dw
        """ update Pz_d """
        for d_i in self.Sd:
            for z_k in range(0, self.K):
                sum_w = self.MINX
                for w_j in self.Sw:
                    sum_w += self.Ndw[d_i][w_j] * self.Pz_dw[d_i][w_j][z_k]
                self.Pz_d[d_i][z_k] = sum_w / self.Nd[d_i]

    def run_model(self):
        """ run EM """
        for step_i in range(self.MAX_step):
            self.E_step()
            self.M_step()
            print "run step %d success" % step_i

    def get_Pw_d(self):
        """ get Pw_d for output """
        for d_i in self.Sd:
            for w_j in self.Sw:
                sum = 0
                for z_k in range(self.K):
                    sum += self.Pz_d[d_i][z_k] * self.Pw_z[z_k][w_j]
                self.Pw_d.setdefault(d_i, {})
                self.Pw_d[d_i].setdefault(w_j, 0)
                self.Pw_d[d_i][w_j]  = sum
        return self.Pw_d

    def print_model(self):
        print "Pw_z: " 
        print self.Pw_z
        print "Pz_d: "
        print self.Pz_d
        print "Pw_d = Pz_d * Pw_z: "
        print self.get_Pw_d()
        print "Pw_d: "
        for d_i in self.Sd:
            for w_j in self.Sw:
                print "%s\t%s\t%.5f" % (d_i, w_j, self.Pw_d[d_i][w_j])
            print ""
