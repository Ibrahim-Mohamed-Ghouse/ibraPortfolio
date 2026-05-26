from __future__ import annotations

import html
from datetime import datetime
from pathlib import Path

import streamlit as st

from portfolio_content import (
    CERTIFICATIONS,
    EDUCATION,
    EXPERIENCE,
    FOCUS_AREAS,
    HERO_STATS,
    PROFILE,
    PROJECTS,
    SKILL_GROUPS,
    SUMMARY_PARAGRAPHS,
)

BASE_DIR = Path(__file__).resolve().parent
BASE_CSS_PATH = BASE_DIR / "static" / "css" / "site.css"
IMPROVED_CSS_PATH = BASE_DIR / "static" / "css" / "site_improved.css"
CV_STATIC_URL = "/app/static/docs/ibrahim-mohamed-ghouse-cv.pdf"
NAV_ITEMS = [
    ("experience", "Experience"),
    ("projects", "Projects"),
    ("credentials", "Credentials"),
    ("contact", "Contact"),
]


@st.cache_data(show_spinner=False)
def _read_css(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_css() -> None:
    st.markdown(f"<style>{_read_css(BASE_CSS_PATH)}</style>", unsafe_allow_html=True)
    st.markdown(f"<style>{_read_css(IMPROVED_CSS_PATH)}</style>", unsafe_allow_html=True)


def inject_scroll_behavior() -> None:
    st.html(
        """
        <script>
        (() => {
          const bindPortfolioEffects = () => {
            const root = document.querySelector(".portfolio-root");
            if (!root || root.dataset.effectsBound === "true") {
              return;
            }

            const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
            const revealItems = Array.from(root.querySelectorAll(".reveal"));
            const navLinks = Array.from(root.querySelectorAll('.site-nav a[href^="#"]'));
            const sections = Array.from(root.querySelectorAll("main section[id]"));

            const setActiveLink = (id) => {
              navLinks.forEach((link) => {
                const active = link.getAttribute("href") === `#${id}`;
                link.classList.toggle("is-active", active);
                if (active) {
                  link.setAttribute("aria-current", "page");
                } else {
                  link.removeAttribute("aria-current");
                }
              });
            };

            if (prefersReducedMotion) {
              revealItems.forEach((item) => item.classList.add("is-visible"));
            } else {
              root.classList.add("motion-ready");
              const revealObserver = new IntersectionObserver(
                (entries, observer) => {
                  entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                      entry.target.classList.add("is-visible");
                      observer.unobserve(entry.target);
                    }
                  });
                },
                {
                  threshold: 0.16,
                  rootMargin: "0px 0px -12% 0px",
                }
              );

              revealItems.forEach((item) => revealObserver.observe(item));
            }

            if (sections.length && navLinks.length) {
              let activeFrame = null;
              const scrollContainer = document.querySelector('[data-testid="stAppViewContainer"]');

              const updateActiveSection = () => {
                activeFrame = null;
                const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
                const targetLine = viewportHeight * 0.34;

                let activeId = sections[0].id;
                let bestDistance = Number.POSITIVE_INFINITY;

                sections.forEach((section) => {
                  const rect = section.getBoundingClientRect();
                  const isVisible = rect.bottom > 0 && rect.top < viewportHeight;

                  if (!isVisible) {
                    return;
                  }

                  const nearestPoint = Math.min(Math.max(targetLine, rect.top), rect.bottom);
                  const distance = Math.abs(nearestPoint - targetLine);

                  if (distance < bestDistance) {
                    bestDistance = distance;
                    activeId = section.id;
                  }
                });

                setActiveLink(activeId);
              };

              const scheduleActiveUpdate = () => {
                if (activeFrame !== null) {
                  return;
                }

                activeFrame = window.requestAnimationFrame(updateActiveSection);
              };

              const sectionObserver = new IntersectionObserver(
                () => {
                  scheduleActiveUpdate();
                },
                {
                  threshold: [0, 0.2, 0.45, 0.7, 0.95],
                  rootMargin: "-22% 0px -48% 0px",
                }
              );

              sections.forEach((section) => sectionObserver.observe(section));

              if (scrollContainer) {
                scrollContainer.addEventListener("scroll", scheduleActiveUpdate, { passive: true });
              }

              window.addEventListener("scroll", scheduleActiveUpdate, { passive: true });
              window.addEventListener("resize", scheduleActiveUpdate);
              scheduleActiveUpdate();
            }

            root.dataset.effectsBound = "true";
          };

          if (!window.__portfolioMotionBootstrapped) {
            window.__portfolioMotionBootstrapped = true;
            const observer = new MutationObserver(() => bindPortfolioEffects());
            observer.observe(document.body, { childList: true, subtree: true });
          }

          bindPortfolioEffects();
          requestAnimationFrame(() => bindPortfolioEffects());
        })();
        </script>
        """,
        unsafe_allow_javascript=True,
    )


def _stagger(index: int) -> str:
    return f"stagger-{(index % 5) + 1}"


def _list(items: list[str], list_class: str) -> str:
    points = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ul class="{list_class}">{points}</ul>'


def _nav() -> str:
    return "".join(f'<a href="#{anchor}">{html.escape(label)}</a>' for anchor, label in NAV_ITEMS)


def _hero_name() -> str:
    full_name = f"{PROFILE['first_name']} {PROFILE['middle_name']} {PROFILE['last_name']}"
    return (
        '<h1 class="hero-name-editorial">'
        f"<span>{html.escape(full_name)}</span>"
        "<em>Aspiring Solution Architect.</em>"
        "</h1>"
    )


def _meta_pills() -> str:
    items = [
        html.escape(PROFILE["location"]),
        f'<a href="tel:{html.escape(PROFILE["phone_href"])}">{html.escape(PROFILE["phone_display"])}</a>',
        f'<a href="mailto:{html.escape(PROFILE["email"])}">{html.escape(PROFILE["email"])}</a>',
    ]
    return "".join(f"<li>{item}</li>" for item in items)


def _stats() -> str:
    cards = []
    for index, item in enumerate(HERO_STATS):
        cards.append(
            f"""
            <article class="stat-card">
              <h3>{html.escape(item["value"])}</h3>
              <p>{html.escape(item["label"])}</p>
            </article>
            """
        )
    return "".join(cards)


def _focus_chips() -> str:
    chips = []
    for index, item in enumerate(FOCUS_AREAS):
        chips.append(f'<span class="chip">{html.escape(item)}</span>')
    return "".join(chips)


def _certifications() -> str:
    cards = []
    for index, item in enumerate(CERTIFICATIONS):
        status_markup = ""
        if item.get("status"):
            status_markup = f'<span class="cert-status">{html.escape(item["status"])}</span>'
        cards.append(
            f"""
            <article class="cert-card">
              <div class="cert-topline">
                <p class="cert-code">{html.escape(item["code"])}</p>
                {status_markup}
              </div>
              <h3 class="cert-name">{html.escape(item["name"])}</h3>
              <p class="cert-issuer">{html.escape(item["issuer"])}</p>
            </article>
            """
        )
    return "".join(cards)


def _experiences() -> str:
    rows = []
    for index, item in enumerate(EXPERIENCE):
        rows.append(
            f"""
            <article class="experience-row">
              <div class="experience-meta">
                <p class="experience-period">{html.escape(item["period"])}</p>
                <p class="experience-org">{html.escape(item["company"])}</p>
              </div>
              <div class="experience-body">
                <h3>{html.escape(item["role"])}</h3>
                <p class="experience-overview">{html.escape(item["overview"])}</p>
                {_list(item["bullets"], "bullet-list")}
              </div>
            </article>
            """
        )
    return "".join(rows)


def _projects() -> str:
    cards = []
    for index, item in enumerate(PROJECTS):
        tags = "".join(f'<span class="project-tag">{html.escape(tag)}</span>' for tag in item["stack"])
        cards.append(
            f"""
            <article class="project-card">
              <p class="project-index">{index + 1:03d}</p>
              <h3 class="project-name">{html.escape(item["name"])}</h3>
              <p class="project-body">{html.escape(item["summary"])}</p>
              <div class="project-tags">{tags}</div>
            </article>
            """
        )
    return "".join(cards)


def _education() -> str:
    cards = []
    for index, item in enumerate(EDUCATION):
        badge = ""
        if item.get("badge"):
            badge = f'<p class="education-badge">{html.escape(item["badge"])}</p>'
        cards.append(
            f"""
            <article class="education-card">
              <div class="education-years">{html.escape(item["period"])}</div>
              <div class="education-content">
                {badge}
                <h3>{html.escape(item["degree"])}</h3>
                <p class="education-school">{html.escape(item["school"])}</p>
                <p class="education-detail">{html.escape(item["details"])}</p>
              </div>
            </article>
            """
        )
    return "".join(cards)


def _skill_groups() -> str:
    rows = []
    for index, group in enumerate(SKILL_GROUPS):
        pills = "".join(f'<span class="skill-pill">{html.escape(item)}</span>' for item in group["items"])
        rows.append(
            f"""
            <article class="skill-row">
              <p class="skill-category">{html.escape(group["category"])}</p>
              <div class="skill-items">{pills}</div>
            </article>
            """
        )
    return "".join(rows)


def _contact_rows() -> str:
    rows = [
        ("Email", PROFILE["email"], f'mailto:{PROFILE["email"]}'),
        ("Phone", PROFILE["phone_display"], f'tel:{PROFILE["phone_href"]}'),
        ("Location", PROFILE["location"], ""),
    ]
    if PROFILE.get("linkedin_url"):
        rows.append(("LinkedIn", "View profile", PROFILE["linkedin_url"]))
    if PROFILE.get("github_url"):
        rows.append(("GitHub", "View repositories", PROFILE["github_url"]))

    rendered = []
    for index, (label, value, href) in enumerate(rows):
        value_markup = html.escape(value)
        if href:
            value_markup = f'<a class="contact-value" href="{html.escape(href)}">{value_markup}</a>'
        else:
            value_markup = f'<span class="contact-value">{value_markup}</span>'
        rendered.append(
            f"""
            <div class="contact-row">
              <span class="contact-label">{html.escape(label)}</span>
              {value_markup}
            </div>
            """
        )
    return "".join(rendered)


def render_hero(cv_href: str) -> str:
    return f"""
    <section class="hero" id="top">
      <div class="hero-grid hero-grid-editorial">
        <div class="hero-copy hero-copy-editorial reveal reveal-left is-visible">
          <p class="hero-eyebrow">{html.escape(PROFILE["hero_eyebrow"])}</p>
          {_hero_name()}
          <p class="hero-bio">{html.escape(PROFILE["headline"])}</p>
          <p class="hero-summary">{html.escape(PROFILE["subheadline"])}</p>

          <div class="hero-actions reveal reveal-up stagger-2">
            <a class="button button-primary" href="#projects">View Projects</a>
            <a class="hero-text-link" href="mailto:{html.escape(PROFILE["email"])}">Get in touch</a>
            <a class="hero-text-link" href="{cv_href}" download="Ibrahim-Mohamed-Ghouse-CV.pdf">Download CV</a>
          </div>

        </div>

        <aside class="hero-panel reveal reveal-right is-visible" aria-label="Current positioning">
          <h2>{html.escape(PROFILE["availability"])}</h2>
          <p>{html.escape(PROFILE["summary"])}</p>

          <div class="hero-panel-block reveal reveal-up stagger-4">
            <div class="chip-wrap" aria-label="Focus areas">
              {_focus_chips()}
            </div>
          </div>
        </aside>
      </div>
    </section>
    """


def render_experience_section() -> str:
    return f"""
    <section class="section section-tight" id="experience">
      <div class="section-heading reveal reveal-up">
        <h2>Research, positioning, and hands-on delivery across client-facing and applied AI work.</h2>
      </div>
      <div class="experience-list experience-list-compact">
        {_experiences()}
      </div>
    </section>
    """


def render_projects_section() -> str:
    return f"""
    <section class="section section-tight section-featured" id="projects">
      <div class="project-rail-header reveal reveal-up">
        <div class="section-heading section-heading-compact">
          <h2>Selected builds across telemetry analytics, multi-agent AI, and embedded computer vision.</h2>
        </div>
        <p class="project-rail-hint">
          Swipe or scroll sideways to explore the work.
        </p>
      </div>
      <div class="project-rail-shell">
        <div class="project-rail" aria-label="Project gallery">
          {_projects()}
        </div>
      </div>
    </section>
    """


def render_credentials_section() -> str:
    return f"""
    <section class="section section-tight" id="credentials">
      <div class="section-heading reveal reveal-up">
        <h2>Education, certifications, and technical strengths supporting practical delivery.</h2>
      </div>
      <div class="credentials-layout">
        <div class="credentials-column">
          <div class="credentials-subheading">
            <p class="credentials-label">Education</p>
          </div>
          <div class="education-stack education-stack-compact">
            {_education()}
          </div>
        </div>
        <div class="credentials-column">
          <div class="credentials-subheading">
            <p class="credentials-label">Certifications</p>
          </div>
          <div class="cert-stack cert-stack-compact">
            {_certifications()}
          </div>
        </div>
      </div>
      <div class="skills-cluster">
        <div class="credentials-subheading">
          <p class="credentials-label">Skills</p>
        </div>
        <div class="skills-list skills-list-compact">
          {_skill_groups()}
        </div>
      </div>
    </section>
    """


def render_contact_section(cv_href: str) -> str:
    return f"""
    <section class="section contact-section" id="contact">
      <div class="contact-card reveal reveal-up">
        <div class="contact-copy">
          <h2>Let's work on something meaningful.</h2>
          <p>
            I am looking for opportunities where I can contribute across technical discovery,
            solution thinking, and applied AI work.
          </p>
          <div class="contact-actions">
            <a class="button button-primary" href="mailto:{html.escape(PROFILE["email"])}">Start a conversation</a>
            <a class="button button-secondary" href="{cv_href}" download="Ibrahim-Mohamed-Ghouse-CV.pdf">Download CV</a>
          </div>
        </div>
        <div class="contact-info-grid">
          {_contact_rows()}
        </div>
      </div>
    </section>
    """


def render_footer() -> str:
    return f"""
    <footer class="site-footer">
      <div class="footer-inner">
        <p>{html.escape(PROFILE["name"])} <span>/</span> {datetime.now().year}</p>
        <div class="footer-contact">
          <span>{html.escape(PROFILE["location"])}</span>
          <a href="tel:{html.escape(PROFILE["phone_href"])}">{html.escape(PROFILE["phone_display"])}</a>
          <a href="mailto:{html.escape(PROFILE["email"])}">{html.escape(PROFILE["email"])}</a>
        </div>
      </div>
    </footer>
    """


def build_page(cv_href: str) -> str:
    return f"""
    <div class="portfolio-root portfolio-improved">
      <header class="site-header reveal reveal-down is-visible">
        <div class="header-inner">
          <a class="brand" href="#top" aria-label="Go to top of page">
            <span class="brand-mark" aria-hidden="true">IM</span>
            <span class="brand-text">
              <strong>{html.escape(PROFILE["name"])}</strong>
              <span>Portfolio</span>
            </span>
          </a>
          <nav class="site-nav" aria-label="Primary">
            {_nav()}
          </nav>
        </div>
      </header>

      <main id="main-content">
        {render_hero(CV_STATIC_URL)}
        {render_experience_section()}
        {render_projects_section()}
        {render_credentials_section()}
        {render_contact_section(cv_href)}
      </main>

      {render_footer()}
    </div>
    """


def main() -> None:
    st.set_page_config(
        page_title=f"{PROFILE['name']} | Portfolio",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    load_css()
    st.html(build_page(CV_STATIC_URL), width="stretch")
    inject_scroll_behavior()


if __name__ == "__main__":
    main()
