# -*- coding: utf-8 -*-
"""ent 分类 7 个占位重复文件删除后，清理 i18n 数据源中的孤儿 key。

待删文件（7 对重复中的占位副本）：
  rater-9 / rater-10 / assessor-6 / assessor-7 / analysis-13 / tester-rater-1 / checker-1
对应的功能主工具保留：lund-kennedy-score / lund-mackay-score / vocal-cord-assessment /
grbas-scale / laryngeal-nerve / tdi-score / fistula-test

清理范围（仅删这 7 个 slug 的 key，不影响主工具）：
  - content_deepdive.json: key = "ent/<slug>"
  - slug-en.json / _en_override.json: key = "ent/<slug>"
  - ent.json / ent-body.json（若存在）: key = 裸 "<slug>"
"""
import json
import os

SLUGS = ["rater-9", "rater-10", "assessor-6", "assessor-7",
         "analysis-13", "tester-rater-1", "checker-1"]
BASE = "i18n/tools/"
FULL = ["content_deepdive.json", "slug-en.json", "_en_override.json"]
BARE = ["ent.json", "ent-body.json"]


def clean(path, keys_to_remove, prefix=""):
    if not os.path.exists(path):
        print(f"  skip(不存在): {path}")
        return 0
    d = json.load(open(path, encoding="utf-8"))
    removed = [k for k in d if k in keys_to_remove]
    for k in removed:
        del d[k]
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  {os.path.basename(path)}: 删除 {len(removed)} 个孤儿 key -> {removed}")
    return len(removed)


def main():
    print("== 清理 i18n 孤儿 key ==")
    full_keys = {"ent/" + s for s in SLUGS}
    for fn in FULL:
        clean(BASE + fn, full_keys)
    bare_keys = set(SLUGS)
    for fn in BARE:
        clean(BASE + fn, bare_keys)


if __name__ == "__main__":
    main()
