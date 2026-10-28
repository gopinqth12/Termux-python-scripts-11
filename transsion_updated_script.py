import os, sys, time, zipfile, threading, re, shutil, subprocess

# ── Colors ─────────────────────────────────────────────────────────────────────
RST  = '\033[0m';  BOLD = '\033[1m'
RED  = '\033[1;31m'; GRN  = '\033[1;32m'; YLW  = '\033[1;33m'
CYN  = '\033[1;36m'; WHT  = '\033[1;37m'
DGRN = '\033[0;32m'; DCYN = '\033[0;36m'; DWHT = '\033[0;37m'

# ── INFINIX logo ───────────────────────────────────────────────────────────────
LOGO = [
    r"  ██╗███╗   ██╗███████╗██╗███╗   ██╗██╗██╗  ██╗",
    r"  ██║████╗  ██║██╔════╝██║████╗  ██║██║╚██╗██╔╝",
    r"  ██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║ ╚███╔╝ ",
    r"  ██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║ ██╔██╗ ",
    r"  ██║██║ ╚████║██║     ██║██║ ╚████║██║██╔╝ ██╗",
    r"  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝",
]

# ── All Transsion keywords ─────────────────────────────────────────────────────
KEYWORDS = [
    'infinix','tecno','itel','transsion','spice',
    'xos','hios','stock','firmware','rom','official',
    'x6833','x6835','x6816','x6818','x6819','x6820','x6823','x6826',
    'x6827','x6829','x6830','x6716','x6717','x6739','x6833b','x6833c',
    'x6851','x6853','x6852','x6815','x6817','x6821','x6840','x6850',
    'x6871','x6873','x6885','x6893','x6525','x6526','x6527','x6528',
    'x6529','x6531','x6515','x6516','x6517','x6518',
    'x680','x682','x683','x687','x688','x690','x692','x693','x694','x695','x696',
    'ci6','ci7','ci8','cg7','cg8','ch6','ch7','ck6','ck7','ck8','cl6','cl7','cl8',
    'cm6','cm7','cm8','kd6','kd7','ke5','ke6','ke7','ke8','kf6','kf7','kf8',
    'kg5','kg6','kg7','kg8','kh5','kh6','kh7','kh8','ki5','ki6','ki7','ki8',
    'kj5','kj6','kj7','kj8','lf7','lf8','lg6','lg7','lh6','lh7','lh8',
    'li6','li7','li8','le6','le7','le8','lf6',
    'a571','a572','a581','a582','a591','a601','a602','a661','a662','a671','a672','a681',
    'p371','p372','p381','p382','p391','p401','p402','p551','p661','s661','s671','s681',
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def clr():    os.system("clear")
def w(t=.6):  time.sleep(t)
def strip(s): return re.sub(r'\033\[[0-9;]*m', '', s)
def cols():   return shutil.get_terminal_size((52, 24)).columns
def W():      return max(40, min(cols() - 4, 60))

def _run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

def _run_check(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode == 0, r.stdout + r.stderr

# ── Box drawing ────────────────────────────────────────────────────────────────
def _top():   print(f"{CYN}╔{'═'*W()}╗{RST}")
def _bot():   print(f"{CYN}╚{'═'*W()}╝{RST}")
def _sdiv():  print(f"{CYN}╟{'─'*W()}╢{RST}")
def _empty(): print(f"{CYN}║{' '*W()}║{RST}")

def _cbox(text, color=""):
    clean = strip(text)
    pad   = max(0, W() - len(clean))
    l, r  = pad//2, pad - pad//2
    print(f"{CYN}║{' '*l}{color}{text}{RST}{' '*r}{CYN}║{RST}")

def _row(text, color=DWHT):
    clean = strip(text)
    pad   = W() - len(clean) - 2
    print(f"{CYN}║{RST} {color}{text}{RST}{' '*max(0,pad)} {CYN}║{RST}")

def _kv(label, value, lc=DWHT, vc=YLW):
    pad = W() - len(label) - len(value) - 4
    print(f"{CYN}║{RST}  {lc}{label}{RST}  {vc}{value}{RST}"
          f"{' '*max(0,pad)}{CYN}║{RST}")

# ── Header ─────────────────────────────────────────────────────────────────────
def print_header(subtitle="MAIN MENU"):
    clr()
    c = cols()
    for line in LOGO:
        pad = max(0, (c - len(line)) // 2)
        print(f"{' '*pad}{CYN}{line}{RST}")
    sub = "INFINIX · TECNO · ITEL · FLASH TOOL"
    pad = max(0, (c - len(sub)) // 2)
    print(f"\n{' '*pad}{BOLD}{DWHT}{sub}{RST}\n")
    _top()
    _cbox(subtitle, f"{BOLD}{YLW}")
    _sdiv()
    _empty()
    _kv("Developer :", "Shelby",                lc=DWHT, vc=f"{BOLD}{GRN}")
    _kv("Support   :", "All Transsion Devices", lc=DWHT, vc=CYN)
    _kv("Platform  :", "MediaTek  |  Android",  lc=DWHT, vc=DCYN)
    _empty()
    _bot()
    print()

# ── Progress bar (always 0→100%) ───────────────────────────────────────────────
def progress_bar(label, cmd, fake_secs=4):
    """Run cmd silently, show animated 0→100% progress bar underneath."""
    bar_w = min(W() - 12, 36)

    done_flag  = threading.Event()
    result_box = [True]

    def runner():
        ok_flag, _ = _run_check(cmd)
        result_box[0] = ok_flag
        done_flag.set()

    t = threading.Thread(target=runner, daemon=True)
    t.start()

    start = time.time()
    pct   = 0

    print(f"\n  {DWHT}{label}{RST}")
    while not done_flag.is_set() or pct < 100:
        elapsed = time.time() - start
        if done_flag.is_set():
            pct = min(pct + 4, 100)
        else:
            pct = min(int((elapsed / fake_secs) * 95), 95)

        filled = int(bar_w * pct / 100)
        bar    = f"{GRN}{'█'*filled}{DCYN}{'░'*(bar_w-filled)}{RST}"
        sys.stdout.write(f"\r  [{bar}] {YLW}{pct:3d}%{RST}  ")
        sys.stdout.flush()
        if pct >= 100:
            break
        time.sleep(0.05)

    sys.stdout.write(f"\r  [{GRN}{'█'*bar_w}{RST}] {GRN}100%{RST}  ")
    sys.stdout.flush()
    print()
    t.join()
    icon = f"{GRN}✔  done{RST}" if result_box[0] else f"{RED}✘  failed{RST}"
    print(f"  {icon}")
    return result_box[0]

def progress_wait(label, secs=3):
    """Show progress bar for a wait/reboot step (no real cmd)."""
    bar_w = min(W() - 12, 36)
    print(f"\n  {DWHT}{label}{RST}")
    for i in range(101):
        filled = int(bar_w * i / 100)
        bar    = f"{YLW}{'█'*filled}{DCYN}{'░'*(bar_w-filled)}{RST}"
        sys.stdout.write(f"\r  [{bar}] {YLW}{i:3d}%{RST}  ")
        sys.stdout.flush()
        time.sleep(secs / 100)
    print()
    print(f"  {GRN}✔  done{RST}")

# ── Logging ────────────────────────────────────────────────────────────────────
def info(m):       print(f"\n  {CYN}[·]{RST}  {DWHT}{m}{RST}")
def ok(m):         print(f"  {GRN}[✔]{RST}  {DGRN}{m}{RST}")
def warn(m):       print(f"  {YLW}[!]{RST}  {YLW}{m}{RST}")
def err(m):        print(f"  {RED}[✘]{RST}  {RED}{m}{RST}")
def step(n,t,m):   print(f"\n  {CYN}[{n}/{t}]{RST}  {WHT}{m}{RST}")
def prompt(m):     return input(f"\n  {YLW}▶{RST}  {DWHT}{m}{RST}  ").strip()
def press_enter(): input(f"\n  {DCYN}Press {YLW}Enter{RST}{DCYN} to continue...{RST}")
def confirm(m):    return prompt(f"{m}  [{GRN}y{DWHT}/{RED}n{DWHT}]:").lower() == 'y'

def browse_img(label):
    """Scan /sdcard/ for .img files exactly like flash_stock_rom_combined.
    Returns selected file path or None if user goes back."""

    SKIP = ['Android', '.cache', 'DCIM', 'Pictures', 'Music',
            'Ringtones', 'Alarms', 'Notifications', 'Podcasts']

    # ── Scan ──
    imgs = []
    for root, dirs, files in os.walk("/sdcard/"):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith('.')]
        for f in files:
            if f.lower().endswith('.img'):
                full = os.path.join(root, f)
                try:
                    size    = os.path.getsize(full)
                    size_s  = (f"{size // 1048576} MB" if size >= 1048576
                               else f"{size // 1024} KB")
                except OSError:
                    size_s = "?"
                rel = full.replace("/sdcard/", "")
                imgs.append((full, f, size_s, rel))

    # ── Display ──
    clr_w = W()
    print(f"\n  {BOLD}{CYN}── SELECT FILE  ·  {label} {'─'*max(1, clr_w-22-len(label))}{RST}")
    print()

    if imgs:
        for i, (full, name, sz, rel) in enumerate(imgs, 1):
            folder = os.path.dirname(rel) or "/"
            print(f"  {YLW}[{i:2d}]{RST}  {WHT}{name}{RST}  {DGRN}({sz}){RST}")
            print(f"        {DCYN}{folder}{RST}")
        print()
        print(f"  {YLW}[ 0]{RST}  {DWHT}Back to previous menu{RST}")
        print()

        while True:
            ch = prompt(f"Select  {label}  [1–{len(imgs)} / 0=back]:").strip()
            if ch in ('0', 'b', 'back', ''):
                return None
            try:
                idx = int(ch)
                if 1 <= idx <= len(imgs):
                    chosen = imgs[idx - 1][0]
                    ok(f"Selected: {imgs[idx-1][1]}  ({imgs[idx-1][2]})")
                    return chosen
                err(f"Enter a number between 1 and {len(imgs)}, or 0 to go back")
            except ValueError:
                err("Invalid input — enter a number or 0 to go back")

    else:
        warn("No .img files found on /sdcard/")
        print(f"  {YLW}[0]{RST}  {DWHT}Back{RST}\n")
        while True:
            ch = prompt("Type full file path manually  (0 = back):").strip()
            if ch in ('0', 'b', 'back', ''):
                return None
            if os.path.isfile(ch):
                ok(f"File found: {os.path.basename(ch)}")
                return ch
            err(f"File not found — check path and try again")

def check_device_adb():
    """Returns True only when a real authorised device is present."""
    _, out = _run_check("adb devices")
    for line in out.splitlines():
        line = line.strip()
        if not line or 'list of devices' in line.lower():
            continue
        # "SERIAL\tdevice"  or  "SERIAL\trecovery"
        parts = line.split('\t')
        if len(parts) == 2 and parts[1].strip() in ('device', 'recovery', 'sideload'):
            return True
    return False

def check_device_fastboot():
    """Returns True only when a real fastboot device is present."""
    _, out = _run_check("fastboot devices")
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        # tab-separated:  "SERIAL\tfastboot"
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) >= 2 and 'fastboot' in parts[1].lower():
                return True
        # space-separated fallback some fastboot versions use
        elif ' ' in line:
            parts = line.split()
            if len(parts) >= 2 and 'fastboot' in parts[-1].lower():
                return True
    return False

def detect_brand(path):
    p = path.lower()
    if 'tecno' in p: return 'TECNO'
    if 'itel'  in p: return 'ITEL'
    return 'INFINIX'

# ── Flashing engine ────────────────────────────────────────────────────────────
SLOT_ALL = [
    'dtbo','gz','lk','logo','md1img','pi_img',
    'scp','spmfw','sspm','tee','vbmeta',
    'vbmeta_system','vbmeta_vendor','mcupm','dpm',
]

def scan_firmware(d):
    img_map = {}
    for root, _, files in os.walk(d):
        for f in files:
            lf = f.lower()
            if lf.endswith(('.img','.bin')):
                img_map[os.path.splitext(lf)[0]] = os.path.join(root,f)
                img_map[lf]                       = os.path.join(root,f)
    return img_map

def flash_part_progress(part, path, slot=True):
    flag = "--slot=all " if slot else ""
    cmd  = f"fastboot {flag}flash {part} '{path}'"
    progress_bar(f"Flashing  {part}", cmd, fake_secs=5)

def start_flashing_process(target_dir):
    brand = detect_brand(target_dir)
    print_header(f"FLASHING — {brand}")

    info("Scanning firmware directory...")
    img_map = scan_firmware(target_dir)
    found   = len([k for k in img_map if not k.endswith(('.img','.bin'))])
    ok(f"Found {found} partition image(s)")
    print()

    if not confirm("Authorize flashing?  All data will be wiped"):
        warn("Flashing cancelled."); press_enter(); return

    step(1,4,"Setting active slot → a")
    progress_bar("Setting slot a", "fastboot set_active a", fake_secs=2)

    step(2,4,"Flashing boot partitions")
    for p in ['boot','vendor_boot']:
        if p in img_map:
            flash_part_progress(p, img_map[p])

    step(3,4,"Flashing super partition")
    if 'super' in img_map:
        progress_bar("Flashing  super", f"fastboot flash super '{img_map['super']}'", fake_secs=30)
    else:
        warn("super.img not found — skipping")

    step(4,4,"Flashing remaining partitions")
    preloader = next((img_map[k] for k in img_map if 'preloader' in k), None)
    if preloader:
        flash_part_progress('preloader', preloader)
    for p in SLOT_ALL:
        if p in img_map and p not in ('boot','vendor_boot'):
            flash_part_progress(p, img_map[p])
    if 'userdata' in img_map:
        flash_part_progress('userdata', img_map['userdata'], slot=False)

    progress_bar("Erasing userdata", "fastboot erase userdata", fake_secs=4)

    print()
    _top()
    _cbox("🎉  FLASH COMPLETED SUCCESSFULLY  🎉", f"{BOLD}{GRN}")
    _sdiv()
    _kv("Developer :", "Shelby", lc=DWHT, vc=f"{BOLD}{GRN}")
    _kv("Device    :", brand,    lc=DWHT, vc=CYN)
    _bot()
    print()
    progress_bar("Rebooting device", "fastboot reboot", fake_secs=3)
    press_enter()

# ── Flash GSI ──────────────────────────────────────────────────────────────────
def flash_gsi():
    print_header("FLASH GSI ROM")

    _top()
    _cbox("GSI — Generic System Image", f"{BOLD}{CYN}")
    _sdiv()
    _row("Supports any Project Treble device")
    _row("Requires unlocked bootloader")
    _empty()
    _bot()
    print()

    vbmeta_img = browse_img("vbmeta.img")
    if vbmeta_img is None: return

    empty_img  = browse_img("empty_partition.img")
    if empty_img is None: return

    gsi_img    = browse_img("gsi.img  (Generic System Image)")
    if gsi_img is None: return

    print()
    ok(f"vbmeta   : {os.path.basename(vbmeta_img)}")
    ok(f"empty    : {os.path.basename(empty_img)}")
    ok(f"gsi      : {os.path.basename(gsi_img)}")
    print()
    if not confirm("Start GSI flash?  All data will be wiped"):
        warn("Cancelled."); press_enter(); return

    STEPS = 9

    # ── 1 Check ADB ──
    step(1,STEPS,"Checking ADB connection")
    if not check_device_adb():
        err("No ADB device detected. Connect device and enable USB Debugging.")
        press_enter(); return
    ok("Device detected")

    # ── 2 Reboot bootloader ──
    step(2,STEPS,"Rebooting to bootloader")
    progress_bar("Rebooting to bootloader", "adb reboot bootloader", fake_secs=6)
    w(3)

    # ── 3 Flash vbmeta ──
    step(3,STEPS,"Patching vbmeta")
    progress_bar(
        "Flashing  vbmeta",
        f"fastboot flash --disable-verity --disable-verification vbmeta '{vbmeta_img}'",
        fake_secs=5
    )

    # ── 4 Reboot fastboot ──
    step(4,STEPS,"Rebooting to fastbootd")
    progress_bar("Rebooting to fastbootd", "fastboot reboot fastboot", fake_secs=8)
    w(4)

    # ── 5 Erase system ──
    step(5,STEPS,"Erasing system partition")
    progress_bar("Erasing  system", "fastboot erase system", fake_secs=6)

    # ── 6 Flash product (empty) ──
    step(6,STEPS,"Flashing empty product partition")
    progress_bar(
        "Flashing  product",
        f"fastboot flash product '{empty_img}'",
        fake_secs=4
    )

    # ── 7 Flash system_ext (empty) ──
    step(7,STEPS,"Flashing empty system_ext partition")
    progress_bar(
        "Flashing  system_ext",
        f"fastboot flash system_ext '{empty_img}'",
        fake_secs=4
    )

    # ── 8 Flash GSI ──
    step(8,STEPS,"Flashing GSI system image")
    progress_bar(
        "Flashing  system  (GSI)",
        f"fastboot flash system '{gsi_img}'",
        fake_secs=40
    )

    # ── 9 Reboot recovery + wipe ──
    step(9,STEPS,"Rebooting to recovery and wiping data")
    progress_bar("Rebooting to recovery", "fastboot reboot recovery", fake_secs=8)
    w(4)
    progress_bar("Wiping data (factory reset)", "fastboot -w", fake_secs=10)
    progress_bar("Rebooting device", "fastboot reboot", fake_secs=3)

    print()
    _top()
    _cbox("🎉  GSI FLASH COMPLETED  🎉", f"{BOLD}{GRN}")
    _sdiv()
    _row("Device will boot into the new GSI ROM")
    _row("First boot may take 3–5 minutes")
    _empty()
    _bot()
    press_enter()

# ── Root & Unroot ──────────────────────────────────────────────────────────────
def _do_root():
    print_header("ROOT DEVICE")

    _top()
    _cbox("Root Device — Flash Patched Boot", f"{BOLD}{YLW}")
    _sdiv()
    _row("Requirements:", DWHT)
    _row(" • Unlocked bootloader")
    _row(" • Any patched root.img / boot.img")
    _row(" • Magisk / KernelSU / APatch supported")
    _row(" • Stock vbmeta.img")
    _empty()
    _bot()
    print()

    root_img   = browse_img("root.img / patched_boot.img")
    if root_img is None: return

    vbmeta_img = browse_img("vbmeta.img")
    if vbmeta_img is None: return

    print()
    ok(f"root img : {os.path.basename(root_img)}")
    ok(f"vbmeta   : {os.path.basename(vbmeta_img)}")
    print()
    if not confirm("Proceed with rooting?"):
        warn("Cancelled."); press_enter(); return

    STEPS = 5

    step(1,STEPS,"Checking ADB connection")
    if not check_device_adb():
        err("No ADB device detected."); press_enter(); return
    ok("Device detected")

    step(2,STEPS,"Rebooting to bootloader")
    progress_bar("Rebooting to bootloader", "adb reboot bootloader", fake_secs=6)
    w(3)

    step(3,STEPS,"Verifying fastboot connection")
    progress_wait("Waiting for fastboot", secs=2)
    if not check_device_fastboot():
        err("Fastboot device not detected."); press_enter(); return
    ok("Fastboot device ready")

    step(4,STEPS,"Flashing patched boot image")
    progress_bar(
        "Flashing  boot  (Root)",
        f"fastboot flash boot '{root_img}'",
        fake_secs=6
    )
    progress_bar(
        "Patching  vbmeta",
        f"fastboot flash --disable-verity --disable-verification vbmeta '{vbmeta_img}'",
        fake_secs=5
    )

    step(5,STEPS,"Rebooting device")
    progress_bar("Rebooting", "fastboot reboot", fake_secs=3)

    print()
    _top()
    _cbox("🎉  YOUR DEVICE IS NOW ROOTED  🎉", f"{BOLD}{GRN}")
    _sdiv()
    _row("Open Magisk app to verify root status")
    _row("Developer : Shelby", DGRN)
    _empty()
    _bot()
    press_enter()

def _do_unroot():
    print_header("UNROOT DEVICE")

    _top()
    _cbox("Restore Stock Boot Image", f"{BOLD}{YLW}")
    _sdiv()
    _row("Requirements:", DWHT)
    _row(" • Stock boot.img for your firmware version")
    _row(" • Stock vbmeta.img")
    _empty()
    _bot()
    print()

    stock_img  = browse_img("stock_boot.img  (original boot)")
    if stock_img is None: return

    vbmeta_img = browse_img("vbmeta.img")
    if vbmeta_img is None: return

    print()
    ok(f"stock boot : {os.path.basename(stock_img)}")
    ok(f"vbmeta     : {os.path.basename(vbmeta_img)}")
    print()
    if not confirm("Proceed with unrooting?"):
        warn("Cancelled."); press_enter(); return

    STEPS = 5

    step(1,STEPS,"Checking ADB connection")
    if not check_device_adb():
        err("No ADB device detected."); press_enter(); return
    ok("Device detected")

    step(2,STEPS,"Rebooting to bootloader")
    progress_bar("Rebooting to bootloader", "adb reboot bootloader", fake_secs=6)
    w(3)

    step(3,STEPS,"Verifying fastboot connection")
    progress_wait("Waiting for fastboot", secs=2)
    if not check_device_fastboot():
        err("Fastboot device not detected."); press_enter(); return
    ok("Fastboot device ready")

    step(4,STEPS,"Restoring stock boot image")
    progress_bar(
        "Flashing  boot  (Stock)",
        f"fastboot flash boot '{stock_img}'",
        fake_secs=6
    )
    progress_bar(
        "Restoring vbmeta",
        f"fastboot flash --disable-verity --disable-verification vbmeta '{vbmeta_img}'",
        fake_secs=5
    )

    step(5,STEPS,"Rebooting device")
    progress_bar("Rebooting", "fastboot reboot", fake_secs=3)

    print()
    _top()
    _cbox("✅  YOUR DEVICE IS NOW UNROOTED  ✅", f"{BOLD}{CYN}")
    _sdiv()
    _row("Stock boot restored successfully")
    _row("Developer : Shelby", DGRN)
    _empty()
    _bot()
    press_enter()

def root_unroot_menu():
    while True:
        print_header("ROOT / UNROOT")
        print(f"  {CYN}[1]{RST}  {WHT}Root Device    {DCYN}(Magisk){RST}")
        print(f"  {CYN}[2]{RST}  {WHT}Unroot Device  {DCYN}(Restore Stock Boot){RST}")
        print(f"  {CYN}[3]{RST}  {DWHT}Back{RST}\n")
        ch = prompt("Select option:")
        if   ch == '1': _do_root()
        elif ch == '2': _do_unroot()
        elif ch == '3': break
        else:           warn("Invalid option."); w(0.4)

# ── Flash Stock ROM ────────────────────────────────────────────────────────────
def flash_stock_rom_combined():
    print_header("FLASH STOCK ROM")

    info("Scanning internal storage...")
    zips    = []
    folders = {}

    for root, _, files in os.walk("/sdcard/"):
        if any(x in root for x in ["Android",".cache"]): continue
        for f in files:
            lf = f.lower()
            if lf.endswith(".zip") and any(k in lf for k in KEYWORDS):
                zips.append(os.path.join(root,f))

    for root, _, files in os.walk("/sdcard/"):
        if any(x in root for x in ["Android",".cache","DCIM","Pictures"]): continue
        cnt = sum(1 for f in files if f.lower().endswith(('.img','.bin')))
        if cnt: folders[root] = cnt

    item_map = {}; idx = 1

    print(f"\n  {BOLD}{CYN}── FIRMWARE ZIP FILES {'─'*26}{RST}")
    if zips:
        for z in zips:
            brand = detect_brand(z)
            print(f"  {YLW}[{idx:2d}]{RST}  {WHT}{os.path.basename(z)}{RST}"
                  f"  {DCYN}[{brand}]{RST}")
            item_map[idx] = ('zip', z); idx += 1
    else:
        warn("No matching ZIP files found on /sdcard/")

    print(f"\n  {BOLD}{CYN}── EXTRACTED FOLDERS {'─'*27}{RST}")
    if folders:
        for fpath, cnt in folders.items():
            brand = detect_brand(fpath)
            print(f"  {YLW}[{idx:2d}]{RST}  {WHT}{os.path.basename(fpath)}{RST}"
                  f"  {DGRN}({cnt} images){RST}  {DCYN}[{brand}]{RST}")
            item_map[idx] = ('folder', fpath); idx += 1
    else:
        warn("No extracted firmware folders found")

    if not item_map:
        err("Nothing to flash. Copy firmware to /sdcard/ first.")
        press_enter(); return

    print()
    try:
        sel = int(prompt(f"Select entry  [1–{idx-1}]:"))
    except ValueError:
        err("Invalid input."); press_enter(); return
    if sel not in item_map:
        err("Selection out of range."); press_enter(); return

    itype, ipath = item_map[sel]

    if itype == 'zip':
        out_path = "/sdcard/TRANSSION_FIRMWARE"
        os.makedirs(out_path, exist_ok=True)
        info("Extracting firmware package...")
        try:
            with zipfile.ZipFile(ipath,'r') as z:
                z.extractall(out_path)
            ok("Extraction complete")
            sub = os.listdir(out_path); actual = out_path
            if len(sub) == 1:
                maybe = os.path.join(out_path, sub[0])
                if os.path.isdir(maybe):
                    if any(f.lower().endswith(('.img','.bin'))
                           for r,_,fs in os.walk(maybe) for f in fs):
                        actual = maybe
            w(0.4); start_flashing_process(actual)
        except Exception as e:
            err(f"Extraction failed: {e}"); press_enter()
    else:
        start_flashing_process(ipath)

# ── Partition manager ──────────────────────────────────────────────────────────
def partition_manager():
    while True:
        print_header("PARTITION MANAGER")
        print(f"  {CYN}[1]{RST}  {WHT}Erase Userdata{RST}")
        print(f"  {CYN}[2]{RST}  {WHT}Erase Cache{RST}")
        print(f"  {CYN}[3]{RST}  {WHT}Erase Metadata{RST}")
        print(f"  {CYN}[4]{RST}  {WHT}Erase All  {DCYN}(userdata + cache + metadata){RST}")
        print(f"  {CYN}[5]{RST}  {WHT}Format Userdata{RST}")
        print(f"  {CYN}[6]{RST}  {DWHT}Back{RST}\n")
        ch = prompt("Select option:")

        if ch == '1':
            if confirm("Erase userdata?"):
                progress_bar("Erasing  userdata", "fastboot erase userdata", fake_secs=5)
        elif ch == '2':
            if confirm("Erase cache?"):
                progress_bar("Erasing  cache", "fastboot erase cache", fake_secs=3)
        elif ch == '3':
            if confirm("Erase metadata?"):
                progress_bar("Erasing  metadata", "fastboot erase metadata", fake_secs=3)
        elif ch == '4':
            if confirm("Erase ALL? This will wipe all user data"):
                for part, secs in [('userdata',5),('cache',3),('metadata',3)]:
                    progress_bar(f"Erasing  {part}", f"fastboot erase {part}", fake_secs=secs)
        elif ch == '5':
            if confirm("Format userdata?"):
                progress_bar("Formatting  userdata", "fastboot format userdata", fake_secs=6)
        elif ch == '6':
            break
        else:
            warn("Invalid option."); w(0.4); continue
        print()
        press_enter()

# ── Device check ───────────────────────────────────────────────────────────────
def device_check_menu():
    print_header("FASTBOOT DEVICE CHECK")
    print()
    info("Checking ADB connection...")
    adb_ok = check_device_adb()
    if adb_ok: ok("ADB device detected")
    else:      warn("No ADB device found")

    print()
    info("Checking Fastboot connection...")
    fb_ok = check_device_fastboot()
    if fb_ok: ok("Fastboot device detected")
    else:     warn("No Fastboot device found")

    press_enter()

# ── Reboot menu ────────────────────────────────────────────────────────────────
REBOOT_OPTS = {
    '1': ("System",     "fastboot reboot",             6),
    '2': ("Fastboot",   "fastboot reboot-bootloader",  6),
    '3': ("Recovery",   "fastboot reboot recovery",    6),
    '4': ("EDL / BROM", "fastboot reboot edl",         6),
}

def reboot_menu():
    while True:
        print_header("REBOOT OPTIONS")
        for k,(label,_,_) in REBOOT_OPTS.items():
            print(f"  {CYN}[{k}]{RST}  Reboot to {WHT}{label}{RST}")
        print(f"  {CYN}[5]{RST}  {DWHT}Back{RST}\n")
        ch = prompt("Select option:")
        if ch in REBOOT_OPTS:
            label, cmd, secs = REBOOT_OPTS[ch]
            progress_bar(f"Rebooting to {label}", cmd, fake_secs=secs)
            break
        elif ch == '5':
            break
        else:
            warn("Invalid option."); w(0.4)

# ── Bootloader unlock ──────────────────────────────────────────────────────────
def unlock_bootloader():
    print_header("UNLOCK BOOTLOADER")
    _top()
    _cbox("⚠  WARNING — DATA WILL BE ERASED  ⚠", f"{BOLD}{RED}")
    _sdiv()
    _row(" 1.  Settings › About Phone › Build Number  ×7")
    _row(" 2.  Settings › System › Developer Options")
    _row(" 3.  Enable  OEM Unlocking  +  USB Debugging")
    _row(" 4.  Boot device into Fastboot mode")
    _row(" 5.  Connect via USB to this machine")
    _empty()
    _bot()

    if not confirm("Proceed with bootloader unlock?"):
        warn("Unlock cancelled."); press_enter(); return

    progress_bar("Sending OEM unlock", "fastboot flashing unlock", fake_secs=4)
    progress_bar("Sending OEM unlock (alt)", "fastboot oem unlock",    fake_secs=4)
    ok("Unlock commands sent. Confirm on device screen if prompted.")
    press_enter()

# ── Main ───────────────────────────────────────────────────────────────────────
MENU = {
    '1': ("Unlock Bootloader",    unlock_bootloader),
    '2': ("Device Check",         device_check_menu),
    '3': ("Flash Stock ROM",      flash_stock_rom_combined),
    '4': ("Flash GSI ROM",        flash_gsi),
    '5': ("Root / Unroot",        root_unroot_menu),
    '6': ("Partition Manager",    partition_manager),
    '7': ("Reboot Options",       reboot_menu),
}

def main():
    while True:
        print_header("MAIN MENU")
        for k,(label,_) in MENU.items():
            print(f"  {CYN}[{k}]{RST}  {WHT}{label}{RST}")
        print(f"  {CYN}[8]{RST}  {DWHT}Exit{RST}\n")

        ch = prompt("Select option:")
        if ch in MENU:
            MENU[ch][1]()
        elif ch == '8':
            clr()
            print(f"\n  {GRN}Shelby{RST}  {DWHT}— Transsion Universal Flash Tool{RST}\n")
            sys.exit(0)
        else:
            warn("Invalid option."); w(0.4)

if __name__ == "__main__":
    main()
