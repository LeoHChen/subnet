#!/usr/bin/env python3
"""Render the CPVSS Markdown design doc into a styled standalone HTML page.

This intentionally avoids third-party dependencies so `make html` works on a
fresh machine with only Python available. It supports the Markdown features used
by the design doc: headings, paragraphs, blockquotes, ordered and unordered
lists, pipe tables, fenced code blocks, links, bold text, and inline code.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


DEFAULT_SOURCE = Path("docs/cpvss-subnet-design.md")
DEFAULT_OUTPUT = Path("index.html")
DEFAULT_RELEASE_METADATA = Path("release.json")

TOKENOMICS_SIMULATOR_SECTION = """
<section id="tokenomics-simulator" data-no-notion="true"><div class="content">
<div class="simulator-shell">
  <div class="simulator-heading">
    <div>
      <h2>Tokenomics Simulator</h2>
      <p>Adjust the emission, staking, launch, and allocation assumptions to see how $POS supply, emissions, and bonded stake move over the launch timeline.</p>
    </div>
    <div class="simulator-status" data-sim-status>Live model</div>
  </div>
  <div class="sim-kpis" aria-label="Tokenomics simulation summary">
    <div class="sim-kpi"><span>Total supply</span><strong data-kpi="supply">-</strong></div>
    <div class="sim-kpi"><span>4-year effective emission</span><strong data-kpi="effectiveEmission">-</strong></div>
    <div class="sim-kpi"><span>Launch bonded stake</span><strong data-kpi="launchStake">-</strong></div>
    <div class="sim-kpi"><span>Bonded stake share</span><strong data-kpi="stakeShare">-</strong></div>
  </div>
  <div class="simulator-grid">
    <div class="sim-panel sim-controls" aria-label="Tokenomics simulator controls">
      <div class="sim-control-group">
        <h3>Emission Timeline</h3>
        <label class="sim-control"><span><span>Token supply</span><strong data-output="supply"></strong></span><input type="range" data-param="supply" min="100000000" max="5000000000" step="50000000" value="1000000000"></label>
        <label class="sim-control"><span><span>Incentive reserve</span><strong data-output="reservePct"></strong></span><input type="range" data-param="reservePct" min="1" max="30" step="0.5" value="12"></label>
        <label class="sim-control"><span><span>Fee offset</span><strong data-output="feeOffset"></strong></span><input type="range" data-param="feeOffset" min="0" max="80" step="5" value="0"></label>
        <label class="sim-control"><span><span>Epoch length</span><strong data-output="epochDays"></strong></span><input type="range" data-param="epochDays" min="7" max="30" step="1" value="7"></label>
        <label class="sim-control"><span><span>Year 1 weight</span><strong data-output="year1Weight"></strong></span><input type="range" data-param="year1Weight" min="0" max="70" step="0.5" value="37.5"></label>
        <label class="sim-control"><span><span>Year 2 weight</span><strong data-output="year2Weight"></strong></span><input type="range" data-param="year2Weight" min="0" max="70" step="0.5" value="29.2"></label>
        <label class="sim-control"><span><span>Year 3 weight</span><strong data-output="year3Weight"></strong></span><input type="range" data-param="year3Weight" min="0" max="70" step="0.5" value="20.8"></label>
        <label class="sim-control"><span><span>Year 4 weight</span><strong data-output="year4Weight"></strong></span><input type="range" data-param="year4Weight" min="0" max="70" step="0.5" value="12.5"></label>
        <p class="sim-note" data-output="yearWeightTotal"></p>
      </div>
      <div class="sim-control-group">
        <h3>Launch Staking</h3>
        <label class="sim-control"><span><span>Launch subnets</span><strong data-output="launchSubnets"></strong></span><input type="range" data-param="launchSubnets" min="1" max="12" step="1" value="4"></label>
        <label class="sim-control"><span><span>Miner agents per subnet</span><strong data-output="minerAgents"></strong></span><input type="range" data-param="minerAgents" min="1" max="64" step="1" value="16"></label>
        <label class="sim-control"><span><span>Validation agents per subnet</span><strong data-output="validationAgents"></strong></span><input type="range" data-param="validationAgents" min="1" max="64" step="1" value="16"></label>
        <label class="sim-control"><span><span>Stake per miner agent</span><strong data-output="minerStake"></strong></span><input type="range" data-param="minerStake" min="0" max="250000" step="5000" value="50000"></label>
        <label class="sim-control"><span><span>Stake per validation agent</span><strong data-output="validationStake"></strong></span><input type="range" data-param="validationStake" min="0" max="150000" step="5000" value="20000"></label>
        <label class="sim-control"><span><span>Subnet-owner stake</span><strong data-output="ownerStake"></strong></span><input type="range" data-param="ownerStake" min="0" max="10000000" step="250000" value="2500000"></label>
      </div>
      <div class="sim-control-group">
        <h3>Year 1 Pool Allocation</h3>
        <label class="sim-control"><span><span>Collection</span><strong data-output="collectionAlloc"></strong></span><input type="range" data-param="collectionAlloc" min="0" max="70" step="1" value="35"></label>
        <label class="sim-control"><span><span>Parsing</span><strong data-output="parsingAlloc"></strong></span><input type="range" data-param="parsingAlloc" min="0" max="70" step="1" value="25"></label>
        <label class="sim-control"><span><span>Validation</span><strong data-output="validationAlloc"></strong></span><input type="range" data-param="validationAlloc" min="0" max="70" step="1" value="15"></label>
        <label class="sim-control"><span><span>Score</span><strong data-output="scoreAlloc"></strong></span><input type="range" data-param="scoreAlloc" min="0" max="70" step="1" value="10"></label>
        <label class="sim-control"><span><span>Search and demand</span><strong data-output="searchAlloc"></strong></span><input type="range" data-param="searchAlloc" min="0" max="70" step="1" value="10"></label>
        <label class="sim-control"><span><span>Security</span><strong data-output="securityAlloc"></strong></span><input type="range" data-param="securityAlloc" min="0" max="70" step="1" value="5"></label>
        <p class="sim-note" data-output="poolAllocTotal"></p>
      </div>
    </div>
    <div class="sim-panel sim-results" aria-label="Tokenomics simulator charts">
      <div class="sim-chart-card">
        <div class="sim-chart-title"><h3>Cumulative Effective Emission</h3><span data-chart-note="line"></span></div>
        <svg class="sim-chart sim-line-chart" data-chart="emission-line" role="img" aria-label="Cumulative effective emission line chart"></svg>
      </div>
      <div class="sim-chart-grid">
        <div class="sim-chart-card">
          <div class="sim-chart-title"><h3>Year 1 Emission Pools</h3><span data-chart-note="pool"></span></div>
          <svg class="sim-chart sim-pie-chart" data-chart="pool-pie" role="img" aria-label="Year 1 emission pool pie chart"></svg>
          <div class="sim-legend" data-legend="pool"></div>
        </div>
        <div class="sim-chart-card">
          <div class="sim-chart-title"><h3>Launch Bonded Stake</h3><span data-chart-note="stake"></span></div>
          <svg class="sim-chart sim-pie-chart" data-chart="stake-pie" role="img" aria-label="Launch bonded stake pie chart"></svg>
          <div class="sim-legend" data-legend="stake"></div>
        </div>
      </div>
      <div class="table-wrap sim-table-wrap"><table class="sim-table"><thead><tr><th>Year</th><th>Gross Cap</th><th>Effective Emission</th><th>Effective / Epoch</th><th>Cumulative Effective</th><th>Supply Share</th></tr></thead><tbody data-sim-table></tbody></table></div>
    </div>
  </div>
</div>
</div></section>
"""

TOKENOMICS_SIMULATOR_CSS = """
      #tokenomics-simulator {
        background:
          linear-gradient(135deg, rgba(29, 124, 114, 0.09), rgba(185, 112, 20, 0.08)),
          var(--paper);
      }
      .simulator-shell {
        display: grid;
        gap: 22px;
      }
      .simulator-heading {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 18px;
      }
      .simulator-heading p { margin-bottom: 0; }
      .simulator-status {
        flex: 0 0 auto;
        min-height: 32px;
        padding: 5px 10px;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: var(--surface);
        color: var(--teal);
        font-size: 13px;
        font-weight: 760;
      }
      .sim-kpis {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
      }
      .sim-kpi,
      .sim-panel,
      .sim-chart-card {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
        box-shadow: var(--shadow);
      }
      .sim-kpi {
        min-height: 92px;
        padding: 16px;
      }
      .sim-kpi span,
      .sim-chart-title span,
      .sim-note {
        color: var(--muted);
        font-size: 13px;
      }
      .sim-kpi strong {
        display: block;
        margin-top: 8px;
        color: var(--ink);
        font-size: clamp(20px, 2vw, 28px);
        line-height: 1.08;
      }
      .simulator-grid {
        display: grid;
        grid-template-columns: minmax(280px, 360px) minmax(0, 1fr);
        gap: 18px;
        align-items: start;
      }
      .sim-panel { padding: 18px; }
      .sim-controls {
        display: grid;
        gap: 18px;
      }
      .sim-control-group {
        display: grid;
        gap: 12px;
      }
      .sim-control-group + .sim-control-group {
        padding-top: 16px;
        border-top: 1px solid var(--line);
      }
      .sim-control-group h3,
      .sim-chart-title h3 {
        margin: 0;
        font-size: 18px;
      }
      .sim-control {
        display: grid;
        gap: 8px;
      }
      .sim-control > span {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 10px;
        color: var(--muted);
        font-size: 13px;
      }
      .sim-control strong {
        color: var(--ink);
        font-size: 13px;
        text-align: right;
        white-space: nowrap;
      }
      .sim-control input[type="range"] {
        width: 100%;
        accent-color: var(--teal);
      }
      .sim-results {
        display: grid;
        gap: 16px;
      }
      .sim-chart-card {
        min-width: 0;
        padding: 16px;
      }
      .sim-chart-title {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 10px;
      }
      .sim-chart {
        display: block;
        width: 100%;
        min-height: 260px;
        overflow: visible;
      }
      .sim-line-chart { min-height: 300px; }
      .sim-pie-chart {
        max-width: 360px;
        margin: 0 auto;
      }
      .sim-chart path,
      .sim-chart polyline,
      .sim-chart circle,
      .sim-chart rect {
        transition: opacity 180ms ease, transform 180ms ease;
      }
      .sim-line-chart polyline {
        stroke-dasharray: 1;
        animation: simDraw 520ms ease both;
      }
      .sim-pie-chart path {
        transform-box: fill-box;
        transform-origin: center;
        animation: simPop 360ms ease both;
      }
      .sim-chart-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
      }
      .sim-legend {
        display: grid;
        gap: 7px;
        margin-top: 12px;
      }
      .sim-legend-item {
        display: grid;
        grid-template-columns: 12px minmax(0, 1fr) auto;
        gap: 8px;
        align-items: center;
        color: var(--muted);
        font-size: 13px;
      }
      .sim-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
      }
      .sim-table-wrap { margin-bottom: 0; }
      .sim-table { min-width: 680px; }
      .sim-pulse .sim-kpi strong {
        animation: simGlow 420ms ease;
      }
      @keyframes simGlow {
        0% { color: var(--amber); }
        100% { color: var(--ink); }
      }
      @keyframes simDraw {
        0% { stroke-dashoffset: 1; opacity: 0.3; }
        100% { stroke-dashoffset: 0; opacity: 1; }
      }
      @keyframes simPop {
        0% { transform: scale(0.96); opacity: 0.4; }
        100% { transform: scale(1); opacity: 1; }
      }
      @media (max-width: 1100px) {
        .sim-kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .simulator-grid { grid-template-columns: 1fr; }
      }
      @media (max-width: 720px) {
        .simulator-heading,
        .sim-chart-title {
          display: grid;
        }
        .sim-kpis,
        .sim-chart-grid {
          grid-template-columns: 1fr;
        }
      }
"""

TOKENOMICS_SIMULATOR_JS = """
        const initTokenomicsSimulator = () => {
          const root = document.getElementById("tokenomics-simulator");
          if (!root) {
            return;
          }
          const colors = ["#1d7c72", "#b97014", "#426d91", "#bd4b37", "#446b2f", "#7b5bb8", "#6b7280"];
          const paramNames = [
            "supply", "reservePct", "feeOffset", "epochDays", "year1Weight", "year2Weight", "year3Weight", "year4Weight",
            "launchSubnets", "minerAgents", "validationAgents", "minerStake", "validationStake", "ownerStake",
            "collectionAlloc", "parsingAlloc", "validationAlloc", "scoreAlloc", "searchAlloc", "securityAlloc",
          ];
          const inputs = new Map(paramNames.map((name) => [name, root.querySelector(`[data-param="${name}"]`)]));
          const value = (name) => Number(inputs.get(name)?.value || 0);
          const fmt = new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 });
          const pct = (number, digits = 1) => `${Number(number).toFixed(digits)}%`;
          const token = (number) => {
            const abs = Math.abs(number);
            if (abs >= 1_000_000_000) return `${(number / 1_000_000_000).toFixed(2)}B $POS`;
            if (abs >= 1_000_000) return `${(number / 1_000_000).toFixed(1)}M $POS`;
            if (abs >= 1_000) return `${(number / 1_000).toFixed(1)}K $POS`;
            return `${fmt.format(number)} $POS`;
          };
          const compact = (number) => token(number).replace(" $POS", "");
          const write = (selector, valueText) => {
            root.querySelectorAll(selector).forEach((node) => {
              node.textContent = valueText;
            });
          };
          const setOutput = (name, valueText) => write(`[data-output="${name}"]`, valueText);
          const normalized = (items) => {
            const total = items.reduce((sum, item) => sum + Math.max(0, item.value), 0) || 1;
            return items.map((item) => ({ ...item, share: Math.max(0, item.value) / total }));
          };
          const piePath = (cx, cy, r, start, end) => {
            const x1 = cx + r * Math.cos(start);
            const y1 = cy + r * Math.sin(start);
            const x2 = cx + r * Math.cos(end);
            const y2 = cy + r * Math.sin(end);
            const large = end - start > Math.PI ? 1 : 0;
            return `M ${cx} ${cy} L ${x1.toFixed(2)} ${y1.toFixed(2)} A ${r} ${r} 0 ${large} 1 ${x2.toFixed(2)} ${y2.toFixed(2)} Z`;
          };
          const drawPie = (chartName, legendName, rawItems) => {
            const svg = root.querySelector(`[data-chart="${chartName}"]`);
            const legend = root.querySelector(`[data-legend="${legendName}"]`);
            if (!svg || !legend) return;
            const items = normalized(rawItems).filter((item) => item.share > 0);
            let angle = -Math.PI / 2;
            const paths = items.map((item, index) => {
              const next = angle + item.share * Math.PI * 2;
              const path = `<path d="${piePath(130, 130, 104, angle, next)}" fill="${colors[index % colors.length]}"><title>${item.label}: ${token(item.value)}</title></path>`;
              angle = next;
              return path;
            }).join("");
            const total = rawItems.reduce((sum, item) => sum + item.value, 0);
            svg.setAttribute("viewBox", "0 0 260 260");
            svg.innerHTML = `${paths}<circle cx="130" cy="130" r="58" fill="var(--surface)" stroke="var(--line)"/><text x="130" y="124" text-anchor="middle" fill="var(--muted)" font-size="13">Total</text><text x="130" y="146" text-anchor="middle" fill="var(--ink)" font-size="18" font-weight="800">${compact(total)}</text>`;
            legend.innerHTML = items.map((item, index) => `<div class="sim-legend-item"><span class="sim-dot" style="background:${colors[index % colors.length]}"></span><span>${item.label}</span><strong>${token(item.value)} (${pct(item.share * 100)})</strong></div>`).join("");
          };
          const drawLine = (annual, cumulative, supply) => {
            const svg = root.querySelector('[data-chart="emission-line"]');
            if (!svg) return;
            const width = 760;
            const height = 310;
            const pad = { left: 72, right: 24, top: 24, bottom: 52 };
            const innerW = width - pad.left - pad.right;
            const innerH = height - pad.top - pad.bottom;
            const points = [0, ...cumulative];
            const maxValue = Math.max(...points, supply * 0.01);
            const x = (index) => pad.left + (index / (points.length - 1)) * innerW;
            const y = (amount) => pad.top + innerH - (amount / maxValue) * innerH;
            const coords = points.map((amount, index) => `${x(index).toFixed(2)},${y(amount).toFixed(2)}`).join(" ");
            const area = `M ${pad.left},${pad.top + innerH} L ${coords.replaceAll(" ", " L ")} L ${pad.left + innerW},${pad.top + innerH} Z`;
            const grid = [0, 0.25, 0.5, 0.75, 1].map((ratio) => {
              const gy = pad.top + innerH - ratio * innerH;
              const label = compact(maxValue * ratio);
              return `<line x1="${pad.left}" y1="${gy}" x2="${pad.left + innerW}" y2="${gy}" stroke="var(--line)" stroke-width="1"/><text x="${pad.left - 10}" y="${gy + 4}" text-anchor="end" fill="var(--muted)" font-size="12">${label}</text>`;
            }).join("");
            const labels = points.map((_, index) => `<text x="${x(index)}" y="${height - 18}" text-anchor="middle" fill="var(--muted)" font-size="12">Y${index}</text>`).join("");
            const circles = points.map((amount, index) => `<circle cx="${x(index)}" cy="${y(amount)}" r="4.5" fill="var(--teal)"><title>Year ${index}: ${token(amount)}</title></circle>`).join("");
            const bars = annual.map((amount, index) => {
              const barW = Math.max(18, innerW / 18);
              const bx = x(index + 1) - barW / 2;
              const by = y(amount);
              const bh = pad.top + innerH - by;
              return `<rect x="${bx}" y="${by}" width="${barW}" height="${bh}" rx="4" fill="var(--amber)" opacity="0.24"><title>Year ${index + 1} effective emission: ${token(amount)}</title></rect>`;
            }).join("");
            svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
            svg.innerHTML = `<rect x="0" y="0" width="${width}" height="${height}" fill="transparent"/>${grid}${labels}${bars}<path d="${area}" fill="var(--teal)" opacity="0.1"/><polyline pathLength="1" points="${coords}" fill="none" stroke="var(--teal)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>${circles}`;
          };
          const update = () => {
            const supply = value("supply");
            const reservePct = value("reservePct");
            const feeOffset = value("feeOffset");
            const epochDays = value("epochDays") || 7;
            const epochsPerYear = Math.max(1, Math.round(365 / epochDays));
            const yearWeights = [
              { label: "Year 1", value: value("year1Weight") },
              { label: "Year 2", value: value("year2Weight") },
              { label: "Year 3", value: value("year3Weight") },
              { label: "Year 4", value: value("year4Weight") },
            ];
            const years = normalized(yearWeights);
            const grossReserve = supply * reservePct / 100;
            const annualGross = years.map((year) => grossReserve * year.share);
            const annualEffective = annualGross.map((amount) => amount * (1 - feeOffset / 100));
            const cumulative = annualEffective.reduce((items, amount) => {
              items.push((items[items.length - 1] || 0) + amount);
              return items;
            }, []);
            const launchSubnets = value("launchSubnets");
            const minerStake = launchSubnets * value("minerAgents") * value("minerStake");
            const validationStake = launchSubnets * value("validationAgents") * value("validationStake");
            const ownerStake = launchSubnets * value("ownerStake");
            const totalStake = minerStake + validationStake + ownerStake;
            const poolInputs = [
              { key: "collection", label: "Collection", value: value("collectionAlloc") },
              { key: "parsing", label: "Parsing", value: value("parsingAlloc") },
              { key: "validation", label: "Validation", value: value("validationAlloc") },
              { key: "score", label: "Score", value: value("scoreAlloc") },
              { key: "search", label: "Search and demand", value: value("searchAlloc") },
              { key: "security", label: "Security", value: value("securityAlloc") },
            ];
            const pools = normalized(poolInputs).map((item) => ({ ...item, value: annualEffective[0] * item.share }));
            setOutput("supply", token(supply));
            setOutput("reservePct", pct(reservePct));
            setOutput("feeOffset", pct(feeOffset, 0));
            setOutput("epochDays", `${fmt.format(epochDays)} days (${fmt.format(epochsPerYear)}/year)`);
            setOutput("launchSubnets", fmt.format(launchSubnets));
            setOutput("minerAgents", fmt.format(value("minerAgents")));
            setOutput("validationAgents", fmt.format(value("validationAgents")));
            setOutput("minerStake", token(value("minerStake")));
            setOutput("validationStake", token(value("validationStake")));
            setOutput("ownerStake", token(value("ownerStake")));
            yearWeights.forEach((year, index) => setOutput(`year${index + 1}Weight`, pct(year.value)));
            poolInputs.forEach((item) => setOutput(`${item.key}Alloc`, pct(item.value, 0)));
            const yearWeightTotal = yearWeights.reduce((sum, item) => sum + item.value, 0);
            const poolTotal = poolInputs.reduce((sum, item) => sum + item.value, 0);
            setOutput("yearWeightTotal", `Schedule weights sum to ${pct(yearWeightTotal)} and are normalized for the line chart.`);
            setOutput("poolAllocTotal", `Pool sliders sum to ${pct(poolTotal, 0)} and are normalized for the pie chart.`);
            write('[data-kpi="supply"]', token(supply));
            write('[data-kpi="effectiveEmission"]', `${token(cumulative[cumulative.length - 1])} (${pct(cumulative[cumulative.length - 1] / supply * 100)})`);
            write('[data-kpi="launchStake"]', token(totalStake));
            write('[data-kpi="stakeShare"]', pct(totalStake / supply * 100, 3));
            write('[data-chart-note="line"]', `${token(grossReserve)} scheduled before fee offset; ${fmt.format(epochsPerYear)} epochs/year`);
            write('[data-chart-note="pool"]', `${token(annualEffective[0])} effective Year 1 cap`);
            write('[data-chart-note="stake"]', `${fmt.format(launchSubnets)} launch subnets`);
            drawLine(annualEffective, cumulative, supply);
            drawPie("pool-pie", "pool", pools);
            drawPie("stake-pie", "stake", [
              { label: "Miner agents", value: minerStake },
              { label: "Validation agents", value: validationStake },
              { label: "Subnet owners", value: ownerStake },
            ]);
            const table = root.querySelector("[data-sim-table]");
            table.innerHTML = annualGross.map((gross, index) => {
              const effective = annualEffective[index];
              return `<tr><td>Year ${index + 1}</td><td>${token(gross)}</td><td>${token(effective)}</td><td>${token(effective / epochsPerYear)}</td><td>${token(cumulative[index])}</td><td>${pct(cumulative[index] / supply * 100)}</td></tr>`;
            }).join("");
            root.classList.remove("sim-pulse");
            void root.offsetWidth;
            root.classList.add("sim-pulse");
          };
          inputs.forEach((input) => input?.addEventListener("input", update));
          update();
        };
"""


def load_release_metadata(path: Path = DEFAULT_RELEASE_METADATA) -> dict[str, str] | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(key): str(value) for key, value in data.items()}


def slugify(text: str, seen: dict[str, int]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = slug or "section"
    count = seen.get(slug, 0)
    seen[slug] = count + 1
    if count:
        return f"{slug}-{count + 1}"
    return slug


def inline(text: str) -> str:
    parts = re.split(r"(`[^`]*`)", text)
    rendered: list[str] = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            rendered.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue

        escaped = html.escape(part)
        escaped = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: (
                f'<a href="{html.escape(m.group(2), quote=True)}">'
                f"{m.group(1)}</a>"
            ),
            escaped,
        )
        escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
        rendered.append(escaped)
    return "".join(rendered)


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    first = lines[index].strip()
    second = lines[index + 1].strip()
    if "|" not in first or "|" not in second:
        return False
    cells = [cell.strip() for cell in second.strip("|").split("|")]
    return all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def is_block_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    stripped = line.strip()
    if not stripped:
        return True
    if re.match(r"#{2,6}\s+", stripped):
        return True
    if stripped.startswith(">"):
        return True
    if re.match(r"[-*]\s+", stripped):
        return True
    if re.match(r"\d+\.\s+", stripped):
        return True
    if stripped.startswith("```"):
        return True
    if is_table_start(lines, index):
        return True
    return False


def split_table_row(row: str) -> list[str]:
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def render_table(lines: list[str], index: int) -> tuple[str, int]:
    headers = split_table_row(lines[index])
    index += 2
    rows: list[list[str]] = []
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped or "|" not in stripped:
            break
        rows.append(split_table_row(stripped))
        index += 1

    head_html = "".join(f"<th>{inline(cell)}</th>" for cell in headers)
    body_rows = []
    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        cells = "".join(f"<td>{inline(cell)}</td>" for cell in padded[: len(headers)])
        body_rows.append(f"<tr>{cells}</tr>")

    table = (
        '<div class="table-wrap"><table><thead><tr>'
        f"{head_html}"
        "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table></div>"
    )
    return table, index


def render_markdown_body(lines: list[str], heading_slugs: dict[int, str]) -> str:
    output: list[str] = []
    i = 0
    in_section = False

    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue

        heading_match = re.match(r"(#{2,6})\s+(.+)", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            if level == 2:
                if in_section:
                    output.append("</div></section>")
                section_id = heading_slugs.get(i, "section")
                output.append(f'<section id="{section_id}"><div class="content">')
                output.append(f"<h2>{inline(text)}</h2>")
                in_section = True
            else:
                output.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1
            continue

        if not in_section:
            output.append('<section id="intro"><div class="content">')
            in_section = True

        if is_table_start(lines, i):
            table_html, i = render_table(lines, i)
            output.append(table_html)
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            language_class = ""
            if language:
                language_class = f' class="language-{html.escape(language, quote=True)}"'
            code = html.escape("\n".join(code_lines))
            output.append(f"<pre><code{language_class}>{code}</code></pre>")
            continue

        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip().lstrip(">").strip())
                i += 1
            output.append(f"<blockquote>{inline(' '.join(quote_lines))}</blockquote>")
            continue

        unordered = re.match(r"[-*]\s+(.+)", stripped)
        if unordered:
            items = []
            while i < len(lines):
                match = re.match(r"[-*]\s+(.+)", lines[i].strip())
                if not match:
                    break
                items.append(f"<li>{inline(match.group(1))}</li>")
                i += 1
            output.append("<ul>" + "".join(items) + "</ul>")
            continue

        ordered = re.match(r"\d+\.\s+(.+)", stripped)
        if ordered:
            items = []
            while i < len(lines):
                match = re.match(r"\d+\.\s+(.+)", lines[i].strip())
                if not match:
                    break
                items.append(f"<li>{inline(match.group(1))}</li>")
                i += 1
            output.append("<ol>" + "".join(items) + "</ol>")
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines) and not is_block_start(lines, i):
            paragraph_lines.append(lines[i].strip())
            i += 1
        output.append(f"<p>{inline(' '.join(paragraph_lines))}</p>")

    if in_section:
        output.append("</div></section>")

    return "\n".join(output)


def parse_document(markdown: str) -> dict[str, object]:
    lines = markdown.splitlines()
    title = "Poseidon Subnet CPVSS Design and Launch Roadmap"
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()

    first_h2 = next((i for i, line in enumerate(lines) if line.startswith("## ")), len(lines))
    meta_lines = lines[1:first_h2]
    metadata: list[tuple[str, str]] = []
    for line in meta_lines:
        clean = line.strip()
        if not clean or ":" not in clean:
            continue
        key, value = clean.split(":", 1)
        metadata.append((key.strip(), value.strip()))

    body_lines = lines[first_h2:]
    seen: dict[str, int] = {}
    nav: list[tuple[str, str]] = []
    heading_slugs: dict[int, str] = {}
    for index, line in enumerate(body_lines):
        if line.startswith("## "):
            text = line[3:].strip()
            slug = slugify(text, seen)
            heading_slugs[index] = slug
            nav.append((text, slug))

    body = render_markdown_body(body_lines, heading_slugs)
    return {"title": title, "metadata": metadata, "nav": nav, "body": body, "source_markdown": markdown}


def release_banner(release_info: dict[str, str] | None) -> str:
    if not release_info:
        return ""

    release = html.escape(release_info.get("release", "unreleased"))
    commit = html.escape(release_info.get("commit", "unknown"))
    release_date = html.escape(release_info.get("release_date", "unknown"))
    release_page = html.escape(release_info.get("release_page", ""), quote=True)
    page_link = ""
    if release_page:
        page_link = (
            '<span>Snapshot: '
            f'<a href="{release_page}">{release_page}</a>'
            "</span>"
        )

    return (
        '<div class="release-banner">'
        f"<span>Major release: <strong>{release}</strong></span>"
        f"<span>Source commit: <code>{commit}</code></span>"
        f"<span>Release date: {release_date}</span>"
        f"{page_link}"
        "</div>"
    )


def inject_tokenomics_simulator(body: str) -> str:
    anchor = '<section id="cpvss-overview"'
    if anchor not in body:
        return body + TOKENOMICS_SIMULATOR_SECTION
    return body.replace(anchor, TOKENOMICS_SIMULATOR_SECTION + "\n" + anchor, 1)


def render_page(
    document: dict[str, object],
    source_path: Path,
    release_info: dict[str, str] | None = None,
) -> str:
    title = str(document["title"])
    metadata = document["metadata"]
    nav = list(document["nav"])  # type: ignore[arg-type]
    body = inject_tokenomics_simulator(str(document["body"]))
    if ("Tokenomics Simulator", "tokenomics-simulator") not in nav:
        insert_at = next(
            (index + 1 for index, (_, slug) in enumerate(nav) if slug == "incentive-and-emission-schedule"),
            len(nav),
        )
        nav.insert(insert_at, ("Tokenomics Simulator", "tokenomics-simulator"))
    meta_html = "".join(
        f'<span class="pill">{html.escape(key)}: {html.escape(value)}</span>'
        for key, value in metadata  # type: ignore[misc]
    )
    nav_html = "".join(
        f'<a href="#{slug}">{html.escape(text)}</a>' for text, slug in nav
    )
    source_href = html.escape(source_path.as_posix(), quote=True)
    notion_markdown = json.dumps(str(document.get("source_markdown", ""))).replace("</", "<\\/")
    release_html = release_banner(release_info)

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)}</title>
    <style>
      :root {{
        --ink: #1f2523;
        --muted: #5f6864;
        --line: #d8ded9;
        --paper: #fbfaf6;
        --surface: #ffffff;
        --teal: #1d7c72;
        --teal-soft: #e3f2ee;
        --amber: #b97014;
        --amber-soft: #fbedd9;
        --coral: #bd4b37;
        --green: #446b2f;
        --blue: #426d91;
        --sidebar: #f4f1e9;
        --hero-bg: linear-gradient(90deg, rgba(29, 124, 114, 0.12), rgba(185, 112, 20, 0.08)), var(--surface);
        --th-bg: #eef4ef;
        --quote-bg: var(--ink);
        --quote-text: #f8f4e9;
        --control-bg: rgba(255, 255, 255, 0.86);
        --pill-bg: rgba(255, 255, 255, 0.72);
        --section-alt: rgba(255, 255, 255, 0.56);
        --shadow: 0 18px 45px rgba(37, 42, 38, 0.08);
      }}

      body[data-theme="protocol"] {{
        --ink: #eef4ef;
        --muted: #b9c5bf;
        --line: #34423d;
        --paper: #101816;
        --surface: #17211f;
        --teal: #62d4c1;
        --teal-soft: #183b35;
        --amber: #f0b65d;
        --amber-soft: #342819;
        --coral: #ff8f77;
        --green: #9bcf7c;
        --blue: #88b8e6;
        --sidebar: #0c1210;
        --hero-bg: linear-gradient(90deg, rgba(98, 212, 193, 0.14), rgba(240, 182, 93, 0.1)), var(--surface);
        --th-bg: #1d302c;
        --quote-bg: #0c1210;
        --quote-text: #effaf7;
        --control-bg: rgba(12, 18, 16, 0.88);
        --pill-bg: rgba(12, 18, 16, 0.45);
        --section-alt: rgba(255, 255, 255, 0.03);
        --shadow: 0 18px 45px rgba(0, 0, 0, 0.24);
      }}

      body[data-theme="market"] {{
        --ink: #20242a;
        --muted: #626a76;
        --line: #d7dce4;
        --paper: #f7f8fb;
        --surface: #ffffff;
        --teal: #006d83;
        --teal-soft: #e1f4f7;
        --amber: #996100;
        --amber-soft: #fff1d5;
        --coral: #c44b5d;
        --green: #386d4a;
        --blue: #3b64b4;
        --sidebar: #edf2f8;
        --hero-bg: linear-gradient(90deg, rgba(0, 109, 131, 0.1), rgba(196, 75, 93, 0.08)), var(--surface);
        --th-bg: #e8eef7;
        --quote-bg: #20242a;
        --quote-text: #f8fbff;
        --control-bg: rgba(255, 255, 255, 0.9);
        --pill-bg: rgba(255, 255, 255, 0.76);
        --section-alt: rgba(255, 255, 255, 0.66);
        --shadow: 0 18px 45px rgba(47, 62, 82, 0.11);
      }}

      * {{ box-sizing: border-box; }}
      html {{ scroll-behavior: smooth; }}
      body {{
        margin: 0;
        color: var(--ink);
        background: var(--paper);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        line-height: 1.6;
      }}
      a {{
        color: var(--teal);
        text-decoration-thickness: 1px;
        text-underline-offset: 3px;
      }}
      .page-shell {{
        display: grid;
        grid-template-columns: 280px minmax(0, 1fr);
        min-height: 100vh;
      }}
      .top-actions {{
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 10;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: flex-end;
        max-width: min(560px, calc(100vw - 32px));
        padding: 8px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--control-bg);
        box-shadow: var(--shadow);
        backdrop-filter: blur(12px);
      }}
      .style-switcher {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
      }}
      button {{
        min-height: 34px;
        border: 1px solid var(--line);
        border-radius: 7px;
        background: var(--surface);
        color: var(--ink);
        font: inherit;
        font-size: 13px;
        font-weight: 750;
        cursor: pointer;
      }}
      .theme-button {{ padding: 5px 10px; }}
      .theme-button[aria-pressed="true"], .pdf-button, .notion-button {{
        border-color: var(--teal);
        background: var(--teal);
        color: #ffffff;
      }}
      .pdf-button, .notion-button {{ padding: 5px 12px; }}
      .notion-button {{ min-width: 112px; }}
      aside {{
        position: sticky;
        top: 0;
        height: 100vh;
        padding: 32px 24px;
        border-right: 1px solid var(--line);
        background: var(--sidebar);
        overflow: auto;
      }}
      .brand {{ margin-bottom: 28px; }}
      .brand .eyebrow {{
        color: var(--amber);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0;
        text-transform: uppercase;
      }}
      .brand h1 {{
        margin: 8px 0 12px;
        font-size: 24px;
        line-height: 1.12;
      }}
      .brand p {{
        margin: 0;
        color: var(--muted);
        font-size: 14px;
      }}
      nav {{
        display: grid;
        gap: 6px;
      }}
      nav a {{
        display: block;
        padding: 8px 10px;
        color: var(--ink);
        border-radius: 6px;
        text-decoration: none;
        font-size: 14px;
      }}
      nav a:hover {{
        background: var(--teal-soft);
        color: var(--teal);
      }}
      main {{ min-width: 0; }}
      .hero {{
        padding: 58px clamp(24px, 5vw, 76px) 30px;
        background: var(--hero-bg);
        border-bottom: 1px solid var(--line);
      }}
      .hero-inner {{ max-width: 1100px; }}
      .meta-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;
        padding-right: 300px;
      }}
      .pill {{
        display: inline-flex;
        align-items: center;
        min-height: 30px;
        padding: 4px 10px;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: var(--pill-bg);
        color: var(--muted);
        font-size: 13px;
        font-weight: 650;
      }}
      .hero h2 {{
        max-width: 900px;
        margin: 0;
        font-size: clamp(34px, 5vw, 64px);
        line-height: 1.02;
        letter-spacing: 0;
      }}
      .hero p {{
        max-width: 780px;
        margin: 22px 0 0;
        color: var(--muted);
        font-size: 19px;
      }}
      .release-banner {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        max-width: 980px;
        margin-top: 22px;
      }}
      .release-banner span {{
        display: inline-flex;
        align-items: center;
        min-height: 32px;
        padding: 5px 10px;
        border: 1px solid var(--line);
        border-radius: 7px;
        background: var(--surface);
        color: var(--ink);
        font-size: 13px;
        font-weight: 700;
      }}
      section {{
        padding: 48px clamp(24px, 5vw, 76px);
        border-bottom: 1px solid var(--line);
      }}
      section:nth-of-type(even) {{ background: var(--section-alt); }}
      .content {{ max-width: 1120px; }}
      h2, h3, h4, h5, h6 {{
        line-height: 1.18;
        letter-spacing: 0;
      }}
      h2 {{
        margin: 0 0 18px;
        font-size: clamp(28px, 3vw, 42px);
      }}
      h3 {{
        margin: 34px 0 12px;
        font-size: 24px;
      }}
      h4 {{
        margin: 24px 0 8px;
        font-size: 18px;
        color: var(--teal);
      }}
      p {{ max-width: 880px; }}
      blockquote {{
        max-width: 1000px;
        margin: 24px 0;
        padding: 24px 28px;
        border-left: 5px solid var(--teal);
        border-radius: 8px;
        background: var(--quote-bg);
        color: var(--quote-text);
        font-size: clamp(19px, 2vw, 28px);
        line-height: 1.35;
        font-weight: 720;
      }}
      .table-wrap {{
        width: 100%;
        margin: 24px 0;
        overflow-x: auto;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
      }}
      table {{
        width: 100%;
        min-width: 820px;
        border-collapse: collapse;
      }}
      th, td {{
        padding: 14px 16px;
        border-bottom: 1px solid var(--line);
        text-align: left;
        vertical-align: top;
      }}
      th {{
        background: var(--th-bg);
        color: var(--ink);
        font-size: 13px;
        text-transform: uppercase;
      }}
      tr:last-child td {{ border-bottom: 0; }}
      ul, ol {{
        max-width: 880px;
        padding-left: 24px;
      }}
      li + li {{ margin-top: 7px; }}
      code {{
        padding: 2px 5px;
        border: 1px solid var(--line);
        border-radius: 5px;
        background: var(--surface);
        font-size: 0.92em;
      }}
      pre {{
        max-width: 880px;
        margin: 18px 0;
        padding: 16px 18px;
        overflow-x: auto;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
      }}
      pre code {{
        padding: 0;
        border: 0;
        background: transparent;
        font-size: 13px;
        line-height: 1.55;
      }}
      .footer {{
        padding: 36px clamp(24px, 5vw, 76px);
        background: var(--quote-bg);
        color: var(--quote-text);
      }}
      .footer p {{
        margin: 0;
        color: var(--quote-text);
      }}
{TOKENOMICS_SIMULATOR_CSS}
      @media (max-width: 980px) {{
        .page-shell {{ display: block; }}
        aside {{
          position: static;
          height: auto;
          padding: 24px;
          border-right: 0;
          border-bottom: 1px solid var(--line);
        }}
        nav {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        .meta-row {{ padding-right: 0; }}
      }}
      @media (max-width: 560px) {{
        nav {{ grid-template-columns: 1fr; }}
        .hero, section, .footer {{
          padding-left: 18px;
          padding-right: 18px;
        }}
        .hero h2 {{ font-size: 36px; }}
        .hero p {{ font-size: 16px; }}
        th, td {{ padding: 12px; }}
      }}
      @media print {{
        @page {{ margin: 0.55in; }}
        body {{
          background: #ffffff;
          color: #1f2523;
        }}
        .top-actions, aside {{ display: none; }}
        .page-shell {{ display: block; }}
        .hero, section, .footer {{ padding: 24px 0; }}
        blockquote {{ font-size: 18px; }}
        pre {{
          white-space: pre-wrap;
          break-inside: avoid;
        }}
        .table-wrap {{
          overflow: visible;
          break-inside: avoid;
        }}
        table {{
          min-width: 0;
          font-size: 10px;
        }}
        th, td {{ padding: 7px 8px; }}
        h2, h3, h4 {{ break-after: avoid; }}
        tr {{ break-inside: avoid; }}
      }}
    </style>
  </head>
  <body data-theme="executive">
    <div class="top-actions" aria-label="Document actions">
      <div class="style-switcher" role="group" aria-label="Style">
        <button class="theme-button" type="button" data-theme-option="executive" aria-pressed="true">Executive</button>
        <button class="theme-button" type="button" data-theme-option="protocol" aria-pressed="false">Protocol</button>
        <button class="theme-button" type="button" data-theme-option="market" aria-pressed="false">Market</button>
      </div>
      <button class="pdf-button" type="button" id="export-pdf">Export PDF</button>
      <button class="notion-button" type="button" id="export-notion">Copy to Notion</button>
    </div>
    <div class="page-shell">
      <aside>
        <div class="brand">
          <div class="eyebrow">Poseidon Subnet</div>
          <h1>{html.escape(title)}</h1>
          <p>Source Markdown: <a href="{source_href}">{source_href}</a></p>
        </div>
        <nav aria-label="Document sections">
          {nav_html}
        </nav>
      </aside>
      <main>
        <header class="hero" id="summary">
          <div class="hero-inner">
            <div class="meta-row">{meta_html}</div>
            <h2>{html.escape(title)}</h2>
            <p>Generated from the Markdown source. Edit the Markdown and run <code>make html</code> to rebuild this page.</p>
            {release_html}
          </div>
        </header>
        {body}
        <footer class="footer">
          <p>Generated from {source_href}. Use the Export PDF or Copy to Notion buttons to share this document.</p>
        </footer>
      </main>
    </div>
    <script>
      (() => {{
        const storageKey = "cpvss-theme";
        const buttons = Array.from(document.querySelectorAll("[data-theme-option]"));
        const exportButton = document.getElementById("export-pdf");
        const exportNotionButton = document.getElementById("export-notion");
        const notionMarkdown = {notion_markdown};
        const getSavedTheme = () => {{
          try {{
            return localStorage.getItem(storageKey);
          }} catch {{
            return null;
          }}
        }};
        const saveTheme = (theme) => {{
          try {{
            localStorage.setItem(storageKey, theme);
          }} catch {{
            /* Theme persistence is optional for local files. */
          }}
        }};
        const setTheme = (theme) => {{
          const allowed = buttons.map((button) => button.dataset.themeOption);
          const nextTheme = allowed.includes(theme) ? theme : "executive";
          document.body.dataset.theme = nextTheme;
          buttons.forEach((button) => {{
            button.setAttribute("aria-pressed", String(button.dataset.themeOption === nextTheme));
          }});
          saveTheme(nextTheme);
        }};
        buttons.forEach((button) => {{
          button.addEventListener("click", () => setTheme(button.dataset.themeOption));
        }});
        exportButton.addEventListener("click", () => window.print());
        const htmlEscape = (value) => {{
          return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
        }};
        const cleanClone = (node) => {{
          const clone = node.cloneNode(true);
          clone.querySelectorAll("[class], [id], [style]").forEach((element) => {{
            element.removeAttribute("class");
            element.removeAttribute("id");
            element.removeAttribute("style");
          }});
          return clone;
        }};
        const notionHtml = () => {{
          const title = document.querySelector(".hero h2")?.textContent?.trim() || document.title;
          const metadata = Array.from(document.querySelectorAll(".meta-row .pill"))
            .map((item) => "<p><strong>" + htmlEscape(item.textContent.trim()) + "</strong></p>")
            .join("");
          const sections = Array.from(document.querySelectorAll("main > section:not([data-no-notion])"))
            .map((section) => {{
              const content = section.querySelector(".content") || section;
              return cleanClone(content).innerHTML;
            }})
            .join("\\n");
          return "<article><h1>" + htmlEscape(title) + "</h1>" + metadata + sections + "</article>";
        }};
        const fallbackCopy = (text) => {{
          const textarea = document.createElement("textarea");
          textarea.value = text;
          textarea.setAttribute("readonly", "");
          textarea.style.position = "fixed";
          textarea.style.left = "-9999px";
          textarea.style.top = "0";
          document.body.appendChild(textarea);
          textarea.select();
          const copied = document.execCommand("copy");
          textarea.remove();
          if (!copied) {{
            throw new Error("Clipboard copy failed");
          }}
        }};
        const writeNotionClipboard = async (markdown, htmlContent) => {{
          if (navigator.clipboard && window.ClipboardItem && typeof navigator.clipboard.write === "function") {{
            const item = new ClipboardItem({{
              "text/html": new Blob([htmlContent], {{ type: "text/html" }}),
              "text/plain": new Blob([markdown], {{ type: "text/plain" }}),
            }});
            await navigator.clipboard.write([item]);
            return;
          }}
          if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {{
            await navigator.clipboard.writeText(markdown);
            return;
          }}
          fallbackCopy(markdown);
        }};
        const setNotionButtonLabel = (label) => {{
          const original = "Copy to Notion";
          exportNotionButton.textContent = label;
          window.setTimeout(() => {{
            exportNotionButton.textContent = original;
          }}, 1800);
        }};
        const exportNotion = async () => {{
          try {{
            await writeNotionClipboard(notionMarkdown, notionHtml());
            setNotionButtonLabel("Copied");
          }} catch (error) {{
            console.error(error);
            setNotionButtonLabel("Copy failed");
          }}
        }};
        exportNotionButton.addEventListener("click", exportNotion);
{TOKENOMICS_SIMULATOR_JS}
        initTokenomicsSimulator();
        setTheme(getSavedTheme() || "executive");
      }})();
    </script>
  </body>
</html>
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--release", help="Major release name, for example v1.0.0")
    parser.add_argument("--commit", help="Source commit hash for the release")
    parser.add_argument("--release-date", help="Release date in YYYY-MM-DD form")
    parser.add_argument("--release-page", help="Versioned HTML snapshot path")
    parser.add_argument(
        "--metadata-out",
        type=Path,
        help="Write release metadata for future `make html` runs",
    )
    return parser.parse_args(argv[1:])


def release_info_from_args(args: argparse.Namespace) -> dict[str, str] | None:
    if args.release:
        return {
            "release": args.release,
            "commit": args.commit or "unknown",
            "release_date": args.release_date or "unknown",
            "release_page": args.release_page or "",
        }
    return load_release_metadata()


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    source = args.source
    output = args.output

    markdown = source.read_text(encoding="utf-8")
    document = parse_document(markdown)
    release_info = release_info_from_args(args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_page(document, source, release_info), encoding="utf-8")
    if args.metadata_out and release_info:
        args.metadata_out.write_text(
            json.dumps(release_info, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(f"Rendered {source} -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
