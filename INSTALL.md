# Minton Video Library V1.1 — Windows 설치·실행·GitHub 안내

대상: **Windows 10/11, PowerShell, Python 3.12**, 프로젝트 위치 `D:\stockproj\minton_video_library`.

이 프로젝트는 **Docker를 사용하지 않습니다**. 코드 `minton_video_library.py` 하나를 실행합니다. 다른 버전의 Python이 시스템에 있어도 이 프로젝트 전용 Python 3.12 `.venv`를 사용합니다.

## 1. 파일 배치하기

프로젝트 ZIP 파일을 `D:\stockproj`에 압축 해제합니다. 다음 경로인지 확인하세요.

```text
D:\stockproj\minton_video_library\
  minton_video_library.py
  README.md
  INSTALL.md
  .gitignore
```

Windows 탐색기에서 `.gitignore`가 보이지 않으면 **보기 → 숨긴 항목**을 확인하세요. 메모장으로 직접 저장하는 경우 파일명 뒤에 `.txt`가 붙지 않도록 유의하세요.

PowerShell에서 확인:

```powershell
cd D:\stockproj\minton_video_library
Get-ChildItem -Force
```

## 2. Python 3.12 설치 확인

```powershell
py -0p
py -3.12 --version
```

`Python 3.12.x`가 나와야 합니다. 다른 버전만 있거나 `No suitable Python runtime found` 메시지가 나오면 Python 3.12를 먼저 설치하세요.

```powershell
winget install -e --id Python.Python.3.12
```

설치 후 **새 PowerShell 창**을 열어 다시 버전을 확인하세요. `python --version`이 3.13이라고 나와도 괜찮습니다. 이후 명령에서는 명시적으로 `py -3.12`와 `.venv\Scripts\python.exe`만 사용합니다.

## 3. Deno, FFmpeg 설치

yt-dlp의 JavaScript 처리를 위한 **Deno**, 영상·오디오 병합 및 자막 변환을 위한 **FFmpeg**가 필요합니다.

```powershell
winget install -e --id DenoLand.Deno
winget install -e --id Gyan.FFmpeg
```

이미 설치했다면 설치 단계는 생략할 수 있습니다. 새 PowerShell에서 다음을 점검합니다.

```powershell
deno --version
ffmpeg -version
where.exe deno
where.exe ffmpeg
```

`deno` 또는 `ffmpeg`가 인식되지 않으면 터미널을 다시 열고 PATH를 확인하세요. **PowerShell 별칭이나 앱 실행 별칭이 아닌 실제 실행 파일**이 인식되어야 합니다.

## 4. 프로젝트 가상환경 만들기

```powershell
cd D:\stockproj\minton_video_library
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -U PySide6 "yt-dlp[default]"
```

이 방식은 PowerShell 실행 정책에 의한 `Activate.ps1` 차단과 무관하게 동작합니다. 반드시 `.venv\Scripts\python.exe`를 사용하세요.

설치 확인:

```powershell
.\.venv\Scripts\python.exe -m yt_dlp --version
.\.venv\Scripts\python.exe -c "import PySide6; from PySide6.QtMultimedia import QMediaPlayer; print('PySide6/Qt Multimedia OK')"
```

**참고:** 인터넷 연결이 필요합니다. `yt-dlp`와 YouTube 측 변경으로 다운로드 동작이 달라질 수 있으므로 문제가 발생하면 먼저 `yt-dlp`를 최신 버전으로 업데이트하세요.

## 5. 프로그램 실행

```powershell
cd D:\stockproj\minton_video_library
.\.venv\Scripts\python.exe minton_video_library.py
```

GUI 창이 뜨면 다음과 같이 초기 설정합니다.

| 항목 | 권장 초기값 | 설명 |
| --- | --- | --- |
| 저장 폴더 | `D:\99.유튜브다운\minton.youtube` | 폴더 변경 가능, 다음 실행에도 유지 |
| 간격 (초) | `20` | 다음 영상 다운로드 전 대기 (0~3600초) |
| 동시 다운로드 | `1개` | 고정. 다른 영상과 병렬 다운로드하지 않음 |
| 자막 언어 | 한국어 `ko.*` | 기존 사용 옵션. 한국어 자막이 있을 때 SRT 저장 |

### 첫 실행 시험

1. 본인이 이용 권한을 가진 YouTube **영상 링크 1개**를 붙여 넣으세요.
2. **대기열에 추가** → **▶ 다운로드 시작 / 재개**를 누르세요.
3. 진행 상태, 화면 하단 로그, 지정한 저장 폴더의 채널별 디렉터리를 확인하세요.
4. 다운로드된 파일은 **영상 라이브러리**에서 선택하여 재생합니다.
5. 영상별 메모를 저장하고 프로그램을 종료했다 다시 실행하여 유지되는지 확인하세요.
6. 자막이 있다면 **전체 자막 / 구간 이동** 탭에서 SRT 파일을 고르고 항목을 더블클릭해 구간 이동을 확인하세요.

재생목록을 처음 테스트할 때는 소량의 공개 영상이 들어 있는 목록으로 확인하는 것을 권장합니다.

### 중지 / 재개 동작

- **일시정지**: 현재 동영상을 끝까지 처리한 뒤 다음 작업 전에 정지합니다.
- **즉시 중단**: 현재 yt-dlp 프로세스를 종료합니다. `.part` 파일이 남을 수 있으며 재시도 시 이어받기를 시도합니다.
- **선택 항목 다시 대기**: 작업을 대기로 전환합니다. 완료된 영상도 파일이 존재하면 중복 다운로드를 건너뜁니다.
- **선택 대기열 삭제**: 작업 기록만 삭제합니다. 저장된 영상·자막·메모는 삭제되지 않습니다.

## 6. 데이터와 백업

프로그램이 관리하는 세 가지 위치를 구분하세요.

| 종류 | 위치 | GitHub 업로드 |
| --- | --- | --- |
| 프로그램 소스·설명서 | `D:\stockproj\minton_video_library` | 가능 (코드·문서만) |
| 영상·자막·메타데이터 | `D:\99.유튜브다운\minton.youtube\채널명\` (단일) / `채널명\재생목록명\` (목록) | **하지 않음** |
| 메모·설정·대기열 DB | `%LOCALAPPDATA%\MintonVideoLibrary\library.db` | **하지 않음** |
| 실행 로그 | `%LOCALAPPDATA%\MintonVideoLibrary\logs\minton_video_library.log` | **하지 않음** |

프로그램을 종료한 뒤 SQLite DB와 영상 폴더를 별도 위치에 백업하세요. 소스만 GitHub에 업로드해도 영상 메모가 자동으로 백업되지는 않습니다.

DB 파일 위치 확인:

```powershell
explorer.exe "$env:LOCALAPPDATA\MintonVideoLibrary"
```

## 7. GitHub 비공개 저장소에 등록하기

Git과 GitHub CLI(`gh`)를 설치하지 않았다면 다음을 실행합니다.

```powershell
winget install -e --id Git.Git
winget install -e --id GitHub.cli
```

설치 후 새 PowerShell에서 버전 확인:

```powershell
git --version
gh --version
```

Git 사용자 정보가 아직 설정되지 않았다면 **자신의 GitHub 계정 정보**로 변경해 설정하세요.

```powershell
git config --global user.name "GitHub에 표시할 이름"
git config --global user.email "본인 GitHub 계정 이메일"
```

저장소 생성 및 최초 커밋:

```powershell
cd D:\stockproj\minton_video_library
git init
git branch -M main
git add minton_video_library.py README.md INSTALL.md .gitignore
git status
git commit -m "Initial Minton Video Library v1.1"
```

`git status`에서 **`.venv`, 영상, 자막, SQLite DB, 로그가 추적되지 않는지** 꼭 확인하세요. 확인 방법:

```powershell
git status --short
git check-ignore -v .venv\Scripts\python.exe
```

GitHub 로그인 및 **비공개(Private)** 저장소 생성·푸시:

```powershell
gh auth login
gh repo create minton_video_library --private --source . --remote origin --push
```

GitHub의 저장소가 생성되면 나중에 소스 및 문서를 수정했을 때 아래 명령으로 업로드합니다.

```powershell
cd D:\stockproj\minton_video_library
git add minton_video_library.py README.md INSTALL.md .gitignore
git commit -m "Update Minton Video Library"
git push
```

`gh`를 사용하지 않으려면 GitHub 웹사이트에서 빈 비공개 저장소 `minton_video_library`를 만들고 표시된 저장소 URL로 `git remote add origin <저장소URL>`을 설정한 뒤 `git push -u origin main`을 실행할 수 있습니다.

**주의:** 이미 Git에 추적된 파일은 `.gitignore` 규칙을 추가해도 자동으로 추적이 해제되지 않습니다. 실수로 영상/DB를 이미 `git add`했다면 커밋·푸시 전에 `git restore --staged <해당파일>`로 스테이징부터 취소하세요. 비밀정보가 이미 게시된 경우 이 조치만으로 공개 이력이 지워지지는 않습니다.

## 8. 문제 해결

| 현상 | 우선 확인 / 조치 |
| --- | --- |
| `py -3.12` 명령 실패 | Python 3.12 설치 및 `py -0p` 결과 확인 |
| PowerShell 활성화 정책 오류 | 활성화하지 말고 `.\.venv\Scripts\python.exe`를 직접 실행 |
| `No module named PySide6` 또는 `yt_dlp` | 같은 `.venv`에 설치했는지 4절의 명령 재실행 |
| `Deno` 또는 `FFmpeg`가 없다는 경고 | 새 PowerShell에서 `deno --version`, `ffmpeg -version` 검사 |
| yt-dlp 추출 실패 / HTTP 403 | `.venv`의 yt-dlp 갱신, URL 접근 권한·로그 확인. 일부 영상은 다운로드 불가 |
| 자막이 보이지 않음 | 실제 `*.srt` 생성 여부 확인. 한국어 자막이 없는 경우 받을 수 없음 |
| 동영상이 내장 플레이어에서 재생되지 않음 | 우측 **기본 플레이어로 열기**로 테스트하고 영상 코덱 확인 |
| 영상 목록에 기존 파일이 없음 | 현재 저장 폴더와 **폴더 다시 검색** 실행 여부 확인 |
| 메모가 GitHub에 없음 | 메모는 로컬 SQLite DB에만 저장. 6절의 별도 백업 필요 |
| `git`/`gh` 명령을 찾지 못함 | 설치 후 새 PowerShell에서 PATH 재확인 |

다운로드 오류 발생 시 업데이트 및 로그 보기:

```powershell
cd D:\stockproj\minton_video_library
.\.venv\Scripts\python.exe -m pip install -U "yt-dlp[default]"
notepad "$env:LOCALAPPDATA\MintonVideoLibrary\logs\minton_video_library.log"
```

로그를 공유할 때는 영상 URL, 로컬 파일 경로, 사용자 정보 등 개인 정보가 있는지 확인하세요.

## 9. 이후 버전 업데이트

프로그램을 먼저 종료하고 `minton_video_library.py` 파일을 새 버전으로 교체하거나 Git에서 업데이트합니다. **`library.db`와 다운로드 폴더는 삭제하지 마세요.**

```powershell
cd D:\stockproj\minton_video_library
.\.venv\Scripts\python.exe -m pip install -U PySide6 "yt-dlp[default]"
.\.venv\Scripts\python.exe minton_video_library.py
```

문제가 생겼다면 변경 직전의 Python 소스, `%LOCALAPPDATA%\MintonVideoLibrary\library.db`, 관련 로그를 함께 보관하세요.

---

**운영 원칙:** 다운로드와 저장·사용은 접근 권한과 저작권·플랫폼 이용약관을 준수하는 영상으로 제한합니다. 개발 중 기존 기능·로그·UI 동작을 보존하고, Python 파일 상단의 전체 기능 주석을 최신 상태로 유지합니다.

---

## V1.1 업데이트 및 재생목록 확인

기존 설치자는 프로그램 종료 후 **`minton_video_library.py`만 새 파일로 교체**하세요.
`%LOCALAPPDATA%\MintonVideoLibrary\library.db` 와 다운로드 폴더는 지우지 마세요.
다음 실행 시 DB에 재생목록 컨텍스트와 수동 제목 컬럼이 자동 추가됩니다. 메모와 과거 로그는 유지됩니다.

재생목록 URL은 `https://www.youtube.com/watch?v=96Y3Airgf6M&list=PLX1IndZwkjj0` 또는
`https://www.youtube.com/playlist?list=PLX1IndZwkjj0` 형식 모두 지원합니다.
수동 재생목록 폴더명을 선택하면 해당 이름이 우선하며, `PLX1IndZwkjj0`는
`윤이콕TV\물A조라고 놀리지말아요\` 로 분류합니다.

동영상 파일을 외부 탐색기에서 삭제했다면 최대 약 15초 후 라이브러리 기본 목록에서 숨겨집니다.
**누락 영상도 표시**를 켜면 해당 DB 레코드와 메모가 여전히 확인됩니다.
폴더를 옮기면 자동 재검색은 약 60초마다 실행되며, 같은 YouTube 영상 ID가
파일명/metadata에 있어야 메모가 정확히 연결됩니다.
라이브러리의 **파일 이동** 버튼을 쓰면 영상, 자막, metadata 경로가 같이 변경됩니다.
파일 삭제는 **영상 휴지통 삭제** 버튼 사용을 권장합니다.

자막이 안 보이면 폴더의 `*.ko.srt`를 확인한 다음 **전체 자막 / 구간 이동** 탭에서
SRT 목록을 선택하거나 **전체 자막 큰창**을 누르세요. 자막 항목 더블클릭 시
영상이 탐색 가능할 때 해당 구간으로 재생합니다. 유튜브 원본에 제공되지 않는 한국어 자막은 받을 수 없습니다.

한국어 자동 번역 서비스는 사용하지 않습니다. YouTube에서 한국어 제목/설명을
제공하면 우선 사용하며, 미제공 시에는 **한글 제목/파일명 변경**으로 직접 설정합니다.

검증 범위: Python 문법 및 URL/SQL/폴더/자막/메모 핵심 테스트 수행.
본 환경에서는 Windows/PySide6 영상 재생과 실제 YouTube 다운로드까지 통합 검증하지 못했습니다.
