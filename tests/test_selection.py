from treefy.core.selection import Node, SelectionManager


def create_simple_tree(tmp_path):
    # Structure : root/
    #             ├── dir1/
    #             │   └── file1
    #             └── file2
    root = Node(tmp_path)
    dir1_path = tmp_path / "dir1"
    file1_path = dir1_path / "file1"
    file2_path = tmp_path / "file2"
    dir1_path.mkdir()
    file1_path.touch()
    file2_path.touch()

    dir1 = Node(dir1_path, root)
    file1 = Node(file1_path, dir1)
    file2 = Node(file2_path, root)

    root.add_child(dir1)
    root.add_child(file2)
    dir1.add_child(file1)

    return root, dir1, file1, file2


def test_exclude_file_excludes_it_only(tmp_path):
    root, dir1, file1, file2 = create_simple_tree(tmp_path)
    manager = SelectionManager(root)

    manager.exclude(file2)

    assert not manager.is_included(file2)
    assert manager.is_included(root)
    assert manager.is_included(dir1)


def test_exclude_directory_excludes_descendants(tmp_path):
    root, dir1, file1, file2 = create_simple_tree(tmp_path)
    manager = SelectionManager(root)

    manager.exclude(dir1)

    assert not manager.is_included(dir1)
    assert not manager.is_included(file1)
    assert manager.is_included(file2)
    assert manager.is_included(root)


def test_exclude_all_children_excludes_parent(tmp_path):
    root, dir1, file1, file2 = create_simple_tree(tmp_path)
    manager = SelectionManager(root)

    manager.exclude(file2)
    manager.exclude(dir1)
    manager.exclude(file1)

    assert not manager.is_included(file2)
    assert not manager.is_included(file1)
    assert not manager.is_included(dir1)
    assert not manager.is_included(root)


def test_include_restores_ancestors_and_descendants(tmp_path):
    root, dir1, file1, file2 = create_simple_tree(tmp_path)
    manager = SelectionManager(root)

    manager.exclude(dir1)
    manager.include(file1)

    assert manager.is_included(file1)
    assert manager.is_included(dir1)
    assert manager.is_included(root)


def test_toggle_behavior(tmp_path):
    root, dir1, file1, file2 = create_simple_tree(tmp_path)
    manager = SelectionManager(root)

    # Initially all included
    assert manager.is_included(file2)
    manager.toggle(file2)
    assert not manager.is_included(file2)
    manager.toggle(file2)
    assert manager.is_included(file2)


def test_get_excluded_list(tmp_path):
    root, dir1, file1, file2 = create_simple_tree(tmp_path)
    manager = SelectionManager(root)

    manager.exclude(file2)
    excluded = manager.get_excluded()
    assert file2 in excluded
