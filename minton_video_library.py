# -*- coding: utf-8 -*-
r"""
Minton Video Library v1.3.1 | 배드민턴 유튜브 영상 다운로드 및 관리 프로그램
=====================================================================
[프로그램 전체 기능 및 동작 보존 목록]
01. Windows Python 3.12 + PySide6 기반 단일 Python 소스 GUI.
02. 최초 다운로드 루트 기본값 D:\\99.유튜브다운\\minton.youtube; 선택값은 폴더 힌트와 SQLite에 저장.
03. 여러 YouTube 단일 영상/재생목록 URL을 붙여 넣어 다운로드 대기열에 등록.
04. 재생목록 메타데이터를 먼저 확장하고 각 영상을 개별 대기 항목으로 저장.
05. 동시에 1개만 다운로드하는 순차 작업자(QThread)와 개별 다운로드 간 대기 시간.
06. 대기 간격 사용자 변경(기본 20초, 0~3600초), 작업 실행 중에는 설정 고정.
07. 시작/일시정지(현재 영상 완료 후)/재개/즉시중단(.part 이어받기 가능).
08. 실패/중단/완료된 개별 대기 작업 재시도 및 대기목록 제거.
09. yt-dlp + Deno/EJS 사용: --js-runtimes deno --remote-components ejs:npm.
10. 원래 형식 옵션 유지: 1080p 이하 AVC(H.264) 비디오+AAC 오디오 우선,
    --merge-output-format mp4 및 지정된 동일 포맷 우선순위 문자열 그대로 적용.
11. 한국어 수동/자동 자막 다운로드 후 SRT 변환(--write-subs,
    --write-auto-subs, --sub-langs 'ko.*', --convert-subs srt).
12. 채널명 디렉터리 자동 생성, '채널 - 제목 [영상ID] - YYYY-MM-DD.mp4' 저장.
13. yt-dlp --print after_move:filepath로 병합 완료 파일의 실제 경로 확인.
14. 미디어 메타데이터 .info.json 별도 기록(보관 및 향후 자세분석 연동 용도).
15. SQLite WAL 저장: 설정, 다운로드 대기열, 미디어 색인, 개별 메모 (현재는 라이브러리 내부 DB).
16. 재실행 시 미완료(running) 작업은 대기(queued)로 복구.
17. 기존 다운로드 폴더 하위 미디어를 직접 스캔해 라이브러리로 가져오기.
18. 기존 라이브러리의 영상은 중복 다운로드를 생략(파일 존재 시).
19. 라이브러리 검색(제목/채널/메모/ID), 채널별 필터, 파일 누락 표시.
20. 내장 Qt Multimedia 동영상 재생/일시정지/정지/시간 이동/재생 배속/음량.
21. 라이브러리 선택 시 SRT 다중 파일 탐지, 자막 전체 목록 표시,
    자막 항목 더블클릭 시 해당 시각으로 이동, 재생 자막 현재 줄 표시.
22. 영상별 메모 직접 작성/저장, 영상 전환 및 종료 시 자동 저장.
23. 동영상 파일 및 저장 폴더 Windows 탐색기/기본 플레이어로 열기.
24. 진행 상태·진행률·오류·현재 처리 항목을 GUI에 표시.
25. 로깅 화면과 로테이션 파일 로그(LocalAppData/MintonVideoLibrary/logs; 기존 로그 위치 유지).
26. ffmpeg, deno, yt-dlp 실행환경 확인 및 실행 조건 안내.
27. 창 및 분할창 크기 등 UI 상태 보관(SQLite settings).
28. Windows 콘솔창 없이 yt-dlp subprocess 실행, 한글 Unicode 경로 지원.
29. 삭제 버튼은 대기열 항목만 제거하며 실제 비디오 파일/메모는 보존.
30. 저작권과 이용약관을 준수하는 영상만 다운로드하도록 사용자에게 안내.

[V1.1 추가/수정 - 기존 V1.0의 기능 및 모든 로그 유지]
31. ?v=영상ID&list=목록ID 및 youtu.be?list 혼합 주소를 재생목록 우선 인식.
32. 재생목록 정보를 개별 다운로드 작업에 유지: 채널명/재생목록명/영상.
33. 채널·제목 메타데이터를 한국어 우선으로 요청(youtube:lang=ko).
34. URL 등록 시 채널 폴더명/재생목록 폴더명을 수동 지정 가능.
35. 재생목록 별로 동일 영상 URL을 별도 대기열 항목으로 관리.
36. 라이브러리 15초 간격 누락 확인 및 60초 간격 폴더 자동 재검색.
37. 실제 파일 삭제 시 라이브러리 기본 보기에서 자동 숨김, 메모 DB 보존;
    '누락 포함' 체크로 조회 가능, 다시 찾은 동일 ID는 메모 복구.
38. 영상과 연관된 자막/info.json을 함께 지정 폴더로 이동하거나 휴지통 삭제.
39. 영상·연관 자막 파일명을 한글 제목으로 변경, 수동 제목 유지.
40. 라이브러리의 각 컬럼 수동 너비 조절 및 너비 저장/툴팁/가로 스크롤.
41. 대기열 행별 진행률 바와 전체 현재 파일 진행률 바 추가.
42. 자막 파일 탐색: 동일 basename뿐 아니라 동일 YouTube ID 또는 근사 이름.
43. 전체 자막 목록의 별도 큰 창/자막 검색/더블클릭 구간 점프.
44. 동영상 준비(LoadedMedia/BufferedMedia) 후 지연 탐색 적용 및 재생.
45. 상태 변경/폴더 이동/파일 누락/이름변경 등 추가 로그; 기존 메시지 유지.

[V1.2 추가/수정 - 기존 V1.1의 기능과 로그 흐름 유지]
46. SQLite 데이터베이스를 라이브러리 루트/_database/library.db에 저장.
47. 기존 %LOCALAPPDATA%/MintonVideoLibrary/library.db는 SQLite 온라인 백업으로 최초 1회 복제.
48. 영상 파일 경로를 다운로드 루트 기준 상대 경로로 저장하여 드라이브 변경에 대응.
49. 이전 절대경로를 DB 내부 설정의 과거 루트에 맞추어 상대경로로 마이그레이션.
50. AppData에는 로그 및 마지막 라이브러리 경로 힌트만 보관; 메모와 영상 DB는 포터블.
51. 라이브러리 위치 선택/변경 및 --root 인자 지원; 존재하지 않는 경로는 안전하게 재선택.
52. 동영상 크기(Byte / MB / GB)를 DB에 기록하고 라이브러리 컬럼에 표시.
53. 배드민턴 기술·수비·포지션·레슨·대회 등의 대분류/세부 분류 기본 제공.
54. 수동 분류, 여러 태그(쉼표 구분), 분류별 목록 필터와 검색.
55. 구간 시작/끝 시각 기록, 구간 후보 저장/재생/삭제(실제 클립 출력은 후속 버전).
56. SQLite 메모·분류·구간표시 데이터는 파일 스캔/다운로드 시에도 보존.
57. 이전 라이브러리 DB는 삭제하지 않으며, SQLite 파일 검사 및 WAL 체크포인트 지원.

[V1.3 추가/수정 - V1.2 전체 기능과 GUI 로그/파일 로그 흐름 보존]
58. 신규 다운로드 시 YouTube 대표 썸네일을 JPG로 같은 폴더에 저장(--write-thumbnail/--convert-thumbnails jpg).
59. 기존 MP4에서 썸네일만 빠진 경우 이미지 전용 순차 수집(재다운로드 없음), 중단 지원 및 오류 로그.
60. JPG/PNG/WEBP 썸네일 탐색: 기본 파일명, 영상 ID 일치 기준; 파일 이동·개명·휴지통 처리 유지.
61. 라이브러리 목록 첫 열에 썸네일 이미지 표시, 보이는 행만 지연 로드하고 메모리 캐시 제한.
62. 영상 선택 시 큰 썸네일 미리보기와 누락 상태 표시.
63. Qt 플레이어 오디오 장치 명시, 출력 장치 선택, 음소거 토글·음량 설정 저장.
64. 영상의 오디오 트랙 자동 선택 및 ffprobe 기반 소리 진단(무음/코덱/출력 장치 문제 구분).
65. 플레이어의 재생/일시정지를 하나의 토글 버튼으로 통합(■ 정지 버튼은 별도 유지).
66. 라이브러리 목록에 재생목록명과 재생시간(HH:MM:SS) 컬럼 추가, 열 너비 설정 보존.
67. 재생목록명/ID를 영상 DB에 저장, 기존 채널/재생목록 경로 및 info.json에서도 복구.
68. 기존 mp4의 재생시간 메타데이터가 없으면 백그라운드 폴더 검색 시 ffprobe로 보충.
69. 다운로드/썸네일 작업 상호 충돌 방지, 백필 작업의 디스크 이동/종료 중지 보호.
70. 기존 V1.0~V1.2 DB, 메모, 분류, 자막, 클립 구간, 경로 및 로그 내용 유지.

[V1.3.1 수정 - 기존 V1.3 기능/로그/UI 보존]
71. 다운로드 대기열의 실패 행마다 전용 '↻ 다시받기' 버튼 추가.
72. 개별 재시도는 해당 영상/재생목록 작업만 실행하며 다른 대기 작업은 그대로 유지.
73. 재시도 모드 선택: 원래 자막 옵션 그대로 받기 또는 자막 제외하고 영상만 받기.
74. 자막 429/요청 제한 시 yt-dlp 마지막 오류 메시지를 DB/화면/로그에 기록하고 재시도 안내.
75. 오류 발생 후 진행률이 100%로 보이는 혼동 방지: 실패 작업의 진행률을 0%로 초기화.
76. UI의 '로그 파일 열기' 버튼으로 Windows 메모장에서 기존 로그를 즉시 열기.
77. DB 컬럼 retry_without_subs는 구형 DB에서 비파괴 마이그레이션; 기존 작업/메모/로그 보존.
78. 기존 다중 선택 후 '선택 항목 다시 대기' 동작은 원래 자막 설정 재시도로 유지.
79. 파일 다운로드 시 원본 `.part` 이어받기/원본 MP4·SRT·JPG·메모 보존.
80. 사용자 설정 다운로드 간격, Qt 재생기, 오디오 진단, 썸네일, 분류, 자막 탐색 유지.

[저장 위치]
- 프로그램: D:\stockproj\minton_video_library\minton_video_library.py (권장)
- 데이터베이스: 라이브러리루트\_database\library.db (영상과 함께 이동)
- 로그: %LOCALAPPDATA%\MintonVideoLibrary\logs (기존 위치 유지)
- 마지막 사용 폴더 힌트: %LOCALAPPDATA%\MintonVideoLibrary\library_location.json
- 다운로드: 사용자 설정 폴더 아래 채널/재생목록/파일명

[의존성]
  py -3.12 -m venv .venv
  .\\.venv\\Scripts\\python.exe -m pip install -U PySide6 "yt-dlp[default]"
  winget install DenoLand.Deno
  winget install Gyan.FFmpeg
  .\\.venv\\Scripts\\python.exe minton_video_library.py

주의: 유튜브 접속/다운로드는 외부 서비스 상태, 접근 권한, yt-dlp 버전에
영향을 받습니다. 개인 학습/권한이 있는 콘텐츠 용도로 사용하십시오.
"""

from __future__ import annotations

import bisect
from collections import OrderedDict
import hashlib
import html
import json
import logging
import ntpath
from pathlib import PurePosixPath
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
from datetime import datetime
from urllib.parse import parse_qs, urlparse

# Windows Qt Multimedia 기본 FFmpeg 디코더를 명시하여 백엔드/오디오 호환성 향상.
# 사용자가 QT_MEDIA_BACKEND를 이미 지정했다면 그 설정을 우선한다.
os.environ.setdefault('QT_MEDIA_BACKEND', 'ffmpeg')

from PySide6.QtCore import Qt, QThread, QTimer, QUrl, Signal, QFile, QSize
from PySide6.QtGui import QDesktopServices, QFont, QIcon, QPixmap
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer, QMediaDevices
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit,
    QProgressBar, QPushButton, QSlider, QSpinBox, QSplitter, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
    QHeaderView, QAbstractItemView, QCheckBox, QDialog, QInputDialog, QListWidgetItem,
)

APP_TITLE = "Minton Video Library v1.3.1"
APP_DATA = Path(os.getenv("LOCALAPPDATA") or (Path.home() / ".local" / "share")) / "MintonVideoLibrary"
# DB 경로는 앱 폴더와 분리하여 라이브러리 폴더와 항상 함께 이동한다.
LEGACY_DB_PATH = APP_DATA / "library.db"
ROOT_POINTER = APP_DATA / "library_location.json"
DB_PATH = None  # main()이 라이브러리 위치를 확정한 뒤 설정한다.
ACTIVE_ROOT = None
LOG_PATH = APP_DATA / "logs" / "minton_video_library.log"
DEFAULT_ROOT = r"D:\99.유튜브다운\minton.youtube" if os.name == "nt" else str(Path.home() / "Videos" / "minton.youtube")
FORMAT_SELECTOR = "bv[vcodec^=avc1][height<=1080]+ba[acodec^=mp4a]/b[vcodec^=avc1][height<=1080]"
OUTPUT_TEMPLATE = "%(channel)s/%(channel)s - %(title)s [%(id)s] - %(upload_date>%Y-%m-%d)s.%(ext)s"
FILE_TEMPLATE = "%(channel)s - %(title)s [%(id)s] - %(upload_date>%Y-%m-%d)s.%(ext)s"
# 사용자가 정확한 이름을 직접 확인해 준 재생목록. 일반 목록은 ko 우선 메타데이터 사용.
KOREAN_PLAYLIST_OVERRIDES = {
    'PLX1IndZwkjj0': ('윤이콕TV', '물A조라고 놀리지말아요'),
}
VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4v"}
THUMB_EXTS = (".jpg", ".jpeg", ".png", ".webp")

# 기술별 체계적 분류. 여러 영역에 걸친 영상은 쉼표 구분 태그를 함께 이용한다.
BADMINTON_CATEGORIES = {
    '미분류': ['미분류'],
    '기초·기본기': ['그립·라켓 잡기', '준비 자세·스플릿 스텝', '풋워크·스텝',
               '타점·스윙 원리', '체중이동·밸런스', '기초 반복 훈련'],
    '스트로크·기술': ['클리어', '스매시', '드롭·컷트', '헤어핀', '드라이브', '푸시',
                 '리프트·로브', '네트킬', '백핸드', '서브', '리시브', '페인트·응용 기술'],
    '수비·리턴': ['스매시 수비', '드라이브 수비', '네트 수비', '서브 리턴',
               '리시브·리턴 훈련', '수비→공격 전환'],
    '전술·포지션': ['단식 포지션', '복식 전위', '복식 후위', '복식 로테이션',
                '혼합복식', '공격·수비 전환', '경기 운영·전술', '상대 유형별 대응'],
    '레슨·코칭': ['입문 레슨', '중급 레슨', '상급 레슨', '개인 레슨',
               '자세 분석·교정', '연습 드릴', '코치 시범'],
    '대회·경기 영상': ['국제대회', '국내대회', '동호인 대회', '단식 경기',
                 '남자 복식', '여자 복식', '혼합복식 경기', '하이라이트', '경기 분석'],
    '운동·장비·기타': ['체력·근력', '유연성·부상 예방', '라켓·스트링',
                  '셔틀콕·용품', '규칙·판정', '인터뷰·기타'],
}

YT_ID_PATTERN = re.compile(r"\[([A-Za-z0-9_-]{11})\]")
SRT_PATTERN = re.compile(r"(\d\d):(\d\d):(\d\d)[,.](\d{1,3})\s*-->\s*(\d\d):(\d\d):(\d\d)[,.](\d{1,3})")
PROGRESS_PATTERN = re.compile(r"\[download\]\s+(\d+(?:\.\d+)?)%")

APP_DATA.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
LOGGER = logging.getLogger("minton_video_library")
LOGGER.setLevel(logging.INFO)
if not LOGGER.handlers:
    handler = RotatingFileHandler(str(LOG_PATH), maxBytes=5 * 1024 * 1024, backupCount=4, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    LOGGER.addHandler(handler)


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def set_library_root(root: str | Path) -> None:
    """라이브러리 루트를 활성화하고 DB 위치를 변경한다. 변경 전에 연결을 닫아야 한다."""
    global ACTIVE_ROOT, DB_PATH
    new_root = Path(root).expanduser().resolve()
    new_root.mkdir(parents=True, exist_ok=True)
    (new_root / '_database').mkdir(parents=True, exist_ok=True)
    ACTIVE_ROOT = new_root
    DB_PATH = new_root / '_database' / 'library.db'
    ROOT_POINTER.write_text(json.dumps({'root': str(new_root)}, ensure_ascii=False, indent=2), encoding='utf-8')
    LOGGER.info('[라이브러리 위치 설정] 루트: %s | DB: %s', ACTIVE_ROOT, DB_PATH)


def root_relative(path: str | Path) -> str:
    """현재 루트 아래 영상 파일을 안전한 '/' 상대경로로 저장한다."""
    src = Path(path).resolve()
    if ACTIVE_ROOT is None:
        return str(src)
    try:
        return src.relative_to(ACTIVE_ROOT.resolve()).as_posix()
    except ValueError as ex:
        raise ValueError(f'파일이 현재 라이브러리 범위 밖에 있습니다: {src}') from ex


def media_path(saved_path: str, root: Path | None = None) -> Path:
    """DB의 포터블 상대경로를 OS의 실제 절대경로로 복원한다."""
    root = root or ACTIVE_ROOT
    if root is None:
        return Path(saved_path)
    value = Path(str(saved_path))
    if value.is_absolute() or ntpath.isabs(str(saved_path)):
        return value
    resolved = (root / value).resolve()
    if not is_in_directory(resolved, root):
        raise ValueError(f'라이브러리 외부 경로 차단: {saved_path}')
    return resolved


def portable_legacy_path(saved: str, old_root: str, new_root: Path) -> str | None:
    """기존 절대경로를 현재 폴더로 안전하게 옮길 수 있는 상대경로로 계산."""
    if not saved:
        return None
    if not (ntpath.isabs(saved) or Path(saved).is_absolute()):
        try:
            candidate = media_path(saved, new_root)
            return candidate.relative_to(new_root.resolve()).as_posix()
        except ValueError:
            return None
    for candidate_root in (str(new_root), old_root):
        if not candidate_root:
            continue
        try:
            if ntpath.isabs(saved) and ntpath.isabs(candidate_root):
                relative = ntpath.relpath(saved, candidate_root)
                if not (relative == '..' or relative.startswith('..\\') or ntpath.isabs(relative)):
                    return Path(*relative.split('\\')).as_posix()
            elif Path(saved).is_absolute() and Path(candidate_root).is_absolute():
                return Path(saved).relative_to(Path(candidate_root)).as_posix()
        except (ValueError, OSError):
            continue
    return None


def format_size(num_bytes: int) -> str:
    if num_bytes < 0:
        return '-'
    if num_bytes < 1024:
        return f'{num_bytes} B'
    if num_bytes < 1024 ** 2:
        return f'{num_bytes / 1024:.1f} KB'
    if num_bytes < 1024 ** 3:
        return f'{num_bytes / 1024**2:,.1f} MB'
    return f'{num_bytes / 1024**3:,.2f} GB'


def copy_sqlite_database(source: Path, dest: Path) -> None:
    """WAL에 남은 데이터까지 SQLite 백업 API로 복사한다 (기존 DB 삭제 안 함)."""
    if dest.exists():
        raise FileExistsError(f'기존 DB 보호: {dest}')
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with sqlite3.connect(str(source), timeout=20) as src:
            with sqlite3.connect(str(dest), timeout=20) as out:
                src.backup(out)
    except Exception:
        if dest.exists():
            dest.unlink()  # 새로 생성하다 실패한 불완전 파일만 제거
        raise
    LOGGER.info('[기존 DB 백업 복제] %s -> %s (원본 보존)', source, dest)


def migrate_file_paths(db: sqlite3.Connection) -> None:
    """V1.1의 절대경로를 이동 가능한 상대경로로 일괄 교체한다."""
    old_root = get_setting(db, 'download_root', str(ACTIVE_ROOT))
    changed = skipped = 0
    with db:
        for row in db.execute('SELECT video_id,file_path FROM videos').fetchall():
            rel = portable_legacy_path(str(row['file_path']), old_root, ACTIVE_ROOT)
            if rel is None:
                skipped += 1
                continue
            if rel != row['file_path']:
                db.execute('UPDATE videos SET file_path=? WHERE video_id=?', (rel, row['video_id']))
                changed += 1
        db.execute('INSERT INTO settings(key,value) VALUES(?,?) '
                   'ON CONFLICT(key) DO UPDATE SET value=excluded.value',
                   ('download_root', str(ACTIVE_ROOT)))
    if changed or skipped:
        LOGGER.info('[상대경로 변환] %d개 변환 / %d개 경로 미확인(폴더 재검색 필요)', changed, skipped)


def connect_db() -> sqlite3.Connection:
    if DB_PATH is None:
        raise RuntimeError('라이브러리 위치를 먼저 지정해야 합니다')
    conn = sqlite3.connect(str(DB_PATH), timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=20000")
    return conn


def init_db(migrate_old: bool = True) -> None:
    if DB_PATH is None:
        raise RuntimeError('DB 저장 경로가 설정되지 않았습니다')
    if migrate_old and not DB_PATH.exists() and LEGACY_DB_PATH.exists():
        copy_sqlite_database(LEGACY_DB_PATH, DB_PATH)
    with connect_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY, value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL, kind TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'queued',
            progress REAL NOT NULL DEFAULT 0,
            error TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            title TEXT NOT NULL DEFAULT '',
            channel TEXT NOT NULL DEFAULT '',
            upload_date TEXT NOT NULL DEFAULT '',
            duration INTEGER NOT NULL DEFAULT 0,
            file_path TEXT NOT NULL DEFAULT '',
            source_url TEXT NOT NULL DEFAULT '',
            memo TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status, id);
        CREATE INDEX IF NOT EXISTS idx_videos_channel ON videos(channel);
        UPDATE jobs SET status='queued', progress=0 WHERE status='running';
        """)
        # SQLite 구버전 DB는 보존하면서 필요한 컬럼만 안전하게 추가한다.
        migrations = {
            'jobs': {
                'playlist_id': "TEXT NOT NULL DEFAULT ''",
                'playlist_title': "TEXT NOT NULL DEFAULT ''",
                'playlist_channel': "TEXT NOT NULL DEFAULT ''",
                'playlist_index': 'INTEGER NOT NULL DEFAULT 0',
                'channel_override': "TEXT NOT NULL DEFAULT ''",
                'playlist_override': "TEXT NOT NULL DEFAULT ''",
                'retry_without_subs': 'INTEGER NOT NULL DEFAULT 0',
            },
            'videos': {'title_override': "TEXT NOT NULL DEFAULT ''"},
        }
        migrations['videos'].update({
            'file_size': 'INTEGER NOT NULL DEFAULT 0',
            'major_category': "TEXT NOT NULL DEFAULT '미분류'",
            'sub_category': "TEXT NOT NULL DEFAULT '미분류'",
            'tags': "TEXT NOT NULL DEFAULT ''",
            'playlist_title': "TEXT NOT NULL DEFAULT ''",
            'playlist_id': "TEXT NOT NULL DEFAULT ''",
        })
        for table, columns in migrations.items():
            existing = {row['name'] for row in db.execute(f'PRAGMA table_info({table})')}
            for name, definition in columns.items():
                if name not in existing:
                    db.execute(f'ALTER TABLE {table} ADD COLUMN {name} {definition}')
                    LOGGER.info('[DB 마이그레이션] %s.%s 컬럼 추가', table, name)
        db.execute("""CREATE TABLE IF NOT EXISTS clip_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            start_ms INTEGER NOT NULL,
            end_ms INTEGER NOT NULL,
            title TEXT NOT NULL DEFAULT '',
            memo TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            FOREIGN KEY(video_id) REFERENCES videos(video_id)
        )""")
        db.execute('CREATE INDEX IF NOT EXISTS idx_clip_video ON clip_marks(video_id,id)')
        migrate_file_paths(db)
        # 과거에 받은 재생목록 영상은 MP4 경로(채널/목록/파일)에서 이름을 보충한다.
        for row in db.execute("SELECT video_id,file_path FROM videos WHERE playlist_title='' OR playlist_title IS NULL").fetchall():
            inferred = infer_playlist_name(row['file_path'])
            if inferred:
                db.execute('UPDATE videos SET playlist_title=? WHERE video_id=?', (inferred, row['video_id']))



def get_setting(db: sqlite3.Connection, key: str, default: str = "") -> str:
    item = db.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return str(item["value"]) if item else default


def set_setting(db: sqlite3.Connection, key: str, value: str) -> None:
    with db:
        db.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))


def yt_command() -> list[str] | None:
    # 현재 실행 중인 Python 가상환경의 yt-dlp를 우선 사용한다.
    try:
        import importlib.util
        if importlib.util.find_spec("yt_dlp") is not None:
            return [sys.executable, "-m", "yt_dlp"]
    except Exception:
        pass
    exe = shutil.which("yt-dlp")
    return [exe] if exe else None


def canonical_url(value: str) -> tuple[str, str] | None:
    """(정규화 URL, 종류). URL에 list=가 있으면 watch?v보다 우선한다.

    재생목록 링크가 watch?v=...&list=... 형식으로 들어와도 /playlist?list=...
    로 바꿔 처리하므로 개별 영상만 받는 문제를 방지한다.
    """
    try:
        p = urlparse(value.strip().replace('\\&', '&'))
        host = (p.hostname or '').lower()
        if p.scheme not in ('http', 'https') or host not in (
            'youtube.com', 'www.youtube.com', 'm.youtube.com', 'music.youtube.com', 'youtu.be'
        ):
            return None
        q = parse_qs(p.query)
        pl = (q.get('list') or [''])[0].strip()
        if pl and re.fullmatch(r'[A-Za-z0-9_-]{6,128}', pl):
            return f'https://www.youtube.com/playlist?list={pl}', 'playlist'
        if host == 'youtu.be':
            vid = p.path.strip('/').split('/')[0]
            if re.fullmatch(r'[A-Za-z0-9_-]{11}', vid):
                return f'https://www.youtube.com/watch?v={vid}', 'video'
        vid = (q.get('v') or [''])[0]
        m = re.fullmatch(r'/(?:shorts|live|embed)/([A-Za-z0-9_-]{11})/?', p.path)
        if m:
            return f'https://www.youtube.com/watch?v={m.group(1)}', 'video'
        if re.fullmatch(r'[A-Za-z0-9_-]{11}', vid):
            return f'https://www.youtube.com/watch?v={vid}', 'video'
    except (ValueError, TypeError):
        return None
    return None


def safe_name(value: str, fallback: str = '이름없음') -> str:
    """Windows 금지 문자/예약어를 제거한 디렉터리·파일 이름."""
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(value or '')).strip(' .')
    value = re.sub(r'\s+', ' ', value)[:110].rstrip(' .')
    if not value or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])', value):
        return fallback
    return value


def playlist_destination(root: Path, job) -> Path | None:
    playlist = str(job['playlist_title'] or job['playlist_override'] or '')
    if not playlist:
        return None
    channel = str(job['channel_override'] or job['playlist_channel'] or '채널확인필요')
    return root / safe_name(channel, '채널확인필요') / safe_name(playlist, '재생목록')


def infer_playlist_name(saved_path: str) -> str:
    """채널/재생목록/영상.mp4 형태의 상대경로에서 재생목록명을 가져온다."""
    try:
        parts = PurePosixPath(str(saved_path).replace('\\', '/')).parts
        if len(parts) >= 3 and parts[0] not in ('.', '..', '_database'):
            return parts[-2]
    except (ValueError, TypeError):
        pass
    return ''


def find_thumbnail(media: Path) -> Path | None:
    """영상과 같은 이름 또는 동일 YouTube ID의 썸네일을 찾는다."""
    if not media.is_file():
        return None
    for suffix in THUMB_EXTS:
        candidate = media.with_suffix(suffix)
        if candidate.is_file():
            return candidate
    match = YT_ID_PATTERN.search(media.stem)
    if not match:
        return None
    try:
        for path in media.parent.iterdir():
            if (path.is_file() and path.suffix.lower() in THUMB_EXTS
                    and path.stem != media.stem and YT_ID_PATTERN.search(path.stem)
                    and YT_ID_PATTERN.search(path.stem).group(1) == match.group(1)):
                return path
    except OSError:
        pass
    return None


def yt_video_url(source_url: str, video_id: str) -> str:
    """백필 용도의 YouTube 단일 영상 URL만 허용한다 (외부 URL 차단)."""
    vid = extract_video_id(str(source_url or ''))
    if not vid and re.fullmatch(r'[A-Za-z0-9_-]{11}', str(video_id or '')):
        vid = video_id
    return f'https://www.youtube.com/watch?v={vid}' if vid else ''


def probe_duration_seconds(media: Path) -> int:
    """info.json 없는 로컬 영상 길이를 ffprobe로 보충. GUI가 아닌 작업자에서 호출."""
    probe = shutil.which('ffprobe')
    if not probe or not media.is_file():
        return 0
    try:
        result = subprocess.run(
            [probe, '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(media)],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=12, **popen_flags())
        if result.returncode == 0:
            return max(0, int(float(result.stdout.strip())))
    except (ValueError, OSError, subprocess.TimeoutExpired):
        pass
    return 0


def format_duration(seconds: int | float) -> str:
    try:
        n = max(0, int(float(seconds)))
    except (TypeError, ValueError):
        n = 0
    return f'{n // 3600:02d}:{(n // 60) % 60:02d}:{n % 60:02d}' if n else '--:--:--'


def related_sidecars(media: Path) -> list[Path]:
    """영상 이름과 동일한 기본 이름을 가진 자막·메타데이터 파일만 찾는다."""
    suffixes = {'.srt', '.ass', '.vtt', '.lrc', '.json', '.description', '.jpg', '.jpeg', '.webp', '.png'}
    if not media.is_file():
        return []
    try:
        # 원래 다운로드명과 미세하게 다른 SRT도 동일 영상 ID이면 함께 처리한다.
        exact = {p for p in media.parent.iterdir()
                 if p.is_file() and p.name.startswith(media.stem + '.')
                 and p.suffix.lower() in suffixes}
        thumbnail = find_thumbnail(media)
        if thumbnail is not None:
            exact.add(thumbnail)
        return sorted(exact.union(subtitle_candidates(media)))
    except OSError:
        return []


def move_media_bundle(media: Path, destination: Path, new_stem: str | None = None) -> Path:
    """영상 및 연관 자막, info.json 이동/이름변경. 목적지 덮어쓰기 금지."""
    if not media.is_file():
        raise FileNotFoundError(media)
    target = destination / ((new_stem or media.stem) + media.suffix)
    companions = related_sidecars(media)
    pairs = [(media, target)]
    alt = 0
    for p in companions:
        if p.name.startswith(media.stem + '.'):
            name = (new_stem or media.stem) + p.name[len(media.stem):]
        elif new_stem is None:
            name = p.name  # 다른 이름의 동일 영상 ID 자막도 이동한다.
        else:
            alt += 1
            name = f'{new_stem}.alt{alt}{p.suffix}'
        pairs.append((p, destination / name))
    for src, dst in pairs:
        if src.resolve() != dst.resolve() and dst.exists():
            raise FileExistsError(f'동일한 이름의 파일이 이미 존재합니다: {dst}')
    destination.mkdir(parents=True, exist_ok=True)
    for src, dst in pairs:
        if src.resolve() != dst.resolve():
            shutil.move(str(src), str(dst))
    return target


def subtitle_candidates(media: Path) -> list[Path]:
    """동일 이름·동일 영상 ID·유사 제목의 한글 SRT 파일을 탐색한다."""
    if not media.is_file():
        return []
    media_id = YT_ID_PATTERN.search(media.stem)
    media_title = re.sub(r'\s*\[[A-Za-z0-9_-]{11}\].*$', '', media.stem).casefold()
    result = []
    for candidate in media.parent.glob('*.srt'):
        name = candidate.name
        sm = YT_ID_PATTERN.search(candidate.stem)
        if candidate.stem.startswith(media.stem) or (media_id and sm and media_id.group(1) == sm.group(1)):
            result.append(candidate)
        elif not media_id and media_title and len(media_title) > 9:
            other = candidate.stem.casefold()
            common = os.path.commonprefix([media_title, other])
            if len(common) >= 10 and len(common) / max(1, len(media_title)) >= 0.65:
                result.append(candidate)
    return sorted(set(result), key=lambda p: ('.ko.' not in p.name.lower(), p.name.lower()))


def is_in_directory(path: Path, root: Path) -> bool:
    try:
        return path.resolve().is_relative_to(root.resolve())
    except (OSError, ValueError):
        return False


def extract_video_id(url: str) -> str:
    c = canonical_url(url)
    if c and c[1] == "video":
        return parse_qs(urlparse(c[0]).query).get("v", [""])[0]
    return ""


def read_info_json(media: Path) -> dict:
    path = media.with_suffix(".info.json")
    try:
        if path.is_file() and path.stat().st_size < 15_000_000:
            with path.open("r", encoding="utf-8") as fp:
                obj = json.load(fp)
                return obj if isinstance(obj, dict) else {}
    except (OSError, ValueError, UnicodeError):
        pass
    return {}


def local_video_record(path: Path, probe_duration: bool = False) -> dict:
    info = read_info_json(path)
    id_match = YT_ID_PATTERN.search(path.stem)
    file_id = (info.get("id") or (id_match.group(1) if id_match else ""))
    if not file_id:
        file_id = "local:" + hashlib.sha1(root_relative(path).casefold().encode("utf-8")).hexdigest()
    title = info.get("title") or path.stem
    channel = info.get("channel") or path.parent.name
    relative_parts = PurePosixPath(root_relative(path)).parts
    # 재생목록 폴더의 채널명이 이미 한국어인데 YouTube 메타데이터가
    # 영문 이름으로 회귀하면 기존에 지정한 한국어 폴더명을 우선한다.
    if relative_parts and re.search(r'[가-힣]', relative_parts[0]) and not re.search(r'[가-힣]', str(channel)):
        channel = relative_parts[0]
    upload_date = str(info.get("upload_date") or "")
    if len(upload_date) == 8 and upload_date.isdigit():
        upload_date = upload_date[:4] + "-" + upload_date[4:6] + "-" + upload_date[6:]
    elif not upload_date:
        match = re.search(r"(\d{4}-\d{2}-\d{2})$", path.stem)
        upload_date = match.group(1) if match else ""
    # 목록 폴더가 있을 때 채널명은 info.json의 원본 채널을 우선 사용한다.
    duration_raw = info.get('duration') or 0
    try:
        duration = max(0, int(float(duration_raw)))
    except (TypeError, ValueError):
        duration = 0
    if not duration and probe_duration:
        duration = probe_duration_seconds(path)
    relative = root_relative(path)
    playlist_name = infer_playlist_name(relative) or str(info.get('playlist_title') or info.get('playlist') or '')
    return dict(video_id=str(file_id), title=str(title), channel=str(channel),
                upload_date=upload_date, duration=duration,
                file_path=relative, source_url=str(info.get("webpage_url") or ""),
                file_size=path.stat().st_size, playlist_title=playlist_name,
                playlist_id=str(info.get('playlist_id') or ''))


def upsert_video(db: sqlite3.Connection, data: dict) -> str:
    # 갱신 시 기존 메모를 절대 덮어쓰지 않는다.
    # 오래된 로컬 영상 ID(local:절대경로해시)는 파일 위치를 기준으로 재연결한다.
    if str(data['video_id']).startswith('local:'):
        existing = db.execute('SELECT video_id FROM videos WHERE file_path=?',
                              (data['file_path'],)).fetchone()
        if existing:
            data = {**data, 'video_id': existing['video_id']}
        else:
            # 탐색기에서 직접 다른 폴더로 옮긴 로컬 영상: 이름+크기가 같고
            # 과거 경로가 사라진 후보가 딱 하나일 때에만 메모/분류를 재연결한다.
            candidates = db.execute(
                'SELECT video_id,file_path FROM videos WHERE title=? AND file_size=? '
                "AND video_id LIKE 'local:%'",
                (data['title'], data['file_size'])).fetchall()
            missing = [r for r in candidates if not media_path(r['file_path']).is_file()]
            if len(missing) == 1:
                data = {**data, 'video_id': missing[0]['video_id']}
                LOGGER.info('[로컬 영상 경로 재연결] %s -> %s',
                            missing[0]['file_path'], data['file_path'])
    with db:
        db.execute("""
        INSERT INTO videos(video_id,title,channel,upload_date,duration,file_path,source_url,file_size,
                           playlist_title,playlist_id,updated_at)
        VALUES(:video_id,:title,:channel,:upload_date,:duration,:file_path,:source_url,:file_size,
               :playlist_title,:playlist_id,:updated_at)
        ON CONFLICT(video_id) DO UPDATE SET
            title=excluded.title, channel=excluded.channel,
            upload_date=CASE WHEN excluded.upload_date<>'' THEN excluded.upload_date ELSE videos.upload_date END,
            duration=CASE WHEN excluded.duration>0 THEN excluded.duration ELSE videos.duration END,
            file_path=excluded.file_path,
            file_size=excluded.file_size,
            playlist_title=CASE WHEN excluded.playlist_title<>'' THEN excluded.playlist_title ELSE videos.playlist_title END,
            playlist_id=CASE WHEN excluded.playlist_id<>'' THEN excluded.playlist_id ELSE videos.playlist_id END,
            source_url=CASE WHEN excluded.source_url<>'' THEN excluded.source_url ELSE videos.source_url END,
            updated_at=excluded.updated_at
        """, {**{'playlist_title': '', 'playlist_id': ''}, **data, "updated_at": now_str()})
    return str(data['video_id'])


def srt_millis(parts: tuple[str, ...]) -> int:
    h, m, s, ms = parts
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(ms.ljust(3, "0")[:3])


def parse_srt(path: Path) -> list[tuple[int, int, str]]:
    content = None
    for encoding in ("utf-8-sig", "cp949", "utf-16"):
        try:
            content = path.read_text(encoding=encoding)
            break
        except (UnicodeError, OSError):
            pass
    if content is None:
        return []
    result = []
    for block in re.split(r"\r?\n\s*\r?\n", content):
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            match = SRT_PATTERN.search(line)
            if not match:
                continue
            start = srt_millis(match.groups()[:4])
            end = srt_millis(match.groups()[4:])
            text = html.unescape(re.sub(r"<[^>]*>", "", "\n".join(lines[i + 1:]).strip()))
            if text:
                result.append((start, end, text))
            break
        if len(result) >= 20000:
            break
    return sorted(result, key=lambda x: x[0])


def millis_text(ms: int) -> str:
    sec = max(0, int(ms) // 1000)
    return f"{sec // 3600:02d}:{(sec // 60) % 60:02d}:{sec % 60:02d}"


def popen_flags() -> dict:
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NO_WINDOW}
    return {}


class DownloadWorker(QThread):
    message = Signal(str)
    changed = Signal()
    activity = Signal(str)
    progress_signal = Signal(int, float)

    def __init__(self, root: str, interval: int, parent=None, only_job_id: int | None = None):
        super().__init__(parent)
        self.root = Path(root)
        self.interval = interval
        # 실패 행의 다시받기는 다른 대기 작업을 실행하지 않는 전용 1건 모드.
        self.only_job_id = only_job_id
        self._stop = threading.Event()
        self._pause = threading.Event()
        self._lock = threading.Lock()
        self._proc: subprocess.Popen | None = None
        self._cmd_base = yt_command()

    def request_stop(self):
        self._stop.set()
        self._pause.clear()
        with self._lock:
            proc = self._proc
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
            except OSError:
                pass

    def request_pause(self):
        self._pause.set()

    def request_resume(self):
        self._pause.clear()

    def is_paused(self):
        return self._pause.is_set()

    def _set_proc(self, proc):
        with self._lock:
            self._proc = proc

    def _shared_cmd(self):
        return [*self._cmd_base, "--ignore-config", "--js-runtimes", "deno",
                "--remote-components", "ejs:npm", "--extractor-args", "youtube:lang=ko", "--no-color",
                "--socket-timeout", "25", "--retries", "3",
                "--fragment-retries", "3", "--extractor-retries", "2"]

    def _emit(self, text):
        self.message.emit(text)

    def _run_capture(self, command: list[str]) -> tuple[int, str, str]:
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", errors="replace", env=env,
                                **popen_flags())
        self._set_proc(proc)
        try:
            stdout, stderr = proc.communicate()
            return proc.returncode, stdout, stderr
        finally:
            self._set_proc(None)

    def _update_job(self, db, job_id, status, error="", progress=None):
        with db:
            if progress is None:
                db.execute("UPDATE jobs SET status=?,error=?,updated_at=? WHERE id=?",
                           (status, error[:4000], now_str(), job_id))
            else:
                db.execute("UPDATE jobs SET status=?,error=?,progress=?,updated_at=? WHERE id=?",
                           (status, error[:4000], progress, now_str(), job_id))
        self.changed.emit()

    def _expand_playlist(self, db, job):
        self.activity.emit('재생목록 확인 중')
        self._emit(f"[재생목록] {job['url']}")
        cmd = [*self._shared_cmd(), '--flat-playlist', '--dump-single-json', '--yes-playlist', job['url']]
        try:
            code, output, stderr = self._run_capture(cmd)
        except Exception as ex:
            self._update_job(db, job['id'], 'failed', str(ex))
            self._emit(f'[재생목록 실패] {ex}')
            return
        if stderr.strip():
            for line in stderr.strip().splitlines()[-30:]:
                self._emit('[yt-dlp] ' + line)
        if self._stop.is_set():
            self._update_job(db, job['id'], 'queued', '중단되어 재시도 대기')
            return
        if code != 0:
            self._update_job(db, job['id'], 'failed', stderr[-1500:] or '목록 정보 수신 실패')
            return
        try:
            data = json.loads(output)
            entries = data.get('entries') or []
            if not isinstance(entries, list):
                raise ValueError('재생목록 데이터 형식이 올바르지 않습니다')
            plid = str(data.get('id') or parse_qs(urlparse(job['url']).query).get('list', [''])[0])
            known_channel, known_title = KOREAN_PLAYLIST_OVERRIDES.get(plid, ('', ''))
            ptitle = str(job['playlist_override'] or known_title or data.get('title')
                         or data.get('playlist_title') or plid)
            first = next((e for e in entries if isinstance(e, dict)), {})
            owner = str(job['channel_override'] or known_channel or data.get('channel')
                        or data.get('playlist_channel') or data.get('uploader')
                        or data.get('playlist_uploader') or first.get('channel')
                        or first.get('uploader') or '채널확인필요')
            added = skipped = duplicates = 0
            with db:
                for index, entry in enumerate(entries, 1):
                    if not isinstance(entry, dict):
                        skipped += 1
                        continue
                    item_id = str(entry.get('id') or '')
                    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', item_id):
                        raw_url = str(entry.get('webpage_url') or entry.get('url') or '')
                        m = re.search(r'(?:[?&]v=|youtu\.be/)([A-Za-z0-9_-]{11})', raw_url)
                        item_id = m.group(1) if m else ''
                    if not item_id:
                        skipped += 1
                        continue
                    # 기존 DB의 url UNIQUE를 유지하면서, 같은 영상의 서로 다른 재생목록은 구별한다.
                    url = f'https://www.youtube.com/watch?v={item_id}&mv_list={plid}'
                    before = db.total_changes
                    db.execute("""INSERT OR IGNORE INTO jobs
                        (url,kind,title,status,created_at,updated_at,playlist_id,playlist_title,
                         playlist_channel,playlist_index,channel_override,playlist_override)
                        VALUES(?,'video',?,'queued',?,?,?,?,?,?,?,?)""",
                        (url, str(entry.get('title') or item_id), now_str(), now_str(),
                         plid, ptitle, owner, int(entry.get('playlist_index') or index),
                         str(job['channel_override'] or ''), str(job['playlist_override'] or '')))
                    if db.total_changes > before:
                        added += 1
                    else:
                        duplicates += 1
                db.execute('UPDATE jobs SET title=?,updated_at=? WHERE id=?',
                           (f'{owner} / {ptitle}', now_str(), job['id']))
            self._update_job(db, job['id'], 'expanded',
                             f'신규 {added}개 / 중복 {duplicates}개 / 접근 불가 {skipped}개', 100)
            self._emit(f'[재생목록 등록] 채널: {owner}, 제목: {ptitle}, 신규 {added}개, 중복 {duplicates}개, 건너뜀 {skipped}개')
            self._emit(f'[저장 폴더] {self.root / safe_name(owner) / safe_name(ptitle)}')
        except (ValueError, TypeError, json.JSONDecodeError) as ex:
            self._update_job(db, job['id'], 'failed', f'재생목록 JSON 분석 오류: {ex}')

    def _download_one(self, db, job):
        url = job['url']
        video_id = extract_video_id(url)
        dest = playlist_destination(self.root, job)
        if dest is None and job['channel_override']:
            dest = self.root / safe_name(job['channel_override'])
        # yt-dlp 호출에는 내부 구별자 mv_list를 제거한 순수 영상 주소를 전달한다.
        video_url = f'https://www.youtube.com/watch?v={video_id}' if video_id else url
        if video_id:
            existing = db.execute("SELECT file_path FROM videos WHERE video_id=?", (video_id,)).fetchone()
            if existing and media_path(existing['file_path']).is_file():
                old_path = media_path(existing['file_path'])
                if dest and old_path.parent.resolve() != dest.resolve():
                    # V1.0의 채널명\파일처럼 최상위 채널 폴더에 저장된 구형 파일은
                    # 재다운로드하지 않고 재생목록 폴더에 안전하게 이동한다.
                    try:
                        rel = old_path.resolve().relative_to(self.root.resolve())
                        if len(rel.parts) == 2 and job['playlist_title']:
                            moved = move_media_bundle(old_path, dest)
                            with db:
                                db.execute('UPDATE videos SET file_path=?,updated_at=? WHERE video_id=?',
                                           (root_relative(moved), now_str(), video_id))
                            self._emit(f'[기존 영상 재분류] {old_path} -> {moved} (메모·자막 유지)')
                        else:
                            self._emit(f'[중복 생략] 기존 영상이 다른 폴더에 있습니다: {old_path}; '
                                       f'목적지: {dest} / 라이브러리의 파일 이동 버튼으로 이동 가능')
                    except (OSError, ValueError) as ex:
                        self._emit(f'[기존 영상 재분류 보류] {ex}; 파일 이동 버튼으로 처리하세요')
                else:
                    self._emit(f'[중복 생략] {url}')
                if job['playlist_title']:
                    with db:
                        db.execute('UPDATE videos SET playlist_title=?,playlist_id=?,updated_at=? WHERE video_id=?',
                                   (job['playlist_title'], job['playlist_id'], now_str(), video_id))
                self._update_job(db, job['id'], 'done', '이미 라이브러리에 존재', 100)
                return
        self.activity.emit(f"다운로드 중: {job['title'] or url}")
        self._emit(f"[다운로드 시작] #{job['id']} {url}")
        # 재생목록은 yt-dlp가 임의로 영어 채널명을 출력하더라도 확인한
        # 채널 폴더명(사용자 지정/한글 매핑/한국어 메타데이터)을 파일명 접두사로 쓴다.
        file_template = OUTPUT_TEMPLATE
        if dest:
            korean_channel = safe_name(job['channel_override'] or job['playlist_channel'] or dest.name)
            file_template = (korean_channel.replace('%', '%%')
                             + ' - %(title)s [%(id)s] - %(upload_date>%Y-%m-%d)s.%(ext)s')
        skip_subtitles = bool(job['retry_without_subs'])
        # 유튜브 자동자막 ko-vi가 429를 반환할 때는 MP4만 재시도할 수 있게 한다.
        # 기본 다운로드에서는 기존 한국어 일반/자동자막 옵션을 반드시 유지한다.
        subtitle_flags = (["--no-write-subs", "--no-write-auto-subs"] if skip_subtitles else
                          ["--write-subs", "--write-auto-subs", "--sub-langs", "ko.*",
                           "--convert-subs", "srt"])
        if skip_subtitles:
            self._emit(f"[자막 제외 재시도] #{job['id']} 자막 HTTP 429 회피: MP4/썸네일/정보만 받습니다. 기존 SRT는 삭제하지 않습니다")
        cmd = [*self._shared_cmd(), "--no-playlist", "--continue", "--newline", "--progress",
               "-f", FORMAT_SELECTOR, "--merge-output-format", "mp4",
               *subtitle_flags, "--write-info-json", "--no-write-playlist-metafiles",
               "--write-thumbnail", "--convert-thumbnails", "jpg",
               "-P", str(dest if dest else self.root),
               "-o", file_template,
               "--print", "after_move:__MINTON_FILE__%(filepath)s",
               "--print", "after_move:__MINTON_TITLE__%(title)s",
               "--print", "after_move:__MINTON_CHANNEL__%(channel)s",
               "--print", "after_move:__MINTON_ID__%(id)s",
               video_url]
        info: dict[str, str] = {}
        last_log_percentage = -10
        last_persisted_step = -1
        # 종료 코드 1만 보이면 원인을 알 수 없어 yt-dlp 원문 오류를 저장한다.
        yt_errors: list[str] = []
        try:
            env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, encoding="utf-8", errors="replace", bufsize=1,
                                    env=env, **popen_flags())
            self._set_proc(proc)
            try:
                for raw in proc.stdout:
                    line = raw.strip()
                    if not line:
                        continue
                    if line.startswith("__MINTON_"):
                        for key in ("FILE", "TITLE", "CHANNEL", "ID"):
                            prefix = f"__MINTON_{key}__"
                            if line.startswith(prefix):
                                info[key] = line[len(prefix):]
                                break
                        continue
                    match = PROGRESS_PATTERN.search(line)
                    if match:
                        percent = min(100.0, float(match.group(1)))
                        self.progress_signal.emit(job["id"], percent)
                        progress_step = int(percent // 5)
                        if progress_step > last_persisted_step:
                            with db:
                                db.execute("UPDATE jobs SET progress=?,updated_at=? WHERE id=?",
                                           (percent, now_str(), job["id"]))
                            last_persisted_step = progress_step
                        if int(percent // 10) > int(last_log_percentage // 10):
                            self._emit(f"[진행] #{job['id']} {percent:.1f}%")
                            last_log_percentage = percent
                    else:
                        self._emit("[yt-dlp] " + line)
                        if line.startswith('ERROR:') or ('HTTP Error 429' in line):
                            yt_errors.append(line)
                            yt_errors = yt_errors[-5:]
                    if self._stop.is_set() and proc.poll() is None:
                        proc.terminate()
                retcode = proc.wait()
            finally:
                self._set_proc(None)
                if proc.stdout:
                    proc.stdout.close()
            if self._stop.is_set():
                self._update_job(db, job["id"], "queued", "중단됨(.part 재개 가능)")
                return
            if retcode != 0:
                last_error = yt_errors[-1] if yt_errors else '상세 오류는 아래 로그 참고'
                detail = f"yt-dlp 종료 코드 {retcode} | {last_error}"
                self._update_job(db, job["id"], "failed", detail, 0)
                self._emit(f"[실패] #{job['id']} yt-dlp 종료 코드 {retcode}")
                self._emit(f"[실패 상세] #{job['id']} {last_error}")
                if '429' in last_error and 'subtitle' in last_error.lower():
                    self._emit(f"[자막 요청 제한] #{job['id']} 한국어 자동자막에서 HTTP 429. "
                               "반복 요청하지 말고 시간을 두었다가 실패 행의 '다시받기' → '자막 제외하고 영상만'을 선택하세요.")
                return
            media_path = Path(info.get("FILE") or "")
            if not media_path.is_file() and video_id:
                # yt-dlp 버전에 따라 after_move가 출력되지 않는 경우 기존 파일 재탐색
                matches = [p for p in self.root.rglob("*")
                           if f"[{video_id}]" in p.name and p.suffix.lower() in VIDEO_EXTS and p.is_file()]
                if matches:
                    media_path = matches[0]
            if not media_path.is_file():
                self._update_job(db, job["id"], "failed", "성공 응답이지만 저장된 동영상 파일을 찾지 못함", 0)
                return
            data = local_video_record(media_path)
            data['source_url'] = video_url
            if info.get("TITLE"):
                data["title"] = info["TITLE"]
            if info.get('CHANNEL'):
                data['channel'] = info['CHANNEL']
            if job['playlist_channel']:
                data['channel'] = job['playlist_channel']
            if job['channel_override']:
                data['channel'] = job['channel_override']
            if info.get("ID"):
                data["video_id"] = info["ID"]
            data['playlist_title'] = job['playlist_title'] or data['playlist_title']
            data['playlist_id'] = job['playlist_id'] or data['playlist_id']
            upsert_video(db, data)
            if find_thumbnail(media_path):
                self._emit(f'[썸네일 저장] {find_thumbnail(media_path)}')
            else:
                self._emit(f'[썸네일 누락] {media_path.name}: 나중에 누락 썸네일 받기 가능')
            self._update_job(db, job["id"], "done", "", 100)
            self._emit(f"[다운로드 완료] {media_path}")
        except Exception as ex:
            if self._stop.is_set():
                self._update_job(db, job["id"], "queued", "중단됨(.part 재개 가능)")
            else:
                self._update_job(db, job["id"], "failed", str(ex), 0)
                self._emit(f"[다운로드 오류] {type(ex).__name__}: {ex}")
        finally:
            self.changed.emit()

    def run(self):
        if not self._cmd_base:
            self._emit("[오류] yt-dlp 미설치: pip install -U 'yt-dlp[default]'")
            return
        db = connect_db()
        previous_download_finished = None
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            self._emit(f"[대기열 시작] 저장 경로: {self.root}; 다운로드 간격: {self.interval}초")
            while not self._stop.is_set():
                if self._pause.is_set():
                    self.activity.emit("일시정지 (시작/재개 버튼으로 계속)")
                    if self._stop.wait(0.3):
                        break
                    continue
                if self.only_job_id is not None:
                    job = db.execute("SELECT * FROM jobs WHERE status='queued' AND id=?",
                                     (self.only_job_id,)).fetchone()
                else:
                    job = db.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY id LIMIT 1").fetchone()
                if job is None:
                    if self.only_job_id is not None:
                        self._emit(f"[개별 재시도 완료] #{self.only_job_id} 처리 종료, 나머지 대기 작업은 유지")
                    else:
                        self._emit("[대기열 완료] 더 이상 대기 중인 영상이 없습니다.")
                    break
                if job["kind"] == "video" and previous_download_finished is not None:
                    wait_for = self.interval - (time.monotonic() - previous_download_finished)
                    while wait_for > 0 and not self._stop.is_set() and not self._pause.is_set():
                        self.activity.emit(f"다음 다운로드까지 {int(wait_for + 0.99)}초 대기")
                        if self._stop.wait(min(1.0, wait_for)):
                            break
                        wait_for = self.interval - (time.monotonic() - previous_download_finished)
                    if self._stop.is_set() or self._pause.is_set():
                        continue
                self._update_job(db, job["id"], "running", "", 0)
                if job["kind"] == "playlist":
                    self._expand_playlist(db, job)
                else:
                    self._download_one(db, job)
                    previous_download_finished = time.monotonic()
        except Exception as ex:
            self._emit(f"[작업자 오류] {type(ex).__name__}: {ex}")
        finally:
            db.close()
            self.activity.emit("중지됨" if self._stop.is_set() else "대기")
            self.changed.emit()


class ThumbnailWorker(QThread):
    """기존 MP4 썸네일 누락분만 yt-dlp --skip-download로 순차 수집."""
    message = Signal(str)
    changed = Signal()
    progress_signal = Signal(int, int, int)  # 처리 완료, 대상 수, 성공 수

    def __init__(self, root: Path, tasks: list[tuple[Path, str, str]], interval=3, parent=None):
        super().__init__(parent)
        self.root = Path(root)
        self.tasks = tasks
        self.interval = max(0, int(interval))
        self._stop = threading.Event()
        self._proc: subprocess.Popen | None = None
        self._lock = threading.Lock()

    def request_stop(self):
        self._stop.set()
        with self._lock:
            process = self._proc
        if process is not None and process.poll() is None:
            try:
                process.terminate()
            except OSError:
                pass

    def run(self):
        base = yt_command()
        if not base:
            self.message.emit('[썸네일 오류] yt-dlp가 설치되어 있지 않습니다')
            return
        completed = ok = skipped = 0
        self.message.emit(f'[썸네일 일괄 받기] 누락 대상 {len(self.tasks)}개, 요청 간격 {self.interval}초')
        for media, source_url, video_id in self.tasks:
            if self._stop.is_set():
                break
            if not media.is_file() or not is_in_directory(media, self.root):
                skipped += 1
                self.message.emit(f'[썸네일 건너뜀] 영상 파일 누락/루트 밖: {media}')
            elif find_thumbnail(media):
                skipped += 1
            else:
                url = yt_video_url(source_url, video_id)
                if not url:
                    skipped += 1
                    self.message.emit(f'[썸네일 건너뜀] YouTube 영상 ID가 없는 로컬 파일: {media.name}')
                else:
                    # 실제 MP4가 없는 경우에만 콘텐츠를 생성하는 안전한 이미지-only 호출.
                    cmd = [*base, '--ignore-config', '--js-runtimes', 'deno',
                           '--remote-components', 'ejs:npm', '--extractor-args', 'youtube:lang=ko',
                           '--no-color', '--socket-timeout', '25', '--retries', '3',
                           '--extractor-retries', '2', '--no-playlist', '--skip-download',
                           '--write-thumbnail', '--convert-thumbnails', 'jpg',
                           '--no-write-info-json', '--no-write-subs', '--no-write-auto-subs',
                           '--no-write-playlist-metafiles', '-P', str(media.parent),
                           '-o', media.stem.replace('%', '%%') + '.%(ext)s', url]
                    env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
                    try:
                        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                text=True, encoding='utf-8', errors='replace',
                                                env=env, **popen_flags())
                        with self._lock:
                            self._proc = proc
                        try:
                            output, _ = proc.communicate(timeout=180)
                        except subprocess.TimeoutExpired:
                            proc.kill()
                            output, _ = proc.communicate()
                            self.message.emit(f'[썸네일 시간 초과] {media.name}')
                        finally:
                            with self._lock:
                                self._proc = None
                        if find_thumbnail(media):
                            ok += 1
                            self.message.emit(f'[썸네일 저장] {media.name} -> {find_thumbnail(media).name}')
                            self.changed.emit()
                        else:
                            self.message.emit(f'[썸네일 실패] {media.name} / 종료코드 {proc.returncode}: '
                                              f'{output[-450:].strip()}')
                    except (OSError, ValueError) as ex:
                        self.message.emit(f'[썸네일 오류] {media.name}: {ex}')
            completed += 1
            self.progress_signal.emit(completed, len(self.tasks), ok)
            if self._stop.is_set():
                break
            if completed < len(self.tasks) and self.interval:
                if self._stop.wait(self.interval):
                    break
        self.message.emit(f'[썸네일 작업 종료] 성공 {ok}개, 건너뜀 {skipped}개, '
                          f'처리 {completed}/{len(self.tasks)}개' + (' (사용자 중단)' if self._stop.is_set() else ''))
        self.changed.emit()


class ScanWorker(QThread):
    finished_scan = Signal(list)
    message = Signal(str)

    def __init__(self, root: str, known_durations: dict[str, int] | None = None, parent=None):
        super().__init__(parent)
        self.root = Path(root)
        self.known_durations = known_durations or {}

    def run(self):
        results = []
        try:
            if self.root.is_dir():
                for directory, subdirs, filenames in os.walk(self.root):
                    subdirs[:] = [d for d in subdirs if d not in ('_database', '.git', '.venv')]
                    for name in filenames:
                        path = Path(directory) / name
                        if path.suffix.lower() in VIDEO_EXTS:
                            rel = root_relative(path)
                            known = self.known_durations.get(rel, 0)
                            record = local_video_record(path, probe_duration=(not known))
                            if not record['duration'] and known:
                                record['duration'] = known
                            results.append(record)
            self.finished_scan.emit(results)
        except Exception as ex:
            self.message.emit(f"[폴더 검색 오류] {ex}")
            self.finished_scan.emit(results)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db(migrate_old=False)
        self.db = connect_db()
        self.worker: DownloadWorker | None = None
        self.scanner: ScanWorker | None = None
        self.thumbnail_worker: ThumbnailWorker | None = None
        self._thumbnail_cache: OrderedDict[str, tuple[int, QIcon]] = OrderedDict()
        self._row_thumbnail_paths: list[Path | None] = []
        self._thumbnail_visible_timer = QTimer(self)
        self._thumbnail_visible_timer.setSingleShot(True)
        self._thumbnail_visible_timer.timeout.connect(self.refresh_visible_thumbnails)
        self.current_id: str | None = None
        self.current_path: Path | None = None
        self.subtitles: list[tuple[int, int, str]] = []
        self.subtitle_starts: list[int] = []
        self.current_subtitle_index = -1
        self._loading_note = False
        self._loading_category = False
        self._seeking = False
        self._pending_seek: int | None = None
        self.subtitle_window: QDialog | None = None
        self.subtitle_popup_list: QListWidget | None = None
        self._last_missing: set[str] = set()
        self._segment_start: int | None = None
        self._segment_end: int | None = None
        self._build_ui()
        self._load_settings()
        self.setup_audio_devices()
        self.update_play_button()
        self.refresh_jobs()
        self.refresh_library()
        QTimer.singleShot(500, self.scan_library)
        # 실파일 삭제 즉시(최대 15초) 라이브러리에서 숨김; 폴더 이동은 자동 재검색.
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.refresh_library)
        self.check_timer.start(15000)
        self.auto_scan_timer = QTimer(self)
        self.auto_scan_timer.timeout.connect(lambda: self.scan_library(auto=True))
        self.auto_scan_timer.start(60000)
        self.add_log(f"프로그램 시작 | DB: {DB_PATH} | 로그: {LOG_PATH}")
        self.setWindowTitle(APP_TITLE)
        try:
            width = int(get_setting(self.db, "window_width", "1490"))
            height = int(get_setting(self.db, "window_height", "920"))
            self.resize(max(850, min(width, 3000)), max(580, min(height, 2000)))
        except ValueError:
            self.resize(1490, 920)

    def _build_ui(self):
        main = QWidget()
        self.setCentralWidget(main)
        layout = QVBoxLayout(main)
        layout.setSpacing(7)

        settings = QGroupBox("저장 경로 및 순차 다운로드 설정")
        sr = QVBoxLayout(settings)
        folder_row = QHBoxLayout()
        folder_row.addWidget(QLabel("저장 폴더"))
        self.root_input = QLineEdit()
        # DB가 루트에 있으므로 텍스트 직접 수정보다 안전한 폴더 선택만 허용한다.
        self.root_input.setReadOnly(True)
        self.root_input.setToolTip('폴더 전체를 다른 드라이브로 이동했다면 찾기로 새 위치를 선택하세요.')
        folder_row.addWidget(self.root_input, stretch=1)
        self.browse_btn = QPushButton("찾기")
        self.browse_btn.clicked.connect(self.browse_folder)
        folder_row.addWidget(self.browse_btn)
        open_dir_btn = QPushButton("폴더 열기")
        open_dir_btn.clicked.connect(lambda: self.open_folder(self.root_input.text()))
        folder_row.addWidget(open_dir_btn)
        db_open_btn = QPushButton('DB 폴더')
        db_open_btn.setToolTip('영상 폴더 아래 _database\\library.db가 저장되어 있습니다.')
        db_open_btn.clicked.connect(lambda: self.open_folder(str(DB_PATH.parent)))
        folder_row.addWidget(db_open_btn)
        folder_row.addWidget(QLabel("간격 (초)"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(0, 3600)
        self.interval_spin.setSuffix(" 초")
        self.interval_spin.valueChanged.connect(self.save_settings)
        folder_row.addWidget(self.interval_spin)
        sr.addLayout(folder_row)
        layout.addWidget(settings)

        add_box = QGroupBox("YouTube 영상/재생목록 주소 등록 (여러 URL은 줄바꿈으로 구분)")
        ar = QHBoxLayout(add_box)
        self.url_edit = QPlainTextEdit()
        self.url_edit.setPlaceholderText("https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/playlist?list=...")
        self.url_edit.setFixedHeight(65)
        ar.addWidget(self.url_edit, 1)
        self.add_btn = QPushButton("대기열에 추가")
        self.add_btn.setMinimumHeight(60)
        self.add_btn.clicked.connect(self.add_urls)
        ar.addWidget(self.add_btn)
        overrides_row = QHBoxLayout()
        overrides_row.addWidget(QLabel('채널 폴더명(선택)'))
        self.channel_override_input = QLineEdit()
        self.channel_override_input.setPlaceholderText('비워두면 YouTube 한국어 채널명 사용 / 예: 윤이콕TV')
        overrides_row.addWidget(self.channel_override_input, 1)
        overrides_row.addWidget(QLabel('재생목록 폴더명(선택)'))
        self.playlist_override_input = QLineEdit()
        self.playlist_override_input.setPlaceholderText('예: 물A조라고 놀리지 말아요')
        overrides_row.addWidget(self.playlist_override_input, 1)
        layout.addWidget(add_box)
        options_widget = QWidget()
        options_widget.setLayout(overrides_row)
        layout.addWidget(options_widget)

        queue_bar = QHBoxLayout()
        self.start_btn = QPushButton("▶ 다운로드 시작 / 재개")
        self.start_btn.clicked.connect(lambda: self.start_download())
        queue_bar.addWidget(self.start_btn)
        self.pause_btn = QPushButton("Ⅱ 일시정지 (현재 파일 완료 후)")
        self.pause_btn.clicked.connect(self.pause_download)
        queue_bar.addWidget(self.pause_btn)
        self.stop_btn = QPushButton("■ 즉시 중단")
        self.stop_btn.clicked.connect(self.stop_download)
        queue_bar.addWidget(self.stop_btn)
        retry_btn = QPushButton("선택 항목 다시 대기")
        retry_btn.clicked.connect(self.retry_jobs)
        queue_bar.addWidget(retry_btn)
        delete_btn = QPushButton("선택 대기열 삭제")
        delete_btn.clicked.connect(self.delete_jobs)
        queue_bar.addWidget(delete_btn)
        log_open_btn = QPushButton("로그 파일 열기")
        log_open_btn.setToolTip(str(LOG_PATH) + "\nWindows 메모장으로 다운로드 상세 로그를 엽니다.")
        log_open_btn.clicked.connect(self.open_log_file)
        queue_bar.addWidget(log_open_btn)
        queue_bar.addStretch()
        self.activity_label = QLabel("대기")
        queue_bar.addWidget(self.activity_label)
        layout.addLayout(queue_bar)
        progress_row = QHBoxLayout()
        progress_row.addWidget(QLabel('현재 영상 진행률'))
        self.current_progress = QProgressBar()
        self.current_progress.setRange(0, 1000)
        self.current_progress.setValue(0)
        self.current_progress.setFormat('%p%')
        progress_row.addWidget(self.current_progress, 1)
        layout.addLayout(progress_row)

        self.jobs_table = QTableWidget(0, 6)
        self.jobs_table.setHorizontalHeaderLabels(["번호", "상태", "진행률", "영상/재생목록", "오류/메시지", "다시받기"])
        self.jobs_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.jobs_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.jobs_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.jobs_table.verticalHeader().setVisible(False)
        self.jobs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.jobs_table.horizontalHeader().setStretchLastSection(False)
        self.jobs_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.jobs_table.setColumnWidth(3, 370)
        self.jobs_table.setColumnWidth(4, 280)
        self.jobs_table.setColumnWidth(0, 55)
        self.jobs_table.setColumnWidth(1, 100)
        self.jobs_table.setColumnWidth(2, 85)
        self.jobs_table.setColumnWidth(5, 110)
        self.jobs_table.setMinimumHeight(130)

        bottom = QSplitter(Qt.Orientation.Horizontal)
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        lib_bar = QHBoxLayout()
        lib_bar.addWidget(QLabel("영상 라이브러리"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("제목 / 채널 / 메모 / 태그 / 분류 / 영상 ID 검색")
        self.search_input.textChanged.connect(self.refresh_library)
        lib_bar.addWidget(self.search_input, 1)
        self.channel_combo = QComboBox()
        self.channel_combo.setMinimumWidth(140)
        self.channel_combo.currentIndexChanged.connect(self.refresh_library)
        lib_bar.addWidget(self.channel_combo)
        self.category_filter = QComboBox()
        self.category_filter.addItems(['전체 분류', *BADMINTON_CATEGORIES.keys()])
        self.category_filter.currentIndexChanged.connect(self.refresh_library)
        lib_bar.addWidget(self.category_filter)
        self.thumbnail_btn = QPushButton('누락 썸네일 받기')
        self.thumbnail_btn.setToolTip('기존 영상은 다시 받지 않고 누락된 JPG 썸네일만 3초 간격으로 내려받습니다.')
        self.thumbnail_btn.clicked.connect(self.start_thumbnail_backfill)
        lib_bar.addWidget(self.thumbnail_btn)
        self.thumbnail_stop_btn = QPushButton('썸네일 중단')
        self.thumbnail_stop_btn.clicked.connect(self.stop_thumbnail_backfill)
        self.thumbnail_stop_btn.setEnabled(False)
        lib_bar.addWidget(self.thumbnail_stop_btn)
        scan_btn = QPushButton('폴더 다시 검색')
        scan_btn.clicked.connect(lambda: self.scan_library(auto=False))
        lib_bar.addWidget(scan_btn)
        ll.addLayout(lib_bar)
        manage_bar = QHBoxLayout()
        self.show_missing = QCheckBox('누락 영상도 표시')
        self.show_missing.toggled.connect(self.refresh_library)
        manage_bar.addWidget(self.show_missing)
        for label, callback in (('파일 이동', self.move_current_media),
                                ('한글 제목/파일명 변경', self.rename_current_media),
                                ('영상 휴지통 삭제', self.trash_current_media)):
            button = QPushButton(label)
            button.clicked.connect(callback)
            manage_bar.addWidget(button)
        manage_bar.addStretch()
        ll.addLayout(manage_bar)
        self.library_table = QTableWidget(0, 11)
        self.library_table.setHorizontalHeaderLabels(
            ["썸네일", "제목", "채널", "재생목록", "재생시간", "대분류", "세부분류",
             "크기", "업로드일", "메모", "파일"])
        self.library_table.verticalHeader().setVisible(False)
        self.library_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.library_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.library_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # 모든 열을 드래그로 조절 가능하게 하고 열 너비는 종료시 저장한다.
        self.library_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.library_table.horizontalHeader().setStretchLastSection(False)
        self.library_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.library_table.setIconSize(QSize(112, 64))
        self.library_table.verticalHeader().setDefaultSectionSize(72)
        for i, width in enumerate((130, 310, 115, 180, 90, 130, 145, 90, 105, 55, 100)):
            self.library_table.setColumnWidth(i, width)
        self.library_table.verticalScrollBar().valueChanged.connect(self.schedule_visible_thumbnails)
        self.library_table.horizontalScrollBar().valueChanged.connect(self.schedule_visible_thumbnails)
        self.library_table.itemSelectionChanged.connect(self.on_video_selected)
        self.library_table.cellDoubleClicked.connect(lambda _r, _c: self.play_current())
        ll.addWidget(self.library_table)
        bottom.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(4, 0, 0, 0)
        info_row = QHBoxLayout()
        self.preview_thumb = QLabel('썸네일 없음')
        self.preview_thumb.setFixedSize(170, 96)
        self.preview_thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_thumb.setStyleSheet('background:#242424;color:#bdbdbd;border:1px solid #666;')
        info_row.addWidget(self.preview_thumb)
        self.video_info_label = QLabel("라이브러리에서 영상을 선택하세요")
        self.video_info_label.setWordWrap(True)
        info_row.addWidget(self.video_info_label, 1)
        rl.addLayout(info_row)
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(215)
        rl.addWidget(self.video_widget, 3)
        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)
        self.audio.setMuted(False)
        self.audio.setVolume(0.7)
        self.player.tracksChanged.connect(self.ensure_audio_track)
        self.player.positionChanged.connect(self.on_position)
        self.player.durationChanged.connect(self.on_duration)
        self.player.errorOccurred.connect(self.on_player_error)
        self.player.mediaStatusChanged.connect(self.on_media_status)
        self.player.seekableChanged.connect(lambda _ok: self._apply_pending_seek())
        self.subtitle_now = QLabel("")
        self.subtitle_now.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_now.setWordWrap(True)
        self.subtitle_now.setMinimumHeight(42)
        rl.addWidget(self.subtitle_now)
        controls = QHBoxLayout()
        self.play_pause_btn = QPushButton('▶ 재생')
        self.play_pause_btn.setToolTip('재생 중에는 일시정지, 일시정지 중에는 재생')
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        controls.addWidget(self.play_pause_btn)
        stop_play_btn = QPushButton('■ 정지')
        stop_play_btn.clicked.connect(self.player.stop)
        controls.addWidget(stop_play_btn)
        self.player.playbackStateChanged.connect(self.update_play_button)
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setRange(0, 0)
        self.time_slider.sliderPressed.connect(lambda: setattr(self, "_seeking", True))
        self.time_slider.sliderReleased.connect(self.seek_slider)
        controls.addWidget(self.time_slider, 1)
        self.time_label = QLabel("00:00:00 / 00:00:00")
        controls.addWidget(self.time_label)
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "2.0x"])
        self.speed_combo.setCurrentText("1.0x")
        self.speed_combo.currentTextChanged.connect(lambda s: self.player.setPlaybackRate(float(s[:-1])))
        controls.addWidget(self.speed_combo)
        rl.addLayout(controls)
        external_row = QHBoxLayout()
        external_btn = QPushButton("기본 플레이어로 열기")
        external_btn.clicked.connect(self.open_external)
        external_row.addWidget(external_btn)
        folder_btn = QPushButton("파일 폴더 열기")
        folder_btn.clicked.connect(self.open_media_folder)
        external_row.addWidget(folder_btn)
        external_row.addWidget(QLabel("음량"))
        self.mute_btn = QPushButton('🔊')
        self.mute_btn.setToolTip('음소거 켜기/끄기')
        self.mute_btn.clicked.connect(self.toggle_mute)
        external_row.addWidget(self.mute_btn)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.valueChanged.connect(self.change_volume)
        external_row.addWidget(self.volume_slider)
        rl.addLayout(external_row)
        audio_row = QHBoxLayout()
        audio_row.addWidget(QLabel('소리 출력 장치'))
        self.audio_device_combo = QComboBox()
        self.audio_device_combo.setMinimumWidth(150)
        self.audio_device_combo.setToolTip('소리가 나오지 않으면 스피커/헤드셋 출력 장치를 직접 선택하세요.')
        self.audio_device_combo.currentIndexChanged.connect(self.change_audio_device)
        audio_row.addWidget(self.audio_device_combo, 1)
        refresh_audio_btn = QPushButton('장치 새로고침')
        refresh_audio_btn.clicked.connect(self.setup_audio_devices)
        audio_row.addWidget(refresh_audio_btn)
        audio_diag_btn = QPushButton('소리 진단')
        audio_diag_btn.clicked.connect(self.diagnose_audio)
        audio_row.addWidget(audio_diag_btn)
        rl.addLayout(audio_row)
        tabs = QTabWidget()
        memo_tab = QWidget()
        ml = QVBoxLayout(memo_tab)
        self.memo_edit = QTextEdit()
        self.memo_edit.setPlaceholderText("이 영상의 스윙 포인트, 자세 수정 사항, 분석 메모 등을 작성하세요.")
        ml.addWidget(self.memo_edit)
        save_btn = QPushButton("메모 저장 (영상 전환 시에도 자동 저장)")
        save_btn.clicked.connect(self.save_memo)
        ml.addWidget(save_btn)
        tabs.addTab(memo_tab, "영상 메모")
        category_tab = QWidget()
        cat_layout = QVBoxLayout(category_tab)
        cat_layout.addWidget(QLabel('영상별 기술 분류 (여러 특징은 태그로 함께 기록)'))
        row_major = QHBoxLayout()
        row_major.addWidget(QLabel('대분류'))
        self.major_combo = QComboBox()
        self.major_combo.addItems(list(BADMINTON_CATEGORIES))
        self.major_combo.currentTextChanged.connect(self.on_major_changed)
        row_major.addWidget(self.major_combo, 1)
        cat_layout.addLayout(row_major)
        row_sub = QHBoxLayout()
        row_sub.addWidget(QLabel('세부분류'))
        self.sub_combo = QComboBox()
        self.sub_combo.currentTextChanged.connect(self.save_classification)
        row_sub.addWidget(self.sub_combo, 1)
        cat_layout.addLayout(row_sub)
        cat_layout.addWidget(QLabel('태그 (쉼표로 구분: 예: 복식, 스매시, 전위, 초보자)'))
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText('스매시, 복식, 발놀림, 중요구간')
        self.tags_edit.editingFinished.connect(self.save_classification)
        cat_layout.addWidget(self.tags_edit)
        save_cat = QPushButton('분류·태그 저장')
        save_cat.clicked.connect(self.save_classification)
        cat_layout.addWidget(save_cat)
        cat_layout.addStretch()
        tabs.addTab(category_tab, '배드민턴 분류·태그')
        segment_tab = QWidget()
        seg_layout = QVBoxLayout(segment_tab)
        seg_layout.addWidget(QLabel('향후 클립 제작용 구간 표시 (현재 버전은 실제 영상 자르기 미지원)'))
        seg_buttons = QHBoxLayout()
        start_btn = QPushButton('현재 시각 → 시작점')
        start_btn.clicked.connect(self.mark_start)
        seg_buttons.addWidget(start_btn)
        end_btn = QPushButton('현재 시각 → 종료점')
        end_btn.clicked.connect(self.mark_end)
        seg_buttons.addWidget(end_btn)
        seg_layout.addLayout(seg_buttons)
        self.mark_info = QLabel('시작 - / 끝 -')
        seg_layout.addWidget(self.mark_info)
        self.mark_title = QLineEdit()
        self.mark_title.setPlaceholderText('구간명 (예: 스매시 타점 잡는 법)')
        seg_layout.addWidget(self.mark_title)
        save_mark_btn = QPushButton('구간 후보 저장')
        save_mark_btn.clicked.connect(self.save_clip_mark)
        seg_layout.addWidget(save_mark_btn)
        self.clip_list = QListWidget()
        self.clip_list.itemDoubleClicked.connect(self.play_clip_mark)
        seg_layout.addWidget(self.clip_list)
        seg_manage = QHBoxLayout()
        clip_play_btn = QPushButton('구간 시작 재생')
        clip_play_btn.clicked.connect(self.play_clip_mark)
        seg_manage.addWidget(clip_play_btn)
        clip_del_btn = QPushButton('선택 구간 삭제')
        clip_del_btn.clicked.connect(self.delete_clip_mark)
        seg_manage.addWidget(clip_del_btn)
        seg_layout.addLayout(seg_manage)
        tabs.addTab(segment_tab, '클립 구간 기록')
        sub_tab = QWidget()
        sl = QVBoxLayout(sub_tab)
        self.subtitle_combo = QComboBox()
        self.subtitle_combo.currentIndexChanged.connect(self.load_selected_subtitles)
        sl.addWidget(self.subtitle_combo)
        sub_tools = QHBoxLayout()
        sub_tools.addWidget(QLabel('자막 줄 더블클릭 = 해당 구간 재생'))
        self.subtitle_count_label = QLabel('자막 0개')
        sub_tools.addWidget(self.subtitle_count_label)
        sub_tools.addStretch()
        self.subtitle_search = QLineEdit()
        self.subtitle_search.setPlaceholderText('자막 검색')
        self.subtitle_search.textChanged.connect(self.filter_subtitles)
        sub_tools.addWidget(self.subtitle_search)
        popup_btn = QPushButton('전체 자막 큰창')
        popup_btn.clicked.connect(self.show_full_subtitles)
        sub_tools.addWidget(popup_btn)
        sl.addLayout(sub_tools)
        self.subtitle_list = QListWidget()
        self.subtitle_list.setWordWrap(True)
        self.subtitle_list.itemDoubleClicked.connect(self.subtitle_jump)
        sl.addWidget(self.subtitle_list)
        tabs.addTab(sub_tab, "전체 자막 / 구간 이동")
        rl.addWidget(tabs, 2)
        bottom.addWidget(right)
        bottom.setSizes([730, 710])

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumBlockCount(5000)
        self.log_box.setFont(QFont("Consolas", 9))
        self.log_box.setMinimumHeight(82)
        outer = QSplitter(Qt.Orientation.Vertical)
        outer.addWidget(self.jobs_table)
        outer.addWidget(bottom)
        outer.addWidget(self.log_box)
        outer.setSizes([195, 520, 110])
        layout.addWidget(outer, 1)
        self.outer_splitter = outer
        self.inner_splitter = bottom
        self.statusBar().showMessage("동시 다운로드 1개 · 메모와 파일은 로컬에 저장됩니다")

    def _load_settings(self):
        self.root_input.setText(str(ACTIVE_ROOT))
        self.interval_spin.setValue(int(get_setting(self.db, "interval", "20")))
        self.volume_slider.setValue(max(0, min(100, int(get_setting(self.db, 'audio_volume', '70')))))
        self.audio.setMuted(get_setting(self.db, 'audio_muted', '0') == '1')
        self.mute_btn.setText('🔇' if self.audio.isMuted() else '🔊')
        try:
            sizes = json.loads(get_setting(self.db, "split_outer", "[]"))
            if len(sizes) == 3:
                self.outer_splitter.setSizes(sizes)
            sizes = json.loads(get_setting(self.db, "split_inner", "[]"))
            if len(sizes) == 2:
                self.inner_splitter.setSizes(sizes)
        except (ValueError, TypeError):
            pass
        for table, key in ((self.library_table, 'library_col_widths'),
                           (self.jobs_table, 'jobs_col_widths')):
            try:
                sizes = json.loads(get_setting(self.db, key, '[]'))
                if table is self.jobs_table and len(sizes) == 5:
                    # V1.3 다운로드 열 너비 설정은 유지하고 새 다시받기 열만 추가.
                    sizes = [*sizes, 110]
                if table is self.library_table and len(sizes) == 8:
                    # V1.2 제목/채널/분류/크기/업로드일/메모/파일 컬럼 이동
                    sizes = [130, sizes[0], sizes[1], 180, 90, sizes[2], sizes[3],
                             sizes[4], sizes[5], sizes[6], sizes[7]]
                if len(sizes) == table.columnCount():
                    for i, n in enumerate(sizes):
                        table.setColumnWidth(i, max(45, min(2000, int(n))))
            except (ValueError, TypeError):
                pass

    def save_settings(self):
        if not hasattr(self, "db"):
            return
        # 선택된 루트는 파일 경로 힌트와 DB 모두에서 일치해야 한다.
        set_setting(self.db, "download_root", str(ACTIVE_ROOT))
        set_setting(self.db, "interval", str(self.interval_spin.value()))
        if hasattr(self, 'volume_slider'):
            set_setting(self.db, 'audio_volume', str(self.volume_slider.value()))
            set_setting(self.db, 'audio_muted', '1' if self.audio.isMuted() else '0')

    def browse_folder(self):
        if ((self.worker and self.worker.isRunning()) or (self.scanner and self.scanner.isRunning())
                or (self.thumbnail_worker and self.thumbnail_worker.isRunning())):
            QMessageBox.warning(self, '라이브러리 변경', '다운로드/검색 작업 종료 후 라이브러리 위치를 변경하세요.')
            return
        folder = QFileDialog.getExistingDirectory(self, '이동한 minton.youtube 루트 폴더 선택',
                                                  self.root_input.text().strip())
        if not folder or Path(folder).resolve() == ACTIVE_ROOT:
            return
        target = Path(folder).resolve()
        target_db = target / '_database' / 'library.db'
        copy_current_db = False
        if not target_db.exists():
            reply = QMessageBox.question(
                self, '새 라이브러리 위치',
                '선택한 폴더에 _database\\library.db가 없습니다.\n\n'
                '예: 현재 DB(메모·분류·작업)를 복사해 새 위치에서 사용합니다.\n'
                '아니요: 이 폴더에 완전히 새로운 라이브러리를 만듭니다.\n'
                '취소: 변경하지 않습니다.\n\n'
                '중요: DB 복사는 실제 영상 파일을 이동하지 않습니다.',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Cancel:
                return
            copy_current_db = reply == QMessageBox.StandardButton.Yes
        self.save_memo(silent=True)
        self.save_classification(silent=True)
        self.player.stop()
        self.player.setSource(QUrl())
        old_root, old_db = ACTIVE_ROOT, DB_PATH
        try:
            if copy_current_db:
                copy_sqlite_database(DB_PATH, target_db)
            self.db.close()
            set_library_root(target)
            init_db(migrate_old=False)
            self.db = connect_db()
        except Exception as ex:
            set_library_root(old_root)
            self.db = connect_db()
            self.add_log(f'[라이브러리 전환 오류] {ex}')
            QMessageBox.critical(self, '라이브러리 전환 실패', str(ex))
            return
        self.current_id = None
        self.current_path = None
        self._last_missing.clear()
        self._thumbnail_cache.clear()
        self._row_thumbnail_paths.clear()
        self.update_thumbnail_preview()
        self.root_input.setText(str(ACTIVE_ROOT))
        self.memo_edit.clear()
        self.tags_edit.clear()
        self.clip_list.clear()
        self._load_settings()
        self.refresh_jobs()
        self.refresh_library()
        self.scan_library()
        self.add_log(f'[라이브러리 전환] {old_root} -> {ACTIVE_ROOT} | DB: {DB_PATH}')

    def add_log(self, message: str):
        LOGGER.info(message)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.appendPlainText(f"[{timestamp}] {message}")

    def setup_audio_devices(self):
        """Windows 기본 출력과 실제 사운드 장치를 열거한다."""
        previous = get_setting(self.db, 'audio_device_id', '')
        self.audio_device_combo.blockSignals(True)
        self.audio_device_combo.clear()
        devices = QMediaDevices.audioOutputs()
        self._audio_devices = devices
        for device in devices:
            device_id = bytes(device.id()).hex()
            self.audio_device_combo.addItem(device.description(), device_id)
        index = self.audio_device_combo.findData(previous) if previous else -1
        if index < 0 and devices:
            default_device = QMediaDevices.defaultAudioOutput()
            default_id = bytes(default_device.id()).hex()
            index = self.audio_device_combo.findData(default_id)
        if devices:
            self.audio_device_combo.setCurrentIndex(max(0, index))
            self.audio.setDevice(devices[self.audio_device_combo.currentIndex()])
            self.add_log('[오디오 장치] ' + self.audio.device().description())
        else:
            self.add_log('[오디오 경고] Qt에서 사용 가능한 오디오 출력 장치를 찾지 못했습니다')
        self.audio_device_combo.blockSignals(False)

    def change_audio_device(self, idx):
        if 0 <= idx < len(getattr(self, '_audio_devices', [])):
            device = self._audio_devices[idx]
            self.audio.setDevice(device)
            set_setting(self.db, 'audio_device_id', bytes(device.id()).hex())
            self.add_log(f'[오디오 출력 변경] {device.description()}')
            if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                self.player.play()

    def change_volume(self, value):
        self.audio.setVolume(max(0.0, min(1.0, value / 100)))
        if value and self.audio.isMuted():
            self.audio.setMuted(False)
            self.mute_btn.setText('🔊')
        if hasattr(self, 'db'):
            set_setting(self.db, 'audio_volume', str(value))
            set_setting(self.db, 'audio_muted', '1' if self.audio.isMuted() else '0')

    def toggle_mute(self):
        self.audio.setMuted(not self.audio.isMuted())
        self.mute_btn.setText('🔇' if self.audio.isMuted() else '🔊')
        set_setting(self.db, 'audio_muted', '1' if self.audio.isMuted() else '0')
        self.add_log('[오디오 음소거] ' + ('켜짐' if self.audio.isMuted() else '해제'))

    def ensure_audio_track(self):
        tracks = self.player.audioTracks()
        if tracks and self.player.activeAudioTrack() < 0:
            self.player.setActiveAudioTrack(0)
            self.add_log(f'[오디오 트랙 선택] 1/{len(tracks)}')

    def diagnose_audio(self):
        """무음 문제를 구분해 로그와 팝업에 표시한다. 영상 자체는 건드리지 않는다."""
        track_count = len(self.player.audioTracks())
        active = self.player.activeAudioTrack()
        device_name = self.audio.device().description()
        details = [f'현재 출력 장치: {device_name or "없음"}',
                   f'Qt 감지 오디오 트랙: {track_count}개 / 선택: {active}',
                   f'음량: {int(self.audio.volume() * 100)}% / 음소거: {self.audio.isMuted()}',
                   f'Qt 미디어 상태: {self.player.mediaStatus().name}',
                   f'Qt 오류: {self.player.errorString() or "없음"}']
        if self.current_path and self.current_path.is_file() and shutil.which('ffprobe'):
            try:
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-select_streams', 'a',
                     '-show_entries', 'stream=codec_name,channels,sample_rate',
                     '-of', 'json', str(self.current_path)], capture_output=True, text=True,
                    encoding='utf-8', errors='replace', timeout=12, **popen_flags())
                streams = json.loads(result.stdout or '{}').get('streams', []) if result.returncode == 0 else []
                if streams:
                    details.append('ffprobe 오디오: ' + ', '.join(
                        f"{t.get('codec_name', '?')} {t.get('channels', '?')}채널" for t in streams))
                else:
                    details.append('ffprobe 오디오 트랙: 없음 (원본에 소리가 없을 수 있음)')
            except (OSError, subprocess.TimeoutExpired, ValueError) as ex:
                details.append(f'ffprobe 진단 실패: {ex}')
        details.append('조치: 음소거 해제 → 음량 올리기 → 다른 출력 장치 선택 → Windows 볼륨 믹서 확인')
        if track_count == 0:
            details.append('MP4에 음성이 있지만 Qt 트랙이 0개라면 PySide6 업데이트/FFmpeg 백엔드를 점검하세요.')
        self.add_log('[소리 진단] ' + ' | '.join(details))
        QMessageBox.information(self, '영상 소리 진단', '\n'.join(details))

    def toggle_play_pause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.play_current()

    def update_play_button(self, _state=None):
        playing = self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
        self.play_pause_btn.setText('Ⅱ 일시정지' if playing else '▶ 재생')
        self.play_pause_btn.setToolTip('재생 일시정지' if playing else '재생 또는 이어서 재생')

    def schedule_visible_thumbnails(self, _value=None):
        self._thumbnail_visible_timer.start(70)

    def cached_thumbnail_icon(self, path: Path) -> QIcon | None:
        try:
            stat = path.stat()
            key = str(path)
            cached = self._thumbnail_cache.get(key)
            if cached and cached[0] == stat.st_mtime_ns:
                self._thumbnail_cache.move_to_end(key)
                return cached[1]
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                return None
            icon = QIcon(pixmap.scaled(112, 64, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation))
            self._thumbnail_cache[key] = (stat.st_mtime_ns, icon)
            self._thumbnail_cache.move_to_end(key)
            while len(self._thumbnail_cache) > 160:
                self._thumbnail_cache.popitem(last=False)
            return icon
        except OSError:
            return None

    def refresh_visible_thumbnails(self):
        table = self.library_table
        if not self._row_thumbnail_paths or not table.rowCount():
            return
        first = max(0, table.rowAt(0))
        last = table.rowAt(max(0, table.viewport().height() - 1))
        if last < 0:
            last = min(table.rowCount() - 1, first + 15)
        for row_idx in range(max(0, first - 2), min(len(self._row_thumbnail_paths), last + 3)):
            path = self._row_thumbnail_paths[row_idx]
            item = table.item(row_idx, 0)
            if item is None:
                continue
            if path and path.is_file():
                icon = self.cached_thumbnail_icon(path)
                if icon:
                    item.setIcon(icon)
                    item.setText('')
                    item.setToolTip(str(path))

    def update_thumbnail_preview(self):
        self.preview_thumb.setPixmap(QPixmap())
        self.preview_thumb.setText('썸네일 없음')
        if not self.current_path or not self.current_path.is_file():
            return
        path = find_thumbnail(self.current_path)
        if not path:
            return
        pixmap = QPixmap(str(path))
        if not pixmap.isNull():
            self.preview_thumb.setText('')
            self.preview_thumb.setPixmap(pixmap.scaled(self.preview_thumb.size(),
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def start_thumbnail_backfill(self):
        if (self.worker and self.worker.isRunning()) or (self.thumbnail_worker and self.thumbnail_worker.isRunning()):
            QMessageBox.information(self, '작업 진행 중', '영상 다운로드 또는 썸네일 작업이 끝난 뒤 실행하세요.')
            return
        tasks = []
        for rec in self.db.execute('SELECT video_id,source_url,file_path FROM videos ORDER BY channel,title'):
            try:
                media = media_path(rec['file_path'])
                if media.is_file() and is_in_directory(media, ACTIVE_ROOT) and not find_thumbnail(media):
                    tasks.append((media, rec['source_url'], rec['video_id']))
            except (OSError, ValueError) as ex:
                self.add_log(f'[썸네일 경로 건너뜀] {ex}')
        if not tasks:
            QMessageBox.information(self, '썸네일 확인', '누락된 썸네일이 없습니다.')
            return
        runnable = sum(bool(yt_video_url(url, vid)) for _, url, vid in tasks)
        if QMessageBox.question(self, '누락 썸네일 다운로드',
            f'누락된 썸네일 {len(tasks)}개 중 YouTube 주소가 확인된 {runnable}개를 이미지 전용으로 받습니다.\n'
            'MP4는 다시 다운로드하지 않으며, 영상마다 최소 3초 간격을 둡니다.\n계속할까요?') != QMessageBox.StandardButton.Yes:
            return
        self.thumbnail_worker = ThumbnailWorker(ACTIVE_ROOT, tasks, interval=3, parent=self)
        self.thumbnail_worker.message.connect(self.add_log)
        self.thumbnail_worker.progress_signal.connect(self.on_thumbnail_progress)
        self.thumbnail_worker.changed.connect(self.on_thumbnail_changed)
        self.thumbnail_worker.finished.connect(self.on_thumbnail_finished)
        self.thumbnail_btn.setEnabled(False)
        self.thumbnail_stop_btn.setEnabled(True)
        self.browse_btn.setEnabled(False)
        self.add_log(f'[누락 썸네일 다운로드 요청] 대상 {len(tasks)}개 / YouTube 주소 {runnable}개')
        self.thumbnail_worker.start()

    def on_thumbnail_progress(self, completed, total, ok):
        self.statusBar().showMessage(f'썸네일 수집 {completed}/{total} · 성공 {ok}개')

    def on_thumbnail_changed(self):
        self._thumbnail_cache.clear()
        self.refresh_library()
        self.update_thumbnail_preview()

    def stop_thumbnail_backfill(self):
        if self.thumbnail_worker and self.thumbnail_worker.isRunning():
            self.thumbnail_worker.request_stop()
            self.add_log('[썸네일 중단 요청] 현재 이미지 작업을 중단합니다')

    def on_thumbnail_finished(self):
        self.thumbnail_btn.setEnabled(True)
        self.thumbnail_stop_btn.setEnabled(False)
        self.browse_btn.setEnabled(True)
        self.on_thumbnail_changed()
        self.add_log('[썸네일 작업자 종료] 기존 MP4/메모는 변경하지 않았습니다')

    def add_urls(self):
        candidates = re.findall(r"https?://[^\s<>\"']+", self.url_edit.toPlainText())
        added, duplicate, invalid = 0, 0, 0
        channel_override = safe_name(self.channel_override_input.text(), '')
        playlist_override = safe_name(self.playlist_override_input.text(), '')
        with self.db:
            for candidate in candidates:
                parsed = canonical_url(candidate.rstrip("),;"))
                if parsed is None:
                    invalid += 1
                    continue
                url, kind = parsed
                before = self.db.total_changes
                self.db.execute('INSERT OR IGNORE INTO jobs(url,kind,title,status,created_at,updated_at,channel_override,playlist_override) '
                                'VALUES(?,?,?,?,?,?,?,?)',
                                (url, kind, url, 'queued', now_str(), now_str(), channel_override, playlist_override))
                if self.db.total_changes > before:
                    added += 1
                else:
                    duplicate += 1
        self.refresh_jobs()
        self.add_log(f'주소 등록: 신규 {added}, 중복 {duplicate}, 잘못된 주소 {invalid}')
        if channel_override or playlist_override:
            self.add_log(f'[이름 지정] 채널: {channel_override or "자동"} / 목록: {playlist_override or "자동"}')
        if not candidates:
            QMessageBox.warning(self, "주소 확인", "YouTube 영상 또는 재생목록 주소를 붙여 넣으세요.")
        elif added:
            self.url_edit.clear()

    def selected_job_ids(self) -> list[int]:
        ids = set()
        for item in self.jobs_table.selectedItems():
            target = self.jobs_table.item(item.row(), 0)
            if target:
                ids.add(int(target.text()))
        return sorted(ids)

    def open_log_file(self):
        """현재 로테이션 중인 원본 로그를 Windows 메모장으로 연다."""
        try:
            LOGGER.info('[로그 파일 열기] %s', LOG_PATH)
            if not LOG_PATH.exists():
                LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
                LOG_PATH.touch()
            if os.name == 'nt':
                subprocess.Popen(['notepad.exe', str(LOG_PATH)], **popen_flags())
            elif not QDesktopServices.openUrl(QUrl.fromLocalFile(str(LOG_PATH))):
                raise RuntimeError('기본 텍스트 편집기로 로그를 열지 못했습니다')
            self.add_log(f'[로그 파일 열기] {LOG_PATH}')
        except (OSError, RuntimeError) as ex:
            self.add_log(f'[로그 파일 열기 실패] {type(ex).__name__}: {ex}')
            QMessageBox.warning(self, '로그 파일 열기 실패', f'{LOG_PATH}\n\n{ex}')

    def retry_failed_job(self, job_id: int):
        """실패 항목 1개만 재시도. 기존 대기열에 영향을 주지 않는다."""
        job = self.db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
        if not job or job['status'] != 'failed':
            QMessageBox.information(self, '다시받기', '현재 실패 상태인 작업만 다시 받을 수 있습니다.')
            self.refresh_jobs()
            return
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, '다운로드 중', '현재 다운로드를 끝내거나 중단한 뒤 실패 항목을 다시받으세요.')
            return
        if self.thumbnail_worker and self.thumbnail_worker.isRunning():
            QMessageBox.information(self, '썸네일 작업 중', '누락 썸네일 작업을 먼저 종료해 주세요.')
            return
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle(f'#{job_id} 실패 작업 다시받기')
        box.setText(f"이 작업 1개만 다시 다운로드합니다.\n\n{job['title'] or job['url']}")
        box.setInformativeText(
            '한국어 자동자막 HTTP 429 오류라면 「자막 제외하고 영상만」을 권장합니다.\n'
            '자막 제외 모드에서는 기존 자막을 삭제하지 않으며 MP4·썸네일·정보 파일은 다운로드합니다.\n'
            '반복적인 429 요청은 제한을 악화시킬 수 있으니 재시도 간 충분히 시간을 두세요.')
        full_btn = box.addButton('영상+자막 다시받기', QMessageBox.ButtonRole.AcceptRole)
        no_sub_btn = None
        if job['kind'] == 'video':
            no_sub_btn = box.addButton('자막 제외하고 영상만', QMessageBox.ButtonRole.ActionRole)
        box.addButton(QMessageBox.StandardButton.Cancel)
        # 실제 이전 실패 사유에 429가 남아 있다면 원인을 피하는 옵션을 강조.
        if no_sub_btn and '429' in str(job['error']):
            box.setDefaultButton(no_sub_btn)
        else:
            box.setDefaultButton(full_btn)
        box.exec()
        button = box.clickedButton()
        if button is not full_btn and button is not no_sub_btn:
            return
        without_subs = bool(no_sub_btn and button is no_sub_btn)
        with self.db:
            updated = self.db.execute(
                "UPDATE jobs SET status='queued', progress=0, error='',retry_without_subs=?,updated_at=? "
                "WHERE id=? AND status='failed'",
                (1 if without_subs else 0, now_str(), job_id)).rowcount
        if not updated:
            self.refresh_jobs()
            return
        mode = '자막 제외 / 영상만' if without_subs else '원래 영상·자막 옵션'
        self.add_log(f'[개별 재시도 예약] #{job_id} / {mode} / 나머지 대기열 유지')
        self.refresh_jobs()
        self.start_download(only_job_id=job_id)

    def retry_jobs(self):
        ids = self.selected_job_ids()
        if not ids:
            return
        with self.db:
            for job_id in ids:
                self.db.execute("UPDATE jobs SET status='queued',progress=0,error='',retry_without_subs=0,updated_at=? "
                                "WHERE id=? AND status<>'running'", (now_str(), job_id))
        self.add_log(f"대기 상태로 복원: {len(ids)}개")
        self.refresh_jobs()

    def delete_jobs(self):
        ids = self.selected_job_ids()
        if not ids:
            return
        running = self.db.execute("SELECT COUNT(*) FROM jobs WHERE id IN (" + ",".join("?" * len(ids)) + ") AND status='running'", ids).fetchone()[0]
        if running:
            QMessageBox.warning(self, "작업 진행 중", "다운로드 중인 항목은 먼저 중단한 후 삭제하세요.")
            return
        if QMessageBox.question(self, "대기열에서 삭제", f"선택한 {len(ids)}개 작업만 삭제할까요?\n저장된 동영상과 메모는 삭제하지 않습니다.") != QMessageBox.StandardButton.Yes:
            return
        with self.db:
            self.db.executemany("DELETE FROM jobs WHERE id=?", [(x,) for x in ids])
        self.add_log(f"대기열 항목 {len(ids)}개 삭제 (원본 파일 유지)")
        self.refresh_jobs()

    def refresh_jobs(self):
        if not hasattr(self, 'jobs_table'):
            return
        selected = set(self.selected_job_ids())
        rows = self.db.execute('SELECT * FROM jobs ORDER BY id DESC LIMIT 1000').fetchall()
        table = self.jobs_table
        table.blockSignals(True)
        table.setRowCount(len(rows))
        status_text = {'queued': '대기', 'running': '다운로드 중', 'done': '완료',
                       'failed': '실패', 'expanded': '목록 등록'}
        active = None
        for i, job in enumerate(rows):
            vals = [str(job['id']), status_text.get(job['status'], job['status']),
                    '', job['title'] or job['url'], job['error']]
            if job['playlist_title'] and job['kind'] == 'video':
                vals[3] = f"[{job['playlist_channel']} / {job['playlist_title']}] {vals[3]}"
            for col, val in enumerate(vals):
                it = QTableWidgetItem(str(val))
                it.setToolTip(str(val) if col != 3 else f"{vals[3]}\n{job['url']}")
                table.setItem(i, col, it)
            bar = QProgressBar(table)
            bar.setRange(0, 1000)
            bar.setValue(int(float(job['progress']) * 10))
            bar.setFormat(f"{float(job['progress']):.1f}%")
            table.setCellWidget(i, 2, bar)
            # 버튼은 실패 행에서만 표시하며, ID를 바인딩하여 잘못된 행을 재시도하지 않음.
            if job['status'] == 'failed':
                retry_button = QPushButton('↻ 다시받기', table)
                retry_button.setToolTip('이 실패 작업 1개만 다시받기 (영상+자막 / 자막 제외 선택)')
                retry_button.clicked.connect(lambda _checked=False, target_id=int(job['id']):
                                             self.retry_failed_job(target_id))
                table.setCellWidget(i, 5, retry_button)
            else:
                table.removeCellWidget(i, 5)
            if job['status'] == 'running':
                active = job
            if job['id'] in selected:
                table.selectRow(i)
        table.blockSignals(False)
        if active is not None:
            self.current_progress.setValue(int(float(active['progress']) * 10))
            self.current_progress.setFormat(f"{float(active['progress']):.1f}%")
        else:
            # 끝난/실패한 작업의 이전 100% 수치가 현재 진행률에 남지 않게 한다.
            self.current_progress.setValue(0)
            self.current_progress.setFormat('0.0%')

    def on_worker_progress(self, job_id, progress):
        # 기존 동작처럼 테이블 전체 재구성 없이 진행률만 업데이트한다.
        self.current_progress.setValue(int(max(0, min(100, progress)) * 10))
        self.current_progress.setFormat(f'{progress:.1f}%')
        for row in range(self.jobs_table.rowCount()):
            item = self.jobs_table.item(row, 0)
            if item and item.text() == str(job_id):
                bar = self.jobs_table.cellWidget(row, 2)
                if isinstance(bar, QProgressBar):
                    bar.setValue(int(progress * 10))
                    bar.setFormat(f'{progress:.1f}%')
                break

    def start_download(self, only_job_id: int | None = None):
        if self.thumbnail_worker and self.thumbnail_worker.isRunning():
            QMessageBox.information(self, '썸네일 작업 중', '누락 썸네일 작업을 중단하거나 끝낸 뒤 다운로드하세요.')
            return
        if self.worker and self.worker.isRunning():
            self.worker.request_resume()
            self.add_log("[재개] 현재 작업부터 진행")
            return
        cmd = yt_command()
        missing = []
        if not cmd:
            missing.append("yt-dlp: .venv에서 pip install -U 'yt-dlp[default]'")
        if not shutil.which("deno"):
            missing.append("Deno: winget install DenoLand.Deno")
        if not shutil.which("ffmpeg"):
            missing.append("FFmpeg: winget install Gyan.FFmpeg")
        if missing:
            QMessageBox.warning(self, "필수 실행환경 확인", "다음 프로그램을 설치하고 새 PowerShell에서 실행하세요:\n\n" + "\n".join(missing))
            return
        root = self.root_input.text().strip()
        if not root:
            QMessageBox.warning(self, "경로 오류", "다운로드 폴더를 지정하세요.")
            return
        if only_job_id is not None:
            pending = self.db.execute("SELECT 1 FROM jobs WHERE status='queued' AND id=?",
                                      (only_job_id,)).fetchone()
        else:
            pending = self.db.execute("SELECT 1 FROM jobs WHERE status='queued' LIMIT 1").fetchone()
        if not pending:
            QMessageBox.information(self, "대기열 없음", "영상 주소를 먼저 추가하거나 선택 항목을 다시 대기시켜 주세요.")
            return
        try:
            Path(root).mkdir(parents=True, exist_ok=True)
        except OSError as ex:
            QMessageBox.critical(self, "저장 경로 오류", str(ex))
            return
        self.save_settings()
        self.root_input.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.interval_spin.setEnabled(False)
        self.worker = DownloadWorker(root, self.interval_spin.value(), self, only_job_id=only_job_id)
        self.worker.message.connect(self.add_log)
        self.worker.changed.connect(self.on_worker_changed)
        self.worker.activity.connect(self.activity_label.setText)
        self.worker.progress_signal.connect(self.on_worker_progress)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def pause_download(self):
        if self.worker and self.worker.isRunning():
            self.worker.request_pause()
            self.add_log("[일시정지 요청] 현재 영상이 끝나면 다음 작업 전 중지")

    def stop_download(self):
        if self.worker and self.worker.isRunning():
            self.worker.request_stop()
            self.add_log("[즉시 중단 요청] 현재 다운로드는 .part로 남을 수 있습니다")

    def on_worker_changed(self):
        self.refresh_jobs()
        self.refresh_library()
        self.update_thumbnail_preview()

    def on_worker_finished(self):
        self.root_input.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.interval_spin.setEnabled(True)
        self.refresh_jobs()
        self.refresh_library()
        self.add_log("다운로드 작업자 종료")

    def scan_library(self, auto=False):
        if auto and self.worker and self.worker.isRunning():
            return
        if self.scanner and self.scanner.isRunning():
            return
        root = self.root_input.text().strip()
        if not root:
            return
        known_durations = {r['file_path']: int(r['duration'] or 0) for r in
                           self.db.execute('SELECT file_path,duration FROM videos WHERE duration>0')}
        self.scanner = ScanWorker(root, known_durations, self)
        self.scanner.message.connect(self.add_log)
        self.scanner.finished_scan.connect(lambda records: self.on_scan_finished(records, auto))
        self.scanner.start()
        self.statusBar().showMessage("다운로드 폴더의 기존 영상을 검색 중...")

    def on_scan_finished(self, records, auto=False):
        moved = 0
        for record in records:
            old = self.db.execute('SELECT file_path FROM videos WHERE video_id=?', (record['video_id'],)).fetchone()
            try:
                resolved_id = upsert_video(self.db, record)
                if resolved_id != record['video_id']:
                    old = self.db.execute('SELECT file_path FROM videos WHERE video_id=?',
                                          (resolved_id,)).fetchone()
                if old and old['file_path'] != record['file_path']:
                    moved += 1
                if (resolved_id == self.current_id and self.current_path is not None
                        and self.current_path != media_path(record['file_path'])):
                    self.current_path = media_path(record['file_path'])
                    self.player.stop()
                    self.player.setSource(QUrl.fromLocalFile(str(self.current_path)))
                    self.find_subtitle_files()
                    self.update_thumbnail_preview()
                    self.add_log(f'[현재 영상 경로 연결] {self.current_path}')
            except (sqlite3.Error, OSError) as ex:
                self.add_log(f"[색인 오류] {record.get('file_path','')}: {ex}")
        self.statusBar().showMessage(f"폴더 검색 완료: {len(records)}개 영상 확인")
        if not auto or moved:
            self.add_log(f'[라이브러리 검색] 영상 {len(records)}개 확인, 기존 메모 유지; 이동 감지 {moved}개')
        self.refresh_library()

    def refresh_library(self):
        if not hasattr(self, 'library_table'):
            return
        current_channel = self.channel_combo.currentText()
        all_channels = [r[0] for r in self.db.execute('SELECT DISTINCT channel FROM videos ORDER BY channel')]
        if self.channel_combo.count() != len(all_channels) + 1 or [self.channel_combo.itemText(i) for i in range(1, self.channel_combo.count())] != all_channels:
            self.channel_combo.blockSignals(True)
            self.channel_combo.clear()
            self.channel_combo.addItem('전체 채널')
            self.channel_combo.addItems(all_channels)
            index = self.channel_combo.findText(current_channel)
            self.channel_combo.setCurrentIndex(index if index >= 0 else 0)
            self.channel_combo.blockSignals(False)
        text = f'%{self.search_input.text().strip()}%'
        channel = self.channel_combo.currentText()
        filters = ('WHERE (title LIKE ? OR title_override LIKE ? OR channel LIKE ? OR memo LIKE ? '
                   'OR video_id LIKE ? OR major_category LIKE ? OR sub_category LIKE ? OR tags LIKE ?)')
        params = [text] * 8
        if channel != '전체 채널':
            filters += ' AND channel=?'
            params.append(channel)
        category = self.category_filter.currentText()
        if category != '전체 분류':
            filters += ' AND major_category=?'
            params.append(category)
        rows = self.db.execute(f"""SELECT video_id,title,title_override,channel,upload_date,memo,file_path,
            file_size,major_category,sub_category,tags,playlist_title,duration
            FROM videos {filters} ORDER BY upload_date DESC,title LIMIT 10000""", params).fetchall()
        table = self.library_table
        table.blockSignals(True)
        visible = []
        missing = set()
        root = Path(self.root_input.text().strip())
        for rec in rows:
            try:
                path = media_path(rec['file_path'])
                present = path.is_file() and is_in_directory(path, root)
                bytes_used = path.stat().st_size if present else int(rec['file_size'] or 0)
            except (OSError, ValueError):
                present, bytes_used = False, int(rec['file_size'] or 0)
            if not present:
                missing.add(rec['video_id'])
                if not self.show_missing.isChecked():
                    continue
            visible.append((rec, present, bytes_used))
        table.setRowCount(len(visible))
        self._row_thumbnail_paths = []
        selected_row = -1
        for row_idx, (rec, present, bytes_used) in enumerate(visible):
            title = rec['title_override'] or rec['title']
            thumb = find_thumbnail(media_path(rec['file_path'])) if present else None
            self._row_thumbnail_paths.append(thumb)
            values = ['썸네일 없음' if not thumb else '', title, rec['channel'],
                      rec['playlist_title'] or infer_playlist_name(rec['file_path']),
                      format_duration(rec['duration']), rec['major_category'], rec['sub_category'],
                      format_size(bytes_used), rec['upload_date'],
                      '●' if rec['memo'] else '', '있음' if present else '파일 없음']
            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                if col == 1:
                    item.setData(Qt.ItemDataRole.UserRole, rec['video_id'])
                if col in (4, 7):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                if col == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setToolTip(str(media_path(rec['file_path'])) if col == 10 else
                                (rec['tags'] if col in (5, 6) and rec['tags'] else str(val)))
                table.setItem(row_idx, col, item)
            if rec['video_id'] == self.current_id:
                selected_row = row_idx
        if selected_row >= 0:
            table.selectRow(selected_row)
        table.blockSignals(False)
        self.schedule_visible_thumbnails()
        if missing != self._last_missing:
            if missing:
                self.add_log(f'[누락 파일] {len(missing)}개: 기본 라이브러리 보기에서 숨김(메모 DB 보존)')
            elif self._last_missing:
                self.add_log('[파일 복구] 누락 영상이 다시 확인되었습니다')
            self._last_missing = missing
        self.statusBar().showMessage(f'라이브러리 {len(visible)}개 표시 / 누락 {len(missing)}개 | DB: {DB_PATH} | 로그: {LOG_PATH.parent}')

    def on_video_selected(self):
        selected = self.library_table.selectedItems()
        if not selected:
            return
        key_item = self.library_table.item(selected[0].row(), 1)
        if not key_item:
            return
        video_id = key_item.data(Qt.ItemDataRole.UserRole)
        if not video_id:
            return
        row = self.db.execute("SELECT * FROM videos WHERE video_id=?", (video_id,)).fetchone()
        if row is None:
            return
        try:
            selected_path = media_path(row['file_path'])
        except ValueError as ex:
            self.add_log(f'[경로 오류] {ex}')
            return
        if video_id == self.current_id and self.current_path == selected_path:
            return
        self.save_memo(silent=True)
        self.save_classification(silent=True)
        self.current_id = video_id
        self.current_path = selected_path
        playlist = row['playlist_title'] or infer_playlist_name(row['file_path'])
        self.video_info_label.setText(
            f"{row['channel']} · {row['title_override'] or row['title']}\n"
            f"재생목록: {playlist or '단일 영상'} · {format_duration(row['duration'])}"
            f" · {format_size(int(row['file_size']))}")
        self.update_thumbnail_preview()
        self._loading_note = True
        self.memo_edit.setPlainText(row["memo"])
        self._loading_note = False
        self._loading_category = True
        try:
            self.major_combo.setCurrentText(row['major_category'] if row['major_category'] in BADMINTON_CATEGORIES else '미분류')
            self.on_major_changed(self.major_combo.currentText(), save=False)
            idx = self.sub_combo.findText(row['sub_category'])
            if idx >= 0:
                self.sub_combo.setCurrentIndex(idx)
            self.tags_edit.setText(row['tags'])
        finally:
            self._loading_category = False
        self._segment_start = None
        self._segment_end = None
        self.mark_info.setText('시작 - / 끝 -')
        self.mark_title.clear()
        self.refresh_clip_marks()
        self.player.stop()
        self._pending_seek = None
        self.subtitle_now.clear()
        if self.current_path.is_file():
            self.player.setSource(QUrl.fromLocalFile(str(self.current_path)))
        else:
            self.player.setSource(QUrl())
            self.video_info_label.setText("파일이 존재하지 않습니다: " + str(self.current_path))
        self.find_subtitle_files()

    def on_major_changed(self, major: str, save: bool = True):
        self.sub_combo.blockSignals(True)
        self.sub_combo.clear()
        self.sub_combo.addItems(BADMINTON_CATEGORIES.get(major, ['미분류']))
        self.sub_combo.blockSignals(False)
        if save and not self._loading_category:
            self.save_classification()

    def save_classification(self, silent: bool = False):
        if not self.current_id or self._loading_category:
            return
        major = self.major_combo.currentText() or '미분류'
        sub = self.sub_combo.currentText() or '미분류'
        tags = ', '.join(dict.fromkeys(
            part.strip() for part in self.tags_edit.text().replace('，', ',').split(',')
            if part.strip()))
        with self.db:
            self.db.execute('UPDATE videos SET major_category=?,sub_category=?,tags=?,updated_at=? '
                            'WHERE video_id=?', (major, sub, tags, now_str(), self.current_id))
        if not silent:
            self.add_log(f'[분류 저장] {self.current_id} | {major} / {sub} | 태그: {tags}')
            self.refresh_library()

    def mark_start(self):
        if not self.current_id:
            return
        self._segment_start = int(self.player.position())
        self.update_mark_label()
        self.add_log(f'[구간 시작] {self.current_id} {millis_text(self._segment_start)}')

    def mark_end(self):
        if not self.current_id:
            return
        self._segment_end = int(self.player.position())
        self.update_mark_label()
        self.add_log(f'[구간 종료] {self.current_id} {millis_text(self._segment_end)}')

    def update_mark_label(self):
        st = '-' if self._segment_start is None else millis_text(self._segment_start)
        en = '-' if self._segment_end is None else millis_text(self._segment_end)
        self.mark_info.setText(f'시작 {st} / 끝 {en}')

    def save_clip_mark(self):
        if not self.current_id:
            QMessageBox.information(self, '영상 선택', '먼저 영상을 선택하세요.')
            return
        if (self._segment_start is None or self._segment_end is None
                or self._segment_end <= self._segment_start):
            QMessageBox.warning(self, '구간 확인', '시작점과 종료점을 순서대로 지정하세요 (종료 > 시작).')
            return
        title = self.mark_title.text().strip() or '영상 구간'
        with self.db:
            self.db.execute('INSERT INTO clip_marks(video_id,start_ms,end_ms,title,created_at) '
                            'VALUES(?,?,?,?,?)', (self.current_id, self._segment_start,
                                                self._segment_end, title, now_str()))
        self.add_log(f'[구간 후보 저장] {self.current_id}: {title} '
                     f'{millis_text(self._segment_start)} ~ {millis_text(self._segment_end)}')
        self.refresh_clip_marks()

    def refresh_clip_marks(self):
        self.clip_list.clear()
        if not self.current_id:
            return
        rows = self.db.execute('SELECT * FROM clip_marks WHERE video_id=? ORDER BY start_ms,id',
                               (self.current_id,)).fetchall()
        for mark in rows:
            item = QListWidgetItem(f"{millis_text(mark['start_ms'])} ~ "
                                   f"{millis_text(mark['end_ms'])} | {mark['title']}")
            item.setData(Qt.ItemDataRole.UserRole, (mark['id'], mark['start_ms']))
            self.clip_list.addItem(item)

    def play_clip_mark(self, item=None):
        if not isinstance(item, QListWidgetItem):
            item = self.clip_list.currentItem()
        if not item or not self.current_path or not self.current_path.is_file():
            return
        _, ms = item.data(Qt.ItemDataRole.UserRole)
        self._pending_seek = int(ms)
        self.player.play()
        self._apply_pending_seek()
        self.add_log(f'[구간 후보 재생] {self.current_id} | {millis_text(ms)}')

    def delete_clip_mark(self):
        item = self.clip_list.currentItem()
        if item is None:
            return
        mark_id, _ = item.data(Qt.ItemDataRole.UserRole)
        with self.db:
            self.db.execute('DELETE FROM clip_marks WHERE id=? AND video_id=?',
                            (mark_id, self.current_id))
        self.add_log(f'[구간 후보 삭제] {self.current_id} / #{mark_id}')
        self.refresh_clip_marks()

    def save_memo(self, silent=False):
        if not self.current_id or self._loading_note:
            return
        with self.db:
            self.db.execute("UPDATE videos SET memo=?,updated_at=? WHERE video_id=?",
                            (self.memo_edit.toPlainText(), now_str(), self.current_id))
        if not silent:
            self.add_log(f"[메모 저장] {self.current_id}")
            self.refresh_library()

    def play_current(self):
        if self.current_path and self.current_path.is_file():
            self.player.play()
        else:
            QMessageBox.information(self, "영상 선택", "라이브러리에서 존재하는 영상 파일을 선택하세요.")

    def seek_slider(self):
        self._seeking = False
        self.player.setPosition(self.time_slider.value())

    def on_duration(self, length):
        self.time_slider.setRange(0, max(0, int(length)))
        if self.current_id and int(length) > 0:
            seconds = int(length) // 1000
            rec = self.db.execute('SELECT duration FROM videos WHERE video_id=?', (self.current_id,)).fetchone()
            if rec and seconds > 0 and not rec['duration']:
                with self.db:
                    self.db.execute('UPDATE videos SET duration=? WHERE video_id=?', (seconds, self.current_id))
                self.add_log(f'[재생시간 확인] {self.current_id} = {format_duration(seconds)}')
                self.refresh_library()

    def on_position(self, position):
        if not self._seeking:
            self.time_slider.setValue(position)
        self.time_label.setText(f"{millis_text(position)} / {millis_text(self.player.duration())}")
        if not self.subtitles:
            return
        idx = bisect.bisect_right(self.subtitle_starts, position) - 1
        if idx >= 0 and position <= self.subtitles[idx][1]:
            text = self.subtitles[idx][2]
        else:
            idx = -1
            text = ""
        if idx != self.current_subtitle_index:
            self.current_subtitle_index = idx
            self.subtitle_now.setText(text)
            if idx >= 0:
                self.subtitle_list.setCurrentRow(idx)

    def on_player_error(self, error, description):
        if error != QMediaPlayer.Error.NoError:
            self.add_log(f"[재생 오류] {description}. 코덱 문제라면 기본 플레이어로 열기를 사용하세요.")

    def find_subtitle_files(self):
        self.subtitle_combo.blockSignals(True)
        self.subtitle_combo.clear()
        if self.current_path and self.current_path.is_file():
            try:
                for file in subtitle_candidates(self.current_path):
                    self.subtitle_combo.addItem(file.name, str(file))
            except OSError as ex:
                self.add_log(f'[SRT 탐색 오류] {ex}')
        self.subtitle_combo.blockSignals(False)
        self.load_selected_subtitles()

    def load_selected_subtitles(self):
        self.subtitles = []
        self.subtitle_starts = []
        self.current_subtitle_index = -1
        self.subtitle_list.clear()
        self.subtitle_now.clear()
        path = self.subtitle_combo.currentData()
        if path:
            self.subtitles = parse_srt(Path(path))
            self.subtitle_starts = [item[0] for item in self.subtitles]
            for start, end, txt in self.subtitles:
                item = QListWidgetItem(f"{millis_text(start)}  {txt.replace(chr(10), ' / ')}")
                item.setData(Qt.ItemDataRole.UserRole, start)
                item.setToolTip(f"{millis_text(start)} ~ {millis_text(end)}\n{txt}")
                self.subtitle_list.addItem(item)
            self.add_log(f'[SRT 자막] {Path(path).name} ({len(self.subtitles)}개 구간)')
        else:
            if self.current_path:
                self.add_log(f'[SRT 자막] 대응되는 자막 없음: {self.current_path.name}')
        self.subtitle_count_label.setText(f'자막 {len(self.subtitles)}개')
        self.filter_subtitles(self.subtitle_search.text())
        self.refresh_subtitle_popup()

    def filter_subtitles(self, term):
        t = str(term).strip().casefold()
        for i in range(self.subtitle_list.count()):
            item = self.subtitle_list.item(i)
            item.setHidden(t not in item.text().casefold())

    def subtitle_jump(self, item):
        target = item.data(Qt.ItemDataRole.UserRole)
        if target is None:
            pos = self.subtitle_list.row(item)
            if 0 <= pos < len(self.subtitles):
                target = self.subtitles[pos][0]
        if target is not None and self.current_path and self.current_path.is_file():
            self._pending_seek = int(target)
            self.player.play()
            self._apply_pending_seek()
            self.add_log(f'[자막 이동] {millis_text(int(target))} → 재생')

    def _apply_pending_seek(self):
        if self._pending_seek is None:
            return
        status = self.player.mediaStatus()
        if self.player.isSeekable() and status in (QMediaPlayer.MediaStatus.LoadedMedia,
                      QMediaPlayer.MediaStatus.BufferedMedia,
                      QMediaPlayer.MediaStatus.BufferingMedia):
            target = self._pending_seek
            self.player.setPosition(target)
            self._pending_seek = None
            if self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
                self.player.play()

    def on_media_status(self, status):
        if status in (QMediaPlayer.MediaStatus.LoadedMedia, QMediaPlayer.MediaStatus.BufferedMedia,
                      QMediaPlayer.MediaStatus.BufferingMedia):
            self.ensure_audio_track()
            if self._pending_seek is not None:
                QTimer.singleShot(50, self._apply_pending_seek)
        if status == QMediaPlayer.MediaStatus.InvalidMedia and self._pending_seek is not None:
            self.add_log('[자막 이동 오류] 미디어 재생 준비 실패')
            self._pending_seek = None

    def show_full_subtitles(self):
        if self.subtitle_window is None:
            popup = QDialog(self)
            popup.setWindowTitle('Minton Video Library - 전체 자막 / 구간 탐색')
            popup.resize(850, 720)
            v = QVBoxLayout(popup)
            v.addWidget(QLabel('전체 자막 (더블클릭하면 메인 플레이어가 해당 시각부터 재생됩니다)'))
            search = QLineEdit()
            search.setPlaceholderText('자막 내용 검색')
            v.addWidget(search)
            lst = QListWidget()
            lst.setWordWrap(True)
            lst.itemDoubleClicked.connect(self.subtitle_jump)
            search.textChanged.connect(lambda term: [lst.item(i).setHidden(
                str(term).casefold() not in lst.item(i).text().casefold()) for i in range(lst.count())])
            v.addWidget(lst)
            self.subtitle_window = popup
            self.subtitle_popup_list = lst
        self.refresh_subtitle_popup()
        self.subtitle_window.show()
        self.subtitle_window.raise_()
        self.subtitle_window.activateWindow()

    def refresh_subtitle_popup(self):
        lst = self.subtitle_popup_list
        if lst is None:
            return
        lst.clear()
        for start, end, text in self.subtitles:
            item = QListWidgetItem(f"{millis_text(start)}  {text.replace(chr(10), ' / ')}")
            item.setData(Qt.ItemDataRole.UserRole, start)
            item.setToolTip(f'{millis_text(start)} ~ {millis_text(end)}\n{text}')
            lst.addItem(item)

    def current_video_record(self):
        if not self.current_id:
            QMessageBox.information(self, '영상 선택', '라이브러리에서 영상을 선택하세요.')
            return None
        row = self.db.execute('SELECT * FROM videos WHERE video_id=?', (self.current_id,)).fetchone()
        if not row:
            return None
        return row

    def move_current_media(self):
        record = self.current_video_record()
        if not record:
            return
        path = media_path(record['file_path'])
        if not path.is_file():
            QMessageBox.warning(self, '파일 없음', '파일이 없습니다. 폴더 다시 검색으로 복구하세요.')
            return
        destination = QFileDialog.getExistingDirectory(self, '옮길 폴더 지정', str(path.parent))
        if not destination:
            return
        if not is_in_directory(Path(destination), Path(self.root_input.text().strip())):
            QMessageBox.warning(self, '라이브러리 범위 밖',
                                '영상 이동은 현재 다운로드 루트 아래 폴더만 가능합니다.\n'
                                '다른 드라이브로 옮기려면 먼저 저장 폴더를 변경해 주세요.')
            return
        self.save_memo(silent=True)
        self.player.stop()
        try:
            result = move_media_bundle(path, Path(destination))
            with self.db:
                self.db.execute('UPDATE videos SET file_path=?,updated_at=? WHERE video_id=?',
                                (root_relative(result), now_str(), record['video_id']))
            self.current_path = result
            self.update_thumbnail_preview()
            self.player.setSource(QUrl.fromLocalFile(str(result)))
            self.find_subtitle_files()
            self.add_log(f'[영상 이동] {path} -> {result} (연관 SRT/info.json 동반 이동)')
            self.refresh_library()
        except (OSError, ValueError) as ex:
            self.add_log(f'[영상 이동 오류] {ex}')
            QMessageBox.warning(self, '영상 이동 실패', str(ex))

    def rename_current_media(self):
        record = self.current_video_record()
        if not record:
            return
        path = media_path(record['file_path'])
        if not path.is_file():
            QMessageBox.warning(self, '파일 없음', '파일이 없습니다. 폴더 다시 검색으로 복구하세요.')
            return
        title, ok = QInputDialog.getText(self, '한글 제목 / 파일명 변경',
                                         '변경할 한국어 영상 제목을 입력하세요 (영상/자막/메타데이터 동시 변경).',
                                         text=record['title_override'] or record['title'])
        if not ok or not title.strip():
            return
        clean_title = safe_name(title, '제목없음')
        parts = [safe_name(record['channel']), clean_title]
        stem = ' - '.join(parts)
        if re.fullmatch(r'[A-Za-z0-9_-]{11}', record['video_id']):
            stem += f" [{record['video_id']}]"
        if record['upload_date']:
            stem += ' - ' + safe_name(record['upload_date'])
        self.save_memo(silent=True)
        self.player.stop()
        try:
            result = move_media_bundle(path, path.parent, stem)
            with self.db:
                self.db.execute('UPDATE videos SET title_override=?,file_path=?,updated_at=? WHERE video_id=?',
                                (clean_title, root_relative(result), now_str(), record['video_id']))
            self.current_path = result
            self.update_thumbnail_preview()
            self.player.setSource(QUrl.fromLocalFile(str(result)))
            self.find_subtitle_files()
            self.video_info_label.setText(f"{record['channel']} · {clean_title}")
            self.add_log(f'[한글 제목 변경] {path.name} -> {result.name} (메모 유지)')
            self.refresh_library()
        except (OSError, ValueError) as ex:
            self.add_log(f'[제목 변경 오류] {ex}')
            QMessageBox.warning(self, '이름 변경 실패', str(ex))

    def trash_current_media(self):
        record = self.current_video_record()
        if not record:
            return
        path = media_path(record['file_path'])
        if not path.is_file():
            QMessageBox.information(self, '파일 없음', '해당 영상 파일이 이미 없습니다.')
            return
        extras = related_sidecars(path)
        if QMessageBox.question(self, '영상 휴지통 삭제',
                f'다음 영상을 휴지통으로 이동하시겠습니까?\n{path.name}\n'
                f'연관 자막/메타데이터 {len(extras)}개도 함께 처리합니다.\n'
                '메모는 DB에 보존되며 라이브러리에서 숨겨집니다.') != QMessageBox.StandardButton.Yes:
            return
        self.save_memo(silent=True)
        self.player.stop()
        self.player.setSource(QUrl())
        self.update_thumbnail_preview()
        errors = []
        for target in [path, *extras]:
            if target.exists() and not QFile.moveToTrash(str(target)):
                errors.append(str(target))
        self.add_log(f'[휴지통 삭제] {path} (연관 파일 {len(extras)}개, 실패 {len(errors)}개)')
        self.refresh_library()
        if errors:
            QMessageBox.warning(self, '일부 파일 휴지통 실패', '\n'.join(errors))

    def open_folder(self, path: str):
        try:
            folder = Path(path)
            folder.mkdir(parents=True, exist_ok=True)
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))
        except OSError as ex:
            QMessageBox.warning(self, "폴더 오류", str(ex))

    def open_media_folder(self):
        if self.current_path:
            self.open_folder(str(self.current_path.parent))

    def open_external(self):
        if self.current_path and self.current_path.is_file():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.current_path)))

    def closeEvent(self, event):
        if self.thumbnail_worker and self.thumbnail_worker.isRunning():
            QMessageBox.information(self, '썸네일 다운로드 중', '먼저 썸네일 중단을 누른 뒤 종료해 주세요.')
            event.ignore()
            return
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "다운로드 중", "다운로드 작업이 실행 중입니다. 먼저 '즉시 중단'한 후 종료해 주세요.")
            event.ignore()
            return
        if self.scanner and self.scanner.isRunning():
            QMessageBox.information(self, "검색 중", "폴더 검색이 끝난 후 종료해 주세요.")
            event.ignore()
            return
        self.save_memo(silent=True)
        self.save_classification(silent=True)
        self.save_settings()
        set_setting(self.db, "split_outer", json.dumps(self.outer_splitter.sizes()))
        set_setting(self.db, "split_inner", json.dumps(self.inner_splitter.sizes()))
        set_setting(self.db, "window_width", str(self.width()))
        set_setting(self.db, "window_height", str(self.height()))
        set_setting(self.db, 'library_col_widths',
                    json.dumps([self.library_table.columnWidth(i) for i in range(self.library_table.columnCount())]))
        set_setting(self.db, 'jobs_col_widths',
                    json.dumps([self.jobs_table.columnWidth(i) for i in range(self.jobs_table.columnCount())]))
        self.player.stop()
        try:
            self.db.execute('PRAGMA wal_checkpoint(TRUNCATE)')
        except sqlite3.Error as ex:
            LOGGER.warning('[DB WAL 체크포인트 실패] %s', ex)
        self.db.close()
        LOGGER.info("정상 종료")
        event.accept()


def determine_start_root() -> Path | None:
    """명령행/지난 루트/구버전 DB 순으로 선택; 경로가 사라지면 GUI로 재선택."""
    requested = None
    if '--root' in sys.argv:
        idx = sys.argv.index('--root')
        if idx + 1 >= len(sys.argv):
            QMessageBox.critical(None, '--root 오류', '--root 뒤에 라이브러리 폴더 경로를 입력하세요.')
            return None
        requested = sys.argv[idx + 1]
    if requested:
        selected = Path(requested).expanduser()
        if not selected.is_dir():
            QMessageBox.critical(None, '라이브러리 폴더 없음',
                                 f'지정한 라이브러리 폴더가 존재하지 않습니다:\n{selected}')
            return None
        return selected

    last_root = None
    if ROOT_POINTER.exists():
        try:
            last_root = json.loads(ROOT_POINTER.read_text(encoding='utf-8')).get('root')
        except (OSError, ValueError, TypeError):
            LOGGER.warning('[라이브러리 위치 힌트 손상] %s', ROOT_POINTER)

    # 처음 V1.1 -> V1.2 업데이트할 때 저장돼 있던 사용자 지정 경로 우선 사용.
    if not last_root and LEGACY_DB_PATH.is_file():
        try:
            with sqlite3.connect(str(LEGACY_DB_PATH), timeout=20) as db:
                row = db.execute("SELECT value FROM settings WHERE key='download_root'").fetchone()
                last_root = row[0] if row else None
        except sqlite3.Error as ex:
            LOGGER.warning('[이전 다운로드 경로 확인 실패] %s', ex)
    if last_root:
        old = Path(last_root)
        if old.is_dir():
            return old
        QMessageBox.information(None, '라이브러리 위치 변경',
            f'이전 영상 폴더를 찾지 못했습니다:\n{old}\n\n'
            'minton.youtube 폴더 전체를 다른 디스크로 옮겼다면 새로운 위치를 지정하세요.\n'
            '_database 폴더가 포함된 minton.youtube 최상위 폴더를 선택합니다.')
        selected = QFileDialog.getExistingDirectory(None, '이동한 minton.youtube 라이브러리 폴더 선택',
                                                     str(Path.home()))
        return Path(selected) if selected else None
    return Path(DEFAULT_ROOT)


def main():
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Minton.VideoLibrary.1")
        except (OSError, AttributeError):
            pass
    # Qt 옵션 충돌 방지를 위해 --root는 앱 자체에서 처리한다.
    app = QApplication([sys.argv[0]])
    app.setStyle('Fusion')
    app.setApplicationName(APP_TITLE)
    try:
        selected_root = determine_start_root()
        if selected_root is None:
            return
        set_library_root(selected_root)
        init_db(migrate_old=True)
        window = MainWindow()
    except Exception as ex:
        LOGGER.exception('[프로그램 시작 실패] DB 저장 경로/마이그레이션 오류')
        QMessageBox.critical(None, '프로그램 시작 실패',
                             f'{ex}\n\n기존 데이터베이스는 삭제하지 않았습니다.\n'
                             f'이전 DB: {LEGACY_DB_PATH}\n새 DB: {DB_PATH}')
        return
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
