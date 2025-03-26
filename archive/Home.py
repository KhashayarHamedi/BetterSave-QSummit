"""
Home.py
Landing page for the BetterSave Energy application
"""

import streamlit as st
from imports_config import configure_page
from styling import apply_webflow_theme, render_navigation, render_footer

def main():
    """Main landing page entry point"""
    # Configure the page
    configure_page()

    # Apply the Webflow theme
    apply_webflow_theme()

    # Render navigation bar
    render_navigation()

    # Landing page content
    st.markdown("<h1 class='main-header'>Welcome to BetterSave Energy</h1>", unsafe_allow_html=True)

    # Hero section with image
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
            <div class="hero-content">
                <h2 class="hero-title">Sustainable Energy Analytics Platform</h2>
                <p class="hero-description">
                    Transform your energy management with our comprehensive analytics platform. Monitor consumption,
                    track generation patterns, and make data-driven decisions to optimize your energy usage.
                </p>
                <div class="hero-buttons">
                    <a href="/dashboard" class="hero-button primary-button">Explore Dashboard</a>
                    <a href="/prediction" class="hero-button secondary-button">Try Predictions</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Placeholder for hero image - in a real app, you'd use an actual image
        st.markdown("""
            <div class="hero-image-container">
                <div class="placeholder-image">
                    <span style="font-size: 3rem;">⚡</span>
                    <span>Energy Analytics</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Key benefits section
    st.markdown("<h2 class='section-title' style='margin-top: 3rem;'>Key Benefits</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Real-time Analytics</h3>
                <p>Monitor your energy consumption and generation patterns in real-time with interactive visualizations.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔮</div>
                <h3>Predictive Insights</h3>
                <p>Forecast future energy trends and identify opportunities for optimization and cost savings.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌱</div>
                <h3>Renewable Tracking</h3>
                <p>Analyze your energy sources and track your renewable energy contribution to sustainability goals.</p>
            </div>
        """, unsafe_allow_html=True)

    # CTA Section
    st.markdown("""
        <div class="cta-section">
            <h2>Ready to Optimize Your Energy Management?</h2>
            <p>Start using our comprehensive energy analytics platform today.</p>
            <a href="/dashboard" class="cta-button">Get Started</a>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    render_footer()

if __name__ == "__main__":
    main()
