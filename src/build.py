# Build the GitHub Pages site: index.html (EN, copied from src/index.en.html) and vi.html (VI).
# VI text = the approved portfolio translation table (Ho-so-xin-viec/source/portfolio-vi-strings.py)
# plus the few web-only strings in WEB below. Text nodes not found in either table stay as-is.
# Usage: python3 -I src/build.py
import html, re, pathlib, runpy

SRC = pathlib.Path(__file__).resolve().parent
SITE = SRC.parent
T = dict(runpy.run_path(str(SITE.parent / "source" / "portfolio-vi-strings.py"))["T"])

WEB = {
    "Tran Thi Kieu Hanh – Marketing & SEO Portfolio": "Trần Thị Kiều Hạnh – Portfolio Marketing & SEO",
    "About": "Giới thiệu", "SEO": "SEO", "AI": "AI", "Agency": "Agency", "PhimFact": "PhimFact", "Contact": "Liên hệ",
    "Download CV (PDF)": "Tải CV (PDF)", "Portfolio (PDF)": "Portfolio (PDF)", "Send an email": "Gửi email",
    "Open to:": "Vị trí quan tâm:",
    "ACB Bank (supported)": "Ngân hàng ACB (hỗ trợ)", "TNEX Digital Bank": "Ngân hàng số TNEX",
    "100,000+": "100.000+", "+100,000": "+100.000", "+40,000": "+40.000", "+37,000": "+37.000",
    "+29,000": "+29.000", "+20,600": "+20.600", "+20,000": "+20.000", "+13,000": "+13.000",
    "Let's work together": "Rất mong được hợp tác",
    "20 · Contact": "20 · Liên hệ",
    "clicks": "lượt nhấp",
    "impressions · CTR 4.4% · avg. position 7.5": "lượt hiển thị · CTR 4,4% · vị trí TB 7,5",
    "Simple English · 2025 KPI": "Simple English · KPI 2025",
    "& speaking": "& diễn giả",
}
# Headings written as one line on the web (the PDF split them over <br>).
WEB.update({
    "About me": "Giới thiệu",
    "Highlights": "Con số", "in numbers": "nổi bật",
})
T.update(WEB)
# The section title "Agency leadership" on the web: "Agency" + "leadership" -> "Agency" + "Lead"
T["leadership"] = "Lead"

src = (SRC / "index.en.html").read_text(encoding="utf-8")
(SITE / "index.html").write_text(src, encoding="utf-8")

head, body = src.split("<body>", 1)
head = head.replace('<html lang="en">', '<html lang="vi">')
missing = []

def tx(m):
    raw = m.group(1); key = html.unescape(raw).strip()
    if not key or key not in T:
        if key: missing.append(key)
        return m.group(0)
    lead = raw[:len(raw) - len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
    return ">" + lead + html.escape(T[key], quote=False) + trail + "<"

def meta(m):
    k = html.unescape(m.group(2))
    return m.group(1) + html.escape(T.get(k, k), quote=True) + m.group(3)

head = re.sub(r">([^<]+)<", tx, head)
head = re.sub(r'(content=")([^"]*)(")', meta, head)
parts = re.split(r"(<script>.*?</script>)", body, flags=re.S)
body = "".join(p if p.startswith("<script>") else re.sub(r">([^<]+)<", tx, p) for p in parts)
body = re.sub(r"<!--LANG-->.*?<!--/LANG-->", '<!--LANG--><a href="index.html">EN</a><a class="on" href="vi.html">VI</a><!--/LANG-->', body, flags=re.S)
body = body.replace("files/CV_Tran-Thi-Kieu-Hanh_EN.pdf", "files/CV_Tran-Thi-Kieu-Hanh_VI.pdf").replace("files/Portfolio_Tran-Thi-Kieu-Hanh_EN.pdf", "files/Portfolio_Tran-Thi-Kieu-Hanh_VI.pdf")
body = body.replace("<h2>SEO cho <span class=\"b\">YMYL</span> thương hiệu</h2>", "<h2>SEO cho thương hiệu <span class=\"b\">YMYL</span></h2>")
body = body.replace("<h2>Giới thiệu <span class=\"b\">thiệu</span></h2>", "<h2>Giới <span class=\"b\">thiệu</span></h2>")
(SITE / "vi.html").write_text(head + "<body>" + body, encoding="utf-8")

skip = re.compile(r"^(#|[\d.,+~%–·KM -]+$|TNEX$|ACB$|UNICEF$)")
left = [k for k in dict.fromkeys(missing) if not skip.match(k)]
print("VI untranslated:", len(left))
for k in left: print("  ", k)
