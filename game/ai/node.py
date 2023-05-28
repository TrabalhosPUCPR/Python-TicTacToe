class Node:
    def __init__(self, data, data_score=0.0):
        self.data = data
        self.data_score = data_score
        self.children = []

    def __lt__(self, other):
        return self.data_score < other.data_score

    def __le__(self, other):
        return self.data_score <= other.data_score

    def __gt__(self, other):
        return self.data_score > other.data_score

    def __ge__(self, other):
        return self.data_score >= other.data_score

    def is_terminal(self):
        return len(self.children) == 0
