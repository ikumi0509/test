"""学習メモのデータモデル・JSON I/O・エッジ構築"""

import argparse
import json
import uuid
from datetime import date
from itertools import combinations
from pathlib import Path

MEMO_TYPES = ("learned", "todo", "reflection")
DEFAULT_DATA_FILE = Path(__file__).parent / "memos.json"


def create_memo(title, content, memo_type, tags, memo_date=None):
    """メモを作成しバリデーションする。"""
    if not title or not title.strip():
        raise ValueError("タイトルは必須です")
    if memo_type not in MEMO_TYPES:
        raise ValueError(f"タイプは {MEMO_TYPES} のいずれかです")
    if not tags:
        raise ValueError("タグは1つ以上必要です")

    return {
        "id": uuid.uuid4().hex[:8],
        "title": title.strip(),
        "content": content.strip() if content else "",
        "type": memo_type,
        "tags": [t.strip() for t in tags],
        "date": memo_date or date.today().isoformat(),
    }


def load_memos(filepath=DEFAULT_DATA_FILE):
    """JSONファイルからメモを読み込む。ファイルがなければ空リスト。"""
    filepath = Path(filepath)
    if not filepath.exists():
        return []
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("memos", [])


def save_memos(memos, filepath=DEFAULT_DATA_FILE):
    """メモリストをJSONファイルに保存する。"""
    filepath = Path(filepath)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"memos": memos}, f, ensure_ascii=False, indent=2)


def add_memo(memo, filepath=DEFAULT_DATA_FILE):
    """メモを追加してファイルに保存する。"""
    memos = load_memos(filepath)
    memos.append(memo)
    save_memos(memos, filepath)
    return memo


def get_all_tags(memos):
    """全メモからタグの集合を返す。"""
    tags = set()
    for memo in memos:
        tags.update(memo["tags"])
    return tags


def find_memos_by_tag(memos, tag):
    """指定タグを持つメモをフィルタして返す。"""
    return [m for m in memos if tag in m["tags"]]


def build_edges(memos):
    """同じタグを共有するメモペアからエッジを構築する。

    同じペアの複数共有タグは1つのエッジにまとめる。
    Returns: list of (from_id, to_id, shared_tags_label)
    """
    tag_to_ids = {}
    for memo in memos:
        for tag in memo["tags"]:
            tag_to_ids.setdefault(tag, []).append(memo["id"])

    edge_tags = {}
    for tag, ids in tag_to_ids.items():
        if len(ids) < 2:
            continue
        for id1, id2 in combinations(ids, 2):
            key = tuple(sorted((id1, id2)))
            edge_tags.setdefault(key, []).append(tag)

    return [(k[0], k[1], ", ".join(v)) for k, v in edge_tags.items()]


def main(argv=None):
    parser = argparse.ArgumentParser(description="学習メモ管理")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="メモを追加")
    add_p.add_argument("--title", "-t", required=True)
    add_p.add_argument("--content", "-c", default="")
    add_p.add_argument("--type", dest="memo_type", required=True, choices=MEMO_TYPES)
    add_p.add_argument("--tags", nargs="+", required=True)
    add_p.add_argument("--date", "-d", default=None)

    sub.add_parser("list", help="メモ一覧")

    args = parser.parse_args(argv)

    if args.command == "add":
        memo = create_memo(args.title, args.content, args.memo_type, args.tags, args.date)
        add_memo(memo)
        print(f"メモを追加しました: {memo['title']} (id: {memo['id']})")
    elif args.command == "list":
        memos = load_memos()
        if not memos:
            print("メモはありません")
        else:
            for m in memos:
                tags = " ".join(f"#{t}" for t in m["tags"])
                print(f"[{m['date']}] ({m['type']}) {m['title']}  {tags}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
