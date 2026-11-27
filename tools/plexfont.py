"""Local IBM Plex @font-face rules for headless renders (Google Fonts is not reachable from the render sandbox)."""
import os
_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
def css():
    r = []
    for w, n in ((400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold")):
        r.append(f'@font-face{{font-family:"IBM Plex Sans";font-weight:{w};src:url("file://{_D}/IBMPlexSans-{n}.woff2") format("woff2")}}')
    r.append(f'@font-face{{font-family:"IBM Plex Serif";font-weight:600;src:url("file://{_D}/IBMPlexSerif-SemiBold.woff2") format("woff2")}}')
    return "".join(r)
