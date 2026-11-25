# MiracleDesk 브랜딩 패치 — CI 빌드 직전(체크아웃 직후)에 실행한다.
# hbb_common 서브모듈은 포크하지 않고 빌드 시점에 직접 고친다.
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "miracledesk", "assets")
APP_NAME = "MiracleDesk"
SERVER = os.environ.get("RENDEZVOUS_SERVER", "rd.godf.kr")
KEY = os.environ.get("RS_PUB_KEY", "").strip()
if not KEY:
    sys.exit("RS_PUB_KEY 환경변수가 비어 있음 (저장소 Secrets 확인)")


def sub(path, pattern, repl, count=1):
    p = os.path.join(ROOT, path)
    s = open(p, encoding="utf-8").read()
    new, n = re.subn(pattern, repl, s, count=count)
    if n == 0:
        sys.exit(f"패치 실패: {path} :: {pattern}")
    open(p, "w", encoding="utf-8", newline="").write(new)
    print(f"patched {path} ({n})")


cfg = "libs/hbb_common/src/config.rs"
sub(cfg, r'(APP_NAME: RwLock<String> = RwLock::new\()"RustDesk"', rf'\1"{APP_NAME}"')
sub(cfg, r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];',
    f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{SERVER}"];')
sub(cfg, r'pub const RS_PUB_KEY: &str = "[^"]*";', f'pub const RS_PUB_KEY: &str = "{KEY}";')

rc = "flutter/windows/runner/Runner.rc"
sub(rc, r'"FileDescription", "RustDesk Remote Desktop"', f'"FileDescription", "{APP_NAME} Remote Desktop"')
sub(rc, r'"ProductName", "RustDesk"', f'"ProductName", "{APP_NAME}"')
sub(rc, r'"CompanyName", "[^"]*"', '"CompanyName", "GODF"')

packer = "libs/portable/Cargo.toml"
sub(packer, r'description = "RustDesk Remote Desktop"', f'description = "{APP_NAME} Remote Desktop"')
sub(packer, r'LegalCopyright = "[^"]*"', 'LegalCopyright = "GODF"\nCompanyName = "GODF"')
sub(packer, r'ProductName = "RustDesk"', f'ProductName = "{APP_NAME}"')
sub(packer, r'OriginalFilename = "rustdesk\.exe"', f'OriginalFilename = "{APP_NAME}.exe"')
sub(packer, r'FileDescription = "RustDesk Remote Desktop"', f'FileDescription = "{APP_NAME} Remote Desktop"')

copies = {
    "icon.ico": ["res/icon.ico", "flutter/windows/runner/resources/app_icon.ico"],
    "tray-icon.ico": ["res/tray-icon.ico"],
    "icon.png": ["res/icon.png", "res/mac-icon.png"],
    "32x32.png": ["res/32x32.png"],
    "64x64.png": ["res/64x64.png"],
    "128x128.png": ["res/128x128.png"],
    "128x128@2x.png": ["res/128x128@2x.png"],
    "icon.svg": ["flutter/assets/icon.svg"],
    "flutter_icon.png": ["flutter/assets/icon.png"],
    "logo_light.png": ["flutter/assets/logo_light.png", "flutter/assets/logo.png"],
    "logo_dark.png": ["flutter/assets/logo_dark.png"],
}
for src, dsts in copies.items():
    for d in dsts:
        shutil.copyfile(os.path.join(ASSETS, src), os.path.join(ROOT, d))
        print(f"copied {src} -> {d}")
print("MiracleDesk branding OK")
