import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Snag — Your workflow, unhindered",
  description:
    "Snag is a premium, lightweight floating widget for macOS, Windows & Linux. Instantly access screenshots, downloads, clipboard history and saved snippets — without breaking focus.",
  openGraph: {
    title: "Snag — Your workflow, unhindered",
    description:
      "A floating productivity widget that lives at the edge of your screen. Always ready, never in the way.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
