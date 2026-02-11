"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { ShoppingCart, User, Menu, X, Search, MapPin, Phone } from "lucide-react";
import { useCartStore } from "@/lib/store";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const cartCount = useCartStore((state) => state.itemCount);

  // Scroll effect for styling
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header className="fixed w-full top-0 z-[100] transition-all duration-500">
      
      {/* 1. TOP MINI HEADER (PREMIUM LOOK) */}
      <div className={`bg-slate-900 text-white py-2 transition-all duration-500 ${scrolled ? 'h-0 opacity-0 overflow-hidden' : 'h-auto opacity-100'}`}>
        <div className="container-wide flex justify-between items-center text-[10px] font-bold tracking-[0.2em] uppercase">
          <div className="flex gap-6">
            <span className="flex items-center gap-2"><MapPin size={12} className="text-amber-500" /> Karachi, Pakistan</span>
            <span className="flex items-center gap-2"><Phone size={12} className="text-amber-500" /> +92 300 2385209</span>
          </div>
          <div className="hidden md:block animate-pulse text-amber-400">
            Free Worldwide Shipping on Orders Over $200
          </div>
        </div>
      </div>

      {/* 2. MAIN NAV (ULTRA STYLISH) */}
      <nav className={`mx-auto transition-all duration-700 ${
        scrolled 
        ? "max-w-[95%] mt-4 rounded-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl shadow-[0_20px_50px_rgba(0,0,0,0.1)] border border-white/20" 
        : "max-w-full bg-white dark:bg-slate-950 border-b border-slate-100 dark:border-slate-900"
      }`}>
        <div className="container-wide py-3 md:py-4">
          <div className="flex items-center justify-between">
            
            {/* LOGO SECTION WITH 360° SPIN */}
            <Link href="/" className="flex items-center gap-4 group">
              <style>{`
                @keyframes circular-rotate {
                  from { transform: rotate(0deg); }
                  to { transform: rotate(360deg); }
                }
                .logo-spin-infinite {
                  animation: circular-rotate 12s linear infinite;
                }
                .nav-link-ltr {
                  position: relative;
                }
                .nav-link-ltr::after {
                  content: '';
                  position: absolute;
                  width: 0; height: 2px;
                  bottom: -4px; left: 0;
                  background-color: #f59e0b;
                  transition: all 0.3s ease-in-out;
                }
                .nav-link-ltr:hover::after { width: 100%; }
              `}</style>
              
              <div className="relative w-14 h-14 md:w-16 md:h-16 flex items-center justify-center">
                <div className="absolute inset-0 bg-gradient-to-tr from-amber-500 to-pink-500 rounded-full blur-sm opacity-20 group-hover:opacity-50 transition-opacity"></div>
                
                <div className="logo-spin-infinite relative w-full h-full rounded-full overflow-hidden border-2 border-amber-500/30 p-0.5 bg-white">
                  <Image 
                    src="/images/naveed/fz-beauty-vector-initial-logo-art-handwriting-logo-of-initial-signature-wedding-fashion-jewerly-boutique-floral-and-botanical-with-creative-temp-2e76ke.jpg" 
                    alt="Fatima Zehra Signature Logo" 
                    fill
                    className="object-cover"
                    priority
                  />
                </div>
              </div>

              <div className="flex flex-col">
                <span className="text-xl md:text-2xl font-serif font-black tracking-tighter text-slate-900 dark:text-white">
                  FATIMA <span className="text-amber-600">ZEHRA</span>
                </span>
                <span className="text-[9px] font-black tracking-[0.5em] text-slate-400 uppercase">Luxury Boutique</span>
              </div>
            </Link>

            {/* DESKTOP LINKS - SHOP PATH FIXED */}
            <div className="hidden lg:flex items-center gap-10">
              <Link href="/" className="nav-link-ltr text-[11px] font-black uppercase tracking-[0.2em] text-slate-600 dark:text-slate-300 hover:text-amber-600 transition-colors">Home</Link>
              
              {/* Yahan /shop ki bajaye /products kiya hai */}
              <Link href="/products" className="nav-link-ltr text-[11px] font-black uppercase tracking-[0.2em] text-slate-600 dark:text-slate-300 hover:text-amber-600 transition-colors">Shop</Link>
              
              <Link href="/about" className="nav-link-ltr text-[11px] font-black uppercase tracking-[0.2em] text-slate-600 dark:text-slate-300 hover:text-amber-600 transition-colors">About</Link>
              <Link href="/contact" className="nav-link-ltr text-[11px] font-black uppercase tracking-[0.2em] text-slate-600 dark:text-slate-300 hover:text-amber-600 transition-colors">Contact</Link>
            </div>

            {/* ICONS SECTION */}
            <div className="flex items-center gap-3">
              <button className="p-3 text-slate-600 hover:bg-amber-50 dark:hover:bg-amber-900/20 rounded-full transition-all">
                <Search size={20} />
              </button>

              <Link href="/cart" className="group relative p-3 bg-slate-900 dark:bg-amber-600 text-white rounded-full hover:scale-110 transition-all shadow-xl">
                <ShoppingCart size={18} />
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-white text-slate-900 text-[10px] rounded-full flex items-center justify-center font-bold border-2 border-slate-900">
                  {cartCount}
                </span>
              </Link>

              <Link href="/profile" className="hidden sm:flex p-3 border border-slate-200 dark:border-slate-800 rounded-full hover:border-amber-500 transition-all">
                <User size={20} />
              </Link>

              <button onClick={() => setIsOpen(!isOpen)} className="lg:hidden p-3 bg-slate-100 dark:bg-slate-800 rounded-full">
                {isOpen ? <X size={22} /> : <Menu size={22} />}
              </button>
            </div>
          </div>
        </div>

        {/* MOBILE OVERLAY - SHOP PATH FIXED */}
        {isOpen && (
          <div className="lg:hidden absolute top-full left-0 w-full bg-white dark:bg-slate-950 shadow-2xl border-t border-slate-100 p-8 animate-fade-in">
            <div className="flex flex-col gap-6 text-center">
              <Link href="/" className="text-2xl font-serif font-bold text-slate-900" onClick={() => setIsOpen(false)}>Home</Link>
              <Link href="/products" className="text-2xl font-serif font-bold text-slate-900" onClick={() => setIsOpen(false)}>Shop</Link>
              <Link href="/about" className="text-2xl font-serif font-bold text-slate-900" onClick={() => setIsOpen(false)}>About</Link>
              <Link href="/contact" className="text-2xl font-serif font-bold text-slate-900" onClick={() => setIsOpen(false)}>Contact</Link>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}