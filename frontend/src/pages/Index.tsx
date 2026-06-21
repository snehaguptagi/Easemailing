import HeroSection from "@/components/HeroSection";
import AboutSection from "@/components/AboutSection";
import HowItWorksSection from "@/components/HowItWorksSection";
import ComingSoonSection from "@/components/ComingSoonSection";
import CTASection from "@/components/CTASection";

const Index = () => {
  return (
    <div className="min-h-screen">
      <HeroSection />
      <div className="w-full h-px bg-border opacity-20"></div>
      <AboutSection />
      <div className="w-full h-px bg-border opacity-20"></div>
      <HowItWorksSection />
      <div className="w-full h-px bg-border opacity-20"></div>
      <ComingSoonSection />
      <div className="w-full h-px bg-border opacity-20"></div>
      <CTASection />
    </div>
  );
};

export default Index;
