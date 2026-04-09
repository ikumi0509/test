from memo_visualize import build_vis_nodes, build_vis_edges, generate_html, TYPE_COLORS


SAMPLE_MEMOS = [
    {
        "id": "aaa11111",
        "title": "Pythonを学んだ",
        "content": "デコレータの仕組みを理解した",
        "type": "learned",
        "tags": ["python", "decorators"],
        "date": "2026-04-09",
    },
    {
        "id": "bbb22222",
        "title": "テストを書きたい",
        "content": "pytestでTDDを試す",
        "type": "todo",
        "tags": ["python", "testing"],
        "date": "2026-04-09",
    },
    {
        "id": "ccc33333",
        "title": "今日の振り返り",
        "content": "いろいろ学べた",
        "type": "reflection",
        "tags": ["daily"],
        "date": "2026-04-09",
    },
]


# --- build_vis_nodes ---
def test_build_vis_nodes_colors():
    nodes = build_vis_nodes(SAMPLE_MEMOS)
    for node, memo in zip(nodes, SAMPLE_MEMOS):
        expected_color = TYPE_COLORS[memo["type"]]
        assert node["color"]["background"] == expected_color


def test_build_vis_nodes_label_includes_tags():
    nodes = build_vis_nodes(SAMPLE_MEMOS)
    assert "#python" in nodes[0]["label"]
    assert "#decorators" in nodes[0]["label"]


def test_build_vis_nodes_ids_match():
    nodes = build_vis_nodes(SAMPLE_MEMOS)
    for node, memo in zip(nodes, SAMPLE_MEMOS):
        assert node["id"] == memo["id"]


# --- build_vis_edges ---
def test_build_vis_edges_format():
    raw_edges = [("aaa11111", "bbb22222", "python")]
    edges = build_vis_edges(raw_edges)
    assert len(edges) == 1
    assert edges[0]["from"] == "aaa11111"
    assert edges[0]["to"] == "bbb22222"
    assert edges[0]["label"] == "python"


# --- generate_html ---
def test_generate_html_creates_file(tmp_path):
    output = tmp_path / "test_graph.html"
    generate_html(SAMPLE_MEMOS, output)
    assert output.exists()


def test_generate_html_contains_vis_js_cdn(tmp_path):
    output = tmp_path / "test_graph.html"
    generate_html(SAMPLE_MEMOS, output)
    html = output.read_text(encoding="utf-8")
    assert "vis-network" in html


def test_generate_html_contains_memo_data(tmp_path):
    output = tmp_path / "test_graph.html"
    generate_html(SAMPLE_MEMOS, output)
    html = output.read_text(encoding="utf-8")
    assert "Pythonを学んだ" in html
    assert "aaa11111" in html


def test_generate_html_contains_legend(tmp_path):
    output = tmp_path / "test_graph.html"
    generate_html(SAMPLE_MEMOS, output)
    html = output.read_text(encoding="utf-8")
    assert "Learned" in html
    assert "Todo" in html
    assert "Reflection" in html


def test_generate_html_empty_memos(tmp_path):
    output = tmp_path / "test_graph.html"
    generate_html([], output)
    assert output.exists()
    html = output.read_text(encoding="utf-8")
    assert "0 memos" in html
