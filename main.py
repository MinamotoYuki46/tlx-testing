"""
main.py
Entry point untuk menjalankan seluruh regression test TLX TOKI.

Penggunaan:
    python main.py                     # jalankan semua test
    python main.py --tc 01             # jalankan TC-01 saja
    python main.py --tc 17 18 20       # jalankan TC-17, TC-18, TC-20
    python main.py --verbose           # output detail per test
    python main.py --no-headless       # tampilkan browser saat test berjalan
"""

import sys
import os
import argparse
import subprocess


TESTS_DIR = os.path.join(os.path.dirname(__file__), "tests")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Runner regression test TLX TOKI"
    )
    parser.add_argument(
        "--tc",
        nargs="+",
        metavar="N",
        help="Nomor TC yang ingin dijalankan, misal: --tc 01 05 18",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Tampilkan output detail per test case",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Tampilkan browser saat test berjalan (override HEADLESS di .env)",
    )
    return parser.parse_args()


def resolve_test_paths(tc_numbers: list[str] | None) -> list[str]:
    """Kembalikan daftar path file test sesuai nomor TC yang diminta."""
    all_files = sorted(f for f in os.listdir(TESTS_DIR) if f.startswith("test_") and f.endswith(".py"))

    if not tc_numbers:
        return [os.path.join(TESTS_DIR, f) for f in all_files]

    selected = []
    for num in tc_numbers:
        padded = num.zfill(2)
        matches = [f for f in all_files if f.startswith(f"test_{padded}_")]
        if not matches:
            print(f"[WARN] TC-{padded} tidak ditemukan, dilewati.")
        selected.extend(os.path.join(TESTS_DIR, f) for f in matches)

    return selected


def main():
    args = parse_args()

    # Override HEADLESS via env jika --no-headless diberikan
    if args.no_headless:
        os.environ["HEADLESS"] = "false"

    test_paths = resolve_test_paths(args.tc)
    if not test_paths:
        print("Tidak ada test yang cocok untuk dijalankan.")
        sys.exit(1)

    # Tampilkan daftar test yang akan dijalankan
    print("=" * 60)
    print("  TLX TOKI Regression Test Runner")
    print("=" * 60)
    print(f"Menjalankan {len(test_paths)} file test:\n")
    for path in test_paths:
        print(f"  - {os.path.basename(path)}")
    print()

    # Bangun perintah pytest
    cmd = [sys.executable, "-m", "pytest"] + test_paths
    if args.verbose:
        cmd.append("-v")
    cmd += ["--tb=short", "--no-header"]

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
