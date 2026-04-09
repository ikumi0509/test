"""学習メモのネットワークグラフをHTMLで可視化する"""

import json
from pathlib import Path
from string import Template

from memo_data import build_edges, load_memos, DEFAULT_DATA_FILE

TYPE_COLORS = {
    "learned": "#4A90D9",
    "todo": "#27AE60",
    "reflection": "#E67E22",
}

TYPE_LABELS = {
    "learned": "Learned",
    "todo": "Todo",
    "reflection": "Reflection",
}

DEFAULT_OUTPUT = Path(__file__).parent / "memos_graph.html"

HTML_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Learning Memo Graph</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; }
    .header { padding: 16px 24px; background: #16213e; display: flex; align-items: center; gap: 24px; }
    .header h1 { font-size: 20px; font-weight: 600; }
    .legend { display: flex; gap: 16px; }
    .legend-item { display: flex; align-items: center; gap: 6px; font-size: 13px; }
    .legend-dot { width: 12px; height: 12px; border-radius: 50%; }
    #graph { width: 100%; height: 65vh; }
    #detail { padding: 24px; min-height: 20vh; background: #16213e; }
    #detail .placeholder { color: #888; }
    #detail h2 { font-size: 18px; margin-bottom: 8px; }
    #detail .meta { color: #aaa; font-size: 13px; margin-bottom: 12px; }
    #detail .tags span { background: #0f3460; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 6px; }
    #detail .content { margin-top: 12px; white-space: pre-wrap; line-height: 1.6; }
    .stats { margin-left: auto; font-size: 13px; color: #aaa; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Learning Memo Graph</h1>
    <div class="legend">
      <div class="legend-item"><span class="legend-dot" style="background:#4A90D9"></span> Learned</div>
      <div class="legend-item"><span class="legend-dot" style="background:#27AE60"></span> Todo</div>
      <div class="legend-item"><span class="legend-dot" style="background:#E67E22"></span> Reflection</div>
    </div>
    <div class="stats">$stats</div>
  </div>
  <div id="graph"></div>
  <div id="detail">
    <p class="placeholder">Click a node to see its content.</p>
  </div>

  <script>
    var memoData = $memo_data;
    var nodes = new vis.DataSet($nodes_data);
    var edges = new vis.DataSet($edges_data);

    var container = document.getElementById("graph");
    var data = { nodes: nodes, edges: edges };
    var options = {
      nodes: {
        shape: "dot",
        size: 18,
        font: { size: 12, color: "#eee" },
        borderWidth: 2
      },
      edges: {
        font: { size: 9, align: "middle", color: "#888" },
        color: { color: "#444", highlight: "#888" },
        smooth: { type: "continuous" }
      },
      physics: {
        solver: "forceAtlas2Based",
        forceAtlas2Based: { gravitationalConstant: -40, springLength: 120 }
      },
      interaction: { hover: true }
    };

    var network = new vis.Network(container, data, options);

    network.on("click", function(params) {
      var detail = document.getElementById("detail");
      if (params.nodes.length > 0) {
        var id = params.nodes[0];
        var memo = memoData.find(function(m) { return m.id === id; });
        if (memo) {
          var tagsHtml = memo.tags.map(function(t) { return "<span>#" + t + "</span>"; }).join("");
          detail.innerHTML =
            "<h2>" + memo.title + "</h2>" +
            '<div class="meta">' + memo.type + ' | ' + memo.date + '</div>' +
            '<div class="tags">' + tagsHtml + '</div>' +
            '<div class="content">' + memo.content + '</div>';
        }
      } else {
        detail.innerHTML = '<p class="placeholder">Click a node to see its content.</p>';
      }
    });
  </script>
</body>
</html>
""")


def build_vis_nodes(memos):
    """メモリストをvis.jsノード形式に変換する。"""
    nodes = []
    for memo in memos:
        tags_label = " ".join(f"#{t}" for t in memo["tags"])
        nodes.append({
            "id": memo["id"],
            "label": f"{memo['title']}\n{tags_label}",
            "color": {
                "background": TYPE_COLORS.get(memo["type"], "#888"),
                "border": TYPE_COLORS.get(memo["type"], "#888"),
            },
            "title": memo["content"][:100] if memo["content"] else memo["title"],
        })
    return nodes


def build_vis_edges(edges):
    """エッジタプルをvis.jsエッジ形式に変換する。"""
    return [
        {"from": e[0], "to": e[1], "label": e[2]}
        for e in edges
    ]


def generate_html(memos, output_path=DEFAULT_OUTPUT):
    """メモリストからインタラクティブなHTMLグラフを生成する。"""
    edges = build_edges(memos)
    nodes_data = build_vis_nodes(memos)
    edges_data = build_vis_edges(edges)

    stats = f"{len(memos)} memos | {len(edges)} connections"

    html = HTML_TEMPLATE.substitute(
        memo_data=json.dumps(memos, ensure_ascii=False),
        nodes_data=json.dumps(nodes_data, ensure_ascii=False),
        edges_data=json.dumps(edges_data, ensure_ascii=False),
        stats=stats,
    )

    output_path = Path(output_path)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main():
    memos = load_memos()
    if not memos:
        print("メモがありません。先にメモを追加してください。")
        return
    path = generate_html(memos)
    print(f"グラフを生成しました: {path}")


if __name__ == "__main__":
    main()
