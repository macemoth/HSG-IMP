import subprocess
import datetime
from time import sleep

import networkx as nx
import json

class Graphene():

    def __init__(self):
        self.triples = set()
        self.addQueue = set()


    def run(self):
        while(True):
            self.update()
            sleep(1)



    def update(self):
        # Get image
        # TODO

        # Check whether image content has changed significantly
        # TODO
        change = False

        if not change:
            return

        graph_path = "graph.json"
        self.generate_scene_graph()
        new_triples, dropped_triples = self.read_triples_diff(graph_path)
        # TODO: make better output
        for drop in dropped_triples:
            print(f"{drop.object} {drop.predicate} {drop.subject} has dropped out." )

        for new in new_triples:
            print(f"{new.object} {new.predicate} {new.subject} has popped up.")
            self.addQueue.add(new)


    def fetch_image(self):
        pass

    def fetch_image_mock(self):
        if datetime.now().second < 15:
            return "image 1"
        elif datetime.now().second < 30:
            return "image 2"
        elif datetime.now().second < 45:
            return "image 3"
        else: return "image 4"

    def generate_scene_graph(self, reltr_path, img_path, graph_path, device="cpu"):
        subprocess.check_output([f'python',
                                 f"{reltr_path}/mkgraph.py",
                                 "--img_path", f"{img_path}",
                                 "--device", f"{device}",
                                 "--resume", f"{reltr_path}/ckpt/checkpoint0149.pth",
                                 "--export_path", f"{graph_path}"])

    def read_triples_diff(self, graph_path):
        """
        Complete import of a graph.
        """
        triple_dict = None
        triples_read = set()
        with open(graph_path, "r") as file:
            triples = json.load(file)
            file.close()

        for triple_dict in triple_dict:
            subject = triple_dict["subject"]
            relation = triple_dict["relation"]
            object = triple_dict["object"]
            triple = Triple(subject["id"], relation["id"], object["id"])
            triple.setSubjectBox(subject["xmin"], subject["ymin"], subject["xmax"], subject["ymax"])
            triple.setObjectBox(object["xmin"], object["ymin"], object["xmax"], object["ymax"])
            triples_read.add(triple)

        new_triples = triples_read - self.triples
        dropped_triples = self.triples - triples_read

        return new_triples, dropped_triples

    def visualise(self):
        g = nx.Graph()


class Triple():

    def __init__(self, subject, predicate, object):
        self.subject = subject
        self.predicate = predicate
        self.object = object

    def __hash__(self):
        """Should only check on S, P, O, but not other variables"""
        return hash((self.subject, self.predicate, self.object))

    def setObjectBox(self, oxmin, oymin, oxmax, oymax):
        self.obox = (oxmin, oymin, oxmax, oymax)

    def setSubjectBox(self, sxmin, symin, sxmax, symax):
        self.obox = (sxmin, symin, sxmax, symax)

