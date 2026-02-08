import type { Metadata } from "next";
import { FlowgladProvider } from "@flowglad/nextjs";
import "./globals.css";

export const metadata: Metadata = {
  title: "MCP Maker — Adapter Generator",
  description: "Generate MCP servers from any API specification",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased">
        <FlowgladProvider>
          {children}
        </FlowgladProvider>
      </body>
    </html>
  );
}
