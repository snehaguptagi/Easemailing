import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <section className="min-h-screen flex items-center justify-center px-6 py-20">
      <div className="max-w-4xl mx-auto text-center">
        <div className="fade-in-up">
          <h1 className="text-6xl md:text-7xl font-bold mb-6 text-foreground">
            AI Email Assistant
          </h1>
          <p className="text-2xl md:text-3xl font-light mb-8 text-muted-foreground">
            Email-Native Operational Intelligence
          </p>
        </div>
        
        <div className="fade-in-up stagger-1 max-w-3xl mx-auto mb-12">
          <p className="text-lg md:text-xl leading-relaxed text-muted-foreground mb-6">
            Emails aren't just communication. They're action waiting to happen.
          </p>
          <p className="text-lg md:text-xl leading-relaxed text-foreground">
            AI Email Assistant reads them, understands them, and makes them move.
          </p>
        </div>
        
        <div className="fade-in-up stagger-2">
          <Button
            size="lg"
            onClick={() => navigate('/app')}
            className="bg-primary text-primary-foreground hover:bg-accent hover:text-accent-foreground text-lg px-8 py-4 rounded-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            Open the App
          </Button>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;