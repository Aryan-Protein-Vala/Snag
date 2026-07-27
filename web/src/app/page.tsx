export default function Home() {
  return (
    <>
      {/* ──────────── NAV ──────────── */}
      <nav className="nav">
        <div className="container nav-inner">
          <div className="nav-logo">snag<span>.</span></div>
          <ul className="nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#how">How it works</a></li>
            <li><a href="#compare">Compare</a></li>
            <li><a href="#pricing">Pricing</a></li>
          </ul>
          <a href="#pricing" className="btn btn-ghost" style={{ padding: '9px 18px', fontSize: '13px' }}>
            Get Snag
          </a>
        </div>
      </nav>

      {/* ──────────── HERO ──────────── */}
      <section className="hero">
        <div className="hero-glow" />
        <div className="container" style={{ position: 'relative', zIndex: 1 }}>

          <div className="hero-eyebrow anim d1">
            <svg width="8" height="8" viewBox="0 0 8 8" fill="none">
              <circle cx="4" cy="4" r="4" fill="#5ECC7B" />
            </svg>
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
            <a href="#pricing" className="btn btn-white">
              Get Snag — from $0.99
            </a>
            <a href="#how" className="btn btn-ghost">
              See how it works
            </a>
          </div>

          <div className="hero-platforms anim d5">
            <span>Available on</span>
            <span className="platform-badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
              </svg>
              macOS
            </span>
            <span className="platform-badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
              </svg>
              Windows
            </span>
            <span className="platform-badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              Linux
            </span>
          </div>
        </div>
      </section>

      {/* ──────────── WIDGET PREVIEW ──────────── */}
      <section className="preview-section">
        <div className="widget-mockup">
          <div className="widget-top-bar">
            <span className="widget-logo">SNAG</span>
            <span className="widget-close">✕</span>
          </div>
          <div className="widget-tabs">
            <span className="widget-tab active">Scrn</span>
            <span className="widget-tab">Down</span>
            <span className="widget-tab">Clip</span>
            <span className="widget-tab">Snip</span>
          </div>
          {[
            { icon: '🖼', name: 'Screenshot 2026-07-27.png', time: '2m ago' },
            { icon: '🖼', name: 'Dashboard-mockup.png', time: '18m ago' },
            { icon: '🖼', name: 'UI-review-final.png', time: '1h ago' },
            { icon: '🖼', name: 'Snag-hero-dark.png', time: '3h ago' },
            { icon: '🖼', name: 'cover-photo.jpg', time: '5h ago' },
          ].map((item, i) => (
            <div className="widget-item" key={i}>
              <span className="widget-item-icon">{item.icon}</span>
              <span className="widget-item-text">{item.name}</span>
              <span className="widget-item-sub">{item.time}</span>
            </div>
          ))}
        </div>
      </section>

      <div className="divider" />

      {/* ──────────── FEATURES ──────────── */}
      <section className="section" id="features">
        <div className="container">
          <div className="section-label">Core Features</div>
          <h2 className="section-title">Everything you need.<br />Nothing you don&apos;t.</h2>

          <div className="features-grid" style={{ marginTop: '48px' }}>
            {[
              {
                icon: '🖼',
                title: 'Screenshot Watcher',
                desc: 'Automatically surfaces your last 10 screenshots from your Desktop & Pictures/Screenshots folder the moment they&apos;re saved. Drag directly into Slack, Notion, or anywhere.',
              },
              {
                icon: '⬇',
                title: 'Downloads Inbox',
                desc: 'Your 10 most recent downloads, always one click away. Double-click to open. Hover to reveal in Explorer. Drag into any window.',
              },
              {
                icon: '📋',
                title: 'Clipboard History',
                desc: 'Persists your last 15 copied text snippets — even after restarts. Click any entry to instantly re-copy. No clutter, no loops.',
              },
              {
                icon: '📌',
                title: 'Pinned Snippets',
                desc: 'Save boilerplate text, code blocks, credentials, or email templates permanently. Press Enter to add. Always there when you need them.',
              },
              {
                icon: '🔒',
                title: 'Hardware-Locked License',
                desc: 'Each license binds to one machine UUID. Prevents key sharing without a heavy client. Backend verified via Supabase on first activation.',
              },
              {
                icon: '⚡',
                title: 'Instant & Always On',
                desc: 'The widget is frameless, stays on top, and is positioned out of your way. Uses < 80MB RAM. Launch it with a global shortcut in seconds.',
              },
            ].map((f, i) => (
              <div className="feature-card" key={i}>
                <span className="feature-icon">{f.icon}</span>
                <div className="feature-title">{f.title}</div>
                <div className="feature-desc">{f.desc.replace(/&apos;/g, "'")}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="divider" />

      {/* ──────────── HOW IT WORKS ──────────── */}
      <section className="section" id="how">
        <div className="container">
          <div className="section-label">How it works</div>
          <h2 className="section-title">Up and running<br />in 60 seconds.</h2>

          <div className="how-grid">
            {[
              {
                icon: '⬇',
                title: 'Install with one command',
                desc: 'Run `curl -fsSL snag.app/install.sh | bash` in your terminal. The script handles everything — download, extract, and launch.',
              },
              {
                icon: '🔑',
                title: 'Enter your license key',
                desc: 'On first launch, paste your 16-character `SNAG-XXXX-XXXX-XXXX` key. It binds to your machine UUID. Done.',
              },
              {
                icon: '🪟',
                title: 'Widget appears instantly',
                desc: 'Snag floats in the bottom-right corner. Frameless, always-on-top. Click the tabs or drag files out immediately.',
              },
              {
                icon: '✨',
                title: 'Never leave your flow',
                desc: 'Use the global shortcut to summon and dismiss it. Your clipboard history and snippets persist across restarts.',
              },
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

      {/* ──────────── COMPARISON ──────────── */}
      <section className="section" id="compare">
        <div className="container">
          <div className="section-label">Comparison</div>
          <h2 className="section-title">Why not just use<br />what you already have?</h2>
          <p className="section-sub">
            Native tools are fragmented. Switching between Finder, your Downloads folder, and clipboard managers breaks flow. Snag unifies everything in one place.
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
                  ['Screenshot access (instant)', '✓', '✗', '~', '✗'],
                  ['Downloads panel', '✓', '✗', '~', '✗'],
                  ['Clipboard history', '✓', '✗', '✓', '✓'],
                  ['Pinned snippets', '✓', '✗', '✓', '~'],
                  ['Drag-and-drop out', '✓', '✓', '✗', '✗'],
                  ['Always visible on screen', '✓', '✗', '✗', '✗'],
                  ['Cross-platform (Win/Lin/Mac)', '✓', '✗', '✗', '✗'],
                  ['Hardware-locked licensing', '✓', 'N/A', '✗', '✗'],
                  ['< 80MB RAM', '✓', '~', '~', '✓'],
                  ['One-click install', '✓', 'N/A', '~', '~'],
                ].map(([feature, snag, finder, alfred, clipy], i) => (
                  <tr key={i}>
                    <td className="feature-name">{feature}</td>
                    <td className="highlight-col">
                      <span className={snag === '✓' ? 'check' : snag === '✗' ? 'cross' : 'partial'}>{snag}</span>
                    </td>
                    <td><span className={finder === '✓' ? 'check' : finder === '✗' ? 'cross' : 'partial'}>{finder}</span></td>
                    <td><span className={alfred === '✓' ? 'check' : alfred === '✗' ? 'cross' : 'partial'}>{alfred}</span></td>
                    <td><span className={clipy === '✓' ? 'check' : clipy === '✗' ? 'cross' : 'partial'}>{clipy}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <div className="divider" />

      {/* ──────────── PRICING ──────────── */}
      <section className="section" id="pricing">
        <div className="container" style={{ textAlign: 'center' }}>
          <div className="section-label">Pricing</div>
          <h2 className="section-title">Own it. Or try it first.</h2>
          <p className="section-sub" style={{ margin: '0 auto 0' }}>
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
              <a href="#" className="btn btn-ghost" style={{ width: '100%', justifyContent: 'center' }}>
                Start Monthly
              </a>
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
              <a href="#" className="btn btn-white" style={{ width: '100%', justifyContent: 'center' }}>
                Buy Lifetime →
              </a>
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
              <a href="#" className="btn btn-ghost" style={{ width: '100%', justifyContent: 'center' }}>
                Start Yearly
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ──────────── FOOTER ──────────── */}
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
