import pytest
from memo_data import (
    create_memo,
    load_memos,
    save_memos,
    add_memo,
    get_all_tags,
    find_memos_by_tag,
    build_edges,
)


# --- create_memo ---
def test_create_memo_valid():
    memo = create_memo("テスト", "内容", "learned", ["python"])
    assert memo["title"] == "テスト"
    assert memo["content"] == "内容"
    assert memo["type"] == "learned"
    assert memo["tags"] == ["python"]
    assert len(memo["id"]) == 8
    assert memo["date"]  # 今日の日付が入る


def test_create_memo_custom_date():
    memo = create_memo("テスト", "内容", "todo", ["test"], "2026-04-01")
    assert memo["date"] == "2026-04-01"


def test_create_memo_invalid_type():
    with pytest.raises(ValueError, match="タイプは"):
        create_memo("テスト", "内容", "invalid", ["tag"])


def test_create_memo_empty_title():
    with pytest.raises(ValueError, match="タイトルは必須"):
        create_memo("", "内容", "learned", ["tag"])


def test_create_memo_empty_tags():
    with pytest.raises(ValueError, match="タグは1つ以上"):
        create_memo("テスト", "内容", "learned", [])


# --- load / save ---
def test_load_nonexistent_file(tmp_path):
    result = load_memos(tmp_path / "nonexistent.json")
    assert result == []


def test_save_and_load_round_trip(tmp_path):
    filepath = tmp_path / "memos.json"
    memo = create_memo("テスト", "内容", "learned", ["python"])
    save_memos([memo], filepath)
    loaded = load_memos(filepath)
    assert len(loaded) == 1
    assert loaded[0]["title"] == "テスト"


# --- add_memo ---
def test_add_memo_appends(tmp_path):
    filepath = tmp_path / "memos.json"
    m1 = create_memo("メモ1", "内容1", "learned", ["python"])
    m2 = create_memo("メモ2", "内容2", "todo", ["github"])
    add_memo(m1, filepath)
    add_memo(m2, filepath)
    loaded = load_memos(filepath)
    assert len(loaded) == 2


# --- build_edges ---
def test_build_edges_shared_tag():
    memos = [
        {"id": "aaa", "tags": ["python"]},
        {"id": "bbb", "tags": ["python"]},
    ]
    edges = build_edges(memos)
    assert len(edges) == 1
    assert "python" in edges[0][2]


def test_build_edges_no_shared_tags():
    memos = [
        {"id": "aaa", "tags": ["python"]},
        {"id": "bbb", "tags": ["rust"]},
    ]
    edges = build_edges(memos)
    assert len(edges) == 0


def test_build_edges_multiple_shared_tags():
    memos = [
        {"id": "aaa", "tags": ["python", "test"]},
        {"id": "bbb", "tags": ["python", "test"]},
    ]
    edges = build_edges(memos)
    assert len(edges) == 1
    assert "python" in edges[0][2]
    assert "test" in edges[0][2]


def test_build_edges_three_memos_triangle():
    memos = [
        {"id": "aaa", "tags": ["python"]},
        {"id": "bbb", "tags": ["python"]},
        {"id": "ccc", "tags": ["python"]},
    ]
    edges = build_edges(memos)
    assert len(edges) == 3


# --- get_all_tags ---
def test_get_all_tags():
    memos = [
        {"tags": ["python", "test"]},
        {"tags": ["github", "python"]},
    ]
    assert get_all_tags(memos) == {"python", "test", "github"}


# --- find_memos_by_tag ---
def test_find_memos_by_tag_filters_correctly():
    memos = [
        {"id": "aaa", "tags": ["python"]},
        {"id": "bbb", "tags": ["rust"]},
        {"id": "ccc", "tags": ["python", "rust"]},
    ]
    result = find_memos_by_tag(memos, "python")
    assert len(result) == 2
    ids = [m["id"] for m in result]
    assert "aaa" in ids
    assert "ccc" in ids
