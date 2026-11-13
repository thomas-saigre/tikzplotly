"""Show a figure in the web browser with an "Export to TikZ" button in the mode bar.

Plotly's own browser renderer serves the page once and returns, so the page has no way to
reach Python afterwards. Here a small local HTTP server keeps running while the page is open:
clicking the button sends the current view (axis ranges, hidden traces) to that server, which
calls :func:`get_tikz_code` and writes the result to a file.

Plotly itself is not modified: a renderer named ``"tikzplotly"`` is registered with Plotly's
renderer API when tikzplotly is imported, and :func:`show` is a shortcut to it.
"""
import base64
import json
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import cast

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

from ._save import get_tikz_code

try:  # private module: guarded so that a Plotly reorganisation cannot break ``import tikzplotly``
    from plotly.io._base_renderers import ExternalRenderer
except ImportError:  # pragma: no cover
    ExternalRenderer = object

RENDERER_NAME = "tikzplotly"

# A hidden browser tab may only run its timers once a minute, so the idle timeout has to be
# well above 60 s, or a tab left in the background would be considered closed.
PING_MS = 10_000
IDLE_TIMEOUT = 150
# Time left after the page signals it is closing, so that a page reload can reconnect.
CLOSE_GRACE = 5

# "Export to TikZ" icon: a floppy disk with "TikZ" (glyph outlines of Latin Modern Roman Bold),
# in a 1000x1000 box. A single path, because Plotly only colours the first path of an icon,
# and its holes need the evenodd fill rule, set in _POST_SCRIPT.
TIKZ_ICON_PATH = (
    "M110 40H760L960 240V890Q960 960 890 960H110Q40 960 40 890V110Q40 40 110 40Z M120 115V885H885V275L725"
    " 115Z M230 115H690V290Q690 320 660 320H260Q230 320 230 290Z M540 155V280H630V155Z M381 604 374 523H1"
    "47L140 604H156C159 566 162 539 211 539H237V735H185V750C203 749 241 749 260 749C280 749 318 749 336 7"
    "50V735H284V539H310C358 539 361 566 365 604ZM491 750V735H471V599L412 602V617C432 617 434 617 434 631V"
    "735H411V750L452 749ZM475 546C475 532 463 520 449 520C435 520 423 532 423 546C423 561 435 572 449 572"
    "C463 572 475 561 475 546ZM673 701C673 696 668 696 663 696C655 696 655 696 653 705C648 725 641 741 62"
    "9 741C626 741 621 740 621 729C621 729 621 723 624 712C625 709 625 705 625 702C625 676 596 669 572 66"
    "6C584 657 596 645 596 644C619 619 634 610 647 610C648 610 652 610 653 614C639 616 630 628 630 639C63"
    "0 647 636 654 647 654C657 654 671 647 671 625C671 615 667 598 648 598C629 598 612 611 591 634C577 64"
    "8 571 653 563 658L596 528C596 527 597 525 597 523C597 516 591 517 586 517L545 519C541 519 534 519 53"
    "4 529C534 535 541 535 544 535C548 535 554 536 558 536L509 731C508 736 508 737 508 739C508 747 514 75"
    "3 523 753C530 753 540 749 543 739L558 678C568 680 589 685 589 703C589 705 589 707 588 710C588 713 58"
    "7 715 587 719C587 739 605 753 627 753C661 753 673 703 673 701ZM865 655H849C846 692 842 733 773 733H7"
    "26L860 536C863 532 863 532 863 528C863 519 859 519 852 519H679L675 601H691C693 556 716 535 763 535H8"
    "07L672 733C669 737 669 738 669 742C669 750 673 750 680 750H859Z"
)

_POST_SCRIPT = """
(function () {
  var gd = document.getElementById('{plot_id}');
  var token = '__TOKEN__';

  function post(path, body) {
    return fetch('/' + token + path, {method: 'POST', body: JSON.stringify(body || {})});
  }

  function toast(message, failed) {
    var el = document.createElement('div');
    el.textContent = message;
    el.style.cssText = 'position:fixed;left:16px;bottom:16px;padding:8px 12px;z-index:9999;'
      + 'border-radius:4px;color:#fff;font:13px sans-serif;background:'
      + (failed ? '#b3261e' : '#2e7d32');
    document.body.appendChild(el);
    setTimeout(function () { el.remove(); }, failed ? 8000 : 3000);
  }

  // Only the view state is sent: the data stays on the Python side.
  function viewState() {
    var axes = {};
    Object.keys(gd.layout).forEach(function (key) {
      if (/^[xy]axis\\d*$/.test(key)) {
        var axis = gd.layout[key];
        axes[key] = axis.autorange ? null : axis.range;
      }
    });
    return {axes: axes, visible: gd.data.map(function (t) { return t.visible; })};
  }

  var button = {
    name: 'exportTikz',
    title: 'Export to TikZ',
    icon: {width: 1000, height: 1000, path: '__ICON_PATH__'},
    click: function () {
      post('/export', viewState())
        .then(function (r) { return r.json(); })
        .then(function (r) {
          if (r.ok) { toast('Saved ' + r.path); } else { toast(r.error, true); }
        })
        .catch(function () { toast('The Python process is no longer running', true); });
    }
  };

  var style = document.createElement('style');
  style.textContent = '.modebar-btn[data-title="Export to TikZ"] path { fill-rule: evenodd; }';
  document.head.appendChild(style);

  var config = __CONFIG__;
  config.modeBarButtonsToAdd = (config.modeBarButtonsToAdd || []).concat([button]);
  Plotly.react(gd, gd.data, gd.layout, config);

  // Immediate ping: after a reload, cancels the "closing" signal sent by the previous page.
  post('/ping');
  setInterval(function () { post('/ping'); }, __PING_MS__);
  window.addEventListener('pagehide', function () {
    navigator.sendBeacon('/' + token + '/closing');
  });
})();
"""


def _decode_arrays(obj):
    """Turn Plotly's ``{"dtype": ..., "bdata": ...}`` entries back into NumPy arrays.

    Since Plotly 6, ``Figure.to_dict()``, hence the dict a renderer receives, stores NumPy
    arrays in this base64 form, which the rest of tikzplotly cannot index.
    """
    if isinstance(obj, dict):
        if "bdata" in obj and "dtype" in obj:
            array = np.frombuffer(base64.b64decode(obj["bdata"]), dtype=obj["dtype"])
            if "shape" in obj:
                shape = obj["shape"]
                if isinstance(shape, str):
                    shape = [int(n) for n in shape.split(",")]
                array = array.reshape(shape)
            return array
        return {key: _decode_arrays(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_decode_arrays(value) for value in obj]
    return obj


def _free_path(path: Path) -> Path:
    """Return ``path``, or ``stem_1.ext``, ``stem_2.ext``, ... if it already exists."""
    candidate, n = path, 0
    while candidate.exists():
        n += 1
        candidate = path.with_name(f"{path.stem}_{n}{path.suffix}")
    return candidate


class TikzBrowserRenderer(ExternalRenderer):    # type: ignore
    """Plotly renderer opening the figure in the browser with an "Export to TikZ" button.

    Parameters
    ----------
    output, optional
        file written by the button, by default ``"figure.tex"``. If it already exists,
        ``figure_1.tex``, ``figure_2.tex``, ... are used instead, so no export is overwritten.
    config, optional
        Plotly config dict for the page (see ``fig.show(config=...)``), by default None
    **tikz_options
        passed on to :func:`get_tikz_code` (``tikz_options``, ``axis_options``, ``decimate``...).
        Unless ``img_name`` is given, the image of a heatmap is saved next to the ``.tex`` file,
        with the same name.
    """

    def __init__(self, output="figure.tex", config=None, **tikz_options):
        self.output = Path(output)
        self.config = dict(config or {})
        self.tikz_options = tikz_options
        self._lock = threading.Lock()

    def export(self, fig, view=None) -> Path:
        """Write the TikZ code of ``fig``, as currently displayed in the page, to a free file name.

        Parameters
        ----------
        fig
            Plotly figure, or figure dict as received by a renderer
        view, optional
            ``{"axes": {"xaxis": [min, max] or None, ...}, "visible": [...]}`` as sent by the page

        Returns
        -------
            path of the written file
        """
        view = view or {}
        fig = go.Figure(_decode_arrays(fig) if isinstance(fig, dict) else fig)  # copy: fig is reused
        for name, axis_range in (view.get("axes") or {}).items():
            fig.layout[name].range = axis_range
        states = view.get("visible") or []
        traces = tuple(fig.data)
        if len(states) == len(traces):  # get_tikz_code exports hidden traces too
            fig.data = [trace for trace, state in zip(traces, states) if state in (None, True)]

        with self._lock:  # two quick clicks must not pick the same file name
            path = _free_path(self.output)
            path.parent.mkdir(parents=True, exist_ok=True)
            options = {"img_name": str(path.with_suffix(".png")), **self.tikz_options}
            path.write_text(get_tikz_code(fig, **options), encoding="utf-8")
        return path

    def start_server(self, fig):
        """Start serving the page for ``fig`` without opening a browser.

        Returns
        -------
            ``(url, thread)``: the page's address, and the thread serving it, which ends once the
            page has been closed or has not been heard from for ``IDLE_TIMEOUT`` seconds
        """
        if not isinstance(fig, dict):
            fig = go.Figure(fig)  # snapshot: later changes made by the script are not exported
        fig_dict = fig if isinstance(fig, dict) else fig.to_dict()
        token = secrets.token_urlsafe(24)
        script = (_POST_SCRIPT.replace("__TOKEN__", token)
                  .replace("__CONFIG__", json.dumps(self.config))
                  .replace("__PING_MS__", str(PING_MS))
                  .replace("__ICON_PATH__", TIKZ_ICON_PATH))
        html = pio.to_html(
            fig_dict, config=self.config, include_plotlyjs=True,
            include_mathjax="cdn", post_script=script, full_html=True,      # type: ignore
            default_width="100%", default_height="100%", validate=False,
        ).encode("utf-8")

        renderer = self
        state = {"deadline": time.monotonic() + IDLE_TIMEOUT}

        class Handler(BaseHTTPRequestHandler):
            """Serves the page, and answers the requests sent by its script."""

            def _reply(self, status, body, ctype="application/json"):
                self.send_response(status)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _host_ok(self):
                # Rejects DNS rebinding: a remote site reaching this server under its own name.
                server = cast(ThreadingHTTPServer, self.server)
                return self.headers.get("Host") == f"127.0.0.1:{server.server_port}"

            def do_GET(self):  # pylint: disable=invalid-name
                """Serve the page."""
                if not self._host_ok() or self.path != "/":
                    self._reply(403, b"{}")
                    return
                state["deadline"] = time.monotonic() + IDLE_TIMEOUT
                self._reply(200, html, "text/html; charset=utf-8")

            def do_POST(self):  # pylint: disable=invalid-name
                """Handle ``/<token>/ping``, ``/<token>/closing`` and ``/<token>/export``."""
                raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                prefix = f"/{token}/"
                if not self._host_ok() or not self.path.startswith(prefix):
                    self._reply(403, b"{}")
                    return
                action = self.path[len(prefix):]
                if action == "closing":
                    state["deadline"] = time.monotonic() + CLOSE_GRACE
                    self._reply(200, b"{}")
                    return
                state["deadline"] = time.monotonic() + IDLE_TIMEOUT
                if action == "ping":
                    self._reply(200, b"{}")
                    return
                if action != "export":
                    self._reply(404, b"{}")
                    return
                try:
                    path = renderer.export(fig, json.loads(raw or b"{}"))
                    result = {"ok": True, "path": str(path)}
                except Exception as exc:  # pylint: disable=broad-exception-caught  # shown in the page
                    result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
                self._reply(200, json.dumps(result).encode("utf-8"))

            def log_message(self, format, *args):  # pylint: disable=redefined-builtin
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        server.timeout = 0.5

        def serve():
            while time.monotonic() < state["deadline"]:
                server.handle_request()
            server.server_close()

        # Not a daemon thread: the script may reach its end while the page is still open,
        # and the button has to keep working until the page is closed.
        thread = threading.Thread(target=serve, name="tikzplotly-browser", daemon=False)
        thread.start()
        return f"http://127.0.0.1:{server.server_port}/", thread

    def render(self, fig_dict):
        """Called by Plotly, for ``fig.show(renderer="tikzplotly")``."""
        url, _ = self.start_server(fig_dict)
        webbrowser.open(url)


def show(fig, output="figure.tex", config=None, **tikz_options):
    """Show a figure in the web browser, with an "Export to TikZ" button in its mode bar.

    Each click on the button writes the TikZ code of the figure, as currently displayed (zoom,
    traces hidden from the legend), to ``output``, or to ``output_1.tex``, ``output_2.tex``, ...
    if that file already exists. The Python process keeps running while the page is open,
    and stops a few seconds after it is closed.

    Parameters
    ----------
    fig
        Plotly figure
    output, optional
        file written by the button, by default ``"figure.tex"``
    config, optional
        Plotly config dict for the page, by default None
    **tikz_options
        passed on to :func:`get_tikz_code` (``tikz_options``, ``axis_options``, ``decimate``...)
    """
    renderer = TikzBrowserRenderer(output, config=config, **tikz_options)
    url, _ = renderer.start_server(fig)
    webbrowser.open(url)


def register_renderer():
    """Register the ``"tikzplotly"`` renderer with Plotly, so ``fig.show(renderer="tikzplotly")`` works."""
    if ExternalRenderer is object:  # pragma: no cover
        return
    if RENDERER_NAME not in pio.renderers:
        pio.renderers[RENDERER_NAME] = TikzBrowserRenderer()
