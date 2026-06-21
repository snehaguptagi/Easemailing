const HowItWorksSection = () => {
  const steps = [
    {
      number: "01",
      title: "An email arrives",
      description: "A lead, invoice, support request, or escalation."
    },
    {
      number: "02", 
      title: "AI Email Assistant reads it",
      description: "It categorizes the intent and extracts structured fields."
    },
    {
      number: "03",
      title: "It acts, instantly", 
      description: "It updates systems, routes to teams, or drafts replies."
    }
  ];

  return (
    <section className="py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-8 text-foreground fade-in-up">
            How It Works
          </h2>
          <p className="text-xl text-muted-foreground fade-in-up stagger-1">
            From inbox to action, without delay.
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <div key={index} className={`text-center fade-in-up stagger-${index + 1}`}>
              <div className="bg-card rounded-xl p-8 shadow-lg h-full">
                <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl font-bold text-accent-foreground">{step.number}</span>
                </div>
                <h3 className="text-2xl font-semibold mb-4 text-card-foreground">{step.title}</h3>
                <p className="text-lg text-muted-foreground leading-relaxed">{step.description}</p>
              </div>
              
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 transform -translate-y-1/2 left-full w-8 h-0.5 bg-accent"></div>
              )}
            </div>
          ))}
        </div>
        
        <div className="text-center mt-16">
          <div className="bg-card rounded-xl p-8 shadow-lg inline-block fade-in-up stagger-4">
            <p className="text-xl font-semibold text-card-foreground mb-4">
              Real-time Processing Pipeline
            </p>
            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
              <span className="bg-accent px-3 py-1 rounded text-accent-foreground">Email Received</span>
              <span>→</span>
              <span className="bg-accent px-3 py-1 rounded text-accent-foreground">AI Analysis</span>
              <span>→</span>
              <span className="bg-accent px-3 py-1 rounded text-accent-foreground">Action Triggered</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;