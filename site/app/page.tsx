import Nav from "@/components/Nav";
import Hero from "@/components/Hero";
import StrategySection from "@/components/StrategySection";
import ResultsSection from "@/components/ResultsSection";
import NumbersSection from "@/components/NumbersSection";
import MethodSection from "@/components/MethodSection";
import Footer from "@/components/Footer";
import { loadEquityCurve } from "@/lib/data";

export default function Home() {
  const curve = loadEquityCurve();
  return (
    <div className="flex min-h-full flex-col bg-background text-foreground">
      <Nav />
      <main className="flex-1">
        <Hero curve={curve} />
        <StrategySection />
        <ResultsSection curve={curve} />
        <NumbersSection />
        <MethodSection />
      </main>
      <Footer />
    </div>
  );
}
