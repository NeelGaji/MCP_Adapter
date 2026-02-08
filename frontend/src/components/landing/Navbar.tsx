"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X, ArrowUpRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { NexusLogo } from "./NexusLogo";
import { BillingButton } from "@/components/BillingButton";

const NAV_LINKS = [
  { label: "Platform", href: "#platform" },
  { label: "Services", href: "#services" },
  { label: "Pipeline", href: "#pipeline" },
  { label: "Features", href: "#features" },
];

export function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-strong border-b border-border/30">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <NexusLogo size={36} animated />
          <span className="font-bold text-foreground text-lg tracking-tight">MCP Maker</span>
        </Link>

        <nav className="hidden md:flex items-center gap-8">
          {NAV_LINKS.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors relative group"
            >
              {link.label}
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-primary to-primary/40 group-hover:w-full transition-all duration-300" />
            </a>
          ))}
        </nav>

        <div className="hidden md:flex items-center gap-3">
          <BillingButton />
          <Link href="/adapter/ingest">
            <Button variant="outline" size="sm" className="rounded-full text-sm px-5 glass border-border/50 hover:border-primary/40">
              Try Generator
            </Button>
          </Link>
          <Button size="sm" className="btn-gradient rounded-full text-sm px-5 relative z-10">
            <span>Get Started</span>
            <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </div>

        <button className="md:hidden text-foreground" onClick={() => setOpen(!open)}>
          {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t border-border/30 glass-strong px-6 py-4 space-y-3">
          {NAV_LINKS.map((link) => (
            <a key={link.label} href={link.href} className="block text-sm text-muted-foreground hover:text-foreground py-2" onClick={() => setOpen(false)}>
              {link.label}
            </a>
          ))}
          <div className="flex gap-3 pt-2">
            <Link href="/adapter/ingest" onClick={() => setOpen(false)}>
              <Button variant="outline" size="sm" className="rounded-full text-sm">Try Generator</Button>
            </Link>
            <Button size="sm" className="btn-gradient rounded-full text-sm relative z-10">
              <span>Get Started</span>
            </Button>
          </div>
        </div>
      )}
    </header>
  );
}
