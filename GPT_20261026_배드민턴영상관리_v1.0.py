# -*- coding: utf-8 -*-
"""
Minton Video Library v1.0 | 배드민턴 유튜브 영상 다운로드 및 관리 프로그램
=====================================================================
[프로그램 전체 기능 및 동작 보존 목록]
01. Windows Python 3.12 + PySide6 기반 단일 Python 소스 GUI.
02. 최초 다운로드 루트 기본값 D:\\99.유튜브다운\\minton.youtube; 변경값 SQLite에 저장.
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
15. SQLite WAL 저장: 설정, 다운로드 대기열, 미디어 색인, 개별 메모.
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
25. 로깅 화면과 로테이션 파일 로그(LocalAppData/MintonVideoLibrary/logs).
26. ffmpeg, deno, yt-dlp 실행환경 확인 및 실행 조건 안내.
27. 창 및 분할창 크기 등 UI 상태 보관(SQLite settings).
28. Windows 콘솔창 없이 yt-dlp subprocess 실행, 한글 Unicode 경로 지원.
29. 삭제 버튼은 대기열 항목만 제거하며 실제 비디오 파일/메모는 보존.
30. 저작권과 이용약관을 준수하는 영상만 다운로드하도록 사용자에게 안내.

[저장 위치]
- 프로그램: D:\\stockproj\\minton_video_library\\minton_video_library.py (권장)
- 데이터베이스/로그: %LOCALAPPDATA%\\MintonVideoLibrary\\ (Git과 분리)
- 다운로드: 사용자 설정 폴더 아래 %(channel)s\\파일명

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
import hashlib
import html
import json
import logging
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

from PySide6.QtCore import Qt, QThread, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QMainWindow, QMessageBox, QPlainTextEdit,
    QProgressBar, QPushButton, QSlider, QSpinBox, QSplitter, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
    QHeaderView, QAbstractItemView,
)

APP_TITLE = "Minton Video Library v1.0"
APP_DATA = Path(os.getenv("LOCALAPPDATA") or (Path.home() / ".local" / "share")) / "MintonVideoLibrary"
DB_PATH = APP_DATA / "library.db"
LOG_PATH = APP_DATA / "logs" / "minton_video_library.log"
DEFAULT_ROOT = r"D:\99.유튜브다운\minton.youtube" if os.name == "nt" else str(Path.home() / "Videos" / "minton.youtube")
FORMAT_SELECTOR = "bv[vcodec^=avc1][height<=1080]+ba[acodec^=mp4a]/b[vcodec^=avc1][height<=1080]"
OUTPUT_TEMPLATE = "%(channel)s/%(channel)s - %(title)s [%(id)s] - %(upload_date>%Y-%m-%d)s.%(ext)s"
VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4v"}
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


def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=20000")
    return conn


def init_db() -> None:
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
    """(중복이 제거된 URL, kind). 외부 URL/임의 명령 실행 방지."""
    try:
        p = urlparse(value.strip())
        host = (p.hostname or "").lower()
        if p.scheme not in ("http", "https") or host not in (
            "youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"
        ):
            return None
        q = parse_qs(p.query)
        if host == "youtu.be":
            vid = p.path.strip("/").split("/")[0]
            if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
                return f"https://www.youtube.com/watch?v={vid}", "video"
        vid = (q.get("v") or [""])[0]
        pl = (q.get("list") or [""])[0]
        if p.path.rstrip("/") == "/playlist" and pl:
            return f"https://www.youtube.com/playlist?list={pl}", "playlist"
        m = re.fullmatch(r"/(?:shorts|live|embed)/([A-Za-z0-9_-]{11})/?", p.path)
        if m:
            return f"https://www.youtube.com/watch?v={m.group(1)}", "video"
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
            return f"https://www.youtube.com/watch?v={vid}", "video"
        if pl:
            return f"https://www.youtube.com/playlist?list={pl}", "playlist"
    except (ValueError, TypeError):
        return None
    return None


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


def local_video_record(path: Path) -> dict:
    info = read_info_json(path)
    id_match = YT_ID_PATTERN.search(path.stem)
    file_id = (info.get("id") or (id_match.group(1) if id_match else ""))
    if not file_id:
        file_id = "local:" + hashlib.sha1(str(path.resolve()).casefold().encode("utf-8")).hexdigest()
    title = info.get("title") or path.stem
    channel = info.get("channel") or path.parent.name
    upload_date = str(info.get("upload_date") or "")
    if len(upload_date) == 8 and upload_date.isdigit():
        upload_date = upload_date[:4] + "-" + upload_date[4:6] + "-" + upload_date[6:]
    elif not upload_date:
        match = re.search(r"(\d{4}-\d{2}-\d{2})$", path.stem)
        upload_date = match.group(1) if match else ""
    return dict(video_id=str(file_id), title=str(title), channel=str(channel),
                upload_date=upload_date, duration=int(info.get("duration") or 0),
                file_path=str(path), source_url=str(info.get("webpage_url") or ""))


def upsert_video(db: sqlite3.Connection, data: dict) -> None:
    # 갱신 시 기존 메모를 절대 덮어쓰지 않는다.
    with db:
        db.execute("""
        INSERT INTO videos(video_id,title,channel,upload_date,duration,file_path,source_url,updated_at)
        VALUES(:video_id,:title,:channel,:upload_date,:duration,:file_path,:source_url,:updated_at)
        ON CONFLICT(video_id) DO UPDATE SET
            title=excluded.title, channel=excluded.channel,
            upload_date=CASE WHEN excluded.upload_date<>'' THEN excluded.upload_date ELSE videos.upload_date END,
            duration=CASE WHEN excluded.duration>0 THEN excluded.duration ELSE videos.duration END,
            file_path=excluded.file_path,
            source_url=CASE WHEN excluded.source_url<>'' THEN excluded.source_url ELSE videos.source_url END,
            updated_at=excluded.updated_at
        """, {**data, "updated_at": now_str()})


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

    def __init__(self, root: str, interval: int, parent=None):
        super().__init__(parent)
        self.root = Path(root)
        self.interval = interval
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
                "--remote-components", "ejs:npm", "--no-color",
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
        self.activity.emit("재생목록 확인 중")
        self._emit(f"[재생목록] {job['url']}")
        cmd = [*self._shared_cmd(), "--flat-playlist", "--dump-single-json", "--yes-playlist", job["url"]]
        try:
            code, output, stderr = self._run_capture(cmd)
        except Exception as ex:
            self._update_job(db, job["id"], "failed", str(ex))
            self._emit(f"[재생목록 실패] {ex}")
            return
        if stderr.strip():
            for line in stderr.strip().splitlines()[-30:]:
                self._emit("[yt-dlp] " + line)
        if self._stop.is_set():
            self._update_job(db, job["id"], "queued", "중단되어 재시도 대기")
            return
        if code != 0:
            self._update_job(db, job["id"], "failed", stderr[-1500:] or "목록 정보 수신 실패")
            return
        try:
            data = json.loads(output)
            entries = data.get("entries") or []
            if not isinstance(entries, list):
                raise ValueError("재생목록 데이터 형식이 올바르지 않습니다")
            added = 0
            skipped = 0
            with db:
                for entry in entries:
                    if not isinstance(entry, dict):
                        skipped += 1
                        continue
                    item_id = str(entry.get("id") or "")
                    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", item_id):
                        vurl = canonical_url(str(entry.get("webpage_url") or entry.get("url") or ""))
                        item_id = extract_video_id(vurl[0]) if vurl and vurl[1] == "video" else ""
                    if not item_id:
                        skipped += 1
                        continue
                    url = f"https://www.youtube.com/watch?v={item_id}"
                    before = db.total_changes
                    db.execute("INSERT OR IGNORE INTO jobs(url,kind,title,status,created_at,updated_at) "
                               "VALUES(?,'video',?,'queued',?,?)",
                               (url, str(entry.get("title") or item_id), now_str(), now_str()))
                    added += db.total_changes - before
            self._update_job(db, job["id"], "expanded", f"신규 {added}개 / 접근 불가 {skipped}개", 100)
            self._emit(f"[재생목록 등록] 제목: {data.get('title','')}, 신규 {added}개, 건너뜀 {skipped}개")
        except (ValueError, json.JSONDecodeError) as ex:
            self._update_job(db, job["id"], "failed", f"재생목록 JSON 분석 오류: {ex}")

    def _download_one(self, db, job):
        url = job["url"]
        video_id = extract_video_id(url)
        if video_id:
            existing = db.execute("SELECT file_path FROM videos WHERE video_id=?", (video_id,)).fetchone()
            if existing and Path(existing["file_path"]).is_file():
                self._update_job(db, job["id"], "done", "이미 라이브러리에 존재", 100)
                self._emit(f"[중복 생략] {url}")
                return
        self.activity.emit(f"다운로드 중: {job['title'] or url}")
        self._emit(f"[다운로드 시작] #{job['id']} {url}")
        cmd = [*self._shared_cmd(), "--no-playlist", "--continue", "--newline", "--progress",
               "-f", FORMAT_SELECTOR, "--merge-output-format", "mp4",
               "--write-subs", "--write-auto-subs", "--sub-langs", "ko.*",
               "--convert-subs", "srt", "--write-info-json", "--no-write-playlist-metafiles",
               "-P", str(self.root), "-o", OUTPUT_TEMPLATE,
               "--print", "after_move:__MINTON_FILE__%(filepath)s",
               "--print", "after_move:__MINTON_TITLE__%(title)s",
               "--print", "after_move:__MINTON_CHANNEL__%(channel)s",
               "--print", "after_move:__MINTON_ID__%(id)s",
               url]
        info: dict[str, str] = {}
        last_log_percentage = -10
        last_persisted_step = -1
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
                self._update_job(db, job["id"], "failed", f"yt-dlp 종료 코드 {retcode} (상세 로그 참고)")
                self._emit(f"[실패] #{job['id']} yt-dlp 종료 코드 {retcode}")
                return
            media_path = Path(info.get("FILE") or "")
            if not media_path.is_file() and video_id:
                # yt-dlp 버전에 따라 after_move가 출력되지 않는 경우 기존 파일 재탐색
                matches = [p for p in self.root.rglob("*")
                           if f"[{video_id}]" in p.name and p.suffix.lower() in VIDEO_EXTS and p.is_file()]
                if matches:
                    media_path = matches[0]
            if not media_path.is_file():
                self._update_job(db, job["id"], "failed", "성공 응답이지만 저장된 동영상 파일을 찾지 못함")
                return
            data = local_video_record(media_path)
            data["source_url"] = url
            if info.get("TITLE"):
                data["title"] = info["TITLE"]
            if info.get("CHANNEL"):
                data["channel"] = info["CHANNEL"]
            if info.get("ID"):
                data["video_id"] = info["ID"]
            upsert_video(db, data)
            self._update_job(db, job["id"], "done", "", 100)
            self._emit(f"[다운로드 완료] {media_path}")
        except Exception as ex:
            if self._stop.is_set():
                self._update_job(db, job["id"], "queued", "중단됨(.part 재개 가능)")
            else:
                self._update_job(db, job["id"], "failed", str(ex))
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
                job = db.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY id LIMIT 1").fetchone()
                if job is None:
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


class ScanWorker(QThread):
    finished_scan = Signal(list)
    message = Signal(str)

    def __init__(self, root: str, parent=None):
        super().__init__(parent)
        self.root = Path(root)

    def run(self):
        results = []
        try:
            if self.root.is_dir():
                for directory, _, filenames in os.walk(self.root):
                    for name in filenames:
                        path = Path(directory) / name
                        if path.suffix.lower() in VIDEO_EXTS:
                            results.append(local_video_record(path))
            self.finished_scan.emit(results)
        except Exception as ex:
            self.message.emit(f"[폴더 검색 오류] {ex}")
            self.finished_scan.emit(results)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        self.db = connect_db()
        self.worker: DownloadWorker | None = None
        self.scanner: ScanWorker | None = None
        self.current_id: str | None = None
        self.current_path: Path | None = None
        self.subtitles: list[tuple[int, int, str]] = []
        self.subtitle_starts: list[int] = []
        self.current_subtitle_index = -1
        self._loading_note = False
        self._seeking = False
        self._build_ui()
        self._load_settings()
        self.refresh_jobs()
        self.refresh_library()
        QTimer.singleShot(500, self.scan_library)
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
        self.root_input.editingFinished.connect(self.save_settings)
        folder_row.addWidget(self.root_input, stretch=1)
        self.browse_btn = QPushButton("찾기")
        self.browse_btn.clicked.connect(self.browse_folder)
        folder_row.addWidget(self.browse_btn)
        open_dir_btn = QPushButton("폴더 열기")
        open_dir_btn.clicked.connect(lambda: self.open_folder(self.root_input.text()))
        folder_row.addWidget(open_dir_btn)
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
        layout.addWidget(add_box)

        queue_bar = QHBoxLayout()
        self.start_btn = QPushButton("▶ 다운로드 시작 / 재개")
        self.start_btn.clicked.connect(self.start_download)
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
        queue_bar.addStretch()
        self.activity_label = QLabel("대기")
        queue_bar.addWidget(self.activity_label)
        layout.addLayout(queue_bar)

        self.jobs_table = QTableWidget(0, 5)
        self.jobs_table.setHorizontalHeaderLabels(["번호", "상태", "진행률", "영상/재생목록", "오류/메시지"])
        self.jobs_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.jobs_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.jobs_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.jobs_table.verticalHeader().setVisible(False)
        self.jobs_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.jobs_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.jobs_table.setColumnWidth(0, 55)
        self.jobs_table.setColumnWidth(1, 100)
        self.jobs_table.setColumnWidth(2, 85)
        self.jobs_table.setMinimumHeight(130)

        bottom = QSplitter(Qt.Orientation.Horizontal)
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        lib_bar = QHBoxLayout()
        lib_bar.addWidget(QLabel("영상 라이브러리"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("제목 / 채널 / 메모 / 영상 ID 검색")
        self.search_input.textChanged.connect(self.refresh_library)
        lib_bar.addWidget(self.search_input, 1)
        self.channel_combo = QComboBox()
        self.channel_combo.setMinimumWidth(140)
        self.channel_combo.currentIndexChanged.connect(self.refresh_library)
        lib_bar.addWidget(self.channel_combo)
        scan_btn = QPushButton("폴더 다시 검색")
        scan_btn.clicked.connect(self.scan_library)
        lib_bar.addWidget(scan_btn)
        ll.addLayout(lib_bar)
        self.library_table = QTableWidget(0, 5)
        self.library_table.setHorizontalHeaderLabels(["제목", "채널", "업로드일", "메모", "파일"])
        self.library_table.verticalHeader().setVisible(False)
        self.library_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.library_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.library_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.library_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.library_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.library_table.setColumnWidth(1, 115)
        self.library_table.setColumnWidth(2, 95)
        self.library_table.setColumnWidth(3, 50)
        self.library_table.itemSelectionChanged.connect(self.on_video_selected)
        self.library_table.cellDoubleClicked.connect(lambda _r, _c: self.play_current())
        ll.addWidget(self.library_table)
        bottom.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(4, 0, 0, 0)
        self.video_info_label = QLabel("라이브러리에서 영상을 선택하세요")
        self.video_info_label.setWordWrap(True)
        rl.addWidget(self.video_info_label)
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(215)
        rl.addWidget(self.video_widget, 3)
        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)
        self.audio.setVolume(0.7)
        self.player.positionChanged.connect(self.on_position)
        self.player.durationChanged.connect(self.on_duration)
        self.player.errorOccurred.connect(self.on_player_error)
        self.subtitle_now = QLabel("")
        self.subtitle_now.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_now.setWordWrap(True)
        self.subtitle_now.setMinimumHeight(42)
        rl.addWidget(self.subtitle_now)
        controls = QHBoxLayout()
        for name, callback in (("▶", self.play_current), ("Ⅱ", self.player.pause), ("■", self.player.stop)):
            btn = QPushButton(name)
            btn.setMaximumWidth(43)
            btn.clicked.connect(callback)
            controls.addWidget(btn)
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
        volume = QSlider(Qt.Orientation.Horizontal)
        volume.setRange(0, 100)
        volume.setValue(70)
        volume.valueChanged.connect(lambda n: self.audio.setVolume(n / 100))
        external_row.addWidget(volume)
        rl.addLayout(external_row)
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
        sub_tab = QWidget()
        sl = QVBoxLayout(sub_tab)
        self.subtitle_combo = QComboBox()
        self.subtitle_combo.currentIndexChanged.connect(self.load_selected_subtitles)
        sl.addWidget(self.subtitle_combo)
        sl.addWidget(QLabel("자막을 더블클릭하면 해당 구간으로 이동합니다."))
        self.subtitle_list = QListWidget()
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
        self.root_input.setText(get_setting(self.db, "download_root", DEFAULT_ROOT))
        self.interval_spin.setValue(int(get_setting(self.db, "interval", "20")))
        try:
            sizes = json.loads(get_setting(self.db, "split_outer", "[]"))
            if len(sizes) == 3:
                self.outer_splitter.setSizes(sizes)
            sizes = json.loads(get_setting(self.db, "split_inner", "[]"))
            if len(sizes) == 2:
                self.inner_splitter.setSizes(sizes)
        except (ValueError, TypeError):
            pass

    def save_settings(self):
        if not hasattr(self, "db"):
            return
        set_setting(self.db, "download_root", self.root_input.text().strip())
        set_setting(self.db, "interval", str(self.interval_spin.value()))

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "다운로드 경로 선택", self.root_input.text().strip())
        if folder:
            self.root_input.setText(folder)
            self.save_settings()
            self.scan_library()

    def add_log(self, message: str):
        LOGGER.info(message)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.appendPlainText(f"[{timestamp}] {message}")

    def add_urls(self):
        candidates = re.findall(r"https?://[^\s<>\"']+", self.url_edit.toPlainText())
        added, duplicate, invalid = 0, 0, 0
        with self.db:
            for candidate in candidates:
                parsed = canonical_url(candidate.rstrip("),;"))
                if parsed is None:
                    invalid += 1
                    continue
                url, kind = parsed
                before = self.db.total_changes
                self.db.execute("INSERT OR IGNORE INTO jobs(url,kind,title,status,created_at,updated_at) "
                                "VALUES(?,?,?,?,?,?)", (url, kind, url, "queued", now_str(), now_str()))
                if self.db.total_changes > before:
                    added += 1
                else:
                    duplicate += 1
        self.refresh_jobs()
        self.add_log(f"주소 등록: 신규 {added}, 중복 {duplicate}, 잘못된 주소 {invalid}")
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

    def retry_jobs(self):
        ids = self.selected_job_ids()
        if not ids:
            return
        with self.db:
            for job_id in ids:
                self.db.execute("UPDATE jobs SET status='queued',progress=0,error='',updated_at=? "
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
        if not hasattr(self, "jobs_table"):
            return
        selected = set(self.selected_job_ids())
        rows = self.db.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT 1000").fetchall()
        table = self.jobs_table
        table.blockSignals(True)
        table.setRowCount(len(rows))
        status_text = {"queued": "대기", "running": "다운로드 중", "done": "완료", "failed": "실패", "expanded": "목록 등록"}
        for i, job in enumerate(rows):
            vals = [str(job["id"]), status_text.get(job["status"], job["status"]),
                    f"{job['progress']:.0f}%", job["title"] or job["url"], job["error"]]
            for col, val in enumerate(vals):
                it = QTableWidgetItem(str(val))
                if col == 3:
                    it.setToolTip(job["url"])
                table.setItem(i, col, it)
            if job["id"] in selected:
                table.selectRow(i)
        table.blockSignals(False)

    def on_worker_progress(self, job_id, progress):
        # 진행률 갱신마다 전체 대기열 테이블을 다시 구성하지 않는다.
        for row in range(self.jobs_table.rowCount()):
            item = self.jobs_table.item(row, 0)
            if item and item.text() == str(job_id):
                value = self.jobs_table.item(row, 2)
                if value:
                    value.setText(f"{progress:.1f}%")
                break

    def start_download(self):
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
        if not self.db.execute("SELECT 1 FROM jobs WHERE status='queued' LIMIT 1").fetchone():
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
        self.worker = DownloadWorker(root, self.interval_spin.value(), self)
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

    def on_worker_finished(self):
        self.root_input.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.interval_spin.setEnabled(True)
        self.refresh_jobs()
        self.refresh_library()
        self.add_log("다운로드 작업자 종료")

    def scan_library(self):
        if self.scanner and self.scanner.isRunning():
            return
        root = self.root_input.text().strip()
        if not root:
            return
        self.scanner = ScanWorker(root, self)
        self.scanner.message.connect(self.add_log)
        self.scanner.finished_scan.connect(self.on_scan_finished)
        self.scanner.start()
        self.statusBar().showMessage("다운로드 폴더의 기존 영상을 검색 중...")

    def on_scan_finished(self, records):
        for record in records:
            try:
                upsert_video(self.db, record)
            except (sqlite3.Error, OSError) as ex:
                self.add_log(f"[색인 오류] {record.get('file_path','')}: {ex}")
        self.statusBar().showMessage(f"폴더 검색 완료: {len(records)}개 영상 확인")
        self.add_log(f"[라이브러리 검색] 영상 {len(records)}개 확인, 기존 메모 유지")
        self.refresh_library()

    def refresh_library(self):
        if not hasattr(self, "library_table"):
            return
        current_channel = self.channel_combo.currentText()
        all_channels = [r[0] for r in self.db.execute("SELECT DISTINCT channel FROM videos ORDER BY channel")]
        if self.channel_combo.count() != len(all_channels) + 1 or [self.channel_combo.itemText(i) for i in range(1, self.channel_combo.count())] != all_channels:
            self.channel_combo.blockSignals(True)
            self.channel_combo.clear()
            self.channel_combo.addItem("전체 채널")
            self.channel_combo.addItems(all_channels)
            index = self.channel_combo.findText(current_channel)
            self.channel_combo.setCurrentIndex(index if index >= 0 else 0)
            self.channel_combo.blockSignals(False)
        text = f"%{self.search_input.text().strip()}%"
        channel = self.channel_combo.currentText()
        filters = "WHERE (title LIKE ? OR channel LIKE ? OR memo LIKE ? OR video_id LIKE ?)"
        params = [text] * 4
        if channel != "전체 채널":
            filters += " AND channel=?"
            params.append(channel)
        rows = self.db.execute(f"SELECT video_id,title,channel,upload_date,memo,file_path FROM videos {filters} ORDER BY upload_date DESC,title LIMIT 10000", params).fetchall()
        table = self.library_table
        table.blockSignals(True)
        table.setRowCount(len(rows))
        selected_row = -1
        for row_idx, rec in enumerate(rows):
            present = Path(rec["file_path"]).is_file()
            values = [rec["title"], rec["channel"], rec["upload_date"],
                      "●" if rec["memo"] else "", "있음" if present else "파일 없음"]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                if col == 0:
                    item.setData(Qt.ItemDataRole.UserRole, rec["video_id"])
                if col == 4:
                    item.setToolTip(rec["file_path"])
                table.setItem(row_idx, col, item)
            if rec["video_id"] == self.current_id:
                selected_row = row_idx
        if selected_row >= 0:
            table.selectRow(selected_row)
        table.blockSignals(False)
        self.statusBar().showMessage(f"라이브러리 {len(rows)}개 표시 | DB/로그는 {APP_DATA}에 보관")

    def on_video_selected(self):
        selected = self.library_table.selectedItems()
        if not selected:
            return
        key_item = self.library_table.item(selected[0].row(), 0)
        if not key_item:
            return
        video_id = key_item.data(Qt.ItemDataRole.UserRole)
        if not video_id or video_id == self.current_id:
            return
        self.save_memo(silent=True)
        row = self.db.execute("SELECT * FROM videos WHERE video_id=?", (video_id,)).fetchone()
        if row is None:
            return
        self.current_id = video_id
        self.current_path = Path(row["file_path"])
        self.video_info_label.setText(f"{row['channel']} · {row['title']}")
        self._loading_note = True
        self.memo_edit.setPlainText(row["memo"])
        self._loading_note = False
        self.player.stop()
        self.subtitle_now.clear()
        if self.current_path.is_file():
            self.player.setSource(QUrl.fromLocalFile(str(self.current_path)))
        else:
            self.player.setSource(QUrl())
            self.video_info_label.setText("파일이 존재하지 않습니다: " + str(self.current_path))
        self.find_subtitle_files()
        self.refresh_library()

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
                files = sorted(self.current_path.parent.glob(self.current_path.stem + "*.srt"))
                for file in files:
                    self.subtitle_combo.addItem(file.name, str(file))
            except OSError:
                pass
        self.subtitle_combo.blockSignals(False)
        self.load_selected_subtitles()

    def load_selected_subtitles(self):
        self.subtitles = []
        self.subtitle_starts = []
        self.current_subtitle_index = -1
        self.subtitle_list.clear()
        self.subtitle_now.clear()
        path = self.subtitle_combo.currentData()
        if not path:
            return
        self.subtitles = parse_srt(Path(path))
        self.subtitle_starts = [item[0] for item in self.subtitles]
        self.subtitle_list.addItems([f"{millis_text(start)}  {txt.replace(chr(10), ' / ')}"
                                     for start, end, txt in self.subtitles])
        self.add_log(f"[SRT 자막] {Path(path).name} ({len(self.subtitles)}개 구간)")

    def subtitle_jump(self, item):
        pos = self.subtitle_list.row(item)
        if 0 <= pos < len(self.subtitles):
            self.player.setPosition(self.subtitles[pos][0])
            if self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
                self.player.play()

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
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "다운로드 중", "다운로드 작업이 실행 중입니다. 먼저 '즉시 중단'한 후 종료해 주세요.")
            event.ignore()
            return
        if self.scanner and self.scanner.isRunning():
            QMessageBox.information(self, "검색 중", "폴더 검색이 끝난 후 종료해 주세요.")
            event.ignore()
            return
        self.save_memo(silent=True)
        self.save_settings()
        set_setting(self.db, "split_outer", json.dumps(self.outer_splitter.sizes()))
        set_setting(self.db, "split_inner", json.dumps(self.inner_splitter.sizes()))
        set_setting(self.db, "window_width", str(self.width()))
        set_setting(self.db, "window_height", str(self.height()))
        self.player.stop()
        self.db.close()
        LOGGER.info("정상 종료")
        event.accept()


def main():
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Minton.VideoLibrary.1")
        except (OSError, AttributeError):
            pass
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName(APP_TITLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
