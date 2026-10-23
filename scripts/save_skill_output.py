#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def generate_filename() -> str:
    """
    生成文件名，避免覆盖已有文件
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"skill_output_{timestamp}.txt"


def save_content_to_txt(content: str, output_dir=None) -> Path:
    """
    将内容保存为 txt 文件
    """
    if not content or not content.strip():
        raise ValueError("保存内容为空，无法写入文件。")

    save_dir = Path(output_dir) if output_dir is not None else Path.cwd() / "outputs" / "medical-dialog"
    save_dir.mkdir(parents=True, exist_ok=True)

    filename = generate_filename()
    file_path = save_dir / filename

    # 防止极端情况下同一秒生成重名文件
    counter = 1
    while file_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"skill_output_{timestamp}_{counter}.txt"
        file_path = save_dir / filename
        counter += 1

    # 写入 txt 文件，使用 UTF-8 编码
    with file_path.open("x", encoding="utf-8", newline="\n") as f:
        f.write(content)

        if not content.endswith("\n"):
            f.write("\n")

    return file_path.resolve()


def read_content_from_stdin() -> str:
    """
    从标准输入读取内容
    """
    if sys.stdin.isatty():
        raise ValueError("请提供 --input、--content 或通过标准输入传入文本。")
    content = sys.stdin.read()

    if not content or not content.strip():
        raise ValueError("未从标准输入读取到有效内容。")

    return content


def parse_args():
    parser = argparse.ArgumentParser(
        description="将已有 Skill 总结保存为 UTF-8 TXT，支持指定输出目录。"
    )

    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--content",
        type=str,
        default=None,
        help="需要保存的文本内容。如果不传，则从标准输入读取。",
    )

    source.add_argument("--input", type=Path, help="读取已有 UTF-8 文本文件。")
    parser.add_argument("--output-dir", type=Path, help="输出目录，默认当前工作区的 outputs/medical-dialog。")
    return parser.parse_args()


def main():
    try:
        args = parse_args()

        if args.input is not None:
            content = args.input.read_text(encoding="utf-8-sig")
        elif args.content is not None:
            content = args.content
        else:
            content = read_content_from_stdin()

        saved_path = save_content_to_txt(content, args.output_dir)

        result = {
            "success": True,
            "path": str(saved_path),
            "message": "文件已成功保存到本机。",
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    except Exception as e:
        result = {
            "success": False,
            "error": str(e),
        }

        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
