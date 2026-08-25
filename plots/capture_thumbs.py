"""Recrop wedding art and screenshot VoC / footy-coach mid-play."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "projects"
W, H = 450, 800


def cover_crop(im: Image.Image, box, dest: Path):
    x0, y0, x1, y1 = box
    crop = im.crop((x0, y0, x1, y1)).convert("RGB")
    tw, th = W, H
    scale = max(tw / crop.width, th / crop.height)
    nw, nh = int(crop.width * scale), int(crop.height * scale)
    crop = crop.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    crop = crop.crop((left, top, left + tw, top + th))
    dest.parent.mkdir(parents=True, exist_ok=True)
    crop.save(dest, "JPEG", quality=88, optimize=True)
    print(dest, crop.size)


def wedding():
    src = Path("/home/michael/projects/wedding-rsvps/assets/img/beth-michael.png")
    im = Image.open(src)
    # Tight 9:16 on the bus itself so it sits in the middle, not in the
    # bottom-right with a white L of padding.
    crop_w = 740
    crop_h = int(crop_w * H / W)
    box = (144, 520, 144 + crop_w, 520 + crop_h)
    cover_crop(im, box, OUT / "wedding-rsvps.jpg")


def screenshot_voc(browser):
    page = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page.goto("http://127.0.0.1:8767/", wait_until="networkidle")
    page.locator("#btn-start").click()
    page.locator("#btn-propose").click()
    page.locator("#proposal-button").click()
    page.wait_for_selector("#whip-expected")
    page.wait_for_timeout(400)
    tmp = "/tmp/voc-mid.png"
    page.screenshot(path=tmp, full_page=False)
    im = Image.open(tmp).convert("RGB")
    cover_crop(im, (0, 0, im.width, im.height), OUT / "voc_simulator.jpg")
    page.close()


def screenshot_footy(browser):
    # Landscape so the pitch is large; players are ~0.55*scale pixels.
    page = browser.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=2)
    page.goto("http://127.0.0.1:5173/", wait_until="networkidle")
    page.wait_for_selector("#pitch")
    page.get_by_role("button", name="Kick off").click()
    page.wait_for_timeout(3200)
    tmp = "/tmp/footy-pitch.png"
    page.locator("#pitch").screenshot(path=tmp)
    page.screenshot(path="/tmp/footy-full.png", full_page=False)
    im = Image.open(tmp).convert("RGB")
    # Zoom on midfield so the blobs read as players in a 90×160 thumb.
    cx, cy = im.width // 2, im.height // 2
    crop_h = int(im.height * 0.42)
    crop_w = int(crop_h * W / H)
    left = max(0, cx - crop_w // 2)
    top = max(0, cy - crop_h // 2)
    right = min(im.width, left + crop_w)
    bottom = min(im.height, top + crop_h)
    cover_crop(im, (left, top, right, bottom), OUT / "footy-coach.jpg")
    page.close()


def screenshot_bus(browser):
    page = browser.new_page(viewport={"width": 390, "height": 693}, device_scale_factor=2)
    page.goto("http://127.0.0.1:8768/", wait_until="networkidle")
    page.wait_for_timeout(300)
    tmp = "/tmp/bus-times.png"
    page.screenshot(path=tmp, full_page=False)
    im = Image.open(tmp).convert("RGB")
    cover_crop(im, (0, 0, im.width, im.height), OUT / "ldn-bus-times.jpg")
    page.close()


if __name__ == "__main__":
    import sys

    targets = set(sys.argv[1:] or ["wedding", "voc", "footy", "bus"])
    if "wedding" in targets:
        wedding()
    if targets & {"voc", "footy", "bus"}:
        from playwright.sync_api import sync_playwright

        chrome = "/usr/bin/chromium"
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=chrome,
                args=["--no-sandbox", "--disable-gpu"],
                headless=True,
            )
            if "voc" in targets:
                screenshot_voc(browser)
            if "footy" in targets:
                screenshot_footy(browser)
            if "bus" in targets:
                screenshot_bus(browser)
            browser.close()
