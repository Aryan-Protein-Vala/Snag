"use client";
import { useState } from "react";

// ─── SVG Line Art Icons ────────────────────────────────────────────────────
const Icons = {
  screenshot: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
      <polyline points="21 15 16 10 5 21"/>
    </svg>
  ),
  download: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
      <polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
    </svg>
  ),
  clipboard: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
      <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
      <line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/>
    </svg>
  ),
  pin: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
    </svg>
  ),
  lock: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
  ),
  zap: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
    </svg>
  ),
  terminal: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>
    </svg>
  ),
  key: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>
    </svg>
  ),
  widget: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
      <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
    </svg>
  ),
  focus: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/>
      <line x1="4.93" y1="4.93" x2="9.17" y2="9.17"/><line x1="14.83" y1="14.83" x2="19.07" y2="19.07"/>
      <line x1="14.83" y1="9.17" x2="19.07" y2="4.93"/><line x1="4.93" y1="19.07" x2="9.17" y2="14.83"/>
    </svg>
  ),
  imgIcon: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
      <polyline points="21 15 16 10 5 21"/>
    </svg>
  ),
  fileIcon: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14 2 14 8 20 8"/>
    </svg>
  ),
  drag: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="5 9 2 12 5 15"/><polyline points="9 5 12 2 15 5"/>
      <polyline points="15 19 12 22 9 19"/><polyline points="19 9 22 12 19 15"/>
      <line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/>
    </svg>
  ),
  close: (
    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  ),
  copy: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
    </svg>
  ),
};

// ─── Platform SVG Logos ───────────────────────────────────────────────────
const AppleLogo = () => (
  <svg width="16" height="16" viewBox="0 0 814 1000" fill="currentColor">
    <path d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76 0-103.7 40.8-165.9 40.8s-105-42.3-150.3-109.7C171.2 649 128 580 128 513.5c0-131.1 85.4-200.2 168.8-200.2 46.2 0 84.7 30.4 113.5 30.4 27.5 0 70.6-32.4 122.6-32.4 20.4 0 98.7 1.9 148.4 74.8zm-196-175.2c22.4-26.7 38.7-64 38.7-101.3 0-5.8-.6-11.6-1.9-16.2-37.4 1.3-82.6 24.9-110 53-20.4 22.3-38.7 58.7-38.7 95.5 0 6.4 1.3 12.9 1.9 15.2 2.6.6 6.5 1.3 10.4 1.3 34.9 0 78.2-23 99.6-47.5z"/>
  </svg>
);

const WindowsLogo = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.9-1.801"/>
  </svg>
);

const LinuxLogo = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12.504 0C12 0 9 .3 7 2.4 5 4.5 4.5 7.2 5.7 11.1c.5 1.6.9 2.9 1.2 3.6-.3.3-.8.9-1.2 1.8-.6 1.1-.9 2.3-.9 3.6 0 2.7 1.5 4.5 3.9 4.5 1.4 0 2.8-.5 3.9-1.5 1.1 1 2.5 1.5 3.9 1.5 2.4 0 3.9-1.8 3.9-4.5 0-1.3-.3-2.5-.9-3.6-.4-.9-.9-1.5-1.2-1.8.3-.7.7-2 1.2-3.6 1.2-3.9.7-6.6-1.3-8.7C17 .3 14 0 12.504 0zm1.3 5.8c.8.5 1.4 1.4 1.7 2.4.3.8.2 1.5-.1 2-.4-.5-1-.9-1.7-1.2-.7-.3-1.5-.5-2.2-.5-.8 0-1.5.2-2.2.5-.7.3-1.3.7-1.7 1.2-.3-.5-.4-1.2-.1-2 .3-1 .9-1.9 1.7-2.4C10.2 5.3 11.2 5 12 5c.8 0 1.6.3 1.804.8z"/>
  </svg>
);

// ─── Download Modal ────────────────────────────────────────────────────────
type Platform = "mac" | "windows" | "linux" | null;

const downloadInfo: Record<string, { title: string; cmd: string; note: string }> = {
  mac: {
    title: "Install on macOS",
    cmd: "curl -fsSL https://snag.app/install.sh | bash",
    note: "Requires macOS 12+. Removes Gatekeeper quarantine automatically.",
  },
  windows: {
    title: "Install on Windows",
    cmd: 'irm https://snag.app/install.ps1 | iex',
    note: "Run in PowerShell as Administrator. Extracts to %LOCALAPPDATA%\\Snag.",
  },
  linux: {
    title: "Install on Linux",
    cmd: "curl -fsSL https://snag.app/install.sh | bash",
    note: "Supports Ubuntu 20.04+, Fedora 36+, Arch. Installs to ~/.local/bin.",
  },
};

function DownloadModal({ platform, onClose }: { platform: Platform; onClose: () => void }) {
  const [copied, setCopied] = useState(false);
  if (!platform) return null;
  const info = downloadInfo[platform];

  const handleCopy = () => {
    navigator.clipboard.writeText(info.cmd);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>{Icons.close}</button>
        <div className="modal-title">{info.title}</div>
        <p className="modal-sub">Run this command in your terminal:</p>
        <div className="modal-cmd-box">
          <code className="modal-cmd">{info.cmd}</code>
          <button className="modal-copy" onClick={handleCopy}>
            {Icons.copy}
            {copied ? "Copied!" : "Copy"}
          </button>
        </div>
        <p className="modal-note">{info.note}</p>
      </div>
    </div>
  );
}

// ─── Interactive Widget Preview ────────────────────────────────────────────
const TABS = [
  { id: "Screenshots", icon: Icons.screenshot },
  { id: "Downloads", icon: Icons.download },
  { id: "Clipboard", icon: Icons.clipboard },
  { id: "Snippets", icon: Icons.pin },
];

const TAB_DATA: Record<string, { icon: "img" | "file" | "text"; name: string; sub: string }[]> = {
  Screenshots: [
    { icon: "img", name: "Screenshot 2026-07-27.png", sub: "2m ago" },
    { icon: "img", name: "Dashboard-mockup.png", sub: "18m ago" },
    { icon: "img", name: "UI-review-final.png", sub: "1h ago" },
    { icon: "img", name: "Snag-hero-dark.png", sub: "3h ago" },
    { icon: "img", name: "cover-photo.jpg", sub: "5h ago" },
  ],
  Downloads: [
    { icon: "file", name: "figma-plugin-v2.zip", sub: "5m ago" },
    { icon: "file", name: "invoice_july.pdf", sub: "1h ago" },
    { icon: "file", name: "project-brief.docx", sub: "3h ago" },
    { icon: "file", name: "font-pack.zip", sub: "Yesterday" },
  ],
  Clipboard: [
    { icon: "text", name: "const token = process.env.NEXT_PU…", sub: "12s ago" },
    { icon: "text", name: "https://github.com/Aryan-Protein…", sub: "4m ago" },
    { icon: "text", name: "Dear team, please find attached…", sub: "30m ago" },
  ],
  Snippets: [
    { icon: "text", name: "npm run dev", sub: "Pinned" },
    { icon: "text", name: "git add . && git commit -m ''", sub: "Pinned" },
    { icon: "text", name: "Dear [Name], Hope this email…", sub: "Pinned" },
  ],
};

const ANNOTATIONS = [
  { id: "close", x: 60, y: 0, label: "Close & quit cleanly", lineX: 92, lineY: 6 },
  { id: "tabs",  x: -120, y: 0, label: "4 tabs: Scrn / Down / Clip / Snip", lineX: 20, lineY: 18 },
  { id: "drag",  x: 100, y: 0, label: "Drag files out to any app", lineX: 70, lineY: 90 },
  { id: "copy",  x: 100, y: 0, label: "Click to copy to clipboard", lineX: 85, lineY: 45 },
];

function WidgetPreview() {
  const [activeTab, setActiveTab] = useState("Screenshots");
  const items = TAB_DATA[activeTab] ?? [];

  return (
    <div className="widget-preview-wrap">
      {/* Annotation callouts */}
      <div className="widget-annotations">
        {ANNOTATIONS.map((a) => (
          <div key={a.id} className="annotation" style={{ left: `${a.lineX}%`, top: `${a.lineY}%` }}>
            <div className={`annotation-dot`} />
            <div className={`annotation-line ${a.x < 0 ? "line-left" : "line-right"}`} />
            <div className={`annotation-label ${a.x < 0 ? "label-left" : "label-right"}`}>
              {a.label}
            </div>
          </div>
        ))}
      </div>

      {/* Widget card */}
      <div className="widget-card">
        {/* Top bar */}
        <div className="wc-topbar">
          <span className="wc-logo">snag.</span>
          <button className="wc-close">{Icons.close}</button>
        </div>

        {/* Tabs */}
        <div className="wc-tabs">
          {TABS.map((t) => (
            <button
              key={t.id}
              className={`wc-tab ${activeTab === t.id ? "active" : ""}`}
              onClick={() => setActiveTab(t.id)}
              title={t.id}
            >
              {t.icon}
            </button>
          ))}
        </div>

        {/* Items */}
        <div className="wc-list" style={{ minHeight: "235px", display: "flex", flexDirection: "column", justifyContent: "flex-start" }}>
          {items.map((item, i) => (
            <div className="wc-item" key={i}>
              <span className="wc-item-icon">
                {item.icon === "img" ? Icons.imgIcon : item.icon === "file" ? Icons.fileIcon : Icons.clipboard}
              </span>
              <span className="wc-item-name">{item.name}</span>
              <span className="wc-item-sub">{item.sub}</span>
              <span className="wc-drag-hint">{Icons.drag}</span>
            </div>
          ))}
        </div>

        {/* Drag hint badge */}
        <div className="wc-footer-hint">
          {Icons.drag}
          <span>Drag any item out to any app</span>
        </div>
      </div>
    </div>
  );
}

// ─── Page ──────────────────────────────────────────────────────────────────
export default function Home() {
  const [downloadPlatform, setDownloadPlatform] = useState<Platform>(null);

  return (
    <>
      <DownloadModal platform={downloadPlatform} onClose={() => setDownloadPlatform(null)} />

      {/* ── NAV ── */}
      <nav className="nav">
        <div className="container nav-inner">
          <div className="nav-logo">snag<span>.</span></div>
          <ul className="nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#how">How it works</a></li>
            <li><a href="#compare">Compare</a></li>
            <li><a href="#pricing">Pricing</a></li>
          </ul>
          <a href="#pricing" className="btn btn-ghost" style={{ padding: "9px 18px", fontSize: "13px" }}>
            Get Snag
          </a>
        </div>
      </nav>

      {/* ── HERO ── */}
      <section className="hero">
        <div className="hero-glow" />
        <div className="container" style={{ position: "relative", zIndex: 1 }}>
          <div className="hero-eyebrow anim d1">
            <svg width="8" height="8" viewBox="0 0 8 8"><circle cx="4" cy="4" r="4" fill="#5ECC7B" /></svg>
            Cross-platform · macOS · Windows · Linux
          </div>

          <h1 className="hero-title anim d2">
            Your workflow,<br />unhindered.
          </h1>

          <p className="hero-sub anim d3">
            A premium floating widget that lives at the edge of your screen.
            Screenshots, downloads, clipboard history, and pinned snippets —
            one keystroke away. Always ready, never in the way.
          </p>

          <div className="hero-cta anim d4">
            <a href="#pricing" className="btn btn-white">Get Snag — from $0.99</a>
            <a href="#how" className="btn btn-ghost">See how it works</a>
          </div>

          {/* ── Platform Badges ── */}
          <div className="hero-platforms anim d5">
            <span className="platforms-label">Available on</span>

            <button className="platform-badge" onClick={() => setDownloadPlatform("mac")}>
              <AppleLogo />
              macOS
            </button>
            <button className="platform-badge" onClick={() => setDownloadPlatform("windows")}>
              <WindowsLogo />
              Windows
            </button>
            <button className="platform-badge" onClick={() => setDownloadPlatform("linux")}>
              <LinuxLogo />
              Linux
            </button>
          </div>
        </div>
      </section>

      {/* ── ANNOTATED WIDGET PREVIEW ── */}
      <section className="preview-section">
        <WidgetPreview />
      </section>

      <div className="divider" />

      {/* ── FEATURES ── */}
      <section className="section" id="features">
        <div className="container">
          <div className="section-label">Core Features</div>
          <h2 className="section-title">Everything you need.<br />Nothing you don&apos;t.</h2>
          <div className="features-grid" style={{ marginTop: "48px" }}>
            {[
              { icon: Icons.screenshot, title: "Screenshot Watcher",      desc: "Automatically surfaces your last 10 screenshots the moment they land on your Desktop or Pictures folder. Drag directly into Slack, Notion, or anywhere." },
              { icon: Icons.download,   title: "Downloads Inbox",          desc: "Your 10 most recent downloads, always one click away. Double-click to open. Hover to reveal in Explorer/Finder. Drag into any window." },
              { icon: Icons.clipboard,  title: "Clipboard History",         desc: "Persists your last 15 copied text snippets — even after restarts. Click any entry to instantly re-copy. No clutter, no feedback loops." },
              { icon: Icons.pin,        title: "Pinned Snippets",           desc: "Save boilerplate text, code blocks, credentials, or email templates permanently. Press Enter to add. Always there when you need them." },
              { icon: Icons.lock,       title: "Hardware-Locked License",   desc: "Each license binds to one machine UUID. Prevents key sharing without a heavy client. Backend verified via Supabase on first activation." },
              { icon: Icons.zap,        title: "Instant & Always On",       desc: "The widget is frameless, stays on top, and is positioned out of your way. Uses < 80MB RAM. Launch it with a global shortcut in seconds." },
            ].map((f, i) => (
              <div className="feature-card" key={i}>
                <span className="feature-icon">{f.icon}</span>
                <div className="feature-title">{f.title}</div>
                <div className="feature-desc">{f.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="divider" />

      {/* ── HOW IT WORKS ── */}
      <section className="section" id="how">
        <div className="container">
          <div className="section-label">How it works</div>
          <h2 className="section-title">Up and running<br />in 60 seconds.</h2>
          <div className="how-grid">
            {[
              { icon: Icons.terminal, title: "Install with one command",  desc: 'Run curl -fsSL snag.app/install.sh | bash in your terminal. The script handles everything — download, extract, and launch.' },
              { icon: Icons.key,      title: "Enter your license key",    desc: 'On first launch, paste your 16-character SNAG-XXXX-XXXX-XXXX key. It binds to your machine UUID. Done.' },
              { icon: Icons.widget,   title: "Widget appears instantly",  desc: 'Snag floats in the bottom-right corner. Frameless, always-on-top. Click the tabs or drag files out immediately.' },
              { icon: Icons.focus,    title: "Never leave your flow",     desc: 'Use the global shortcut to summon and dismiss it. Your clipboard history and snippets persist across restarts.' },
            ].map((s, i) => (
              <div className="how-step" key={i}>
                <span className="step-icon">{s.icon}</span>
                <div className="how-step-title">{s.title}</div>
                <div className="how-step-desc">{s.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="divider" />

      {/* ── COMPARISON ── */}
      <section className="section" id="compare">
        <div className="container">
          <div className="section-label">Comparison</div>
          <h2 className="section-title">Why not just use<br />what you already have?</h2>
          <p className="section-sub">
            Native tools are fragmented. Snag unifies screenshots, downloads, clipboard, and snippets in one floating surface without breaking your flow.
          </p>
          <div className="comparison-wrapper">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Feature</th>
                  <th className="highlight">Snag</th>
                  <th>macOS Finder</th>
                  <th>Alfred / Raycast</th>
                  <th>Clipy / Pasta</th>
                </tr>
              </thead>
              <tbody>
                {[
                  ["Screenshot access (instant)", "✓", "✗", "~", "✗"],
                  ["Downloads panel",             "✓", "✗", "~", "✗"],
                  ["Clipboard history",           "✓", "✗", "✓", "✓"],
                  ["Pinned snippets",             "✓", "✗", "✓", "~"],
                  ["Drag-and-drop out",           "✓", "✓", "✗", "✗"],
                  ["Always visible on screen",   "✓", "✗", "✗", "✗"],
                  ["Cross-platform (Win/Lin/Mac)","✓", "✗", "✗", "✗"],
                  ["Hardware-locked licensing",  "✓", "N/A","✗", "✗"],
                  ["< 80MB RAM",                 "✓", "~", "~", "✓"],
                  ["One-command install",         "✓", "N/A","~", "~"],
                ].map(([feature, snag, finder, alfred, clipy], i) => (
                  <tr key={i}>
                    <td className="feature-name">{feature}</td>
                    <td className="highlight-col">
                      <span className={snag === "✓" ? "check" : snag === "✗" ? "cross" : "partial"}>{snag}</span>
                    </td>
                    <td><span className={finder === "✓" ? "check" : finder === "✗" ? "cross" : "partial"}>{finder}</span></td>
                    <td><span className={alfred === "✓" ? "check" : alfred === "✗" ? "cross" : "partial"}>{alfred}</span></td>
                    <td><span className={clipy === "✓" ? "check" : clipy === "✗" ? "cross" : "partial"}>{clipy}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <div className="divider" />

      {/* ── PRICING ── */}
      <section className="section" id="pricing">
        <div className="container" style={{ textAlign: "center" }}>
          <div className="section-label">Pricing</div>
          <h2 className="section-title">Own it. Or try it first.</h2>
          <p className="section-sub" style={{ margin: "0 auto" }}>
            No subscriptions required. Lifetime is the best value — one payment, forever yours.
          </p>
          <div className="pricing-grid">
            {/* Monthly */}
            <div className="pricing-card">
              <div className="pricing-plan">Monthly</div>
              <div className="pricing-amount">$0.99</div>
              <div className="pricing-period">per month</div>
              <div className="pricing-inr">₹29 / month</div>
              <ul className="pricing-features">
                <li>All 4 tabs unlocked</li>
                <li>Cross-platform access</li>
                <li>Regular updates</li>
              </ul>
              <a href="#" className="btn btn-ghost" style={{ width: "100%", justifyContent: "center" }}>Start Monthly</a>
            </div>
            {/* Lifetime */}
            <div className="pricing-card featured">
              <div className="pricing-badge">Best Value</div>
              <div className="pricing-plan">Lifetime</div>
              <div className="pricing-amount">$14.99</div>
              <div className="pricing-period">one-time</div>
              <div className="pricing-inr">₹899 — pay once, own forever</div>
              <ul className="pricing-features">
                <li>Everything in Monthly</li>
                <li>All future updates included</li>
                <li>Priority support</li>
                <li>Hardware-locked to 1 device</li>
              </ul>
              <a href="#" className="btn btn-white" style={{ width: "100%", justifyContent: "center" }}>Buy Lifetime →</a>
            </div>
            {/* Yearly */}
            <div className="pricing-card">
              <div className="pricing-plan">Yearly</div>
              <div className="pricing-amount">$3.99</div>
              <div className="pricing-period">per year</div>
              <div className="pricing-inr">₹199 / year · save 66%</div>
              <ul className="pricing-features">
                <li>All 4 tabs unlocked</li>
                <li>Cross-platform access</li>
                <li>Regular updates</li>
              </ul>
              <a href="#" className="btn btn-ghost" style={{ width: "100%", justifyContent: "center" }}>Start Yearly</a>
            </div>
          </div>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer>
        <div className="container footer">
          <span>© {new Date().getFullYear()} Snag. Built for focus.</span>
          <span>macOS · Windows · Linux</span>
          <span>Powered by Next.js &amp; Supabase</span>
        </div>
      </footer>
    </>
  );
}
