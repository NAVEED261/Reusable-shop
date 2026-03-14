"use client";

import Image from "next/image";
import Link from "next/link";
import ProductCard from "@/components/ProductCard";
import { CATEGORIES, getProductsByCategory } from "@/lib/products";
import { ArrowRight, Heart, Truck, Shield, Star, Play, Sparkles } from "lucide-react";

export default function HomePage() {
  const handleAddToCart = (product: any) => {
    alert(`${product.name} added to cart!`);
  };

  // Categories with your provided Image Paths
  const boutiqueCategories = [
    { 
      name: "Fancy Suits", 
      path: "/images/naveed/IMG_20180729_211838.jpg", 
      tag: "Wedding Wear" 
    },
    { 
      name: "Shalwar Qameez", 
      path: "/images/naveed/IMG_20251220_191017_697.jpg", 
      tag: "Luxury Edition" 
    },
    { 
      name: "Cotton Suits", 
      path: "/images/naveed/IMG_20230601_205523_081.jpg", 
      tag: "Premium Fabric" 
    },
    { 
      name: "Designer Brands", 
      path: "/images/naveed/IMG_20221007_200512_708.jpg", 
      tag: "New Arrival" 
    }
  ];

  return (
    <main className="min-h-screen bg-white dark:bg-slate-950 overflow-x-hidden">
      
      {/* ==================== HERO SECTION ==================== */}
      <section className="relative min-h-[90vh] flex items-center pt-20 overflow-hidden">
        <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-pink-100 dark:bg-pink-900/20 rounded-full blur-[120px] -z-10"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[400px] h-[400px] bg-amber-100 dark:bg-amber-900/10 rounded-full blur-[100px] -z-10"></div>
        
        <div className="container-wide grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 z-10 space-y-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 dark:bg-white/10 text-white rounded-full text-xs font-bold tracking-[0.2em] uppercase">
              <Sparkles size={14} className="text-amber-400" /> New Collection 2026
            </div>

            <h1 className="text-6xl md:text-8xl font-serif font-bold text-slate-900 dark:text-white leading-[0.95] tracking-tighter">
              Timeless <span className="text-amber-500 italic font-normal">Elegance</span> <br />
              Redefined.
            </h1>

            <p className="text-lg md:text-xl text-slate-600 dark:text-slate-400 max-w-xl leading-relaxed font-light">
              Fatima Zehra Boutique brings you a curated blend of traditional craftsmanship and modern silhouettes. Experience the luxury of premium fabrics.
            </p>

            <div className="flex flex-wrap gap-5">
              <Link href="/products" className="group relative px-8 py-4 bg-slate-900 text-white overflow-hidden rounded-sm transition-all duration-500">
                <span className="relative z-10 flex items-center gap-3 font-bold text-sm tracking-widest uppercase">
                  Explore Boutique <ArrowRight size={18} className="group-hover:translate-x-2 transition-transform" />
                </span>
                <div className="absolute inset-0 bg-amber-600 translate-y-[101%] group-hover:translate-y-0 transition-transform duration-500"></div>
              </Link>
            </div>
          </div>

          <div className="lg:col-span-5 relative h-[600px] md:h-[700px]">
            <div className="absolute -top-10 -left-10 w-40 h-40 border-l-2 border-t-2 border-amber-500/30 z-0"></div>
            <div className="relative h-full w-full overflow-hidden rounded-sm shadow-2xl group">
              <Image
                src="/images/naveed/IMG_20251220_191017_697.jpg"
                alt="Fatima Zehra Luxury Collection"
                fill
                className="object-cover object-top transition-transform duration-1000 group-hover:scale-110"
                priority
              />
            </div>
          </div>
        </div>
      </section>

      {/* ==================== STRATEGIC VALUES ==================== */}
      <section className="py-12 bg-slate-900 text-white">
        <div className="container-wide flex flex-wrap justify-between gap-8">
          {[
            { icon: <Truck />, title: "Express Shipping", desc: "Across Pakistan" },
            { icon: <Shield />, title: "Secure Payment", desc: "100% Protected" },
            { icon: <Heart />, title: "Made with Love", desc: "Artisan Crafted" },
          ].map((item, i) => (
            <div key={i} className="flex items-center gap-4">
              <div className="text-amber-500">{item.icon}</div>
              <div>
                <h4 className="text-sm font-bold tracking-widest uppercase">{item.title}</h4>
                <p className="text-xs text-slate-400">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ==================== CATEGORIES: UPDATED WITH YOUR PATHS ==================== */}
      <section className="section-padding overflow-hidden bg-white dark:bg-slate-950">
        <div className="container-wide">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
            <div className="max-w-xl">
              <span className="text-amber-600 font-bold text-xs uppercase tracking-[0.4em] mb-4 block">The Collections</span>
              <h2 className="text-4xl md:text-6xl font-serif font-bold text-slate-900 dark:text-white leading-tight">
                Shop by <span className="italic font-normal">Department</span>
              </h2>
            </div>
            <p className="text-slate-500 max-w-xs text-sm leading-relaxed italic border-l-2 border-amber-500 pl-4 font-medium">
              Carefully curated masterpieces designed to make you stand out.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {boutiqueCategories.map((cat, i) => (
              <Link 
                key={i} 
                href={`/products?category=${cat.name}`} 
                className="group relative h-[500px] overflow-hidden rounded-[2rem] shadow-xl transition-all duration-700 hover:-translate-y-3"
              >
                <Image 
                  src={cat.path} 
                  alt={cat.name} 
                  fill 
                  className="object-cover object-top transition-transform duration-1000 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent opacity-80 group-hover:opacity-70 transition-opacity z-10"></div>
                
                <div className="absolute top-6 left-6 z-20">
                   <span className="bg-white/10 backdrop-blur-md text-white text-[9px] font-black px-4 py-2 rounded-full border border-white/20 uppercase tracking-widest">
                     {cat.tag}
                   </span>
                </div>

                <div className="absolute bottom-10 left-8 z-20 translate-y-2 group-hover:translate-y-0 transition-transform duration-500">
                  <p className="text-amber-500 text-[10px] font-black uppercase tracking-[0.4em] mb-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    Explore
                  </p>
                  <h3 className="text-white text-3xl font-serif font-bold mb-4">{cat.name}</h3>
                  <div className="flex items-center gap-2 text-white text-[10px] font-bold uppercase tracking-widest border-b border-white/30 w-fit pb-1 group-hover:border-amber-500 transition-colors">
                    View Catalog <span>→</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ==================== DYNAMIC PRODUCT SHOWCASE ==================== */}
      <section className="section-padding bg-slate-50 dark:bg-slate-900/50">
        <div className="container-wide">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-serif font-bold mb-4 tracking-tight text-slate-900 dark:text-white">Trending <span className="text-pink-600">Now</span></h2>
            <div className="w-24 h-1 bg-amber-500 mx-auto rounded-full"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-8">
            {getProductsByCategory(CATEGORIES[0].name)
              .slice(0, 5)
              .map((product) => (
                <div key={product.id}>
                  <ProductCard product={product} onAddToCart={handleAddToCart} />
                </div>
              ))}
          </div>
        </div>
      </section>

      {/* ==================== LUXURY CTA ==================== */}
      <section className="py-32 relative group overflow-hidden">
        <Image 
          src="/images/naveed/IMG_20221007_200512_708.jpg" 
          alt="CTA Background" 
          fill 
          className="object-cover brightness-50 transition-transform duration-[3s] group-hover:scale-110"
        />
        <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-[1px]"></div>
        <div className="container-wide relative z-10 text-center text-white">
           <h2 className="text-4xl md:text-7xl font-serif font-bold mb-8 tracking-tighter">
             Ready to wear your <br /> <span className="text-amber-500 italic font-normal">Confidence?</span>
           </h2>
           <Link href="/products" className="inline-block bg-white text-slate-900 px-12 py-5 font-bold text-xs uppercase tracking-[0.3em] hover:bg-amber-500 hover:text-white transition-all shadow-2xl rounded-sm">
             Shop the Collection
           </Link>
        </div>
      </section>
    </main>
  );
}