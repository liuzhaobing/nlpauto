#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
from sklearn.cluster import DBSCAN


class VectorCluster:

    @staticmethod
    def run(vectors, distance=0.2, min_samples=3):
        vectors = np.array(vectors)
        db = DBSCAN(eps=distance, min_samples=min_samples, metric="cosine")
        result = db.fit_predict(vectors)
        cluster = {}
        for i, c in enumerate(result):
            if c == -1:
                continue
            c = str(c)
            if c not in cluster:
                cluster[c] = []
            cluster[c].append(i)
        return cluster
