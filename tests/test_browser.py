"""Tests of the "Export to TikZ" button: the local server is exercised directly, without a browser."""
import http.client
import json
import re

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import pytest

import tikzplotly
from tikzplotly import _browser


@pytest.fixture(name="short_timeouts")
def fixture_short_timeouts(monkeypatch):
    monkeypatch.setattr(_browser, "IDLE_TIMEOUT", 10)
    monkeypatch.setattr(_browser, "CLOSE_GRACE", 0)


def make_figure():
    x = np.linspace(0, 10, 11)
    fig = go.Figure([go.Scatter(x=x, y=x**2, name="a"), go.Scatter(x=x, y=x, name="b")])
    fig.update_layout(title="demo")
    return fig


class Page:
    """Plays the part of the browser page."""

    def __init__(self, url):
        self.port = int(url.rstrip("/").rsplit(":", 1)[1])
        status, html = self.request("GET", "/")
        assert status == 200
        self.html = html.decode("utf-8")
        token_match = re.search(r"var token = '([^']+)'", self.html)
        assert token_match is not None
        self.token = token_match.group(1)

    def request(self, method, path, body=None, host=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        headers = {"Host": host or f"127.0.0.1:{self.port}"}
        conn.request(method, path, json.dumps(body or {}) if method == "POST" else None, headers)
        response = conn.getresponse()
        return response.status, response.read()

    def post(self, action, body=None, token=None):
        status, raw = self.request("POST", f"/{token or self.token}/{action}", body)
        return status, json.loads(raw)

    def close(self, thread):
        self.post("closing")
        thread.join(timeout=10)
        assert not thread.is_alive()


def test_renderer_registered():
    assert isinstance(pio.renderers["tikzplotly"], tikzplotly.TikzBrowserRenderer)


def test_export_button(tmp_path, short_timeouts):  # pylint: disable=unused-argument
    renderer = tikzplotly.TikzBrowserRenderer(tmp_path / "out" / "fig.tex", axis_options="width=8cm")
    url, thread = renderer.start_server(make_figure())
    page = Page(url)
    assert "exportTikz" in page.html

    status, result = page.post("export", {"axes": {"xaxis": None, "yaxis": None}, "visible": [None, None]})
    assert status == 200 and result["ok"]
    first = (tmp_path / "out" / "fig.tex").read_text(encoding="utf-8")
    assert "width=8cm" in first and "\\addlegendentry{b}" in first and "xmin" not in first

    # Zoomed in, second trace hidden from the legend: a new file, reflecting the view.
    _, result = page.post("export", {"axes": {"xaxis": [2, 5], "yaxis": [0, 30]}, "visible": [True, "legendonly"]})
    assert result["path"] == str(tmp_path / "out" / "fig_1.tex")
    second = (tmp_path / "out" / "fig_1.tex").read_text(encoding="utf-8")
    assert "xmin=2" in second and "ymax=30" in second
    assert "\\addlegendentry{a}" in second and "\\addlegendentry{b}" not in second

    page.close(thread)


def test_requests_rejected(tmp_path, short_timeouts):  # pylint: disable=unused-argument
    renderer = tikzplotly.TikzBrowserRenderer(tmp_path / "fig.tex")
    url, thread = renderer.start_server(make_figure())
    page = Page(url)
    assert page.post("export", token="wrong")[0] == 403
    assert page.request("POST", "/export")[0] == 403
    assert page.request("GET", "/", host="evil.example:80")[0] == 403
    assert page.post("unknown")[0] == 404
    assert not list(tmp_path.iterdir())
    page.close(thread)


def test_export_error_reported(tmp_path, short_timeouts):  # pylint: disable=unused-argument
    blocker = tmp_path / "blocker"
    blocker.write_text("", encoding="utf-8")  # a file where a directory is needed
    renderer = tikzplotly.TikzBrowserRenderer(blocker / "fig.tex")
    url, thread = renderer.start_server(make_figure())
    page = Page(url)
    status, result = page.post("export")
    assert status == 200 and not result["ok"] and result["error"]
    page.close(thread)


def test_idle_timeout(monkeypatch, tmp_path):
    monkeypatch.setattr(_browser, "IDLE_TIMEOUT", 0.5)
    _, thread = tikzplotly.TikzBrowserRenderer(tmp_path / "fig.tex").start_server(make_figure())
    thread.join(timeout=10)
    assert not thread.is_alive()


def test_figure_dict_with_binary_arrays(tmp_path):
    """Renderers receive ``fig.to_dict()``, where NumPy arrays are base64-encoded since Plotly 6."""
    renderer = tikzplotly.TikzBrowserRenderer(tmp_path / "fig.tex")
    path = renderer.export(make_figure().to_dict())
    assert path.read_text(encoding="utf-8") == tikzplotly.get_tikz_code(make_figure(), img_name=str(tmp_path / "fig.png"))


def test_heatmap_image_next_to_tex(tmp_path):
    renderer = tikzplotly.TikzBrowserRenderer(tmp_path / "map.tex")
    fig = go.Figure(go.Heatmap(z=np.arange(6.0).reshape(2, 3), colorscale="Viridis"))
    renderer.export(fig.to_dict())
    renderer.export(fig.to_dict())
    assert sorted(p.name for p in tmp_path.iterdir()) == ["map.png", "map.tex", "map_1.png", "map_1.tex"]


def test_show_opens_browser(monkeypatch, tmp_path, short_timeouts):  # pylint: disable=unused-argument
    opened = []
    monkeypatch.setattr(_browser.webbrowser, "open", opened.append)
    started = []
    original = _browser.TikzBrowserRenderer.start_server

    def start_server(self, fig):
        started.append(original(self, fig))
        return started[-1]

    monkeypatch.setattr(_browser.TikzBrowserRenderer, "start_server", start_server)

    fig = make_figure()
    tikzplotly.show(fig, tmp_path / "fig.tex")
    fig.show(renderer="tikzplotly")
    assert opened == [url for url, _ in started] and len(opened) == 2
    for url, thread in started:
        Page(url).close(thread)
