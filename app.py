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
CSS_PATH = BASE_DIR / "static" / "css" / "site.css"
CV_STATIC_URL = "/app/static/docs/ibrahim-mohamed-ghouse-cv.pdf"
NAV_ITEMS = [
    ("about", "About"),
    ("experience", "Experience"),
    ("projects", "Projects"),
    ("education", "Education"),
    ("skills", "Skills"),
    ("contact", "Contact"),
]


@st.cache_data(show_spinner=False)
def read_css_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_css() -> None:
    st.markdown(f"<style>{read_css_text(CSS_PATH)}</style>", unsafe_allow_html=True)


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


def stagger_class(index: int) -> str:
    return f"stagger-{(index % 5) + 1}"


def render_list(items: list[str], list_class: str) -> str:
    points = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ul class="{list_class}">{points}</ul>'


def render_nav() -> str:
    return "".join(f'<a href="#{anchor}">{html.escape(label)}</a>' for anchor, label in NAV_ITEMS)


def render_hero_name() -> str:
    return (
        '<h1 class="hero-name-editorial">'
        f"<span>{html.escape(PROFILE['first_name'])}</span>"
        f"<em>{html.escape(PROFILE['middle_name'])}</em>"
        f"<span>{html.escape(PROFILE['last_name'])}</span>"
        "</h1>"
    )


def render_meta_pills() -> str:
    items = [
        html.escape(PROFILE["location"]),
        f'<a href="tel:{html.escape(PROFILE["phone_href"])}">{html.escape(PROFILE["phone_display"])}</a>',
        f'<a href="mailto:{html.escape(PROFILE["email"])}">{html.escape(PROFILE["email"])}</a>',
    ]
    return "".join(f"<li>{item}</li>" for item in items)


def render_stats() -> str:
    cards = []
    for index, item in enumerate(HERO_STATS):
        cards.append(
            f"""
            <article class="stat-card reveal reveal-scale {stagger_class(index)}">
              <h3>{html.escape(item["value"])}</h3>
              <p>{html.escape(item["label"])}</p>
            </article>
            """
        )
    return "".join(cards)


def render_focus_chips(items: list[str]) -> str:
    chips = []
    for index, item in enumerate(items):
        chips.append(f'<span class="chip reveal reveal-scale {stagger_class(index)}">{html.escape(item)}</span>')
    return "".join(chips)


def render_certifications() -> str:
    cards = []
    for index, item in enumerate(CERTIFICATIONS):
        status_markup = ""
        if item.get("status"):
            status_markup = f'<span class="cert-status">{html.escape(item["status"])}</span>'
        cards.append(
            f"""
            <article class="cert-card reveal reveal-up {stagger_class(index)}">
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


def render_experiences() -> str:
    rows = []
    for index, item in enumerate(EXPERIENCE):
        rows.append(
            f"""
            <article class="experience-row reveal reveal-up {stagger_class(index)}">
              <div class="experience-meta">
                <p class="experience-period">{html.escape(item["period"])}</p>
                <p class="experience-org">{html.escape(item["company"])}</p>
              </div>
              <div class="experience-body">
                <h3>{html.escape(item["role"])}</h3>
                <p class="experience-overview">{html.escape(item["overview"])}</p>
                {render_list(item["bullets"], "bullet-list")}
              </div>
            </article>
            """
        )
    return "".join(rows)


def render_projects() -> str:
    cards = []
    for index, item in enumerate(PROJECTS):
        if item.get("placeholder"):
            cards.append(
                f"""
                <article class="project-card project-card-placeholder reveal reveal-scale {stagger_class(index)}">
                  <div class="project-placeholder-inner">
                    <p class="project-index">{html.escape(item["eyebrow"])}</p>
                    <h3 class="project-name">{html.escape(item["name"])}</h3>
                  </div>
                </article>
                """
            )
            continue

        tags = "".join(f'<span class="project-tag">{html.escape(tag)}</span>' for tag in item["stack"])
        cards.append(
            f"""
            <article class="project-card reveal reveal-up {stagger_class(index)}">
              <p class="project-index">{index + 1:03d}</p>
              <h3 class="project-name">{html.escape(item["name"])}</h3>
              <p class="project-body">{html.escape(item["summary"])}</p>
              <div class="project-tags">{tags}</div>
            </article>
            """
        )
    return "".join(cards)


def render_education() -> str:
    cards = []
    for index, item in enumerate(EDUCATION):
        badge = ""
        if item.get("badge"):
            badge = f'<p class="education-badge">{html.escape(item["badge"])}</p>'

        cards.append(
            f"""
            <article class="education-card reveal reveal-up {stagger_class(index)}">
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


def render_skill_groups() -> str:
    rows = []
    for index, group in enumerate(SKILL_GROUPS):
        pills = "".join(f'<span class="skill-pill">{html.escape(item)}</span>' for item in group["items"])
        rows.append(
            f"""
            <article class="skill-row reveal reveal-up {stagger_class(index)}">
              <p class="skill-category">{html.escape(group["category"])}</p>
              <div class="skill-items">{pills}</div>
            </article>
            """
        )
    return "".join(rows)


def render_contact_rows() -> str:
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
            <div class="contact-row reveal reveal-up {stagger_class(index)}">
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
          {render_hero_name()}
          <p class="hero-bio">{html.escape(PROFILE["headline"])}</p>
          <p class="hero-summary">{html.escape(PROFILE["subheadline"])}</p>

          <div class="hero-actions reveal reveal-up stagger-2">
            <a class="button button-primary" href="#projects">View Projects</a>
            <a class="button button-secondary" href="mailto:{html.escape(PROFILE["email"])}">Get in touch</a>
            <a class="button button-ghost" href="{cv_href}" download="Ibrahim-Mohamed-Ghouse-CV.pdf">Download CV</a>
          </div>

          <ul class="hero-meta reveal reveal-up stagger-3" aria-label="Contact details">
            {render_meta_pills()}
          </ul>
        </div>

        <aside class="hero-panel reveal reveal-right is-visible" aria-label="Current positioning">
          <p class="panel-label">Current positioning</p>
          <h2>{html.escape(PROFILE["availability"])}</h2>
          <p>{html.escape(PROFILE["summary"])}</p>

          <div class="stat-grid">
            {render_stats()}
          </div>

          <div class="hero-panel-block reveal reveal-up stagger-4">
            <p class="panel-label panel-label-light">Focus areas</p>
            <div class="chip-wrap" aria-label="Focus areas">
              {render_focus_chips(FOCUS_AREAS)}
            </div>
          </div>
        </aside>
      </div>
    </section>
    """


def render_about_section() -> str:
    paragraphs = "".join(f"<p>{html.escape(paragraph)}</p>" for paragraph in SUMMARY_PARAGRAPHS)
    return f"""
    <section class="section" id="about">
      <div class="section-heading reveal reveal-up">
        <p class="eyebrow">Summary</p>
        <h2>Technical depth, business instinct, and applied AI work built to solve real problems.</h2>
      </div>
      <div class="summary-grid">
        <div class="summary-copy reveal reveal-up stagger-1">
          {paragraphs}
        </div>
        <aside class="cert-column">
          <p class="eyebrow reveal reveal-up stagger-2">Certifications</p>
          <div class="cert-stack">
            {render_certifications()}
          </div>
        </aside>
      </div>
    </section>
    """


def render_experience_section() -> str:
    return f"""
    <section class="section" id="experience">
      <div class="section-heading reveal reveal-up">
        <p class="eyebrow">Experience</p>
        <h2>Research, positioning, and hands-on delivery in work that sits close to real users.</h2>
      </div>
      <div class="experience-list">
        {render_experiences()}
      </div>
    </section>
    """


def render_projects_section() -> str:
    return f"""
    <section class="section section-featured" id="projects">
      <div class="section-heading reveal reveal-up">
        <p class="eyebrow">Projects</p>
        <h2>Selected builds across telemetry analytics, multi-agent AI, and embedded computer vision.</h2>
      </div>
      <div class="project-card-grid">
        {render_projects()}
      </div>
    </section>
    """


def render_education_section() -> str:
    return f"""
    <section class="section" id="education">
      <div class="section-heading reveal reveal-up">
        <p class="eyebrow">Education</p>
        <h2>Academic grounding in AI, data, software engineering, and systems thinking.</h2>
      </div>
      <div class="education-stack">
        {render_education()}
      </div>
    </section>
    """


def render_skills_section() -> str:
    return f"""
    <section class="section" id="skills">
      <div class="section-heading reveal reveal-up">
        <p class="eyebrow">Skills</p>
        <h2>Technical, analytical, and client-facing strengths that support end-to-end delivery.</h2>
      </div>
      <div class="skills-list">
        {render_skill_groups()}
      </div>
    </section>
    """


def render_contact_section(cv_href: str) -> str:
    return f"""
    <section class="section contact-section" id="contact">
      <div class="contact-card reveal reveal-up">
        <div class="contact-copy">
          <p class="eyebrow">Contact</p>
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
          {render_contact_rows()}
        </div>
      </div>
    </section>
    """


def render_footer() -> str:
    return f"""
    <footer class="site-footer">
      <div class="footer-inner">
        <p>{html.escape(PROFILE["name"])} <span>/</span> {datetime.now().year}</p>
        <p>Dark-mode Streamlit portfolio with motion, richer content, and editorial structure.</p>
      </div>
    </footer>
    """


def build_page(cv_href: str) -> str:
    return f"""
    <div class="portfolio-root">
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
            {render_nav()}
          </nav>
        </div>
      </header>

      <main id="main-content">
        {render_hero(cv_href)}
        {render_about_section()}
        {render_experience_section()}
        {render_projects_section()}
        {render_education_section()}
        {render_skills_section()}
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
