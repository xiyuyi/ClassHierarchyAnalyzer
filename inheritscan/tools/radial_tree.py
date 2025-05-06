from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

import networkx as nx
import numpy as np


def radial_tree_layout(graph: nx.DiGraph, root="root") -> dict:
    def layout_subtree(node):
        if node not in graph:
            return base_spacing
        children = list(graph.successors(node))
        if not children:
            pos[node] = (0.0, 0.0)
            radii[node] = base_spacing
            return base_spacing

        child_radii = []
        for child in children:
            r = layout_subtree(child)
            child_radii.append((child, r))

        n_children = len(child_radii)
        min_r = min(r for _, r in child_radii)
        circumvent = (
            sum([2.5 * r for _, r in child_radii])
            + n_children * min_r
            + 2.5 * min_r
        )

        parent_clearance = circumvent / (2 * np.pi)
        total_angle = 2 * np.pi
        angle_proportions = [
            (2.5 * r + min_r) / circumvent for _, r in child_radii
        ]
        angle_steps = [prop * total_angle for prop in angle_proportions]

        current_angle = 0
        max_r = 0
        for (child, r), angle_step in zip(child_radii, angle_steps):
            distance = max(r, parent_clearance)
            x = distance * np.cos(current_angle)
            y = distance * np.sin(current_angle)
            translate_subtree(child, x, y)
            pos[child] = (x, y)
            current_angle += angle_step
            max_r = max(max_r, distance + r)

        # center parent
        cx = sum(pos[child][0] for child, _ in child_radii) / n_children
        cy = sum(pos[child][1] for child, _ in child_radii) / n_children
        for child, _ in child_radii:
            translate_subtree(child, -cx, -cy)

        pos[node] = (0.0, 0.0)
        radii[node] = max_r
        return max_r

    def translate_subtree(node, dx, dy):
        if node not in pos:
            return
        x, y = pos[node]
        pos[node] = (x + dx, y + dy)
        for child in graph.successors(node):
            translate_subtree(child, dx, dy)

    def rotate_subtree(node, center_x, center_y, angle_rad):
        if node not in pos:
            return
        x, y = pos[node]
        rel_x = x - center_x
        rel_y = y - center_y
        new_rel_x = rel_x * np.cos(angle_rad) - rel_y * np.sin(angle_rad)
        new_rel_y = rel_x * np.sin(angle_rad) + rel_y * np.cos(angle_rad)
        pos[node] = (new_rel_x + center_x, new_rel_y + center_y)
        for child in graph.successors(node):
            rotate_subtree(child, center_x, center_y, angle_rad)

    pos = {}
    radii = {}
    base_spacing = 10

    # 1. Handle multiple roots
    if root in graph:
        root_nodes = [root]
    else:
        root_nodes = [n for n in graph.nodes if graph.in_degree(n) == 0]

    for i, r in enumerate(root_nodes):
        layout_subtree(r)
        translate_subtree(r, 100 * i, 0)  # space them out

    # 2. Handle isolated/unconnected nodes
    unplaced = [n for n in graph.nodes if n not in pos]
    for i, node in enumerate(unplaced):
        angle = 2 * np.pi * i / max(len(unplaced), 1)
        pos[node] = (200 * np.cos(angle), 200 * np.sin(angle))

    return pos
