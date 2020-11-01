

class MulDivTree:
    MAX_DEPTH = 40
    minimum_map = {}

    def __init__(self, parent=None, data=1, depth=0):
        self.data = data
        self.depth = depth
        self.mul_2 = None
        self.div_3 = None
        self.parent = parent

        if self.data not in MulDivTree.minimum_map.keys():
            MulDivTree.minimum_map[self.data] = self.depth
        else:
            MulDivTree.minimum_map[self.data] = min(MulDivTree.minimum_map[self.data], self.depth)

        if self.depth < self.MAX_DEPTH:
            # ignore if a better match is already known
            if not (self.data * 2 in MulDivTree.minimum_map.keys() and self.depth+1 >= MulDivTree.minimum_map[self.data * 2]):
                self.mul_2 = MulDivTree(parent=self, data=self.data * 2, depth=self.depth+1)           
            if not (self.data // 3 in MulDivTree.minimum_map.keys() and self.depth+1 >= MulDivTree.minimum_map[self.data // 3]):
                self.div_3 = MulDivTree(parent=self, data=self.data // 3, depth=self.depth+1)


if __name__ == '__main__':
    tree = MulDivTree()
    print(tree.minimum_map[3012])
