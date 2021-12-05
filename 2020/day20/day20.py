from math import prod
import re
import networkx as nx
from tiles import sample, tiles_and_ids


class Tile(dict):
    ID: int
    up: str
    down: str
    left: str
    right: str
    img: str
    poss_up: set = set()
    poss_down: set = set()
    poss_left: set = set()
    poss_right: set = set()

    @staticmethod
    def build(s):
        s = s.split("\n")
        id_out = int(re.search(" (.*):", s[0]).group(1))
        up_out = s[1]
        down_out = s[-1]
        left_out = ""
        right_out = ""
        img_out = ""

        for row in s[1:]:
            left_out += row[0]
            img_out += row[1:-1] + "\n"
            right_out += row[-1]

        img_out = img_out.strip()
        img_out = img_out[img_out.find("\n") + 1 : img_out.rfind("\n")]

        final = {
            "ID": id_out,
            "up": up_out,
            "down": down_out,
            "left": left_out,
            "right": right_out,
            "img": img_out,
        }
        return Tile(final)

    @property
    def all_possible(self):
        possible = set()
        for s in [self["up"], self["down"], self["left"], self["right"]]:
            possible.add(s)
            possible.add(s[::-1])
        return possible

    @property
    def up_right(self):
        if (len(self["poss_up"]) == 0) & (len(self["poss_right"]) == 0):
            return True
        return False

    @property
    def up_left(self):
        if (len(self["poss_up"]) == 0) & (len(self["poss_left"]) == 0):
            return True
        return False

    @property
    def down_right(self):
        if (len(self["poss_down"]) == 0) & (len(self["poss_right"]) == 0):
            return True
        return False

    @property
    def down_left(self):
        if (len(self["poss_down"]) == 0) & (len(self["poss_left"]) == 0):
            return True
        return False

    @property
    def is_corner(self):
        if any([self.up_right, self.up_left, self.down_right, self.down_left]):
            return True
        return False

    def rotate(self):
        """Rotate 90 degrees anti-clockwise
        text rotation: https://stackoverflow.com/a/60263655/14083170
        """
        up_backup = self["up"]
        self["up"] = self["left"]
        self["left"] = self["down"]
        self["down"] = self["right"]
        self["right"] = up_backup

        poss_up_backup = self["poss_up"]
        self["poss_up"] = self["poss_left"]
        self["poss_left"] = self["poss_down"]
        self["poss_down"] = self["poss_right"]
        self["poss_right"] = poss_up_backup

        figure = self["img"].split("\n")
        rotated = list(zip(*reversed(figure)))
        rotated = "\n".join("".join(c for c in row) for row in rotated)
        self["img"] = rotated
        return

    def connect(self, other):
        """Change orientation of <self> until it matches with <other>."""
        other_search_space = ["poss_up", "poss_down", "poss_right", "poss_left"]
        for way in other_search_space:
            if self["ID"] in other[way]:
                target_dir = way[5:]

        self_to_other = {"up": "down", "down": "up", "right": "left", "left": "right"}

        other_dir = self_to_other[target_dir]
        n_times = 0
        while self[target_dir] != other[other_dir]:
            self.rotate()

            n_times += 1
            if n_times > 12:
                print("FAILED: Too many rotations.")
                raise AttributeError("Infinite Loop Avoided.")
        return


class SeaMonsterMap(dict):
    tiles: list
    stable: set = set()

    @staticmethod
    def build(data):
        return SeaMonsterMap({"tiles": [Tile.build(s) for s in data.split("\n\n")]})

    def link_neighbors(self):
        tiles = self["tiles"]

        for tile in tiles:
            other_tiles = tiles.copy()
            other_tiles.remove(tile)
            tile["poss_up"] = set(
                [t["ID"] for t in other_tiles if tile["down"] in t.all_possible]
            )
            tile["poss_down"] = set(
                [t["ID"] for t in other_tiles if tile["up"] in t.all_possible]
            )
            tile["poss_left"] = set(
                [t["ID"] for t in other_tiles if tile["left"] in t.all_possible]
            )
            tile["poss_right"] = set(
                [t["ID"] for t in other_tiles if tile["right"] in t.all_possible]
            )

        self["tiles"] = tiles
        return

    @property
    def graph(self):
        tiles = self["tiles"]

        edges = set()
        for tile in tiles:
            neighbors = set()
            for direction in ["poss_up", "poss_down", "poss_left", "poss_right"]:
                neighbors = neighbors | set(
                    [(tile["ID"], other) for other in tile[direction]]
                )
            edges = edges | neighbors
        G = nx.Graph()
        G.add_edges_from(edges)
        return G

    @property
    def corners(self):
        """Build a dictionary {"UR": Tile, "UL": Tile, "DR": Tile, "DL": Tile}"""
        self.link_neighbors()

        raw_corners = [t for t in self["tiles"] if t.is_corner]

        corner_goals = {
            "UR": lambda t: t.up_right,
            "UL": lambda t: t.up_left,
            "DR": lambda t: t.down_right,
            "DL": lambda t: t.down_left,
        }
        corners = {}

        for orientation, tile in zip(corner_goals, raw_corners):

            current_orientation = [
                lbl for lbl, f in corner_goals.items() if f(tile) == True
            ][0]
            while current_orientation != orientation:
                tile.rotate()
                current_orientation = [
                    lbl for lbl, f in corner_goals.items() if f(tile) == True
                ][0]
            corners[orientation] = tile
        return corners

    @property
    def product_of_corners(self):
        corners = self.corners.values()
        return prod([t["ID"] for t in corners])

    def get(self, tile_id):
        return [t for t in self["tiles"] if t["ID"] == tile_id][0]

    def fill_one_layer(self):
        for stable in self.stable:
            for neighbor in self.graph.neighbors(stable):
                if neighbor not in self.stable:
                    self.get(neighbor).connect(self.get(stable))
                    self.stable.add(neighbor)
                    print(f"{neighbor} added. Now at {len(self.stable)}")
        return

    def fill_interior(self):
        """Rotate all tiles until they fit into the puzzle."""
        self.stable = self.stable | set([t["ID"] for t in self.corners.values()])

        while len(self.stable) < len(self["tiles"]):
            self.fill_one_layer()
        return


m = SeaMonsterMap.build(sample)
m.fill_interior()

# pred = m.product_of_corners
# assert pred == 20899048083289
# print("Test Passed.")


# if __name__ == "__main__":
#     m = SeaMonsterMap.build(tiles_and_ids)
#     print(m.product_of_corners)
