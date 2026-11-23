#!/usr/bin/env python3
"""生成 source/apps.json（可作为「手动导入的源包」）。

用法：
  python3 tools/gen-source.py --owner <GitHub 用户名> --repo <仓库名> \
      --version 8.2.0 --build 8200 --ipa ~/Desktop/无忧签_8.2.0_未签名.ipa

生成规则：
- bundleIdentifier 用**实际分发 ipa 里的值**（com.wuyouqian.WuyouSign），
  不能写工程里的 Team 后缀版，否则客户端会把同一个应用当成另一个。
- downloadURL 指向该仓库的 Release 附件，必须是完整 https 地址——
  手动导入的源包不带 ipa，相对路径装不上。
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

DEFAULT_BUNDLE_ID = "com.wuyouqian.WuyouSign"


def ipa_info(path):
    """读 ipa 里的 CFBundleIdentifier / 版本 / build，读不到就报错而不是猜。"""
    try:
        out = subprocess.check_output(
            ["unzip", "-p", path, "Payload/WuyouSign.app/Info.plist"], stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        sys.exit("读不到 ipa 里的 Payload/WuyouSign.app/Info.plist")
    import plistlib

    plist = plistlib.loads(out)
    return (
        plist.get("CFBundleIdentifier", DEFAULT_BUNDLE_ID),
        plist.get("CFBundleShortVersionString", ""),
        str(plist.get("CFBundleVersion", "")),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--build", required=True)
    ap.add_argument("--ipa", required=True)
    ap.add_argument("--out", default="source/apps.json")
    args = ap.parse_args()

    size = os.path.getsize(os.path.expanduser(args.ipa))
    bundle_id, ipa_version, ipa_build = ipa_info(os.path.expanduser(args.ipa))
    if ipa_version and ipa_version != args.version:
        sys.exit(f"版本不一致：ipa 里是 {ipa_version}，参数是 {args.version}")
    if ipa_build and ipa_build != args.build:
        sys.exit(f"build 不一致：ipa 里是 {ipa_build}，参数是 {args.build}")

    tag = f"v{args.version}"
    asset = f"WuyouSign_{args.version}.ipa"
    download = f"https://github.com/{args.owner}/{args.repo}/releases/download/{tag}/{asset}"
    site = f"https://github.com/{args.owner}/{args.repo}"

    payload = {
        "name": "无忧签官方源",
        "identifier": "top.wuyouqian.official",
        "subtitle": "无忧签官方发布",
        "description": "无忧签自己的应用源：这里只放官方构建。安装包用你自己的 Apple ID 重签，7 天后需要回来续一次。",
        "iconURL": f"{site}/raw/main/source/icon.png",
        "website": site,
        "tintColor": "#1F6FEB",
        "featuredApps": [bundle_id],
        "apps": [
            {
                "name": "无忧签",
                "bundleIdentifier": bundle_id,
                "developerName": "无忧签",
                "subtitle": "用免费 Apple ID 给 iPhone 装应用，不用电脑",
                "localizedDescription": "免电脑配对、连接通道自检、免费证书签名与续签。iOS 16 及更早需要电脑导出一次配对文件。",
                "iconURL": f"{site}/raw/main/source/icon.png",
                "tintColor": "#1F6FEB",
                "category": "utilities",
                "version": args.version,
                "versionDate": datetime.now().astimezone().isoformat(timespec="seconds"),
                "versionDescription": "修复续签匹配不到应用、续签失败静默、iOS 16 免电脑配对白等 150 秒、断连被误报成 VPN 异常；新增手动导入源包。",
                "downloadURL": download,
                "size": size,
                "minOSVersion": "15.0",
                "wuyouqian": {
                    "build": int(args.build),
                    "channel": "stable",
                    "note": "签名到期时间由客户端从装好的描述文件里读，不在这里写死。",
                },
            }
        ],
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"写好 {args.out}")
    print(f"  bundleId  {bundle_id}")
    print(f"  download  {download}")
    print(f"  size      {size}")


if __name__ == "__main__":
    main()
