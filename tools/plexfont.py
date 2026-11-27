"""IBM Plex @font-face rules for headless renders (Google Fonts is not reachable from the render sandbox).
Fonts are embedded as data: URIs so they load in set_content() pages as well as file:// pages."""
import os, base64, functools
_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
@functools.lru_cache(None)
def css():
    def face(fam, w, f):
        b = base64.b64encode(open(os.path.join(_D, f), "rb").read()).decode()
        return f'@font-face{{font-family:"{fam}";font-weight:{w};src:url(data:font/woff2;base64,{b}) format("woff2")}}'
    r = [face("IBM Plex Sans", w, f"IBMPlexSans-{n}.woff2") for w, n in ((400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold"))]
    r.append(face("IBM Plex Serif", 600, "IBMPlexSerif-SemiBold.woff2"))
    return "".join(r)
