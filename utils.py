def create_tree(nodes=[], parent_id=None, config={}):
    '''
        nodes       - List of flat nodes to be converted into the tree
        parentId    - Parent node id to collect children
        config      - Dict with the keys to dynamically construct the tree
    '''
    return list([{**i, config["children_path"]: create_tree(nodes, i[config["key"]], config)} for i in nodes if
                 i[config["parentKey"]] == parent_id])