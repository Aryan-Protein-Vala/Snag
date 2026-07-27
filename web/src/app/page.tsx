import styles from "./page.module.css";

export default function Home() {
  return (
    <main className={styles.main}>
      {/* Hero Section */}
      <section className={`${styles.hero} animate-fade-in`}>
        <h1 className={styles.title}>Your workflow, unhindered.</h1>
        <p className={styles.subtitle}>
          Snag is a premium, lightweight, frameless floating widget for macOS, Windows, and Linux. 
          Rapidly access transient files, screenshots, clipboard history, and saved snippets without breaking focus.
        </p>
        <div className={styles.ctaContainer}>
          <a href="#pricing" className="btn-primary">Get Snag</a>
          <a href="#features" className="btn-secondary">Explore Features</a>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className={`${styles.pricingSection} animate-fade-in delay-2`}>
        <h2 className={styles.sectionTitle}>Simple Pricing</h2>
        <div className={styles.pricingGrid}>
          
          {/* Monthly Plan */}
          <div className={`glass-card ${styles.pricingCard}`}>
            <div className={styles.planName}>Monthly</div>
            <div className={styles.planPrice}>$0.99</div>
            <div className={styles.planDuration}>per month</div>
            <ul className={styles.planFeatures}>
              <li>Full access to all features</li>
              <li>Cross-platform support</li>
              <li>Regular updates</li>
            </ul>
            <button className="btn-secondary" style={{ width: '100%' }}>Subscribe</button>
          </div>

          {/* Lifetime Plan (Decoy Effect - Most Popular) */}
          <div className={`glass-card ${styles.pricingCard} ${styles.popularCard}`}>
            <div className={styles.planName}>Lifetime</div>
            <div className={styles.planPrice}>$14.99</div>
            <div className={styles.planDuration}>one-time payment</div>
            <ul className={styles.planFeatures}>
              <li>Pay once, own forever</li>
              <li>Priority support</li>
              <li>All future updates included</li>
            </ul>
            <button className="btn-primary" style={{ width: '100%' }}>Buy Lifetime</button>
          </div>

          {/* Yearly Plan */}
          <div className={`glass-card ${styles.pricingCard}`}>
            <div className={styles.planName}>Yearly</div>
            <div className={styles.planPrice}>$3.99</div>
            <div className={styles.planDuration}>per year</div>
            <ul className={styles.planFeatures}>
              <li>Save 66% vs monthly</li>
              <li>Full access to all features</li>
              <li>Regular updates</li>
            </ul>
            <button className="btn-secondary" style={{ width: '100%' }}>Subscribe</button>
          </div>

        </div>
      </section>

      <footer className={styles.footer}>
        © {new Date().getFullYear()} Snag. Designed for maximum productivity.
      </footer>
    </main>
  );
}
