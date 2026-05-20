from __future__ import annotations

from datetime import datetime
import html
from pathlib import Path

import streamlit as st

from app import (
    inject_scroll_behavior,
    render_certifications,
    render_contact_section as render_contact_section_base,
    render_education,
    render_experiences,
    render_hero as render_hero_base,
    render_projects,
    render_skill_groups,
)
from portfolio_content import PROFILE

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
def read_css_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_css() -> None:
    st.markdown(f"<style>{read_css_text(BASE_CSS_PATH)}</style>", unsafe_allow_html=True)
    st.markdown(f"<style>{read_css_text(IMPROVED_CSS_PATH)}</style>", unsafe_allow_html=True)


def render_nav() -> str:
    return "".join(f'<a href="#{anchor}">{html.escape(label)}</a>' for anchor, label in NAV_ITEMS)


def render_experience_section() -> str:
    return f"""
    <section class="section section-tight" id="experience">
      <div class="section-heading reveal reveal-up">
        <p class="eyebrow">Experience</p>
        <h2>Research, positioning, and hands-on delivery across client-facing and applied AI work.</h2>
      </div>
      <div class="experience-list experience-list-compact">
        {render_experiences()}
      </div>
    </section>
    """


def render_projects_section() -> str:
    return f"""
    <section class="section section-tight section-featured" id="projects">
      <div class="project-rail-header reveal reveal-up">
        <div class="section-heading section-heading-compact">
          <p class="eyebrow">Projects</p>
          <h2>Selected builds across telemetry analytics, multi-agent AI, and embedded computer vision.</h2>
        </div>
        <p class="project-rail-hint">
          Swipe or scroll sideways to explore the work.
        </p>
      </div>
      <div class="project-rail-shell reveal reveal-up stagger-2">
        <div class="project-rail" aria-label="Project gallery">
          {render_projects()}
        </div>
      </div>
    </section>
    """


def render_credentials_section() -> str:
    return f"""
    <section class="section section-tight" id="credentials">
      <div class="section-heading reveal reveal-up">
        <p class="eyebrow">Credentials</p>
        <h2>Education, certifications, and technical strengths supporting practical delivery.</h2>
      </div>
      <div class="credentials-layout">
        <div class="credentials-column">
          <div class="credentials-subheading reveal reveal-up stagger-1">
            <p class="eyebrow">Education</p>
          </div>
          <div class="education-stack education-stack-compact">
            {render_education()}
          </div>
        </div>
        <div class="credentials-column">
          <div class="credentials-subheading reveal reveal-up stagger-2">
            <p class="eyebrow">Certifications</p>
          </div>
          <div class="cert-stack cert-stack-compact">
            {render_certifications()}
          </div>
        </div>
      </div>
      <div class="skills-cluster">
        <div class="credentials-subheading reveal reveal-up stagger-3">
          <p class="eyebrow">Skills</p>
        </div>
        <div class="skills-list skills-list-compact">
          {render_skill_groups()}
        </div>
      </div>
    </section>
    """


def render_footer() -> str:
    return f"""
    <footer class="site-footer">
      <div class="footer-inner">
        <p>{html.escape(PROFILE["name"])} <span>/</span> {datetime.now().year}</p>
        <p>Abu Dhabi, United Arab Emirates</p>
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
            {render_nav()}
          </nav>
        </div>
      </header>

      <main id="main-content">
        {render_hero_base(cv_href)}
        {render_experience_section()}
        {render_projects_section()}
        {render_credentials_section()}
        {render_contact_section_base(cv_href)}
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
