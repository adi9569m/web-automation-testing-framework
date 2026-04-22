"""Pytest hooks for a polished interactive HTML report."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from pytest_metadata.plugin import metadata_key

try:
    import pytest_html
except ImportError:  # pragma: no cover
    pytest_html = None

REPORT_CSS = Path(__file__).parent / "reports" / "dashboard.css"

TOOLBAR_HTML = """<section class=\"report-toolbar\">
  <div class=\"toolbar-shell\">
    <div class=\"toolbar-main\">
      <div class=\"toolbar-copy\">
        <p class=\"eyebrow\">QA report</p>
        <h2>Automation Results</h2>
        <p class=\"summary-note\">Clean execution view with quick search, status filters, expandable logs, and failure evidence when a test breaks.</p>
        <div class=\"toolbar-highlights\">
          <span class=\"highlight-pill\">SauceDemo</span>
          <span class=\"highlight-pill\">Pytest + Selenium</span>
          <span class=\"highlight-pill\">Interactive HTML</span>
        </div>
      </div>
      <div class=\"toolbar-actions\">
        <input id=\"scenario-search\" class=\"search-input\" type=\"search\" placeholder=\"Search scenarios or details\" />
        <div class=\"quick-filter-group\">
          <button class=\"quick-filter\" type=\"button\" data-status=\"all\">All</button>
          <button class=\"quick-filter\" type=\"button\" data-status=\"passed\">Passed</button>
          <button class=\"quick-filter\" type=\"button\" data-status=\"failed\">Failed</button>
        </div>
      </div>
    </div>
    <div class=\"toolbar-stats\">
      <div class=\"stat-card\">
        <span>Total</span>
        <strong id=\"toolbar-total\">0</strong>
      </div>
      <div class=\"stat-card stat-card-passed\">
        <span>Passed</span>
        <strong id=\"toolbar-passed\">0</strong>
      </div>
      <div class=\"stat-card stat-card-failed\">
        <span>Failed</span>
        <strong id=\"toolbar-failed\">0</strong>
      </div>
      <div class=\"stat-card\">
        <span>Duration</span>
        <strong id=\"toolbar-duration\">00:00:00</strong>
      </div>
    </div>
  </div>
</section>"""

TOOLBAR_SCRIPT = """<script>
(function () {
  const attachToolbar = () => {
    const search = document.getElementById("scenario-search");
    const buttons = Array.from(document.querySelectorAll(".quick-filter"));
    const rows = () => Array.from(document.querySelectorAll("tbody.results-table-row"));

    const render = () => {
      const term = (search?.value || "").trim().toLowerCase();
      rows().forEach((group) => {
        const text = group.textContent.toLowerCase();
        const searchMatch = !term || text.includes(term);
        const statusMatch = group.dataset.statusMatch !== "false";
        group.style.display = searchMatch && statusMatch ? "table-row-group" : "none";
      });
    };

    const applyStatus = (status) => {
      buttons.forEach((button) => {
        button.classList.toggle("active", button.dataset.status === status);
      });

      rows().forEach((group) => {
        const result = (group.querySelector(".col-result")?.textContent || "").trim().toLowerCase();
        group.dataset.statusMatch = status === "all" || result === status ? "true" : "false";
      });

      render();
    };

    const syncStats = () => {
      const total = document.querySelector(".run-count")?.textContent || "";
      const passed = document.querySelector(".filters .passed")?.textContent || "0";
      const failed = document.querySelector(".filters .failed")?.textContent || "0";
      const totalMatch = total.match(/^(\\d+)/);
      const durationMatch = total.match(/took\\s+(.+)\\.?$/i);

      const totalEl = document.getElementById("toolbar-total");
      const passedEl = document.getElementById("toolbar-passed");
      const failedEl = document.getElementById("toolbar-failed");
      const durationEl = document.getElementById("toolbar-duration");

      if (totalEl && totalMatch) totalEl.textContent = totalMatch[1];
      if (passedEl) passedEl.textContent = passed.replace(/[^0-9]/g, "") || "0";
      if (failedEl) failedEl.textContent = failed.replace(/[^0-9]/g, "") || "0";
      if (durationEl && durationMatch) durationEl.textContent = durationMatch[1];
    };

    buttons.forEach((button) => {
      button.addEventListener("click", () => applyStatus(button.dataset.status || "all"));
    });

    search?.addEventListener("input", render);
    syncStats();
    applyStatus("all");
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", attachToolbar);
  } else {
    attachToolbar();
  }
})();
</script>"""


def _detail_chip(label: str, value: str) -> str:
    return f'<div class="detail-chip"><span>{label}</span><code>{value}</code></div>'


def _format_duration(duration: float) -> str:
    if duration < 1:
        return f"{round(duration * 1000)} ms"

    minutes, seconds = divmod(int(round(duration)), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def pytest_configure(config: pytest.Config) -> None:
    """Register report metadata and custom styling."""
    metadata = config.stash[metadata_key]
    metadata["Project"] = "Web Application Testing & Automation Suite"
    metadata["Target App"] = "SauceDemo Login"
    metadata["Generated"] = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")

    css_files = list(getattr(config.option, "css", []) or [])
    css_path = str(REPORT_CSS)
    if css_path not in css_files:
        css_files.append(css_path)
    config.option.css = css_files


@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report) -> None:
    """Set a friendlier report title."""
    report.title = "Automation Results"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Capture test outcome details so later hooks can use them."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call":
        return

    report.description = str(item.function.__doc__ or item.name).strip()
    report.test_name = item.name.replace("test_", "").replace("_", " ").title()
    report.file_name = item.location[0]

    if pytest_html is None:
        return

    extras = list(getattr(report, "extras", []))
    extras.append(pytest_html.extras.text(report.description, name="Scenario"))

    driver = item.funcargs.get("driver")
    if report.failed and driver is not None:
        screenshots_dir = Path(__file__).parent / "reports" / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot_path = screenshots_dir / screenshot_name
        if driver.save_screenshot(str(screenshot_path)):
            extras.append(pytest_html.extras.image(str(screenshot_path), name="Failure screenshot"))

    report.extras = extras


def pytest_html_results_summary(prefix, summary, postfix, session) -> None:
    """Add the custom toolbar and interactions above the report."""
    prefix[:] = [TOOLBAR_HTML]
    summary[:] = []
    postfix[:] = [TOOLBAR_SCRIPT]


def pytest_html_results_table_header(cells) -> None:
    """Customize report columns."""
    cells[:] = [
        '<th class="sortable" data-column-type="result">Status</th>',
        '<th class="sortable" data-column-type="testId">Scenario</th>',
        '<th>Details</th>',
        '<th class="sortable" data-column-type="duration">Duration</th>',
    ]


def pytest_html_results_table_row(report, cells) -> None:
    """Render concise scenario-focused row data."""
    cells[:] = [
        f'<td class="col-result status-{report.outcome}">{report.outcome.title()}</td>',
        f'<td class="col-testId">{getattr(report, "test_name", report.nodeid)}</td>',
        f'<td class="col-description">{getattr(report, "description", report.nodeid)}</td>',
        f'<td class="col-duration">{_format_duration(report.duration)}</td>',
    ]


def pytest_html_results_table_html(report, data) -> None:
    """Prepend structured metadata above logs/extras."""
    data[:0] = [
        '<div class="detail-chip-grid">'
        + _detail_chip("Node", report.nodeid)
        + _detail_chip("File", getattr(report, "file_name", ""))
        + _detail_chip("Outcome", report.outcome.title())
        + '</div>'
    ]


def pytest_metadata(metadata: dict, config: pytest.Config) -> None:
    """Keep environment table focused on useful run context."""
    metadata.pop("Plugins", None)
