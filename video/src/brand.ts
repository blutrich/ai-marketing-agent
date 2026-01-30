/**
 * Base44 Brand Configuration
 * Source: brands/base44/brand.json and brand-system.md
 *
 * ALWAYS import this file for consistent brand colors across all videos.
 */

export const BASE44_COLORS = {
  // Backgrounds - light gradient (PRIMARY)
  bgTop: "#E8F4F8",           // Light blue
  bgBottom: "#FDF5F0",        // Cream/peach
  bgSecondary: "#F0F0F0",     // Light gray

  // Cards & Surfaces
  cardBg: "#FFFFFF",          // White cards
  cardBgAlt: "#f9f9f9",       // Off-white
  codeBg: "#f5f5f5",          // Code background

  // Text colors (on light backgrounds)
  text: "#000000",            // Primary text - true black
  textSecondary: "#666666",   // Secondary text
  textMuted: "#999999",       // Muted text

  // Orange accent palette
  accent: "#FF983B",          // Primary accent (use sparingly!)
  accentLight: "#FFE9DF",     // Light accent
  accentMedium: "#FFBFA1",    // Medium accent
  accentDark: "#EA6020",      // Dark accent (hover states)
  accentDarkest: "#C94001",   // Darkest accent (rare)

  // Button colors
  buttonBg: "#000000",        // Black buttons (NOT orange!)
  buttonText: "#FFFFFF",      // White text on buttons
} as const;

// Gradient helper
export const BASE44_GRADIENT = `linear-gradient(180deg, ${BASE44_COLORS.bgTop} 0%, ${BASE44_COLORS.bgBottom} 100%)`;

// Shadow styles
export const BASE44_SHADOWS = {
  card: "0 4px 24px rgba(0,0,0,0.08)",
  elevated: "0 8px 32px rgba(0,0,0,0.12)",
} as const;

// Font configuration
export const BASE44_FONTS = {
  heading: "BC Novatica Cyr",
  headingAlt: "STK Miso",
  headingFallback: "Arial",
  body: "Inter",
  bodyFallback: "Arial",
  code: "Courier New",
} as const;

/**
 * BRAND RULES - DO NOT VIOLATE:
 *
 * ✅ DO:
 * - Use light gradient backgrounds
 * - Use true black (#000000) text for readability
 * - Use white cards for content
 * - Use orange (#FF983B) SPARINGLY for accents only
 * - Use black for primary CTAs/buttons
 * - Keep designs clean and spacious
 *
 * ❌ DON'T:
 * - Use dark/black backgrounds (except for special emphasis scenes)
 * - Use white text on light backgrounds
 * - Use orange for buttons or large areas
 * - Overuse orange—it should POP, not dominate
 * - Use heavy shadows or gradients on text
 */
