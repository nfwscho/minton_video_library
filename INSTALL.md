# INSTALL.md — Minton Video Library V1.2 설치·업데이트·이동 안내

## 1. Windows 사전 준비

- Windows 10/11, Python **3.12 (64비트)**, PowerShell
- Deno: YouTube 추출 JS 런타임
- FFmpeg: H.264/AAC 영상 병합, 자막 변환에 필요
- PySide6: GUI/동영상 재생
- yt-dlp: 영상 및 한국어 자막 내려받기

설치 확인 (PowerShell 새 창):

```powershell
py -3.12 --version
winget install -e --id DenoLand.Deno
winget install -e --id Gyan.FFmpeg
# PowerShell을 다시 연 다음 확인
deno --version
ffmpeg -version
```

환경마다 winget 패키지 설치 여부·PATH 적용이 다를 수 있습니다. `deno`/`ffmpeg`를 찾을 수 없으면 PowerShell을 완전히 닫았다가 새로 여세요.

## 2. 프로젝트 폴더 설치

파일 구조를 다음과 같이 둡니다.

```text
D:\stockproj\minton_video_library\
├── minton_video_library.py
├── README.md
├── INSTALL.md
└── .gitignore
```

PowerShell:

```powershell
cd D:\stockproj\minton_video_library
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --upgrade PySide6 "yt-dlp[default]"
.\.venv\Scripts\python.exe minton_video_library.py
```

`py -3.12`가 실행되지 않으면 Python 3.12를 먼저 설치하세요. 이미 `.venv`가 있으면 다시 만들지 않아도 됩니다.

## 3. V1.1에서 V1.2로 업데이트

**중요: 기존 메모가 저장된 AppData DB를 절대 먼저 삭제하지 마세요.**

1. V1.1 프로그램을 완전히 종료합니다. 영상 다운로드가 진행 중이면 중단한 뒤 종료합니다.
2. 기존 DB를 별도 백업합니다. 예:

   ```powershell
   $oldDb = Join-Path $env:LOCALAPPDATA 'MintonVideoLibrary\library.db'
   Copy-Item $oldDb 'D:\stockproj\minton_video_library\library_pre_v12_backup.db' -ErrorAction Stop
   ```

   이 파일은 `.gitignore`로 Git 업로드에서 제외됩니다. 백업 파일을 별도 디스크에도 보관하면 더 안전합니다.
3. V1.2의 `minton_video_library.py`, `README.md`, `INSTALL.md`, `.gitignore` 파일을 기존 프로젝트 폴더에 덮어씁니다. **영상 폴더 및 기존 AppData DB는 건드리지 마세요.**
4. 기존 가상환경으로 V1.2를 실행합니다.

   ```powershell
   cd D:\stockproj\minton_video_library
   .\.venv\Scripts\python.exe minton_video_library.py
   ```

5. V1.2는 현재 다운로드 폴더(`D:\99.유튜브다운\minton.youtube` 또는 V1.1 설정 경로) 아래 `_database\library.db`가 없으면 기존 `%LOCALAPPDATA%\MintonVideoLibrary\library.db`를 SQLite 백업 API로 **복제**합니다. 기존 DB 파일은 보존합니다.
6. 예전 DB에 저장된 영상 **절대경로**를 라이브러리 기준 **상대경로**로 바꿉니다. 새로운 `file_size`, `major_category`, `sub_category`, `tags`, `clip_marks` 데이터 구조가 추가됩니다. **기존 메모·대기열·제목 변경·로그는 삭제하지 않습니다.**
7. 프로그램에서 **폴더 다시 검색**을 누르고 영상과 메모, 크기, 분류 등을 확인하세요.

> 기존 V1.1 AppData DB가 없는 신규 설치에서는 `D:\99.유튜브다운\minton.youtube\_database\library.db`를 새로 생성합니다. 대상 폴더에 이미 `library.db`가 있다면 **덮어쓰거나 이전 DB를 자동으로 합치지 않습니다.** 원본과 다른 종류의 라이브러리를 수동 병합하는 기능은 없습니다.

## 4. 디스크 변경 / 외장하드 이동

예: `D:\99.유튜브다운\minton.youtube`에서 `E:\minton.youtube`로 이동.

1. 프로그램 종료.
2. **`minton.youtube` 폴더 전체**를 복사합니다. 채널 폴더, 재생목록 폴더, SRT, `.info.json`, **`_database\library.db`**가 함께 있어야 합니다.
3. 새 드라이브의 `_database\library.db`가 존재하는지 먼저 확인합니다.
4. 프로그램의 상단 **찾기**로 `E:\minton.youtube` 폴더를 선택합니다. 이전 경로가 사라졌다면 프로그램 시작 때 폴더 선택 창이 나타납니다.
5. **폴더 다시 검색** → 파일 크기·메모·분류·클립 기록 확인 후 이전 폴더 정리.

새 PC에서 직접 경로를 지정해 시작할 수도 있습니다.

```powershell
cd D:\stockproj\minton_video_library
.\.venv\Scripts\python.exe minton_video_library.py --root "E:\minton.youtube"
```

새 PC에서는 Python/Deno/FFmpeg 설치 및 새 `.venv` 생성이 필요할 수 있습니다. 라이브러리 DB는 영상과 함께 이동되지만 **Windows용 Python GUI가 휴대폰에서 직접 실행되는 것은 아닙니다.** 휴대폰에서는 MP4 및 SRT 파일을 호환 플레이어로 열고, 추후 클립 내보내기를 통해 구간 파일을 따로 옮기는 방식을 권장합니다.

**DB만 별도로 복사하는 것은 충분하지 않습니다.** DB가 기존 루트 상대경로로 동영상을 가리키므로 동일한 폴더 구조의 실제 미디어 파일도 함께 필요합니다.

### 프로그램에서 다른 빈 폴더를 고른 경우

찾기로 `_database\library.db`가 없는 곳을 지정하면 **현재 DB 복사 / 새 라이브러리 시작 / 취소** 중 선택할 수 있습니다. 현재 DB 복사는 **영상 파일을 복사하지 않으므로**, 동일한 폴더 구조의 영상을 직접 옮긴 뒤 검색해야 합니다. 실수로 새 라이브러리를 생성해도 기존 폴더의 원본 DB는 삭제되지 않습니다.

## 5. UI 사용법

### 다운로드

1. 상단 다운로드 폴더를 확인합니다. 라이브러리 DB가 이 폴더에 종속되므로 **경로 직접 입력 대신 찾기**로 변경합니다.
2. YouTube 영상 또는 재생목록 URL을 한 줄씩 넣습니다. `watch?v=...&list=...`도 전체 재생목록으로 처리됩니다.
3. 원하는 경우 **채널 폴더명/재생목록 폴더명**을 입력하고 대기열에 추가합니다.
4. **다운로드 시작/재개**를 누릅니다. 기본 간격은 20초이며, 동시에 1개만 받습니다.
5. 대기열의 진행률 바/숫자·하단 로그를 확인합니다. 다운로드 실패 시 항목을 다시 대기로 바꿀 수 있습니다.

### 영상 분류 및 자막/메모

1. 영상 라이브러리에는 **크기·대분류·세부분류** 열이 추가됩니다. 제목 등 모든 열 너비를 조정할 수 있습니다.
2. 영상 선택 → **배드민턴 분류·태그** 탭 → 대분류와 세부분류 선택, 태그 입력 → 저장. 분류 변경 시에도 자동 저장됩니다.
3. 채널·대분류 필터 및 검색창에서 분류·태그·메모 검색을 활용할 수 있습니다.
4. 영상 선택 → **영상 메모**에 자유 메모를 작성합니다. 기존 동작처럼 버튼·선택 변경·종료 때 저장됩니다.
5. **전체 자막 / 구간 이동**에서 SRT 선택, 검색, 큰 창, 자막 줄 더블클릭 구간 이동을 사용합니다.
6. **클립 구간 기록** 탭에서 현재 영상 시각을 시작/끝으로 지정하고 구간명을 저장합니다. 이 기능은 현재 **구간 기록만** 수행하고 MP4 출력은 하지 않습니다.

### 외부 파일 삭제/이동

- 탐색기에서 삭제한 파일은 기본 라이브러리에서 숨기며 메모/분류 데이터는 DB에 유지합니다.
- 탐색기에서 같은 다운로드 루트 안으로 파일을 이동하면 자동 검색 또는 **폴더 다시 검색**으로 연결을 시도합니다. YouTube ID가 있는 영상은 해당 ID로 식별합니다.
- 프로그램 **파일 이동** 버튼은 자막/info.json 파일을 함께 옮깁니다. **휴지통 삭제**는 연관 파일도 함께 처리합니다.

## 6. 동영상 포맷과 휴대폰 활용

V1.1의 사용자 지정 yt-dlp 옵션을 그대로 유지합니다.

```text
--js-runtimes deno --remote-components ejs:npm
-f "bv[vcodec^=avc1][height<=1080]+ba[acodec^=mp4a]/b[vcodec^=avc1][height<=1080]"
--merge-output-format mp4
--write-subs --write-auto-subs --sub-langs "ko.*" --convert-subs srt
```

모바일 클립 출력은 향후 FFmpeg로 선택 구간을 재인코딩 또는 스트림 복사하여 정확도/처리 속도를 선택하는 기능을 계획할 수 있습니다. 재생할 Android 기기의 지원 코덱, 파일 크기, 자막 파일명 일치 여부를 확인하세요.

## 7. Git 및 GitHub 업로드

```powershell
cd D:\stockproj\minton_video_library
git status
git add minton_video_library.py README.md INSTALL.md .gitignore
git commit -m "feat: v1.2 portable library DB and badminton video classification"
git push origin main
```

새 저장소라면 `git init`, `git branch -M main`, GitHub CLI로 `gh auth login`, `gh repo create minton_video_library --private --source . --remote origin --push` 순서로 등록할 수 있습니다. 기존 GitHub 원격 저장소가 있으면 새로 만들지 말고 위의 `git push`만 실행하세요.

`.gitignore`가 DB, 영상, 자막, 로그 및 venv를 제외하도록 설정되어 있어도, **과거에 Git에 이미 추가된 대용량 파일은 자동 추적 해제되지 않습니다.** 그런 경우 `git rm --cached <파일경로>`로 인덱스에서만 제외한 뒤 커밋하세요.

## 8. 오류 해결

| 현상 | 해결 |
|---|---|
| `No module named PySide6` | `.\.venv\Scripts\python.exe -m pip install -U PySide6` |
| `No module named yt_dlp` | `.\.venv\Scripts\python.exe -m pip install -U "yt-dlp[default]"` |
| Deno/FFmpeg 실행 실패 | `deno --version`, `ffmpeg -version` 검사, PowerShell 재실행, 설치 경로 PATH 확인 |
| YouTube 다운로드 403/형식 없음 | yt-dlp 업데이트, 영상 접근 권한/지역/계정 조건, H.264/AAC 형식 제공 여부 확인. 로그 보존 |
| 업그레이드 후 메모/영상 표시 안 됨 | `D:\99.유튜브다운\minton.youtube\_database\library.db` 존재 확인, 원본 AppData DB 확인, `폴더 다시 검색` 실행 |
| 외장 디스크 변경 후 파일 누락 | **찾기**에서 DB가 포함된 새 `minton.youtube` 최상위 폴더 선택 |
| 영상 크기 미표시 | 폴더 다시 검색. 이미 파일이 없는 경우 이전 DB에 크기 기록이 없으면 `-` 또는 `0 B`로 표시될 수 있음 |
| 자막 목록 비어 있음 | 해당 영상의 `.srt` 유무와 자막 드롭다운 확인. YouTube가 한국어 자막을 제공하지 않으면 생성되지 않음 |
| 분류가 다른 PC에서 안 보임 | 메모·분류가 있는 `_database\library.db`까지 복사했는지 확인 |
| DB 파일 잠김 | 프로그램과 DB 뷰어를 종료하고 다시 시도. **실행 중 DB 파일만 복사하지 않기** |

로그 경로(변경 없음):

```powershell
notepad "$env:LOCALAPPDATA\MintonVideoLibrary\logs\minton_video_library.log"
```

**지원/검증 범위:** Python 문법 검사, SQLite V1.1 백업 복제·마이그레이션, 구간/분류 보존, 파일 크기 및 라이브러리 이동 복구는 테스트했습니다. 이 제작 환경에 PySide6가 설치되어 있지 않아 실제 Windows GUI/yt-dlp/FFmpeg 통합 실행은 미검증입니다.
