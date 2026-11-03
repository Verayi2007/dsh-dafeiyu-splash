"""Push the current git index to GitHub through the REST API.

git push over https://github.com is unreachable from this machine (port 443 blocked),
while api.github.com and codeload.github.com answer fine, so the commit is uploaded
as blobs -> tree -> commit -> ref instead.
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

REPO = "Verayi2007/dsh-dafeiyu-splash"
ROOT = Path(__file__).resolve().parents[1]


def api(method: str, path: str, payload=None):
    cmd = ["gh", "api", "--method", method, f"repos/{REPO}{path}", "--input", "-"]
    data = b"{}" if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    proc = subprocess.run(cmd, input=data, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", "replace"))
        raise SystemExit(f"gh api failed: {method} {path}")
    out = proc.stdout.decode("utf-8", "replace").strip()
    return json.loads(out) if out else {}


def head_sha():
    try:
        return api("GET", "/git/ref/heads/main")["object"]["sha"]
    except SystemExit:
        return None


files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
print(f"{len(files)} files")

head = head_sha()
if head is None:
    # GitHub refuses Git Data API writes on a repository with zero commits, so the
    # first commit is made through the Contents API.
    readme = (ROOT / "README.md").read_bytes()
    seed = api(
        "PUT",
        "/contents/README.md",
        {"message": "docs: README", "content": base64.b64encode(readme).decode("ascii"), "branch": "main"},
    )
    base_sha = seed["commit"]["sha"]
else:
    base_sha = head
    existing = api("GET", "/contents/README.md?ref=main")
    api(
        "PUT",
        "/contents/README.md",
        {
            "message": "docs: README",
            "content": base64.b64encode((ROOT / "README.md").read_bytes()).decode("ascii"),
            "sha": existing["sha"],
            "branch": "main",
        },
    )
    base_sha = api("GET", "/git/ref/heads/main")["object"]["sha"]

base_tree = api("GET", f"/git/commits/{base_sha}")["tree"]["sha"]
print("base", base_sha[:8])

tree = []
for rel in files:
    data = (ROOT / rel).read_bytes()
    blob = api("POST", "/git/blobs", {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
    tree.append({"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    print(f"  blob {rel} ({len(data)} bytes)")

tree_res = api("POST", "/git/trees", {"tree": tree, "base_tree": base_tree})
commit = api(
    "POST",
    "/git/commits",
    {
        "message": "开屏动效：大肥鱼娘从水下浮上来\n\n"
        "- 立绘取自社区二创的 DeepSeek 鲸鱼娘（assets/feiyu.webp，CC BY-NC-SA 4.0）\n"
        "- 上浮（14px 模糊 -> 0）、冷光晕、声呐细环、按 alpha 遮罩的高光斜扫、气泡、字标落款\n"
        "- 3.7s 自动收幕，点击/按键/滚轮可跳过，遵循 prefers-reduced-motion\n"
        "- 一份视觉源码编译出浏览器预览页与 DSH 客户端插件（单文件、零外部请求）\n"
        "- 纯客户端插件：一个 shell.overlay 条目，不注册服务、不加工具、不联网",
        "tree": tree_res["sha"],
        "parents": [base_sha],
    },
)
api("PATCH", "/git/refs/heads/main", {"sha": commit["sha"], "force": True})
print("pushed:", commit["sha"][:8])
