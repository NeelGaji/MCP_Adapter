"use client";

import Link from "next/link";
import { NexusLogo } from "./NexusLogo";

const FOOTER_LINKS = {
  Platform: ["MCP Generator", "Orchestration", "DAuth", "Multi-Model Routing"],
  Resources: ["Documentation", "API Reference", "Changelog", "Status"],
  Company: ["About", "Blog", "Careers", "Contact"],
};

export function Footer() {
  return (
    <footer className="relative border-t border-border/30">
      <div className="section-glow-line absolute top-0 left-0 right-0" />
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-10">
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2.5 mb-4">
              <NexusLogo size={32} />
              <span className="font-bold text-foreground">MYME</span>
            </Link>
            <p className="text-sm text-muted-foreground leading-relaxed">
              The orchestration layer for MCP servers. Generate, govern, deploy.
            </p>
          </div>
          {Object.entries(FOOTER_LINKS).map(([title, links]) => (
            <div key={title}>
              <h4 className="font-bold text-foreground text-sm mb-4">{title}</h4>
              <ul className="space-y-2.5">
                {links.map((link) => (
                  <li key={link}>
                    <a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">{link}</a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-12 pt-6 border-t border-border/30 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-muted-foreground">
          <span>&copy; 2026 MYME. All rights reserved.</span>
          <div className="flex gap-6">
            <a href="#" className="hover:text-primary transition-colors">Privacy</a>
            <a href="#" className="hover:text-primary transition-colors">Terms</a>
            <a href="#" className="hover:text-primary transition-colors">Security</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
