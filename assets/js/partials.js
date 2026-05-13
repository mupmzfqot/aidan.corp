// Inject shared nav/footer so we don't duplicate markup across pages.
// data-base="" for root, "../" for one level deep, "../../" for two levels deep.

(function () {
  const root = document.documentElement;
  const base = root.dataset.base || '';
  const active = root.dataset.page || '';

  const navHTML = `
    <nav class="nav" aria-label="Primary">
      <div class="nav-inner">
        <a class="nav-brand" href="${base || './'}" aria-label="Aidan Group of Companies">
          <img src="${base}assets/images/logo-dark.png" alt="Aidan" />
        </a>
        <ul class="nav-links">
          <li><a href="${base || './'}" data-key="home">Home</a></li>
          <li><a href="${base}group/" data-key="group">Group</a></li>
          <li><a href="${base}ventures/" data-key="ventures">Ventures</a></li>
          <li class="nav-dropdown">
            <a href="#" data-key="people" aria-haspopup="true">People</a>
            <ul class="nav-dropdown-menu">
              <li><a href="${base}people/culture/" data-key="culture">Culture</a></li>
              <li><a href="${base}people/career/" data-key="career">Career</a></li>
            </ul>
          </li>
          <li><a href="${base}contact/" class="nav-cta" data-key="contact">
            Contact
            <svg class="ti" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </a></li>
        </ul>
        <button class="nav-burger" aria-label="Menu" aria-expanded="false">
          <svg class="ti" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
      </div>
    </nav>
  `;

  const footerHTML = `
    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <div>
            <div class="footer-brand">
              <img src="${base}assets/images/logo-white.png" alt="Aidan" />
            </div>
            <p style="color: rgba(247,239,229,0.7); max-width: 360px;">
              A strategic group of companies in Technology, Education, and Marketing — building tomorrow, together.
            </p>
            <div class="social-row mt-4">
              <a href="https://www.facebook.com/aidangroupofcompanies" target="_blank" rel="noopener" aria-label="Facebook">
                <svg class="ti" viewBox="0 0 24 24"><path d="M7 10v4h3v7h4v-7h3l1-4h-4V8a1 1 0 0 1 1-1h3V3h-3a5 5 0 0 0-5 5v2H7"/></svg>
              </a>
              <a href="mailto:contact@aidan.my" aria-label="Email">
                <svg class="ti" viewBox="0 0 24 24"><path d="M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM3 7l9 6 9-6"/></svg>
              </a>
              <a href="tel:+60341430572" aria-label="Phone">
                <svg class="ti" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5l1.5-2.5 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>
              </a>
            </div>
          </div>
          <div>
            <h5>Company</h5>
            <ul>
              <li><a href="${base}group/">Group</a></li>
              <li><a href="${base}ventures/">Ventures</a></li>
              <li><a href="${base}contact/">Contact</a></li>
            </ul>
          </div>
          <div>
            <h5>People</h5>
            <ul>
              <li><a href="${base}people/culture/">Culture</a></li>
              <li><a href="${base}people/career/">Career</a></li>
              <li><a href="mailto:career@aidan.my">career@aidan.my</a></li>
            </ul>
          </div>
          <div>
            <h5>Headquarter</h5>
            <ul>
              <li style="color: rgba(247,239,229,0.7); font-size: .9rem; line-height: 1.6;">
                100-1, 102-1, 102-2 Jalan 2/23A,<br/>
                Taman Danau Kota,<br/>
                53300 Setapak,<br/>
                Kuala Lumpur, Malaysia
              </li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <span>&copy; ${new Date().getFullYear()} Aidan Group of Companies. All Rights Reserved.</span>
          <span>Building tomorrow, together.</span>
        </div>
      </div>
    </footer>
  `;

  const navMount = document.getElementById('nav-mount');
  const footerMount = document.getElementById('footer-mount');
  if (navMount) navMount.outerHTML = navHTML;
  if (footerMount) footerMount.outerHTML = footerHTML;

  // Mark active link
  if (active) {
    document.querySelectorAll(`.nav-links a[data-key="${active}"]`).forEach(a => a.classList.add('is-active'));
    // Also mark parent "People" if culture/career active
    if (active === 'culture' || active === 'career') {
      document.querySelectorAll('.nav-links a[data-key="people"]').forEach(a => a.classList.add('is-active'));
    }
  }
})();
