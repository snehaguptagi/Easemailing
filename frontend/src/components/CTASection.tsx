import { Button } from "@/components/ui/button";

const CTASection = () => {
  return (
    <section className="py-20 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <div className="bg-card rounded-2xl p-12 shadow-xl">
          <h2 className="text-4xl md:text-5xl font-bold mb-8 text-card-foreground fade-in-up">
            Final Call
          </h2>
          
          <div className="space-y-6 mb-12 fade-in-up stagger-1">
            <p className="text-2xl font-semibold text-card-foreground">
              Don't manage emails. Orchestrate operations.
            </p>
            <p className="text-lg text-muted-foreground leading-relaxed max-w-2xl mx-auto">
              If you want your inbox to be a system of execution, not just communication—
              join the waitlist.
            </p>
          </div>
          
          <div className="fade-in-up stagger-2">
            <Button 
              size="lg"
              className="bg-primary text-primary-foreground hover:bg-accent hover:text-accent-foreground text-xl px-12 py-6 rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              Join Waitlist
            </Button>
          </div>
          
          <div className="mt-12 pt-8 border-t border-border fade-in-up stagger-3">
            <div className="grid md:grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-3xl font-bold text-card-foreground mb-2">10ms</div>
                <div className="text-sm text-muted-foreground">Average Processing Time</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-card-foreground mb-2">99.9%</div>
                <div className="text-sm text-muted-foreground">Accuracy Rate</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-card-foreground mb-2">24/7</div>
                <div className="text-sm text-muted-foreground">Continuous Operation</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTASection;